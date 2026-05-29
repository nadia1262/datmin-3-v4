"""
dual_driver_analysis.py — IKN x Mining Dual-Driver Analysis
============================================================
Tests whether proximity to IKN and mining density predict
deforestation probability using Logistic Regression.
"""

import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import *


def load_change_data(model_name, start_year, end_year):
    """Load change points with ancillary driver variables."""
    change_file = os.path.join(CHANGE_DIR, f'change_points_{start_year}_{end_year}.csv')
    if not os.path.exists(change_file):
        print(f"  [FAIL] Change file not found: {change_file}")
        return None

    df = pd.read_csv(change_file)
    print(f"  Loaded change data: {len(df)} points")

    # We need driver variables -- load from prediction file
    pred_start = os.path.join(PREDICTIONS_DIR, f'predictions_{model_name}_{start_year}.csv')
    if os.path.exists(pred_start):
        pred_df = pd.read_csv(pred_start)
        pred_df['lon'] = pred_df['lon'].round(4)
        pred_df['lat'] = pred_df['lat'].round(4)
        df['lon'] = df['lon'].round(4)
        df['lat'] = df['lat'].round(4)

        # Merge driver columns
        driver_cols_available = [c for c in ['elevation', 'rainfall_annual', 'distance_to_ikn', 'mining_density_10km'] if c in pred_df.columns]
        if driver_cols_available:
            df = df.merge(pred_df[['lon', 'lat'] + driver_cols_available], on=['lon', 'lat'], how='left')
            print(f"  Merged driver variables: {driver_cols_available}")

    return df


def run_logistic_regression(df, target_col, driver_cols, label):
    """Run logistic regression to test driver significance."""
    print(f"\n  --- {label} ---")

    # Filter to available columns
    available = [c for c in driver_cols if c in df.columns]
    if not available:
        print(f"  [SKIP] No driver variables available")
        return None

    subset = df[available + [target_col]].dropna()
    if len(subset) < 100:
        print(f"  [SKIP] Too few samples ({len(subset)})")
        return None

    X = subset[available]
    y = subset[target_col]

    # Positive class count
    n_pos = y.sum()
    n_neg = len(y) - n_pos
    print(f"  Samples: {len(subset)} (positive: {n_pos}, negative: {n_neg})")

    if n_pos < 10 or n_neg < 10:
        print(f"  [SKIP] Not enough positive/negative samples")
        return None

    # Standardize
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Statsmodels for p-values
    X_sm = sm.add_constant(X_scaled)
    try:
        logit_model = sm.Logit(y, X_sm).fit(disp=0, maxiter=100)
        print(f"\n  Pseudo R-squared: {logit_model.prsquared:.4f}")
        print(f"  Log-Likelihood: {logit_model.llf:.1f}")
        print(f"\n  {'Variable':<25s} {'Coef':>8s} {'Std Err':>8s} {'z':>8s} {'P>|z|':>8s} {'Odds Ratio':>12s}")
        print(f"  {'-'*71}")

        var_names = ['intercept'] + available
        results_rows = []
        for i, var in enumerate(var_names):
            coef = logit_model.params[i]
            se = logit_model.bse[i]
            z = logit_model.tvalues[i]
            p = logit_model.pvalues[i]
            odds = np.exp(coef)
            sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
            print(f"  {var:<25s} {coef:>8.4f} {se:>8.4f} {z:>8.2f} {p:>8.4f} {odds:>12.4f} {sig}")
            results_rows.append({
                'variable': var, 'coefficient': coef, 'std_error': se,
                'z_value': z, 'p_value': p, 'odds_ratio': odds,
                'significant': sig != ''
            })

        return pd.DataFrame(results_rows)

    except Exception as e:
        print(f"  [FAIL] Logistic regression failed: {e}")
        return None


