"""
change_detection.py — Temporal Change Detection Pipeline
========================================================
Compares predicted land cover across years to detect transitions.
Generates transition matrices, change maps, and hotspot analysis.
"""

import os
import sys
import argparse
import time
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import *


def load_predictions(model_name, years):
    """Load and merge predictions across years into a temporal profile."""
    all_dfs = {}
    for year in years:
        fpath = os.path.join(PREDICTIONS_DIR, f'predictions_{model_name}_{year}.csv')
        if os.path.exists(fpath):
            df = pd.read_csv(fpath)
            all_dfs[year] = df
            print(f"  Loaded {year}: {len(df)} rows")
        else:
            print(f"  [SKIP] {fpath} not found")

    if len(all_dfs) < 2:
        print("  [FAIL] Need at least 2 years for change detection")
        return None

    return all_dfs


def build_temporal_profile(all_dfs, years):
    """Build a unified temporal profile by matching points across years via coordinates."""
    # Use the year with the most points as reference
    ref_year = max(all_dfs.keys(), key=lambda y: len(all_dfs[y]))
    ref_df = all_dfs[ref_year][['lon', 'lat']].copy()
    ref_df = ref_df.round(4)  # Round to avoid floating point matching issues

    profile = ref_df.copy()

    for year in sorted(all_dfs.keys()):
        df = all_dfs[year].copy()
        df['lon'] = df['lon'].round(4)
        df['lat'] = df['lat'].round(4)

        # Merge on coordinates
        merged = profile.merge(
            df[['lon', 'lat', 'predicted_class']].rename(columns={'predicted_class': f'class_{year}'}),
            on=['lon', 'lat'],
            how='left'
        )
        profile = merged

    # Drop rows with any missing year
    class_cols = [f'class_{y}' for y in sorted(all_dfs.keys())]
    profile = profile.dropna(subset=class_cols)

    for col in class_cols:
        profile[col] = profile[col].astype(int)

    print(f"  Temporal profile: {len(profile)} matched points across {len(all_dfs)} years")
    return profile


def compute_transition_matrix(profile, start_year, end_year):
    """Compute NxN transition matrix between two years."""
    col_start = f'class_{start_year}'
    col_end = f'class_{end_year}'

    cm = pd.crosstab(
        profile[col_start].map(CLASS_NAMES),
        profile[col_end].map(CLASS_NAMES),
        margins=True
    )
    return cm


def detect_transitions(profile, start_year, end_year):
    """Flag individual point transitions."""
    col_start = f'class_{start_year}'
    col_end = f'class_{end_year}'

    print(f"\n  Detecting transitions: {start_year} -> {end_year}...")

    df = profile[['lon', 'lat', col_start, col_end]].copy()
    df.columns = ['lon', 'lat', 'class_start', 'class_end']

    df['is_changed'] = (df['class_start'] != df['class_end']).astype(int)
    df['transition_code'] = df['class_start'].astype(str) + '->' + df['class_end'].astype(str)

    # Specific transition types
    df['forest_loss'] = ((df['class_start'] == 0) & (df['class_end'] != 0)).astype(int)
    df['forest_gain'] = ((df['class_start'] != 0) & (df['class_end'] == 0)).astype(int)
    df['urbanization'] = ((df['class_start'] != 2) & (df['class_end'] == 2)).astype(int)
    df['mining_expansion'] = ((df['class_start'] != 3) & (df['class_end'] == 3)).astype(int)

    n_total = len(df)
    n_changed = df['is_changed'].sum()
    pct = 100 * n_changed / n_total if n_total > 0 else 0

    print(f"  Total points: {n_total}")
    print(f"  Changed: {n_changed} ({pct:.1f}%)")
    print(f"  Forest loss: {df['forest_loss'].sum()}")
    print(f"  Forest gain: {df['forest_gain'].sum()}")
    print(f"  Urbanization: {df['urbanization'].sum()}")
    print(f"  Mining expansion: {df['mining_expansion'].sum()}")

    # Top transitions
    top_trans = df[df['is_changed'] == 1]['transition_code'].value_counts().head(10)
    print(f"\n  Top 10 transitions:")
    for code, count in top_trans.items():
        from_cls = int(code.split('->')[0])
        to_cls = int(code.split('->')[1])
        from_name = CLASS_NAMES.get(from_cls, '?')
        to_name = CLASS_NAMES.get(to_cls, '?')
        print(f"    {from_name} -> {to_name}: {count} ({100*count/n_total:.2f}%)")

    return df


