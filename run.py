#!/usr/bin/env python3
"""Run the paper's computations; cached embeddings are the default."""
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parent
# Keep scientific-library/model caches under this checkout.
os.environ.setdefault('XDG_CACHE_HOME', str(ROOT/'.cache'))
os.environ.setdefault('HF_HOME', str(ROOT/'.cache/huggingface'))
os.environ.setdefault('TORCH_HOME', str(ROOT/'.cache/torch'))

import sys, argparse, json, platform, importlib.metadata, traceback
from datetime import datetime, timezone
sys.path.insert(0, str(ROOT/'src'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--validate', action='store_true', help='Validate supplied data/caches without models, GPU or API.')
    parser.add_argument('--experiments', nargs='+', default=['reference', 'ablation'])
    parser.add_argument('--search', choices=['full', 'smoke'], default='full')
    parser.add_argument('--models', nargs='+', choices=['RF', 'XGB', 'SVM', 'MLP'])
    parser.add_argument('--jobs', type=int, default=1)
    parser.add_argument('--output', default=str(ROOT/'results'))
    parser.add_argument('--allow-api', action='store_true', help='Explicitly permit Qwen API for missing Qwen caches; requires editing API_KEY=xxx.')
    parser.add_argument('--save-models', action='store_true', help='Persist fitted reference model and its preprocessing.')
    args = parser.parse_args()
    from hrlcor.data import validate, digest
    if args.validate:
        validate(); return 0
    from hrlcor.experiments import Runner, AVAILABLE
    experiments = AVAILABLE if args.experiments == ['all'] else args.experiments
    unknown = set(experiments) - set(AVAILABLE)
    if unknown: parser.error('Unknown experiments: ' + ', '.join(sorted(unknown)))
    if any(name not in ('baseline', 'gnn') for name in experiments):
        from hrlcor.data import load_embedding
        load_embedding('unimol')
    import warnings
    from sklearn.exceptions import ConvergenceWarning
    warnings.filterwarnings('once', category=ConvergenceWarning)
    runner = Runner(args)
    versions = {}
    for package in ['numpy', 'pandas', 'scipy', 'scikit-learn', 'xgboost', 'shap', 'rdkit', 'torch']:
        try: versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError: pass
    metadata = {'python': platform.python_version(), 'platform': platform.platform(), 'packages': versions,
                'arguments': vars(args), 'dataset_sha256': digest(ROOT/'data/raw/dataset.csv'),
                'started_utc': datetime.now(timezone.utc).isoformat(), 'experiments': {}}
    failed = []
    for name in experiments:
        print(f'\n[{name}] starting', flush=True)
        try:
            getattr(runner, name)()
            metadata['experiments'][name] = 'completed'
        except Exception as error:
            metadata['experiments'][name] = {'status': 'FAILED', 'reason': str(error)}
            failed.append(name)
            traceback.print_exc()
        (runner.out/'run_metadata.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\nResults: {runner.out}; failed experiments: {failed}', flush=True)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
