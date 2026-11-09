# 输出文件

| 文件 | 内容 |
|---|---|
| `S*.csv` | SI 对应表格，详见 [对应表](../docs/REPRODUCTION_MAP.md) |
| `*_all_models.csv` | 各算法的完整比较结果 |
| `S12_mean_SD.csv` | 随机种子的均值与标准差 |
| `S14_mean_residual_CI.csv` | 残差统计与均值置信区间 |
| `RESULTS_TO_SEND.md` | 数值汇总 |
| `run_metadata.json` | 软件版本、运行参数和任务状态 |
| `reference_check.csv` | 参考模型与论文报告值对照 |
| `reference_four_regressors.csv` | 四回归器比较 |
| `gnn_metrics.csv`、`gnn_predictions.csv` | GNN 指标及预测 |
| `Fig5_all_predictions.csv` | 全部 75 个分子的预测数据 |
| `Main_Table2_dimensions.csv` | 通道维数 |
| `shap_values_DS15.csv`、`SHAP_settings.json` | SHAP 数值与设置 |
| `nearest_training_molecules.csv` | 最近训练分子 |
| `models/reference.joblib` | 保存的参考模型及预处理器 |

本目录已有服务器运行结果。再次运行会更新同名文件，需要保留时请先备份。`python scripts/make_report.py` 可从已有 CSV 更新汇总。

[中文复现步骤](../README.md) · [English instructions](../README_en.md)
