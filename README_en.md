# Data and code

[中文](README.md)

This repository contains the data and code for the paper.

## 1. Environment

Environment: Linux and Python 3.10.20.

| Package | Version |
|---|---|
| Python | 3.10.20 |
| numpy | `2.2.6` |
| pandas | `2.3.3` |
| scipy | `1.15.3` |
| scikit-learn | `1.7.2` |
| xgboost | `3.2.0` |
| joblib | `>=1.3.2,<2` |
| rdkit | `2026.3.2` |
| shap | `0.49.1` |
| torch | `2.5.1` |

Dependencies are listed in `requirements.txt` and `requirements-gnn.txt`. Install them from the repository root:

```bash
source "$HOME/miniconda3/etc/profile.d/conda.sh"
source scripts/server_env.sh
conda create --prefix "$HRL_PROJECT_ROOT/envs/core" \
    --override-channels -c conda-forge python=3.10.20 pip -y
conda activate "$HRL_PROJECT_ROOT/envs/core"
python -m pip install -r requirements.txt -r requirements-gnn.txt
```

## 2. Data and caches

- Dataset: `data/raw/dataset.csv`.
- Fixed split: `data/splits.csv`; the first 60 molecules are DS60 and the last 15 are DS15.
- Text embeddings: the supplied CSVs in `data/embeddings/`.
- Structural embeddings: place the matching `unimol.csv` and `unimol.json` in `data/embeddings/` using these filenames.

Existing structural caches are reused. If missing, generate them in an environment with Uni-Mol installed:

```bash
python scripts/prepare_embeddings.py --kind unimol
```

Extraction dependencies are in `requirements-unimol.txt`; use a separate extraction environment. Switch back to the core environment afterward.

Validate the input files:

```bash
python run.py --validate
```

## 3. Complete reproduction

From the repository root:

```bash
nohup bash server_run.sh > server_run.log 2>&1 < /dev/null &
echo $! > server_run.pid
```

Monitor progress:

```bash
tail -n 40 server_run.log
ps -p "$(cat server_run.pid)" -o pid,etime,args
```

The script runs all numerical experiments, exports templates and parameter grids, and collects the results. Structural embeddings are loaded from existing caches when available. Running again updates files in `results/`; back up that directory to preserve the supplied outputs.

## 4. Outputs and individual experiments

- `results/S*.csv`: SI tables; see the [table mapping](docs/REPRODUCTION_MAP.md).
- `results/RESULTS_TO_SEND.md`: numerical summary.
- `results/run_metadata.json`: package versions, arguments and task status.
- `results/models/reference.joblib`: reference model saved with `--save-models`.

Results are saved in `results/`. Run individual experiments, for example:

```bash
python run.py --experiments reference ablation --jobs 1 --save-models
python run.py --experiments allocation
python run.py --experiments seeds
```

Run `python scripts/make_report.py` afterward to update the summary. Use `--search smoke` for a quick execution check.

## 5. Optional Qwen API

To generate new text embeddings, replace `API_KEY = "xxx"` in `src/hrlcor/optional_api.py` with your own key, then run:

```bash
python -m pip install -r requirements-api.txt
python scripts/prepare_embeddings.py --kind qwen --allow-api \
    --key qwen_ed3 --refresh-text
```

Generated caches are saved to `generated_embeddings/`.

[Data notes](data/README.md) · [Result files](results/README.md) · Paper citation: `waiting`
