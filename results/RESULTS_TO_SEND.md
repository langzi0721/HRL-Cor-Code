# Server reproduction results

Only actual outputs from this directory are collected. Missing tables remain marked.

## Run status

```json
{
  "python": "3.10.20",
  "platform": "Linux-5.14.0-570.55.1.el9_6.x86_64-x86_64-with-glibc2.34",
  "packages": {
    "numpy": "2.2.6",
    "pandas": "2.3.3",
    "scipy": "1.15.3",
    "scikit-learn": "1.7.2",
    "xgboost": "3.2.0",
    "shap": "0.49.1",
    "rdkit": "2026.3.2",
    "torch": "2.5.1+cu121"
  },
  "experiments": {
    "reference": "completed",
    "benchmark": "completed",
    "baseline": "completed",
    "allocation": "completed",
    "smiles": "completed",
    "reductions": "completed",
    "pca": "completed",
    "templates": "completed",
    "encoders": "completed",
    "seeds": "completed",
    "ablation": "completed",
    "explain": "completed",
    "proximity": "completed",
    "gnn": "completed"
  }
}
```

## Reference model

| Model | R2 | r | MAE_pp | RMSE_pp |
| --- | --- | --- | --- | --- |
| XGB | 0.7418424012 | 0.8907487016 | 39.55238844 | 46.17607395 |

## Check against the paper

| Quantity | Paper | Rerun | Matches_to_4dp |
| --- | --- | --- | --- |
| R2 | 0.7418 | 0.7418424012 | True |
| r | 0.8907 | 0.8907487016 | True |

## Feature dimensions

| Channel | Original_dimension | Retained_dimension |
| --- | --- | --- |
| Structural | 512 | 12 |
| Text | 1024 | 37 |
| Explicit descriptors | 2 | 2 |
| Heterogeneous | 1538 | 51 |

## Four reference regressors

| Configuration | Model | Seed | R2 | r | MAE_pp | RMSE_pp | Structural_dim | Text_dim | Numerical_dim | Total_dim | Search_mode | Convergence_warning_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ED3 reference | RF | 42 | 0.4852949046 | 0.785932091 | 58.13958835 | 65.20092879 | 12 | 37 | 2 | 51 | full | 0 |
| ED3 reference | XGB | 42 | 0.7418424012 | 0.8907487016 | 39.55238844 | 46.17607395 | 12 | 37 | 2 | 51 | full | 0 |
| ED3 reference | SVM | 42 | 0.4195073208 | 0.6736587358 | 60.17685322 | 69.24252907 | 12 | 37 | 2 | 51 | full | 0 |
| ED3 reference | MLP | 42 | 0.4971378287 | 0.7327584507 | 57.32759481 | 64.44645477 | 12 | 37 | 2 | 51 | full | 36 |

## Descriptor baseline

| Configuration | Model | Seed | R2 | r | MAE_pp | RMSE_pp | Structural_dim | Text_dim | Numerical_dim | Total_dim | Search_mode | Convergence_warning_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Five descriptors | RF | 42 | 0.3033868076 | 0.553978158 | 65.77029359 | 75.85258676 | 0 | 0 | 5 | 5 | full | 0 |
| Five descriptors | XGB | 42 | 0.1261964871 | 0.4074809588 | 73.3670656 | 84.95353239 | 0 | 0 | 5 | 5 | full | 0 |
| Five descriptors | SVM | 42 | 0.2223955102 | 0.5035939968 | 68.03144461 | 80.14084702 | 0 | 0 | 5 | 5 | full | 0 |
| Five descriptors | MLP | 42 | 0.306654721 | 0.5688948857 | 63.88460751 | 75.67445987 | 0 | 0 | 5 | 5 | full | 109 |

## GNN baseline

| Model | Device | R2 | r | MAE_pp | RMSE_pp |
| --- | --- | --- | --- | --- | --- |
| GNN | cuda | 0.4511292625 | 0.6821846348 | 55.83232102 | 67.3301508 |

## Descriptor allocation