def plot_driver_effects(df, output_dir):
    """Plot marginal effects of IKN distance and mining density on deforestation."""
    os.makedirs(output_dir, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 1: Deforestation rate vs distance to IKN
    if 'distance_to_ikn' in df.columns and 'forest_loss' in df.columns:
        df_valid = df[['distance_to_ikn', 'forest_loss']].dropna()
        if len(df_valid) > 0:
            df_valid['dist_bin'] = pd.cut(df_valid['distance_to_ikn'], bins=20)
            agg = df_valid.groupby('dist_bin', observed=True)['forest_loss'].agg(['mean', 'count']).reset_index()
            agg['dist_mid'] = agg['dist_bin'].apply(lambda x: x.mid)
            axes[0].bar(range(len(agg)), agg['mean'] * 100, color='#e74c3c', alpha=0.7)
            axes[0].set_xlabel('Distance to IKN (km, binned)', fontsize=11)
            axes[0].set_ylabel('Deforestation Rate (%)', fontsize=11)
            axes[0].set_title('Forest Loss Rate vs Distance to IKN', fontsize=13, fontweight='bold')
            axes[0].tick_params(axis='x', rotation=45)

    # Plot 2: Deforestation rate vs mining density
    if 'mining_density_10km' in df.columns and 'forest_loss' in df.columns:
        df_valid = df[['mining_density_10km', 'forest_loss']].dropna()
        if len(df_valid) > 0:
            df_valid['mining_bin'] = pd.cut(df_valid['mining_density_10km'], bins=20)
            agg = df_valid.groupby('mining_bin', observed=True)['forest_loss'].agg(['mean', 'count']).reset_index()
            axes[1].bar(range(len(agg)), agg['mean'] * 100, color='#f39c12', alpha=0.7)
            axes[1].set_xlabel('Mining Density 10km (%)', fontsize=11)
            axes[1].set_ylabel('Deforestation Rate (%)', fontsize=11)
            axes[1].set_title('Forest Loss Rate vs Mining Density', fontsize=13, fontweight='bold')
            axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    fig_path = os.path.join(output_dir, 'driver_effects.png')
    fig.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Saved {fig_path}")


def run_analysis(model_name, start_year, end_year):
    """Main dual-driver analysis pipeline."""
    print(f"\n{'='*60}")
    print(f"  DUAL-DRIVER ANALYSIS: IKN x MINING")
    print(f"  Period: {start_year} -> {end_year}")
    print(f"{'='*60}")

    os.makedirs(DRIVER_DIR, exist_ok=True)

    # Load data
    df = load_change_data(model_name, start_year, end_year)
    if df is None:
        return

    driver_cols = ['distance_to_ikn', 'mining_density_10km', 'elevation', 'rainfall_annual']

    # Analysis 1: Forest Loss drivers
    if 'forest_loss' in df.columns:
        results = run_logistic_regression(df, 'forest_loss', driver_cols, 'Deforestation Drivers')
        if results is not None:
            results.to_csv(os.path.join(DRIVER_DIR, f'logistic_deforestation_{start_year}_{end_year}.csv'), index=False)

    # Analysis 2: Urbanization drivers
    if 'urbanization' in df.columns:
        results = run_logistic_regression(df, 'urbanization', driver_cols, 'Urbanization Drivers')
        if results is not None:
            results.to_csv(os.path.join(DRIVER_DIR, f'logistic_urbanization_{start_year}_{end_year}.csv'), index=False)

    # Analysis 3: Mining expansion drivers
    if 'mining_expansion' in df.columns:
        results = run_logistic_regression(df, 'mining_expansion', driver_cols, 'Mining Expansion Drivers')
        if results is not None:
            results.to_csv(os.path.join(DRIVER_DIR, f'logistic_mining_{start_year}_{end_year}.csv'), index=False)

    # Plots
    plot_driver_effects(df, DRIVER_DIR)

    print(f"\n  [DONE] Dual-driver analysis complete")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Dual-Driver Analysis')
    parser.add_argument('--model', type=str, default='rf', choices=MODEL_NAMES)
    parser.add_argument('--start', type=int, default=BASELINE_YEAR)
    parser.add_argument('--end', type=int, default=ENDLINE_YEAR)
    args = parser.parse_args()

    run_analysis(args.model, args.start, args.end)
