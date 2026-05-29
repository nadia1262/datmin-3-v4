"""
temporal_consistency_check.py — Check spectral drift across years
================================================================
Compares feature distributions between prediction grids to detect
potential domain shift or systematic preprocessing errors.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import *


def check_temporal_consistency():
    """Compare feature statistics across years."""
    print(f"\n{'='*60}")
    print(f"  TEMPORAL CONSISTENCY CHECK")
    print(f"{'='*60}")

    os.makedirs(os.path.join(RESULTS_DIR, 'temporal_validation'), exist_ok=True)

    stats_rows = []
    for year in YEARS:
        fpath = os.path.join(PREDICTIONS_DIR, f'prediction_grid_{year}.csv')
        if not os.path.exists(fpath):
            print(f"  [SKIP] {year}: file not found")
            continue

        df = pd.read_csv(fpath)
        available = [f for f in FEATURES if f in df.columns]
        if not available:
            print(f"  [SKIP] {year}: no features found")
            continue

        print(f"  {year}: {len(df)} points, {len(available)} features")

        for feat in available:
            col = df[feat].dropna()
            stats_rows.append({
                'year': year,
                'feature': feat,
                'mean': col.mean(),
                'std': col.std(),
                'min': col.min(),
                'max': col.max(),
                'median': col.median(),
                'n': len(col),
                'nan_pct': 100 * df[feat].isna().mean()
            })

    if not stats_rows:
        print("  [FAIL] No data found")
        return

    stats_df = pd.DataFrame(stats_rows)
    stats_df.to_csv(os.path.join(RESULTS_DIR, 'temporal_validation', 'feature_stats_by_year.csv'), index=False)

    # Plot temporal drift for key features
    key_features = ['NDVI', 'NDBI', 'BSI', 'B8']
    key_features = [f for f in key_features if f in stats_df['feature'].unique()]

    if key_features:
        fig, axes = plt.subplots(len(key_features), 1, figsize=(10, 3*len(key_features)))
        if len(key_features) == 1:
            axes = [axes]

        for i, feat in enumerate(key_features):
            subset = stats_df[stats_df['feature'] == feat].sort_values('year')
            axes[i].errorbar(subset['year'], subset['mean'], yerr=subset['std'],
                            fmt='o-', capsize=3, linewidth=2)
            axes[i].set_ylabel(feat, fontsize=11)
            axes[i].set_title(f'{feat} Mean +/- Std by Year', fontsize=12, fontweight='bold')
            axes[i].grid(True, alpha=0.3)

        plt.xlabel('Year')
        plt.tight_layout()
        fig_path = os.path.join(RESULTS_DIR, 'temporal_validation', 'temporal_drift.png')
        fig.savefig(fig_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved {fig_path}")

    # Flag large drifts
    print(f"\n  --- Drift Warnings ---")
    any_drift = False
    for feat in stats_df['feature'].unique():
        sub = stats_df[stats_df['feature'] == feat]
        mean_range = sub['mean'].max() - sub['mean'].min()
        overall_std = sub['std'].mean()
        if overall_std > 0 and mean_range / overall_std > 1.0:
            print(f"  [WARN] {feat}: mean range = {mean_range:.4f}, avg std = {overall_std:.4f} (ratio: {mean_range/overall_std:.2f})")
            any_drift = True

    if not any_drift:
        print(f"  [OK] No significant temporal drift detected")

    print(f"\n  [DONE]")


if __name__ == '__main__':
    check_temporal_consistency()
