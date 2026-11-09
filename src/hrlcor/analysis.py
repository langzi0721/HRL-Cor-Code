"""Only the analyses used in the manuscript and supporting information."""
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, t
from scipy.spatial.distance import cdist


def correlation(a, b):
    if np.std(a) < 1e-12 or np.std(b) < 1e-12:
        return float('nan')
    return float(pearsonr(a, b)[0])


def explain(model, rep, frame, save):
    import shap
    if shap.__version__ != '0.49.1':
        raise RuntimeError('The SI specifies SHAP 0.49.1. Install requirements.txt before this experiment.')
    np.random.seed(42)
    explainer = shap.KernelExplainer(model.predict, rep.train)
    values = np.asarray(explainer.shap_values(rep.test, silent=True))
    if values.ndim == 3 and values.shape[-1] == 1:
        values = values[:, :, 0]
    if values.shape != rep.test.shape or not np.isfinite(values).all():
        raise ValueError('Invalid SHAP output shape or values.')
    base = float(np.asarray(explainer.expected_value).reshape(-1)[0])
    error = np.max(np.abs(model.predict(rep.test) - base - values.sum(axis=1)))
    if error > 1e-4 * max(1., np.max(np.abs(model.predict(rep.test)))):
        raise RuntimeError('SHAP additivity check failed.')
    importance = np.abs(values).mean(axis=0)
    n_uni, n_text, n_phys = rep.dimensions
    channels = ['Structural'] * n_uni + ['Text'] * n_text + ['Explicit descriptors'] * n_phys
    ranking = np.argsort(-importance, kind='stable')
    table = pd.DataFrame({'Feature': rep.names, 'Channel': channels,
                          'Mean_abs_SHAP': importance, 'Share_percent': 100 * importance / importance.sum()})
    top = table.iloc[ranking[:10]].reset_index(drop=True)
    top.insert(0, 'Rank', np.arange(1, len(top) + 1))
    save('S16_shap_top10', top)
    save('S17_shap_channels', table.groupby('Channel', sort=False)[['Mean_abs_SHAP', 'Share_percent']].sum().reset_index())
    correlations = []
    text_rows = []
    for index in ranking[:10]:
        correlations.append({'Feature': rep.names[index], 'Channel': channels[index],
                             'Pearson_r_with_IE_DS60': correlation(rep.train[:, index], frame.ie_ze41.to_numpy()[:60])})
        if n_uni <= index < n_uni + n_text:
            text_rows.append({'Text_component': rep.names[index], **{
                col: correlation(rep.train[:, index], frame[col].to_numpy()[:60])
                for col in ['LUMO / eV', 'E1p', 'P_VSA_MR_5']}})
    save('S18_text_descriptor_correlations', pd.DataFrame(text_rows))
    corrs = pd.DataFrame(correlations)
    save('S19_top10_IE_correlations', corrs)
    save('S20_structural_IE_correlations', corrs[corrs.Channel == 'Structural'])
    save('shap_values_DS15', pd.concat([frame.iloc[60:][['name']].reset_index(drop=True),
                                       pd.DataFrame(values, columns=rep.names)], axis=1))
    return {'shap_version': shap.__version__, 'max_additivity_error': float(error)}


def proximity(model, rep, frame, save):
    from .representations import morgan
    bits = morgan(frame)
    train_bits, test_bits = bits[:60].astype(bool), bits[60:].astype(bool)
    intersections = test_bits.astype(int) @ train_bits.astype(int).T
    unions = test_bits.sum(axis=1)[:, None] + train_bits.sum(axis=1)[None, :] - intersections
    tanimoto = np.divide(intersections, unions, out=np.ones_like(intersections, dtype=float), where=unions != 0)
    scores = {'Morgan': tanimoto.max(axis=1)}
    nearest = {'Morgan': tanimoto.argmax(axis=1)}
    a, b, c = rep.dimensions
    tr, te = rep.train, rep.test
    spaces = {
        'Structural': (tr[:, :a], te[:, :a]),
        'Text': (tr[:, a:a+b], te[:, a:a+b]),
        'Explicit descriptors': (tr[:, a+b:], te[:, a+b:]),
        'Structural-text': (np.hstack([tr[:, :a]/np.sqrt(a), tr[:, a:a+b]/np.sqrt(b)]),
                            np.hstack([te[:, :a]/np.sqrt(a), te[:, a:a+b]/np.sqrt(b)])),
        'Heterogeneous': (np.hstack([tr[:, :a]/np.sqrt(a), tr[:, a:a+b]/np.sqrt(b), tr[:, a+b:]/np.sqrt(c)]),
                          np.hstack([te[:, :a]/np.sqrt(a), te[:, a:a+b]/np.sqrt(b), te[:, a+b:]/np.sqrt(c)])),
    }
    ranges = []
    for label, (x, z) in spaces.items():
        dist = cdist(x, x); np.fill_diagonal(dist, np.inf)
        reference = dist.min(axis=1)
        dmin, dmax = reference.min(), reference.max()
        heldout = cdist(z, x)
        nearest[label] = heldout.argmin(axis=1)
        scores[label] = np.clip((dmax-heldout.min(axis=1))/(dmax-dmin), 0, 1) if dmax > dmin else np.full(15, .5)
        ranges.append({'Space': label, 'Minimum': dmin, 'Median': np.median(reference), 'Maximum': dmax})
    error = np.abs(frame.ie_ze41.to_numpy()[60:] - model.predict(rep.test))
    save('S21_distance_ranges', pd.DataFrame(ranges))
    save('S22_proximity_error_correlations', pd.DataFrame([
        {'Space': label, 'Pearson_r': correlation(values, error)} for label, values in scores.items()]))
    table = pd.DataFrame({'ID': np.arange(1, 16), 'Molecule': frame.name.iloc[60:].to_numpy(), 'Absolute_error_pp': error, **scores})
    save('S23_proximity_scores', table)
    save('nearest_training_molecules', pd.DataFrame({'Molecule': frame.name.iloc[60:].to_numpy(), **{
        label: frame.name.to_numpy()[idx] for label, idx in nearest.items()}}))


def residual_summary(y, pred):
    residual = np.asarray(y) - np.asarray(pred)
    mean, sd = residual.mean(), residual.std(ddof=1)
    half = t.ppf(.975, len(residual)-1)*sd/np.sqrt(len(residual))
    return pd.DataFrame([{'Mean_residual_pp': mean, 'SD_pp_ddof1': sd,
                          'Mean_residual_CI95_lower': mean-half, 'Mean_residual_CI95_upper': mean+half}])
