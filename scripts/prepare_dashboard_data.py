"""
prepare_dashboard_data.py — Pre-compute Dashboard Data
=======================================================
Aggregates classification, change detection, and driver analysis
results into lightweight JSON/CSV files for the Streamlit dashboard.
"""

import os
import sys
import json
import numpy as np
import pandas as pd
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import *


def prepare_classification_summary():
    """Aggregate model comparison data."""
    summaries = []
    for model_name in MODEL_NAMES:
        summary_file = os.path.join(CLASSIFICATION_DIR, f'summary_{model_name}.json')
        if os.path.exists(summary_file):
            with open(summary_file) as f:
                summaries.append(json.load(f))

    if summaries:
        out_file = os.path.join(DASHBOARD_DIR, 'data', 'model_comparison.json')
        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        with open(out_file, 'w') as f:
            json.dump(summaries, f, indent=2, default=str)
        print(f"  [OK] {out_file} ({len(summaries)} models)")
    return summaries


def prepare_temporal_data(model_name):
    """Prepare year-by-year class distribution for dashboard."""
    rows = []
    for year in YEARS:
        pred_file = os.path.join(PREDICTIONS_DIR, f'predictions_{model_name}_{year}.csv')
        if os.path.exists(pred_file):
            df = pd.read_csv(pred_file)
            if 'predicted_class' in df.columns:
                counts = df['predicted_class'].value_counts()
                total = len(df)
                for cls_id, count in counts.items():
                    rows.append({
                        'year': year,
                        'class_id': int(cls_id),
                        'class_name': CLASS_NAMES.get(int(cls_id), f'Class {cls_id}'),
                        'count': int(count),
                        'proportion': round(count / total * 100, 2)
                    })

    if rows:
        out_file = os.path.join(DASHBOARD_DIR, 'data', 'temporal_composition.csv')
        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        pd.DataFrame(rows).to_csv(out_file, index=False)
        print(f"  [OK] {out_file} ({len(rows)} rows)")


def prepare_change_summary():
    """Prepare change detection summary."""
    change_file = os.path.join(CHANGE_DIR, f'change_points_{BASELINE_YEAR}_{ENDLINE_YEAR}.csv')
    if os.path.exists(change_file):
        df = pd.read_csv(change_file)
        summary = {
            'total_points': len(df),
            'changed_points': int(df['is_changed'].sum()) if 'is_changed' in df.columns else 0,
            'forest_loss': int(df['forest_loss'].sum()) if 'forest_loss' in df.columns else 0,
            'forest_gain': int(df['forest_gain'].sum()) if 'forest_gain' in df.columns else 0,
            'urbanization': int(df['urbanization'].sum()) if 'urbanization' in df.columns else 0,
            'mining_expansion': int(df['mining_expansion'].sum()) if 'mining_expansion' in df.columns else 0,
        }
        if summary['total_points'] > 0:
            summary['change_rate_pct'] = round(100 * summary['changed_points'] / summary['total_points'], 2)

        out_file = os.path.join(DASHBOARD_DIR, 'data', 'change_summary.json')
        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        with open(out_file, 'w') as f:
            json.dump(summary, f, indent=2)
        print(f"  [OK] {out_file}")


def prepare_driver_summary():
    """Prepare driver analysis results."""
    for analysis_type in ['deforestation', 'urbanization', 'mining']:
        logit_file = os.path.join(DRIVER_DIR, f'logistic_{analysis_type}_{BASELINE_YEAR}_{ENDLINE_YEAR}.csv')
        if os.path.exists(logit_file):
            df = pd.read_csv(logit_file)
            out_file = os.path.join(DASHBOARD_DIR, 'data', f'driver_{analysis_type}.csv')
            os.makedirs(os.path.dirname(out_file), exist_ok=True)
            df.to_csv(out_file, index=False)
            print(f"  [OK] {out_file}")


def main():
    parser = argparse.ArgumentParser(description='Prepare Dashboard Data')
    parser.add_argument('--model', type=str, default='rf', choices=MODEL_NAMES)
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  PREPARING DASHBOARD DATA")
    print(f"{'='*60}")

    os.makedirs(os.path.join(DASHBOARD_DIR, 'data'), exist_ok=True)

    prepare_classification_summary()
    prepare_temporal_data(args.model)
    prepare_change_summary()
    prepare_driver_summary()

    print(f"\n  [DONE] Dashboard data prepared")


if __name__ == '__main__':
    main()