| Configuration | Model | Seed | R2 | r | MAE_pp | RMSE_pp | Structural_dim | Text_dim | Numerical_dim | Total_dim | Search_mode | Convergence_warning_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ED0 | XGB | 42 | 0.5049742785 | 0.7140377557 | 51.78877764 | 63.94232612 | 12 | 36 | 5 | 53 | full | 0 |
| ED1 | RF | 42 | 0.5316148871 | 0.8097886758 | 53.96133843 | 62.19795273 | 12 | 37 | 4 | 53 | full | 0 |
| ED2 | XGB | 42 | 0.6561514351 | 0.8285344978 | 45.43196435 | 53.29152601 | 12 | 37 | 3 | 52 | full | 0 |
| ED3 | XGB | 42 | 0.7418424012 | 0.8907487016 | 39.55238844 | 46.17607395 | 12 | 37 | 2 | 51 | full | 0 |
| ED4 | XGB | 42 | 0.518930044 | 0.7272772778 | 55.3017597 | 63.03455133 | 12 | 37 | 1 | 50 | full | 0 |
| ED5 | XGB | 42 | 0.5453733046 | 0.7647791988 | 54.96300221 | 61.27763781 | 12 | 37 | 0 | 49 | full | 0 |

## SMILES text

| Configuration | Model | Seed | R2 | r | MAE_pp | RMSE_pp | Structural_dim | Text_dim | Numerical_dim | Total_dim | Search_mode | Convergence_warning_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| With Uni-Mol | XGB | 42 | 0.6176970529 | 0.8152038816 | 46.33736033 | 56.19250223 | 12 | 37 | 2 | 51 | full | 0 |
| Without Uni-Mol | RF | 42 | 0.4191716492 | 0.696418372 | 61.4304115 | 69.26254603 | 0 | 37 | 2 | 39 | full | 0 |

## Reduction strategies

| Configuration | Model | Seed | R2 | r | MAE_pp | RMSE_pp | Structural_dim | Text_dim | Numerical_dim | Total_dim | Search_mode | Convergence_warning_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | MLP | 42 | 0.5045077018 | 0.7355242447 | 59.0256338 | 63.97245281 | 512 | 1024 | 2 | 1538 | full | 21 |
| B | MLP | 42 | 0.5160903959 | 0.7393147905 | 55.79293252 | 63.22031702 | 512 | 37 | 2 | 551 | full | 30 |
| C | SVM | 42 | 0.3982249117 | 0.6551629458 | 61.31428427 | 70.50041137 | 12 | 1024 | 2 | 1038 | full | 0 |
| D | RF | 42 | 0.522169242 | 0.75089013 | 52.41898882 | 62.82197699 | 31 | 37 | 2 | 70 | full | 0 |
| E | XGB | 42 | 0.5505491232 | 0.790973463 | 56.31371643 | 60.92782353 | 31 | 31 | 2 | 64 | full | 0 |
| F | XGB | 42 | 0.7418424012 | 0.8907487016 | 39.55238844 | 46.17607395 | 12 | 37 | 2 | 51 | full | 0 |
| G | SVM | 42 | 0.5421690044 | 0.7423080351 | 53.51085265 | 61.49320717 | 12 | 31 | 2 | 45 | full | 0 |

## PCA retained variance

| Configuration | Model | Seed | R2 | r | MAE_pp | RMSE_pp | Structural_dim | Text_dim | Numerical_dim | Total_dim | Search_mode | Convergence_warning_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 60 | XGB | 42 | 0.6704667647 | 0.8662971385 | 43.05154957 | 52.17039916 | 12 | 16 | 2 | 30 | full | 0 |
| 65 | XGB | 42 | 0.6924474106 | 0.8595338168 | 42.10002687 | 50.40043008 | 12 | 18 | 2 | 32 | full | 0 |
| 70 | XGB | 42 | 0.6804220307 | 0.8498251366 | 43.21255455 | 51.37631664 | 12 | 21 | 2 | 35 | full | 0 |
| 75 | XGB | 42 | 0.6255914487 | 0.8221930822 | 47.20236044 | 55.60929997 | 12 | 24 | 2 | 38 | full | 0 |
| 80 | XGB | 42 | 0.5371275718 | 0.7809533185 | 52.82636865 | 61.83084824 | 12 | 28 | 2 | 42 | full | 0 |
| 85 | XGB | 42 | 0.6302672288 | 0.8679139655 | 47.63980487 | 55.26097223 | 12 | 32 | 2 | 46 | full | 0 |
| 90 | XGB | 42 | 0.7418424012 | 0.8907487016 | 39.55238844 | 46.17607395 | 12 | 37 | 2 | 51 | full | 0 |
| 95 | XGB | 42 | 0.70223229 | 0.8403570365 | 41.30675792 | 49.59219705 | 12 | 44 | 2 | 58 | full | 0 |
| 100 | XGB | 42 | 0.6411847081 | 0.8188353236 | 46.12239594 | 54.43898511 | 12 | 60 | 2 | 74 | full | 0 |

## Text templates

