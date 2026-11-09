"""Original hyperparameter grids and shuffled DS60 three-fold selection."""
import json, warnings
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
from sklearn.model_selection import KFold,ParameterGrid
from sklearn.exceptions import ConvergenceWarning
from xgboost import XGBRegressor
from .data import ROOT

LABELS={'RF':'Random Forest','XGB':'XGBoost','SVM':'SVM (RBF)','MLP':'MLP (Neural Net)'}
REFERENCE={'colsample_bytree':.6,'learning_rate':.05,'max_depth':1,'n_estimators':250,'reg_alpha':.1,'reg_lambda':3.0}

def estimator(code,seed=42,jobs=1,params=None):
    if code=='RF': model=RandomForestRegressor(random_state=seed,n_jobs=jobs)
    elif code=='XGB':model=XGBRegressor(random_state=seed,n_jobs=jobs)
    elif code=='SVM':model=SVR(kernel='rbf')
    elif code=='MLP':model=MLPRegressor(activation='relu',solver='adam',max_iter=800,random_state=seed)
    else:raise ValueError(code)
    return model.set_params(**(params or {}))

def metrics(y,pred):
    r=float(pearsonr(y,pred)[0]) if np.std(pred)>1e-8 and np.std(y)>1e-8 else float('nan')
    return {'R2':float(r2_score(y,pred)),'r':r,'MAE_pp':float(mean_absolute_error(y,pred)),
            'RMSE_pp':float(np.sqrt(mean_squared_error(y,pred)))}

def search(rep,frame,seed=42,jobs=1,mode='full',codes=None):
    grids=json.loads((ROOT/'configs/hyperparameters.json').read_text())
    y=frame['ie_ze41'].to_numpy(float);rows=[];fitted={}
    folds=list(KFold(n_splits=3,shuffle=True,random_state=seed).split(rep.train))
    for code in codes or LABELS:
        convergence_warnings=0
        def fit_checked(model,x,target):
            nonlocal convergence_warnings
            with warnings.catch_warnings(record=True) as seen:
                warnings.simplefilter('always',ConvergenceWarning)
                model.fit(x,target)
            convergence_warnings+=sum(issubclass(w.category,ConvergenceWarning) for w in seen)
            for item in seen:
                if not issubclass(item.category,ConvergenceWarning):warnings.warn(str(item.message),item.category)
        grid=grids[LABELS[code]]
        if code=='MLP':grid['hidden_layer_sizes']=[tuple(v) for v in grid['hidden_layer_sizes']]
        choices=list(ParameterGrid(grid))
        if mode=='smoke':choices=choices[:1]
        best_score,best_params=-np.inf,None
        for params in choices:
            scores=[]
            model=estimator(code,seed,jobs,params)
            for tr,va in folds:
                fit_checked(model,rep.train[tr],y[:60][tr])
                scores.append(r2_score(y[:60][va],model.predict(rep.train[va])))
            score=float(np.mean(scores))
            if score>best_score:best_score,best_params=score,params
        if best_params is None:raise RuntimeError('No valid parameters for '+code)
        model=estimator(code,seed,jobs,best_params);fit_checked(model,rep.train,y[:60])
        rows.append({'Model':code,'Seed':seed,'CV_R2':best_score,**metrics(y[60:],model.predict(rep.test)),
                     'Best_parameters':json.dumps(best_params),'Structural_dim':rep.dimensions[0],
                     'Text_dim':rep.dimensions[1],'Numerical_dim':rep.dimensions[2],
                     'Total_dim':rep.train.shape[1],'Search_mode':mode,'Convergence_warning_count':convergence_warnings})
        fitted[code]=model
    return pd.DataFrame(rows),fitted
