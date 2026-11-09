# 数据文件

| 路径 | 内容 |
|---|---|
| `raw/dataset.csv` | 原始 75 个分子、SMILES、IE 和五个描述符 |
| `splits.csv` | 固定划分：前 60 个为 DS60，后 15 个为 DS15 |
| `embeddings/` | 文本与结构 embedding CSV |
| `manifest.json` | 已提供数据和文本缓存的来源、形状及校验值 |

IE 列名为 `ie_ze41`，允许负值。复现时使用原始文件与行序。

结构缓存 `unimol.csv` 和 `unimol.json` 需要配套放入 `embeddings/`。没有时可按 [README](../README.md) 生成。

文本缓存：`qwen_ed0`–`qwen_ed5` 对应 ED0–ED5，`qwen_ed3` 同时作为模板 A；`qwen_prompt_B`–`qwen_prompt_F` 为其他模板；`qwen_smiles` 为包含 SMILES 的模板；`bge_m3`、`scibert` 为其他文本编码器。

数据来源：[npj Computational Materials 2021](https://doi.org/10.1038/s41524-021-00658-7)、[npj Materials Degradation 2023](https://doi.org/10.1038/s41529-023-00391-0)。第三方数据遵循原来源的授权。

## English

Keep the dataset and cached embeddings in their original order. Place both structural cache files in `embeddings/`. File checksums are recorded in `manifest.json`; see the main [README](../README_en.md) for execution instructions.