| Configuration | Model | Seed | R2 | r | MAE_pp | RMSE_pp | Structural_dim | Text_dim | Numerical_dim | Total_dim | Search_mode | Convergence_warning_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | XGB | 42 | 0.7418424012 | 0.8907487016 | 39.55238844 | 46.17607395 | 12 | 37 | 2 | 51 | full | 0 |
| B | RF | 42 | 0.4591946219 | 0.7032879614 | 55.92736955 | 66.8336299 | 12 | 36 | 2 | 50 | full | 0 |
| C | XGB | 42 | 0.4868779286 | 0.7729343116 | 59.09102067 | 65.10058578 | 12 | 37 | 2 | 51 | full | 0 |
| D | MLP | 42 | 0.5357830147 | 0.8196376321 | 56.83184686 | 61.9205866 | 12 | 25 | 2 | 39 | full | 37 |
| E | MLP | 42 | 0.5019746496 | 0.7550435237 | 57.34945109 | 64.13576412 | 12 | 37 | 2 | 51 | full | 36 |
| F | XGB | 42 | 0.452268761 | 0.7107684934 | 61.25827729 | 67.26022317 | 12 | 22 | 2 | 36 | full | 0 |

## Alternative encoders

| Configuration | Model | Seed | R2 | r | MAE_pp | RMSE_pp | Structural_dim | Text_dim | Numerical_dim | Total_dim | Search_mode | Convergence_warning_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen | XGB | 42 | 0.7418424012 | 0.8907487016 | 39.55238844 | 46.17607395 | 12 | 37 | 2 | 51 | full | 0 |
| BGE-M3 | XGB | 42 | 0.326431541 | 0.6573767631 | 65.43153465 | 74.5873916 | 12 | 35 | 2 | 49 | full | 0 |
| SciBERT | XGB | 42 | 0.4957700419 | 0.7218488483 | 57.04639199 | 64.53404254 | 12 | 21 | 2 | 35 | full | 0 |
| Morgan-Qwen | XGB | 42 | 0.5640026314 | 0.819051312 | 52.17140137 | 60.00901284 | 4 | 37 | 2 | 43 | full | 0 |

## Random seeds

| Configuration | Model | Seed | R2 | r | MAE_pp | RMSE_pp | Structural_dim | Text_dim | Numerical_dim | Total_dim | Search_mode | Convergence_warning_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 37 | XGB | 37 | 0.6500675357 | 0.8334972645 | 46.84088616 | 53.76091677 | 12 | 37 | 2 | 51 | full | 0 |
| 38 | XGB | 38 | 0.7131622512 | 0.8515492309 | 42.43993691 | 48.67351397 | 12 | 37 | 2 | 51 | full | 0 |
| 39 | XGB | 39 | 0.7250929215 | 0.8883531367 | 40.88663765 | 47.65050523 | 12 | 37 | 2 | 51 | full | 0 |
| 40 | XGB | 40 | 0.7465846369 | 0.8933254681 | 39.71353203 | 45.74999158 | 12 | 37 | 2 | 51 | full | 0 |
| 41 | XGB | 41 | 0.7220899196 | 0.8666274933 | 41.46743828 | 47.9100582 | 12 | 37 | 2 | 51 | full | 0 |
| 42 | XGB | 42 | 0.7418424012 | 0.8907487016 | 39.55238844 | 46.17607395 | 12 | 37 | 2 | 51 | full | 0 |
| 43 | XGB | 43 | 0.6576539034 | 0.8503896519 | 48.20537633 | 53.17496818 | 12 | 37 | 2 | 51 | full | 0 |
| 44 | XGB | 44 | 0.7280801816 | 0.8695701368 | 38.75636983 | 47.39090249 | 12 | 37 | 2 | 51 | full | 0 |
| 45 | XGB | 45 | 0.639714927 | 0.8172030237 | 47.99512056 | 54.5503678 | 12 | 37 | 2 | 51 | full | 0 |
| 46 | XGB | 46 | 0.7536579382 | 0.8942471549 | 37.69652449 | 45.10698865 | 12 | 37 | 2 | 51 | full | 0 |

## Seed mean and SD

| Metric | Mean | SD_ddof0 |
| --- | --- | --- |
| R2 | 0.7077946616 | 0.04024004894 |
| r | 0.8655511262 | 0.02560849289 |

## DS15 predictions

