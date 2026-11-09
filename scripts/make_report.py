#!/usr/bin/env python3
"""Collect actual server outputs into one report for the authors to send back."""
from pathlib import Path
import argparse
import csv
import json

TABLES = [
    ('Reference model', 'S13_reference'), ('Check against the paper', 'reference_check'),
    ('Feature dimensions', 'Main_Table2_dimensions'), ('Four reference regressors', 'reference_four_regressors'),
    ('Descriptor baseline', 'S11_descriptor_baseline_all_models'), ('GNN baseline', 'gnn_metrics'),
    ('Descriptor allocation', 'S1_descriptor_allocation'), ('SMILES text', 'S3_smiles_text'),
    ('Reduction strategies', 'S5_reduction_strategies'), ('PCA retained variance', 'S6_PCA_variance'),
    ('Text templates', 'S8_text_templates'), ('Alternative encoders', 'S9_encoders'),
    ('Random seeds', 'S12_random_seeds'), ('Seed mean and SD', 'S12_mean_SD'),
    ('DS15 predictions', 'S14_DS15_predictions'), ('Mean residual interval', 'S14_mean_residual_CI'),
    ('Channel ablation', 'S15_ablation'), ('SHAP top ten', 'S16_shap_top10'),
    ('SHAP channels', 'S17_shap_channels'), ('Text-descriptor correlations', 'S18_text_descriptor_correlations'),
    ('Feature-IE correlations', 'S19_top10_IE_correlations'), ('Structural-IE correlations', 'S20_structural_IE_correlations'),
    ('Distance reference ranges', 'S21_distance_ranges'), ('Proximity-error correlations', 'S22_proximity_error_correlations'),
    ('Individual molecular scores', 'S23_proximity_scores'),
]

def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', type=Path, default=root/'results')
    args = parser.parse_args()
    args.results.mkdir(parents=True, exist_ok=True)
    lines = ['# Server reproduction results', '',
             'Only actual outputs from this directory are collected. Missing tables remain marked.', '']
    metadata_path = args.results/'run_metadata.json'
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
        lines += ['## Run status', '', '```json', json.dumps({
            k: metadata.get(k) for k in ['python', 'platform', 'packages', 'experiments']
        }, ensure_ascii=False, indent=2), '```', '']
    else:
        lines += ['Run metadata: NOT FOUND.', '']
    for title, filename in TABLES:
        lines += ['## '+title, '']
        path = args.results/(filename+'.csv')
        if not path.exists():
            lines += ['NOT GENERATED: '+path.name, '']; continue
        with path.open(encoding='utf-8-sig', newline='') as f:
            rows = list(csv.reader(f))
        if not rows:
            lines += ['EMPTY: '+path.name, '']; continue
        kept = [i for i, label in enumerate(rows[0]) if label not in ('Best_parameters', 'CV_R2')]
        def markdown_row(row):
            return '| '+' | '.join((row[i] if i < len(row) else '').replace('|', '\\|').replace('\n', ' ') for i in kept)+' |'
        lines += [markdown_row(rows[0]), '| '+' | '.join('---' for _ in kept)+' |']
        lines.extend(markdown_row(row) for row in rows[1:])
        lines.append('')
    target = args.results/'RESULTS_TO_SEND.md'
    target.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print('Report saved:', target)

if __name__ == '__main__':
    main()
