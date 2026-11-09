"""Immutable published inputs and validated, ordered embedding caches."""
from pathlib import Path
import hashlib, json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DESCRIPTORS = ['LUMO / eV', 'E1p', 'P_VSA_MR_5', 'CATS3D_02_AP', 'Mor04m']
PHYSICAL = ['CATS3D_02_AP', 'Mor04m']

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load_dataset():
    path = ROOT/'data/raw/dataset.csv'
    frame = pd.read_csv(path)
    frame.columns = frame.columns.str.strip()
    if len(frame) != 75 or not set(['name','isomeric_smiles','ie_ze41']+DESCRIPTORS) <= set(frame):
        raise ValueError('Expected the published 75-row dataset and all required columns.')
    if frame[['name','isomeric_smiles']].isna().any().any() or not np.isfinite(frame[['ie_ze41']+DESCRIPTORS].to_numpy(float)).all():
        raise ValueError('Dataset contains missing identifiers or non-finite numeric values.')
    manifest = json.loads((ROOT/'data/manifest.json').read_text(encoding='utf-8'))
    if digest(path) != manifest['dataset_sha256']:
        raise ValueError('Published dataset changed, including row order; use a separate project for new data.')
    return frame

def load_embedding(key, allow_api=False):
    frame = load_dataset()
    manifest = json.loads((ROOT/'data/manifest.json').read_text(encoding='utf-8'))
    item = manifest['embeddings'].get(key)
    path = ROOT/'data/embeddings'/(key+'.csv')
    if not path.exists():
        if key == 'unimol':
            raise FileNotFoundError('Missing structural cache: '+str(path)+'. In your Uni-Mol environment run: python scripts/prepare_embeddings.py --kind unimol')
        if allow_api and key.startswith('qwen_'):
            from .optional_api import generate
            return generate(frame, key)
        raise FileNotFoundError(f'Missing cache: {path}. Restore the supplied CSV. API access is disabled by default.')
    array = pd.read_csv(path, **({'float_precision':'round_trip'} if key == 'unimol' else {})).to_numpy(float)
    dimension = 768 if key == 'scibert' else (512 if key == 'unimol' else 1024)
    if array.shape != (75, dimension) or not np.isfinite(array).all() or np.any(np.all(array == 0, axis=1)):
        raise ValueError(f'Invalid {key} cache: expected 75 x {dimension}, finite, nonzero rows; got {array.shape}')
    if item and digest(path) != item['sha256']:
        raise ValueError(f'Published cache was modified: {path}')
    if key == 'unimol':
        meta_path = path.with_suffix('.json')
        if not meta_path.exists():
            raise ValueError('Uni-Mol cache metadata missing. Run scripts/prepare_embeddings.py --kind unimol.')
        meta = json.loads(meta_path.read_text(encoding='utf-8'))
        if meta.get('dataset_sha256') != digest(ROOT/'data/raw/dataset.csv') or meta.get('csv_sha256') != digest(path):
            raise ValueError('Uni-Mol cache does not match the dataset/checksum.')
        if meta.get('original_dtype'):
            array = array.astype(meta['original_dtype'])
    return array

def validate():
    frame = load_dataset()
    manifest = json.loads((ROOT/'data/manifest.json').read_text(encoding='utf-8'))
    rows=[]
    for key in manifest['embeddings']:
        x=load_embedding(key)
        rows.append({'cache':key,'rows':x.shape[0],'columns':x.shape[1],'status':'OK'})
    print(f'Dataset OK: {len(frame)} molecules; DS60=60, DS15=15; original order preserved.')
    print(pd.DataFrame(rows).to_string(index=False))
    if (ROOT/'data/embeddings/unimol.csv').exists():
        load_embedding('unimol'); print('Uni-Mol structural cache: OK')
    else:
        print('Uni-Mol structural cache: NOT YET GENERATED (required except for the descriptor baseline/GNN).')
    return rows