| Molecule | True_IE | Predicted_IE | Absolute_error_pp |
| --- | --- | --- | --- |
| 2-Amino-2-methyl-1,3-propanediol | -151.8008513 | -98.24349213 | 53.55735917 |
| 3-Hydroxyacetophenone | -33.1050366 | -62.21434784 | 29.10931124 |
| 4-Hydroxybenzyl alcohol | -135.20191 | -143.1416626 | 7.939752598 |
| 4-Pyridinecarboxylic acid | 39.84782897 | 32.23086548 | 7.616963491 |
| 2,4-Dihydroxybenzoic acid | -141.3369829 | -88.72566986 | 52.61131304 |
| 3,4-Pyridinedicarboxylic acid | 76.04090049 | 35.46986771 | 40.57103278 |
| D-Glucose | -23.40081753 | -37.05073547 | 13.64991794 |
| Itaconic acid | 63.60435532 | 19.2719593 | 44.33239602 |
| L-Sorbose | 46.16377075 | 21.09541893 | 25.06835182 |
| L-Threonine | -215.67651 | -137.0131378 | 78.66337218 |
| Methylmalonic acid | 34.86067066 | 5.353316307 | 29.50735435 |
| Pyridazine | 15.93696116 | -45.9120903 | 61.84905146 |
| Tartronic acid | -32.73124088 | 18.11628151 | 50.84752239 |
| Tricarballylic acid | 50.22488033 | 37.88333511 | 12.34154522 |
| Vanillic acid | -119.4542583 | -33.83367538 | 85.62058292 |

## Mean residual interval

| Mean_residual_pp | SD_pp_ddof1 | Mean_residual_CI95_lower | Mean_residual_CI95_upper |
| --- | --- | --- | --- |
| -3.287631519 | 47.67547983 | -29.68943223 | 23.11416919 |

## Channel ablation

| Channels | Dimension | R2 | r | MAE_pp | RMSE_pp |
| --- | --- | --- | --- | --- | --- |
| Text only | 37 | 0.4865283031 | 0.7083749879 | 55.72027583 | 65.12276076 |
| Structural only | 12 | 0.5455735138 | 0.7512979796 | 54.86197083 | 61.26414355 |
| Explicit descriptors only | 2 | 0.3055431659 | 0.5547222064 | 65.36820034 | 75.73509535 |
| Structural + text | 49 | 0.6355128082 | 0.810972015 | 47.54107834 | 54.86756469 |
| Descriptors + text | 39 | 0.5790758712 | 0.8510634453 | 53.30391694 | 58.9625774 |
| Descriptors + structural | 14 | 0.6020614931 | 0.8052891127 | 51.45364022 | 57.33007785 |
| All three channels | 51 | 0.7418424012 | 0.8907487016 | 39.55238844 | 46.17607395 |

## SHAP top ten

| Rank | Feature | Channel | Mean_abs_SHAP | Share_percent |
| --- | --- | --- | --- | --- |
| 1 | LLM-PC1 | Text | 15.1565628 | 16.60836121 |
| 2 | CATS3D_02_AP | Explicit descriptors | 12.29797832 | 13.47596212 |
| 3 | Mor04m | Explicit descriptors | 10.62950435 | 11.64767039 |
| 4 | LLM-PC15 | Text | 9.185449444 | 10.06529411 |
| 5 | LLM-PC14 | Text | 7.291368551 | 7.989785298 |
| 6 | LLM-PC36 | Text | 7.116710881 | 7.798397732 |
| 7 | Uni-Mol-L11 | Structural | 6.629172702 | 7.264159838 |
| 8 | Uni-Mol-L8 | Structural | 6.460056903 | 7.07884498 |
| 9 | Uni-Mol-L6 | Structural | 4.125022021 | 4.520144615 |
| 10 | Uni-Mol-L7 | Structural | 3.465600854 | 3.797559615 |

## SHAP channels

| Channel | Mean_abs_SHAP | Share_percent |
| --- | --- | --- |
| Structural | 21.07221935 | 23.09065949 |
| Text | 47.25892733 | 51.785708 |
| Explicit descriptors | 22.92748267 | 25.12363251 |

## Text-descriptor correlations

| Text_component | LUMO / eV | E1p | P_VSA_MR_5 |
| --- | --- | --- | --- |
| LLM-PC1 | 0.6329971295 | 0.3485213894 | 0.6681775224 |
| LLM-PC15 | 0.02886982965 | -0.2620213489 | -0.08269164143 |
| LLM-PC14 | 0.2432290733 | -0.1924245046 | 0.07027018207 |
| LLM-PC36 | -0.0875592613 | 0.07866344241 | 0.1365221081 |

## Feature-IE correlations

| Feature | Channel | Pearson_r_with_IE_DS60 |
| --- | --- | --- |
| LLM-PC1 | Text | -0.5535252854 |
| CATS3D_02_AP | Explicit descriptors | -0.5599594113 |
| Mor04m | Explicit descriptors | 0.2903643905 |
| LLM-PC15 | Text | -0.1493648361 |
| LLM-PC14 | Text | -0.2668709916 |
| LLM-PC36 | Text | 0.1926390069 |
| Uni-Mol-L11 | Structural | -0.4678894131 |
| Uni-Mol-L8 | Structural | 0.4167884528 |
| Uni-Mol-L6 | Structural | -0.3816442518 |
| Uni-Mol-L7 | Structural | 0.3339500469 |

