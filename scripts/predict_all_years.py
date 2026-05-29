"""
predict_all_years.py — Apply trained model to prediction grids (2018-2024)
=========================================================================
Uses the trained model from results/classification/trained_models/
to predict land cover class for each year's prediction grid.
"""

import os
import sys
import argparse
import time
import numpy as np
import pandas as pd
import joblib

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import *


def predict_year(model, scaler, year, model_name):
    """Predict land cover for a single year's grid."""
    grid_file = os.path.join(PREDICTIONS_DIR, f'prediction_grid_{year}.csv')
    if not os.path.exists(grid_file):
        print(f"  [SKIP] {grid_file} not found")
        return None

    df = pd.read_csv(grid_file)
    print(f"  Year {year}: {len(df)} points loaded")

    # Extract coordinates if available
    geo_cols = {}
    if '.geo' in df.columns:
        try:
            import json
            coords = df['.geo'].apply(lambda x: json.loads(x)['coordinates'] if pd.notna(x) else [np.nan, np.nan])
            geo_cols['lon'] = coords.apply(lambda c: c[0])
            geo_cols['lat'] = coords.apply(lambda c: c[1])
        except Exception:
            pass
    
    # Try direct lon/lat columns
    for lon_col in ['longitude', 'lon']:
        if lon_col in df.columns:
            geo_cols['lon'] = df[lon_col]
            break
    for lat_col in ['latitude', 'lat']:
        if lat_col in df.columns:
            geo_cols['lat'] = df[lat_col]
            break

    # Check which features are available
    available_features = [f for f in FEATURES if f in df.columns]
    if len(available_features) < len(FEATURES):
        missing = set(FEATURES) - set(available_features)
        print(f"  [WARN] Missing features: {missing}")
        return None

    X = df[FEATURES].values

    # Handle NaN
    nan_mask = np.isnan(X).any(axis=1)
    if nan_mask.sum() > 0:
        print(f"  [WARN] Dropping {nan_mask.sum()} rows with NaN")
        X = X[~nan_mask]
        for k in geo_cols:
            geo_cols[k] = geo_cols[k][~nan_mask].values

    # Scale if needed
    if scaler is not None:
        X = scaler.transform(X)

    # Predict
    preds = model.predict(X)

    # Probabilities (if available)
    proba = None
    if hasattr(model, 'predict_proba'):
        try:
            proba = model.predict_proba(X)
        except Exception:
            pass

    # Build output DataFrame
    result = pd.DataFrame({
        'lon': geo_cols.get('lon', np.nan),
        'lat': geo_cols.get('lat', np.nan),
        'predicted_class': preds,
        'predicted_label': [CLASS_NAMES.get(int(p), 'Unknown') for p in preds],
    })

    # Add probability columns
    if proba is not None:
        for i, cls_name in CLASS_NAMES.items():
            if i < proba.shape[1]:
                result[f'prob_{cls_name}'] = proba[:, i]
        result['max_prob'] = proba.max(axis=1)
        result['entropy'] = -np.sum(proba * np.log2(proba + 1e-10), axis=1)

    # Add original features for downstream analysis
    X_orig = df[FEATURES].values[~nan_mask] if nan_mask.sum() > 0 else df[FEATURES].values
    for i, feat in enumerate(FEATURES):
        result[feat] = X_orig[:, i]

    # Add ancillary columns if present
    for col in ['elevation', 'rainfall_annual', 'distance_to_ikn', 'mining_density_10km']:
        if col in df.columns:
            vals = df[col].values
            if nan_mask.sum() > 0:
                vals = vals[~nan_mask]
            result[col] = vals

    # Save
    out_file = os.path.join(PREDICTIONS_DIR, f'predictions_{model_name}_{year}.csv')
    result.to_csv(out_file, index=False)
    print(f"  [OK] Saved {out_file} ({len(result)} rows)")

    return result


def main():
    parser = argparse.ArgumentParser(description='Predict land cover for all years')
    parser.add_argument('--model', type=str, default='rf', choices=MODEL_NAMES,
                        help='Model to use for prediction')
    parser.add_argument('--years', type=int, nargs='+', default=YEARS,
                        help='Years to predict')
    args = parser.parse_args()

    model_name = args.model
    print(f"\n{'='*60}")
    print(f"  PREDICTING ALL YEARS: {model_name.upper()}")
    print(f"{'='*60}")

    # Load model
    model_file = os.path.join(CLASSIFICATION_DIR, 'trained_models', f'model_{model_name}.pkl')
    if not os.path.exists(model_file):
        print(f"  [FAIL] Model not found: {model_file}")
        sys.exit(1)

    model = joblib.load(model_file)
    print(f"  Loaded model: {model_file}")

    # Load scaler if needed
    scaler = None
    if model_name in MODELS_NEED_SCALING:
        scaler_file = os.path.join(CLASSIFICATION_DIR, 'trained_models', f'scaler_{model_name}.pkl')
        if os.path.exists(scaler_file):
            scaler = joblib.load(scaler_file)
            print(f"  Loaded scaler: {scaler_file}")

    # Predict each year
    t0 = time.time()
    for year in args.years:
        predict_year(model, scaler, year, model_name)

    elapsed = time.time() - t0
    print(f"\n  Total prediction time: {elapsed:.1f}s")
    print(f"  [DONE]")


if __name__ == '__main__':
    main()
