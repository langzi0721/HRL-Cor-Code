#!/usr/bin/env python3
"""Generate only missing structural embeddings, or deliberately request optional Qwen API."""
import os, sys, argparse, json, inspect, random, importlib.metadata
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kind', choices=['unimol', 'qwen'], default='unimol')
    parser.add_argument('--weights-dir', type=Path)
    parser.add_argument('--cpu', action='store_true')
    parser.add_argument('--allow-api', action='store_true')
    parser.add_argument('--key', default='qwen_ed3')
    parser.add_argument('--refresh-text', action='store_true', help='Explicitly use the optional API rather than the published CSV; saves separately.')
    args = parser.parse_args()
    os.environ.setdefault('HF_HOME', str(ROOT/'.cache/huggingface'))
    os.environ.setdefault('TORCH_HOME', str(ROOT/'.cache/torch'))
    from hrlcor.data import load_dataset, load_embedding, digest
    frame = load_dataset()
    if args.kind == 'qwen':
        if not args.allow_api: parser.error('Qwen API requires explicit --allow-api and your own API_KEY replacing xxx.')
        if args.refresh_text:
            from hrlcor.optional_api import generate
            array = generate(frame, args.key)
        else:
            array = load_embedding(args.key, allow_api=True)
        print('Text embeddings ready:', array.shape); return
    target = ROOT/'data/embeddings/unimol.csv'
    if target.exists():
        load_embedding('unimol'); print('Existing structural cache is valid; no model download/inference needed.'); return
    weights = args.weights_dir
    automatic = Path.home()/'mrl-rep/weights/Uni-Mol'
    if weights is None and (automatic/'mol_pre_all_h_220816.pt').exists(): weights = automatic
    if weights is not None:
        if not all((weights/name).is_file() for name in ['mol_pre_all_h_220816.pt', 'mol.dict.txt']):
            raise FileNotFoundError('Explicit-hydrogen Uni-Mol V1 needs mol_pre_all_h_220816.pt and mol.dict.txt.')
        os.environ['UNIMOL_WEIGHT_DIR'] = str(weights.resolve())
    try:
        from unimol_tools import UniMolRepr
        import torch
    except ImportError as e:
        raise RuntimeError('Run this script in your Uni-Mol environment; see README.md. The core reproduction environment does not need Uni-Mol.') from e
    import numpy as np
    import pandas as pd
    random.seed(42); np.random.seed(42); torch.manual_seed(42)
    if torch.cuda.is_available(): torch.cuda.manual_seed_all(42)
    signature = inspect.signature(UniMolRepr).parameters
    kwargs = {'data_type': 'molecule'} if 'data_type' in signature else {'molecule_type': 'molecule'}
    for key, value in [('remove_hs', False), ('model_name', 'unimolv1'), ('batch_size', 32), ('use_cuda', not args.cpu)]:
        if key in signature: kwargs[key] = value
    encoder = UniMolRepr(**kwargs)
    arrays = []
    for smiles in [frame.isomeric_smiles.iloc[:60], frame.isomeric_smiles.iloc[60:]]:
        out = encoder.get_repr([str(s).strip() for s in smiles])
        arrays.append(np.asarray(out['cls_repr'] if isinstance(out, dict) else out))
    array = np.vstack(arrays)
    if array.shape != (75, 512) or not np.isfinite(array).all() or np.any(np.all(array == 0, axis=1)):
        raise ValueError('Invalid structural embedding array: ' + str(array.shape))
    original_dtype = str(array.dtype)
    pd.DataFrame(array.astype(np.float64)).to_csv(target, index=False, float_format='%.17g')
    try: version = importlib.metadata.version('unimol-tools')
    except importlib.metadata.PackageNotFoundError: version = 'unknown/source checkout'
    target.with_suffix('.json').write_text(json.dumps({'dataset_sha256': digest(ROOT/'data/raw/dataset.csv'),
        'csv_sha256': digest(target), 'shape': [75, 512], 'original_dtype': original_dtype, 'unimol_tools_version': version,
        'constructor_arguments': kwargs, 'seed': 42, 'source': 'New Uni-Mol V1 extraction; compare rerun metrics with manuscript.'}, indent=2), encoding='utf-8')
    print('Saved:', target, array.shape)


if __name__ == '__main__':
    main()