## Structural-IE correlations

| Feature | Channel | Pearson_r_with_IE_DS60 |
| --- | --- | --- |
| Uni-Mol-L11 | Structural | -0.4678894131 |
| Uni-Mol-L8 | Structural | 0.4167884528 |
| Uni-Mol-L6 | Structural | -0.3816442518 |
| Uni-Mol-L7 | Structural | 0.3339500469 |

## Distance reference ranges

| Space | Minimum | Median | Maximum |
| --- | --- | --- | --- |
| Structural | 1.434091781 | 2.579544524 | 4.476643003 |
| Text | 8.208204348 | 27.66310065 | 43.58266036 |
| Explicit descriptors | 0 | 0.02879398673 | 1.39983074 |
| Structural-text | 1.632672356 | 4.66794789 | 7.243143179 |
| Heterogeneous | 1.634402214 | 4.846355712 | 7.470958108 |

## Proximity-error correlations

| Space | Pearson_r |
| --- | --- |
| Morgan | 0.2855703021 |
| Structural | -0.07093289573 |
| Text | -0.1945181263 |
| Explicit descriptors | 0.04161680844 |
| Structural-text | -0.1508135421 |
| Heterogeneous | -0.1056476423 |

## Individual molecular scores

| ID | Molecule | Absolute_error_pp | Morgan | Structural | Text | Explicit descriptors | Structural-text | Heterogeneous |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2-Amino-2-methyl-1,3-propanediol | 53.55735917 | 0.4666666667 | 0.8528920741 | 0.4435622481 | 0.9928947911 | 0.4420255501 | 0.3521501133 |
| 2 | 3-Hydroxyacetophenone | 29.10931124 | 0.3461538462 | 0.7214684784 | 0.6829845431 | 0.9762209873 | 0.7063045817 | 0.7162369002 |
| 3 | 4-Hydroxybenzyl alcohol | 7.939752598 | 0.347826087 | 0.8220801953 | 0.7492947585 | 0.9978114509 | 0.7740916254 | 0.7803238247 |
| 4 | 4-Pyridinecarboxylic acid | 7.616963491 | 0.55 | 0.7827697683 | 0.9348650824 | 0.9930810332 | 0.924196952 | 0.9201505106 |
| 5 | 2,4-Dihydroxybenzoic acid | 52.61131304 | 0.6153846154 | 1 | 1 | 0.9909919462 | 1 | 1 |
| 6 | 3,4-Pyridinedicarboxylic acid | 40.57103278 | 0.4782608696 | 0.6966755911 | 1 | 0.9845352484 | 1 | 1 |
| 7 | D-Glucose | 13.64991794 | 0.1351351351 | 0.8238038757 | 0.6411158799 | 0.9981652152 | 0.6267774502 | 0.6218162727 |
| 8 | Itaconic acid | 44.33239602 | 0.3333333333 | 0.7452282494 | 0.547162765 | 0.9237392532 | 0.5631500132 | 0.5571547318 |
| 9 | L-Sorbose | 25.06835182 | 0.2352941176 | 0.6742619432 | 0.51168095 | 0.8725283165 | 0.4922347722 | 0.4809410679 |
| 10 | L-Threonine | 78.66337218 | 0.3684210526 | 0.4804605891 | 0.5399463481 | 0.99884525 | 0.5569388828 | 0.5416775646 |
| 11 | Methylmalonic acid | 29.50735435 | 0.4 | 0.404230972 | 0.4909735317 | 0.9934071772 | 0.4913110527 | 0.4995332016 |
| 12 | Pyridazine | 61.84905146 | 0.2941176471 | 0.708132264 | 0.5674987731 | 0.959419856 | 0.576439421 | 0.5798696093 |
| 13 | Tartronic acid | 50.84752239 | 0.5384615385 | 0.5846365477 | 0.8956305066 | 0.9384343307 | 0.9000817065 | 0.8112993603 |
| 14 | Tricarballylic acid | 12.34154522 | 0.5 | 0.7073878386 | 0.5787094356 | 0.9591619731 | 0.5304033027 | 0.3612277241 |
| 15 | Vanillic acid | 85.62058292 | 0.5714285714 | 0.8422481287 | 0.5570794018 | 0.9814138718 | 0.5693955331 | 0.5823934179 |

