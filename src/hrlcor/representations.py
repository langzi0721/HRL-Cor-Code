"""Training-only transforms matching the original publication protocol."""
from dataclasses import dataclass, field
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LassoCV
from sklearn.feature_selection import SelectFromModel
from .data import load_embedding, DESCRIPTORS, PHYSICAL

@dataclass
class Representation:
    train: np.ndarray
    test: np.ndarray
    names: list
    dimensions: tuple
    transforms: dict = field(default_factory=dict)

def reduce_channel(array, y, method, seed=42, variance=.90):
    scaler=StandardScaler()
    train=scaler.fit_transform(array[:60]);test=scaler.transform(array[60:])
    reducer=None; selected=None
    if method=='PCA':
        reducer=PCA(n_components=None if variance==1 else variance,random_state=seed)
        train,test=reducer.fit_transform(train),reducer.transform(test)
    elif method=='Lasso':
        lasso=LassoCV(cv=5,random_state=seed,max_iter=3000)
        lasso.fit(train,y)
        reducer=SelectFromModel(lasso,prefit=True)
        selected=np.flatnonzero(reducer.get_support())
        train,test=reducer.transform(train),reducer.transform(test)
        if train.shape[1]==0:raise ValueError('Lasso selected no features.')
    elif method!='None':raise ValueError(method)
    return train,test,{'scaler':scaler,'reducer':reducer,'selected_indices':selected}

def morgan(frame):
    from rdkit import Chem
    from rdkit.Chem import rdFingerprintGenerator
    generator=rdFingerprintGenerator.GetMorganGenerator(radius=2,fpSize=2048)
    vectors=[]
    for smiles in frame['isomeric_smiles']:
        mol=Chem.MolFromSmiles(smiles)
        if mol is None:raise ValueError('Invalid SMILES: '+smiles)
        vectors.append(generator.GetFingerprintAsNumPy(mol))
    return np.asarray(vectors,dtype=float)

def build(frame, key='qwen_ed3', descriptors=None, structural='unimol',
          structure_reduction='Lasso', text_reduction='PCA', variance=.90,
          seed=42, allow_api=False):
    descriptors=PHYSICAL if descriptors is None else descriptors
    y=frame['ie_ze41'].to_numpy(float)[:60]
    pieces=[];names=[];dimensions=[];transforms={}
    if structural:
        array=load_embedding('unimol') if structural=='unimol' else morgan(frame)
        tr,te,obj=reduce_channel(array,y,structure_reduction,seed)
        pieces.append((tr,te));dimensions.append(tr.shape[1]);transforms['structural']=obj
        names += [f'Uni-Mol-L{i+1}' if structural=='unimol' and structure_reduction=='Lasso' else f'Structure-{i+1}' for i in range(tr.shape[1])]
    else:dimensions.append(0)
    if key:
        tr,te,obj=reduce_channel(load_embedding(key,allow_api),y,text_reduction,seed,variance)
        pieces.append((tr,te));dimensions.append(tr.shape[1]);transforms['text']=obj
        names += [f'LLM-PC{i+1}' if text_reduction=='PCA' else f'Text-{i+1}' for i in range(tr.shape[1])]
    else:dimensions.append(0)
    if descriptors:
        scaler=StandardScaler();array=frame[descriptors].to_numpy(float)
        pieces.append((scaler.fit_transform(array[:60]),scaler.transform(array[60:])))
        transforms['explicit']=scaler;names+=list(descriptors)
    dimensions.append(len(descriptors))
    if not pieces:raise ValueError('No input channels selected.')
    return Representation(np.hstack([p[0] for p in pieces]),np.hstack([p[1] for p in pieces]),names,tuple(dimensions),transforms)
