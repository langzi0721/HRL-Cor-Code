# 论文数据与代码

[English](README_en.md)

本仓库是论文的数据与代码。

## 1. 环境

运行环境：Linux、Python 3.10.20。

| 库 | 版本 |
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

依赖分别列在 `requirements.txt` 和 `requirements-gnn.txt`。在仓库根目录执行以下命令安装：

```bash
source "$HOME/miniconda3/etc/profile.d/conda.sh"
source scripts/server_env.sh
conda create --prefix "$HRL_PROJECT_ROOT/envs/core" \
    --override-channels -c conda-forge python=3.10.20 pip -y
conda activate "$HRL_PROJECT_ROOT/envs/core"
python -m pip install -r requirements.txt -r requirements-gnn.txt
```

## 2. 数据和缓存

- 原始数据：`data/raw/dataset.csv`。
- 固定划分：`data/splits.csv`，前 60 个为 DS60，后 15 个为 DS15。
- 文本 embedding：`data/embeddings/` 中的已有 CSV。
- 结构 embedding：将配套的 `unimol.csv`、`unimol.json` 放入 `data/embeddings/`，文件名保持不变。

已有结构缓存会直接复用。缺少时，在安装了 Uni-Mol 的环境中生成：

```bash
python scripts/prepare_embeddings.py --kind unimol
```

Uni-Mol 提取依赖见 `requirements-unimol.txt`，建议单独安装到提取环境。生成后切回核心环境即可。

检查输入文件：

```bash
python run.py --validate
```

## 3. 完整复现

在仓库根目录执行：

```bash
nohup bash server_run.sh > server_run.log 2>&1 < /dev/null &
echo $! > server_run.pid
```

查看进度：

```bash
tail -n 40 server_run.log
ps -p "$(cat server_run.pid)" -o pid,etime,args
```

脚本执行全部数值实验、导出模板和参数表，再汇总结果。结构表示优先读取已有缓存。运行会更新 `results/` 下的同名文件，保留旧结果时请先备份。

## 4. 输出和单独运行

- `results/S*.csv`：SI 表格；具体文件对应关系见 [SI 对应表](docs/REPRODUCTION_MAP.md)。
- `results/RESULTS_TO_SEND.md`：数值汇总。
- `results/run_metadata.json`：依赖版本、运行参数和各任务状态。
- `results/models/reference.joblib`：启用 `--save-models` 时保存的参考模型。

结果保存在 `results/`。单独运行实验，例如：

```bash
python run.py --experiments reference ablation --jobs 1 --save-models
python run.py --experiments allocation
python run.py --experiments seeds
```

单独运行后，可用 `python scripts/make_report.py` 更新汇总。`--search smoke` 用于快速检查运行流程。

## 5. 可选 Qwen API

重新生成文本 embedding 时，将 `src/hrlcor/optional_api.py` 中的 `API_KEY = "xxx"` 改成自己的密钥，再执行：

```bash
python -m pip install -r requirements-api.txt
python scripts/prepare_embeddings.py --kind qwen --allow-api \
    --key qwen_ed3 --refresh-text
```

生成的缓存保存到 `generated_embeddings/`。

[数据说明](data/README.md) · [结果文件](results/README.md) · 论文引用信息： waiting`
