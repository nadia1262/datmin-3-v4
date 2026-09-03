"""
driver_analysis_v2.py — IKN x Mining Dual-Driver Analysis (Updated)
====================================================================
Implements Step 9: Update Driver Analysis.
Uses the common spatial domain 2019->2024 to evaluate drivers of change.
Explicitly avoids causal claims ("associated with", not "caused by").
"""

import os
import sys
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
    """Load change points and merge with ancillary driver variables."""
    change_file = os.path.join(CHANGE_DIR_V2, f'change_points_{start_year}_{end_year}.csv')
    if not os.path.exists(change_file):
        print(f"  [FAIL] Change file not found: {change_file}")
        return None

    df = pd.read_csv(change_file)
    print(f"  Loaded change data ({start_year}->{end_year}): {len(df):,} points")

    # Load prediction file for start year to get driver variables
    pred_start = os.path.join(PREDICTIONS_DIR, f'predictions_{model_name}_{start_year}.csv')
    if os.path.exists(pred_start):
        pred_df = pd.read_csv(pred_start)
        pred_df['lon'] = pred_df['lon'].round(4)
        pred_df['lat'] = pred_df['lat'].round(4)
        df['lon'] = df['lon'].round(4)
        df['lat'] = df['lat'].round(4)

        driver_cols_available = [c for c in ['elevation', 'rainfall_annual', 'distance_to_ikn', 'mining_density_10km'] if c in pred_df.columns]
        if driver_cols_available:
            df = df.merge(pred_df[['lon', 'lat'] + driver_cols_available].drop_duplicates(subset=['lon', 'lat']), on=['lon', 'lat'], how='left')
            print(f"  Merged driver variables: {driver_cols_available}")

    return df


def evaluate_model_validity(df, target_col, label):
    """Pre-check if modeling this outcome is scientifically valid."""
    if target_col not in df.columns:
        return "DROP", "Target column not found"

    n_total = len(df)
    n_pos = df[target_col].sum()
    n_neg = n_total - n_pos

    print(f"\n  Checking validity for {label} (target: {target_col})")
    print(f"    Positive cases: {n_pos:,} ({100*n_pos/n_total:.2f}%)")

    if n_pos < 50:
        return "DROP", f"Too few positive cases ({n_pos}). Results would be statistically unreliable."
    elif n_pos < 300:
        return "EXPLORATORY", f"Low positive cases ({n_pos}). Extreme class imbalance."
    else:
        return "KEEP", "Sufficient positive cases for modeling."


def run_logistic_regression(df, target_col, driver_cols, label, status):
    """Run logistic regression to test driver association."""
    print(f"\n  --- Model: {label} [{status}] ---")

    if status == "DROP":
        print(f"  [SKIP] Model dropped due to insufficient data.")
        return None

    available = [c for c in driver_cols if c in df.columns]
    subset = df[available + [target_col]].dropna()
    
    X = subset[available]
    y = subset[target_col]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_sm = sm.add_constant(X_scaled)
    try:
        logit_model = sm.Logit(y, X_sm).fit(disp=0, maxiter=100)
        print(f"\n  Pseudo R-squared: {logit_model.prsquared:.4f}")
        
        if logit_model.prsquared < 0.01:
            print("  [WARN] Very low Pseudo R-squared. Model has weak explanatory power.")
            if status == "KEEP":
                status = "KEEP AS EXPLORATORY ONLY"
                print("  [UPDATE] Status changed to EXPLORATORY.")

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

        return pd.DataFrame(results_rows), status

    except Exception as e:
        print(f"  [FAIL] Logistic regression failed: {e}")
        return None, "DROP"


def run_analysis(model_name, start_year, end_year):
    """Main dual-driver analysis pipeline for new temporal window."""
    print(f"\n{'='*60}")
    print(f"  DRIVER ANALYSIS v2: IKN x MINING (Common Domain)")
    print(f"  Period: {start_year} -> {end_year}")
    print(f"{'='*60}")

    os.makedirs(DRIVER_DIR_V2, exist_ok=True)

    df = load_change_data(model_name, start_year, end_year)
    if df is None:
        return

    driver_cols = ['distance_to_ikn', 'mining_density_10km', 'elevation', 'rainfall_annual']
    
    analyses = [
        ('forest_loss', 'Deforestation'),
        ('urbanization', 'Urbanization'),
        ('mining_expansion', 'Mining Expansion')
    ]

    model_status_log = []

    for target_col, label in analyses:
        status, reason = evaluate_model_validity(df, target_col, label)
        model_status_log.append({'Model': label, 'Status': status, 'Reason': reason})
        
        if status != "DROP":
            results_tuple = run_logistic_regression(df, target_col, driver_cols, label, status)
            if results_tuple is not None:
                results, final_status = results_tuple
                # Update status if changed during fitting
                for item in model_status_log:
                    if item['Model'] == label:
                        item['Status'] = final_status
                
                out_name = f'logistic_{target_col}_{start_year}_{end_year}.csv'
                results.to_csv(os.path.join(DRIVER_DIR_V2, out_name), index=False)

    # Save summary of model statuses
    status_df = pd.DataFrame(model_status_log)
    print("\n" + "="*60)
    print("  MODEL DECISION SUMMARY")
    print("="*60)
    print(status_df.to_string(index=False))
    status_df.to_csv(os.path.join(DRIVER_DIR_V2, 'model_validity_decisions.csv'), index=False)

    print(f"\n  [DONE] Driver analysis complete")


if __name__ == '__main__':
    run_analysis('lgbm', BASELINE_YEAR, ENDLINE_YEAR)
