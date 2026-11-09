# SI 表格与运行命令

命令在仓库根目录执行。下表中的实验名用于 `python run.py --experiments 实验名`。

| SI 表格 | 原脚本 | 当前入口 | 主要结果文件（均位于 results） |
|---|---|---|---|
| S1 | 4.py | `allocation` | `S1_descriptor_allocation.csv` |
| S2 | 4.py | `scripts/export_templates.py` | `S2_allocation_templates.csv` |
| S3 | 5.py、6.py | `smiles` | `S3_smiles_text.csv` |
| S4 | 5.py | `scripts/export_templates.py` | `S4_SMILES_templates.csv` |
| S5 | 11.py | `reductions` | `S5_reduction_strategies.csv` |
| S6 | 8.py | `pca` | `S6_PCA_variance.csv` |
| S7 | 9.py | `scripts/export_templates.py` | `S7_text_templates.csv` |
| S8 | 9.py | `templates` | `S8_text_templates.csv` |
| S9 | 12.py、13.py、14.py | `encoders` | `S9_encoders.csv` |
| S10 | 0.py | `scripts/export_templates.py` | `S10_hyperparameters.csv` |
| S11 | 0.py | `baseline` | `S11_descriptor_baseline.csv` |
| S12 | 2.py | `seeds` | `S12_random_seeds.csv`、`S12_mean_SD.csv` |
| S13 | 1.py | `reference` | `S13_reference.csv` |
| S14 | 3c.py、3e.py | `reference` | `S14_DS15_predictions.csv`、`S14_mean_residual_CI.csv` |
| S15 | 7a.py | `ablation` | `S15_ablation.csv` |
| S16 | 3e.py | `explain` | `S16_shap_top10.csv` |
| S17 | 3e.py | `explain` | `S17_shap_channels.csv` |
| S18 | 3e.py | `explain` | `S18_text_descriptor_correlations.csv` |
| S19 | 3e.py | `explain` | `S19_top10_IE_correlations.csv` |
| S20 | 3e.py | `explain` | `S20_structural_IE_correlations.csv` |
| S21 | 10b.py | `proximity` | `S21_distance_ranges.csv` |
| S22 | 10b.py | `proximity` | `S22_proximity_error_correlations.csv` |
| S23 | 10b.py | `proximity` | `S23_proximity_scores.csv` |

完整运行使用 `bash server_run.sh`，会自动导出模板、参数网格并汇总数值。

- `benchmark`：参考输入上的四回归器比较。
- `gnn`：GNN 基线。
- `pca`：预测特征的 PCA 方差保留率比较。
- `python scripts/make_report.py`：从已有 CSV 更新汇总。

[中文说明](../README.md) · [English](../README_en.md)
