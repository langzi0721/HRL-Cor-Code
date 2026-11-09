"""Optional, explicit paid API access. Never imported during cache-only runs."""
import json, time
import numpy as np
from .data import ROOT, digest
from .prompts import texts

# Optional: users who deliberately regenerate Qwen caches fill their own key.
API_KEY = "xxx"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL = "text-embedding-v4"
DIMENSIONS = 1024

def generate(frame, key):
    folder=ROOT/'generated_embeddings';folder.mkdir(exist_ok=True)
    path=folder/(key+'.csv')
    meta_path=path.with_suffix('.json')
    if path.exists() and meta_path.exists():
        meta=json.loads(meta_path.read_text(encoding='utf-8'))
        if meta.get('dataset_sha256')==digest(ROOT/'data/raw/dataset.csv') and meta.get('csv_sha256')==digest(path):
            import pandas as pd
            array=pd.read_csv(path).to_numpy(float)
            if array.shape==(75,DIMENSIONS) and np.isfinite(array).all() and np.all(np.any(array!=0,axis=1)):
                return array
    if API_KEY.strip() in ('', 'xxx'):
        raise RuntimeError('API was explicitly enabled, but API_KEY is still xxx in src/hrlcor/optional_api.py.')
    import requests
    vectors=[]
    for text in texts(frame, key):
        for attempt in range(3):
            try:
                response=requests.post(BASE_URL.rstrip('/')+'/embeddings',
                    headers={'Authorization':'Bearer '+API_KEY, 'Content-Type':'application/json'},
                    json={'model':MODEL,'input':[text],'dimensions':DIMENSIONS}, timeout=(15,60))
                response.raise_for_status()
                vector=np.asarray(response.json()['data'][0]['embedding'], dtype=float)
                if vector.shape != (DIMENSIONS,) or not np.isfinite(vector).all() or not np.any(vector):
                    raise ValueError('Invalid embedding returned by API.')
                vectors.append(vector);break
            except Exception:
                if attempt==2:
                    raise RuntimeError('Qwen embedding request failed; no zero-vector fallback and no cache was written.') from None
                time.sleep(2**attempt)
    array=np.asarray(vectors)
    # Never overwrite published caches, nor silently mix current API outputs with old ones.
    import pandas as pd
    pd.DataFrame(array).to_csv(path,index=False)
    path.with_suffix('.json').write_text(json.dumps({'model':MODEL,'dimension':DIMENSIONS,
        'dataset_sha256':digest(ROOT/'data/raw/dataset.csv'),'csv_sha256':digest(path),
        'source':'New optional API run; not the legacy published cache.'},indent=2),encoding='utf-8')
    return array