def plot_transition_matrix(cm, start_year, end_year, output_dir):
    """Plot heatmap of transition matrix."""
    os.makedirs(output_dir, exist_ok=True)

    # Remove margins for plotting
    cm_plot = cm.drop('All', axis=0, errors='ignore').drop('All', axis=1, errors='ignore')

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        cm_plot, annot=True, fmt='d', cmap='YlOrRd',
        ax=ax, linewidths=0.5
    )
    ax.set_title(f'Land Cover Transition Matrix: {start_year} -> {end_year}',
                 fontsize=14, fontweight='bold')
    ax.set_xlabel(f'Class in {end_year}', fontsize=12)
    ax.set_ylabel(f'Class in {start_year}', fontsize=12)
    plt.tight_layout()

    fig_path = os.path.join(output_dir, f'transition_matrix_{start_year}_{end_year}.png')
    fig.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved {fig_path}")


def plot_temporal_trends(profile, years, output_dir):
    """Plot class proportions over time."""
    os.makedirs(output_dir, exist_ok=True)

    proportions = []
    for year in sorted(years):
        col = f'class_{year}'
        if col in profile.columns:
            counts = profile[col].value_counts(normalize=True)
            for cls_id, pct in counts.items():
                proportions.append({
                    'year': year,
                    'class': CLASS_NAMES.get(int(cls_id), f'Class {cls_id}'),
                    'proportion': pct * 100
                })

    if not proportions:
        return

    prop_df = pd.DataFrame(proportions)

    fig, ax = plt.subplots(figsize=(12, 6))
    for cls_name in CLASS_LABELS:
        subset = prop_df[prop_df['class'] == cls_name]
        if not subset.empty:
            ax.plot(subset['year'], subset['proportion'], 'o-', label=cls_name, linewidth=2, markersize=6)

    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Proportion (%)', fontsize=12)
    ax.set_title('Land Cover Composition Over Time', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    fig_path = os.path.join(output_dir, 'temporal_trends.png')
    fig.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved {fig_path}")

    # Also save data
    prop_df.to_csv(os.path.join(output_dir, 'temporal_trends.csv'), index=False)


def run_change_detection(model_name, start_year, end_year, full_temporal=False):
    """Main change detection pipeline."""
    print(f"\n{'='*60}")
    print(f"  CHANGE DETECTION: {start_year} -> {end_year}")
    print(f"  Model: {model_name}")
    print(f"{'='*60}")

    os.makedirs(CHANGE_DIR, exist_ok=True)

    # 1. Load predictions
    years_to_load = YEARS if full_temporal else [start_year, end_year]
    all_dfs = load_predictions(model_name, years_to_load)
    if all_dfs is None:
        return

    # 2. Build temporal profile
    profile = build_temporal_profile(all_dfs, list(all_dfs.keys()))
    profile.to_csv(os.path.join(CHANGE_DIR, f'temporal_profile_{model_name}.csv'), index=False)

    # 3. Transition matrix (baseline -> endline)
    cm = compute_transition_matrix(profile, start_year, end_year)
    cm.to_csv(os.path.join(CHANGE_DIR, f'transition_matrix_{start_year}_{end_year}.csv'))
    plot_transition_matrix(cm, start_year, end_year, CHANGE_DIR)
    print(f"\n  Transition Matrix ({start_year} -> {end_year}):")
    print(cm.to_string())

    # 4. Detect individual transitions
    transitions = detect_transitions(profile, start_year, end_year)
    transitions.to_csv(os.path.join(CHANGE_DIR, f'change_points_{start_year}_{end_year}.csv'), index=False)

    # 5. Temporal trends
    if full_temporal and len(all_dfs) > 2:
        plot_temporal_trends(profile, list(all_dfs.keys()), CHANGE_DIR)

    print(f"\n  [DONE] Change detection complete")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Land Cover Change Detection')
    parser.add_argument('--model', type=str, default='rf', choices=MODEL_NAMES)
    parser.add_argument('--start', type=int, default=BASELINE_YEAR)
    parser.add_argument('--end', type=int, default=ENDLINE_YEAR)
    parser.add_argument('--full-temporal', action='store_true',
                        help='Process all years, not just start/end')
    args = parser.parse_args()

    run_change_detection(args.model, args.start, args.end, args.full_temporal)
