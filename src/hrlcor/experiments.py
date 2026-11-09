"""Manuscript experiments with compact tables and optional model persistence."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from .data import ROOT, DESCRIPTORS, PHYSICAL, load_dataset
from .representations import build, Representation
from .models import search, estimator, metrics, REFERENCE
from . import analysis

AVAILABLE = ['reference', 'benchmark', 'baseline', 'allocation', 'smiles', 'reductions',
             'pca', 'templates', 'encoders', 'seeds', 'ablation', 'explain', 'proximity', 'gnn']


class Runner:
    def __init__(self, args):
        self.args = args
        self.frame = load_dataset()
        self.y = self.frame.ie_ze41.to_numpy(float)
        self.out = Path(args.output).resolve()
        if args.search == 'smoke': self.out = self.out / 'smoke'
        self.out.mkdir(parents=True, exist_ok=True)
        self._representations = {}
        self._reference = None

    def save(self, name, table):
        table.to_csv(self.out / (name + '.csv'), index=False, float_format='%.10g', encoding='utf-8')

    def representation(self, **kwargs):
        key = json.dumps(kwargs, sort_keys=True)
        if key not in self._representations:
            self._representations[key] = build(self.frame, allow_api=self.args.allow_api, **kwargs)
        return self._representations[key]

    def evaluate(self, label, rep, seed=42):
        table, models = search(rep, self.frame, seed, self.args.jobs, self.args.search, self.args.models)
        table.insert(0, 'Configuration', label)
        return table, models

    def comparisons(self, name, configs):
        tables = []
        for label, kwargs in configs:
            print('  evaluating', label, flush=True)
            table, _ = self.evaluate(label, self.representation(**kwargs))
            tables.append(table)
        all_models = pd.concat(tables, ignore_index=True)
        # Matches the SI's exploratory selection by DS15 R2; not independent model validation.
        best = all_models.loc[all_models.groupby('Configuration', sort=False).R2.idxmax()].reset_index(drop=True)
        self.save(name, best)
        self.save(name + '_all_models', all_models)

    def reference_model(self):
        if self._reference is None:
            rep = self.representation()
            model = estimator('XGB', jobs=self.args.jobs, params=REFERENCE)
            model.fit(rep.train, self.y[:60])
            self._reference = rep, model
        return self._reference

    def reference(self):
        rep, model = self.reference_model()
        pred = model.predict(rep.test)
        scores = metrics(self.y[60:], pred)
        self.save('S13_reference', pd.DataFrame([{'Model': 'XGB', **scores}]))
        self.save('S14_DS15_predictions', pd.DataFrame({'Molecule': self.frame.name.iloc[60:].to_numpy(),
            'True_IE': self.y[60:], 'Predicted_IE': pred, 'Absolute_error_pp': np.abs(self.y[60:]-pred)}))
        self.save('Fig5_all_predictions', pd.DataFrame({'ID': np.arange(1, 76), 'Dataset': ['DS60']*60+['DS15']*15,
            'Molecule': self.frame.name, 'True_IE': self.y,
            'Predicted_IE': np.concatenate([model.predict(rep.train), pred])}))
        self.save('Main_Table2_dimensions', pd.DataFrame({'Channel': ['Structural', 'Text', 'Explicit descriptors', 'Heterogeneous'],
            'Original_dimension': [512, 1024, 2, 1538], 'Retained_dimension': [*rep.dimensions, sum(rep.dimensions)]}))
        self.save('S14_mean_residual_CI', analysis.residual_summary(self.y[60:], pred))
        expected = json.loads((ROOT / 'reference/expected_reference.json').read_text())
        self.save('reference_check', pd.DataFrame([
            {'Quantity': k, 'Paper': expected[k], 'Rerun': scores[k], 'Matches_to_4dp': round(scores[k], 4) == expected[k]}
            for k in ['R2', 'r']]))
        print(f"  DS15 R2={scores['R2']:.4f}, r={scores['r']:.4f}; dimensions={rep.dimensions}", flush=True)
        if self.args.save_models:
            import joblib
            folder = self.out / 'models'; folder.mkdir(exist_ok=True)
            joblib.dump({'regressor': model, 'transforms': rep.transforms, 'feature_names': rep.names,
                         'dimensions': rep.dimensions, 'explicit_descriptors': PHYSICAL,
                         'dataset': 'DS60', 'text_cache': 'qwen_ed3'}, folder / 'reference.joblib')

    def benchmark(self):
        table, _ = self.evaluate('ED3 reference', self.representation())
        self.save('reference_four_regressors', table)

    def baseline(self):
        self.comparisons('S11_descriptor_baseline', [('Five descriptors', {'key': None, 'structural': None, 'descriptors': DESCRIPTORS})])

    def allocation(self):
        self.comparisons('S1_descriptor_allocation', [(f'ED{i}', {'key': f'qwen_ed{i}', 'descriptors': DESCRIPTORS[i:]}) for i in range(6)])

    def smiles(self):
        self.comparisons('S3_smiles_text', [
            ('With Uni-Mol', {'key': 'qwen_smiles'}),
            ('Without Uni-Mol', {'key': 'qwen_smiles', 'structural': None})])

    def reductions(self):
        pairs = [('None', 'None'), ('None', 'PCA'), ('Lasso', 'None'), ('PCA', 'PCA'),
                 ('PCA', 'Lasso'), ('Lasso', 'PCA'), ('Lasso', 'Lasso')]
        self.comparisons('S5_reduction_strategies', [(chr(65+i), {'structure_reduction': a, 'text_reduction': b}) for i, (a, b) in enumerate(pairs)])

    def pca(self):
        self.comparisons('S6_PCA_variance', [(str(i), {'variance': i/100}) for i in range(60, 101, 5)])

    def templates(self):
        self.comparisons('S8_text_templates', [(x, {'key': 'qwen_ed3' if x == 'A' else 'qwen_prompt_' + x}) for x in 'ABCDEF'])

    def encoders(self):
        self.comparisons('S9_encoders', [
            ('Qwen', {}), ('BGE-M3', {'key': 'bge_m3'}), ('SciBERT', {'key': 'scibert'}),
            ('Morgan-Qwen', {'structural': 'morgan'})])

    def seeds(self):
        tables = []
        for seed in range(37, 47):
            print('  seed', seed, flush=True)
            table, _ = self.evaluate(str(seed), self.representation(seed=seed), seed)
            tables.append(table)
        table = pd.concat(tables, ignore_index=True)
        self.save('S12_seeds_all_models', table)
        best = table.loc[table.groupby('Seed', sort=False).R2.idxmax()].reset_index(drop=True)
        self.save('S12_random_seeds', best)
        self.save('S12_mean_SD', pd.DataFrame([{'Metric': k, 'Mean': best[k].mean(), 'SD_ddof0': best[k].std(ddof=0)} for k in ['R2', 'r']]))

    def ablation(self):
        rep, _ = self.reference_model()
        a, b, _ = rep.dimensions
        A, B, C = np.arange(a), np.arange(a, a+b), np.arange(a+b, rep.train.shape[1])
        # Preserve original 7a.py column order: LLM+UniMol is B then A.
        groups = {'Text only': B, 'Structural only': A, 'Explicit descriptors only': C,
                  'Structural + text': np.r_[B, A], 'Descriptors + text': np.r_[B, C],
                  'Descriptors + structural': np.r_[A, C], 'All three channels': np.r_[A, B, C]}
        rows = []
        for label, indices in groups.items():
            model = estimator('XGB', jobs=self.args.jobs, params=REFERENCE)
            model.fit(rep.train[:, indices], self.y[:60])
            rows.append({'Channels': label, 'Dimension': len(indices), **metrics(self.y[60:], model.predict(rep.test[:, indices]))})
        self.save('S15_ablation', pd.DataFrame(rows))

    def explain(self):
        rep, model = self.reference_model()
        meta = analysis.explain(model, rep, self.frame, self.save)
        (self.out / 'SHAP_settings.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')

    def proximity(self):
        rep, model = self.reference_model()
        analysis.proximity(model, rep, self.frame, self.save)

    def gnn(self):
        from .gnn import run
        run(self.frame, self.save)
