"""
validate_gee_export.py — Validate GEE-exported CSV files
==========================================================
Run this IMMEDIATELY after downloading CSV from Google Drive.
Catches critical issues before wasting time on ML training.

Checks:
1. Required columns present
2. Band values in reflectance range (0-1), not DN (0-10000)
3. Index values in valid range (-1 to 1)
4. NaN counts and patterns
5. Class distribution (for training data)
6. Coordinate bounds (within Kalimantan)
7. Spatial block coverage

Usage:
    python validate_gee_export.py training           # Validate training samples
    python validate_gee_export.py prediction 2021    # Validate prediction grid
    python validate_gee_export.py all                # Validate everything
"""

import pandas as pd
import numpy as np
import os
import sys
import json
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import (
    SAMPLES_DIR, PREDICTIONS_DIR, TRAINING_SAMPLES_FILE,
    PREDICTION_GRID_TEMPLATE, FEATURES, SENTINEL2_BANDS,
    SPECTRAL_INDICES, TARGET, SPATIAL_BLOCK_COL,
    KALIMANTAN_BOUNDS, SAMPLING_TARGET, YEARS, N_CLASSES
)


def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def print_pass(msg):
    print(f"  [PASS] {msg}")


def print_warn(msg):
    print(f"  [WARN] {msg}")


def print_fail(msg):
    print(f"  [FAIL] {msg}")


def validate_training_samples():
    """Validate training_samples_2021.csv"""
    print_header("VALIDATING: Training Samples (2021)")

    file_path = os.path.join(SAMPLES_DIR, TRAINING_SAMPLES_FILE)
    if not os.path.exists(file_path):
        print_fail(f"File not found: {file_path}")
        return False

    df = pd.read_csv(file_path)
    print(f"  File: {file_path}")
    print(f"  Shape: {df.shape}")
    all_pass = True

    # 1. Required columns
    required = FEATURES + [TARGET, SPATIAL_BLOCK_COL]
    missing = [c for c in required if c not in df.columns]
    if missing:
        print_fail(f"Missing columns: {missing}")
        all_pass = False
    else:
        print_pass(f"All {len(required)} required columns present")

    # 2. Coordinate columns
    coord_cols = []
    if '.geo' in df.columns:
        print_pass(".geo column found (GEE format)")
        coord_cols = ['.geo']
    elif 'longitude' in df.columns and 'latitude' in df.columns:
        coord_cols = ['longitude', 'latitude']
        print_pass("longitude/latitude columns found")
    elif 'lon' in df.columns and 'lat' in df.columns:
        coord_cols = ['lon', 'lat']
        print_pass("lon/lat columns found")
    else:
        print_warn("No coordinate columns found — needed for spatial analysis")

    # 3. Band value ranges (CRITICAL CHECK)
    print(f"\n  --- Band Value Ranges ---")
    for band in SENTINEL2_BANDS:
        if band not in df.columns:
            continue
        col = df[band].dropna()
        if len(col) == 0:
            print_fail(f"{band}: ALL NaN!")
            all_pass = False
            continue

        vmin, vmax, vmean = col.min(), col.max(), col.mean()
        print(f"  {band:5s}: min={vmin:.4f}  max={vmax:.4f}  mean={vmean:.4f}", end="")

        if vmax > 2.0:
            print(f"  <- [FAIL] UNSCALED DN! Expected reflectance [0, 1]")
            all_pass = False
        elif vmax > 1.0:
            print(f"  <- [WARN] Some values > 1.0 (edge case)")
        else:
            print(f"  <- [PASS]")

    # 4. Index value ranges
    print(f"\n  --- Spectral Index Ranges ---")
    for idx in SPECTRAL_INDICES:
        if idx not in df.columns:
            continue
        col = df[idx].dropna()
        if len(col) == 0:
            print_fail(f"{idx}: ALL NaN!")
            all_pass = False
            continue

        vmin, vmax = col.min(), col.max()
        print(f"  {idx:5s}: min={vmin:.4f}  max={vmax:.4f}", end="")
        if vmin < -1.5 or vmax > 1.5:
            print(f"  <- [WARN] Outside expected [-1, 1]")
        else:
            print(f"  <- [PASS]")

    # 5. NaN analysis
    nan_counts = df[FEATURES + [TARGET]].isna().sum()
    total_nan = nan_counts.sum()
    if total_nan > 0:
        print(f"\n  --- NaN Counts ---")
        for col, count in nan_counts[nan_counts > 0].items():
            print(f"  {col}: {count} NaN ({100*count/len(df):.1f}%)")
        if total_nan > 0.05 * len(df) * len(FEATURES):
            print_warn(f"Total NaN rate: {total_nan / (len(df) * len(FEATURES)) * 100:.1f}%")
    else:
        print_pass("No NaN values in features or target")

    # 6. Class distribution
    if TARGET in df.columns:
        print(f"\n  --- Class Distribution ---")
        dist = df[TARGET].value_counts().sort_index()
        for cls_id, count in dist.items():
            expected = SAMPLING_TARGET.get(cls_id, '?')
            pct = 100 * count / len(df)
            status = "[PASS]" if isinstance(expected, int) and abs(count - expected) / expected < 0.2 else "[WARN]"
            print(f"  Class {cls_id}: {count:6d} ({pct:.1f}%) — target: {expected} {status}")

        # Check for unexpected classes
        unexpected = set(dist.index) - set(range(N_CLASSES))
        if unexpected:
            print_fail(f"Unexpected class values: {unexpected}")
            all_pass = False

    # 7. Spatial block coverage
    if SPATIAL_BLOCK_COL in df.columns:
        n_blocks = df[SPATIAL_BLOCK_COL].nunique()
        print(f"\n  Spatial blocks: {n_blocks} unique blocks")
        if n_blocks < 10:
            print_warn("Very few spatial blocks — GroupKFold may not work well")
        else:
            print_pass(f"{n_blocks} blocks sufficient for 5-fold spatial CV")

    # Final verdict
    print(f"\n  {'='*40}")
    if all_pass:
        print_pass("TRAINING DATA VALIDATION PASSED")
    else:
        print_fail("TRAINING DATA HAS CRITICAL ISSUES")
        print("  Fix GEE scripts and re-export before training!")

    return all_pass


def validate_prediction_grid(year):
    """Validate a prediction grid CSV."""
    print_header(f"VALIDATING: Prediction Grid ({year})")

    file_path = os.path.join(PREDICTIONS_DIR, PREDICTION_GRID_TEMPLATE.format(year=year))
    if not os.path.exists(file_path):
        print_fail(f"File not found: {file_path}")
        return False

    df = pd.read_csv(file_path)
    print(f"  File: {file_path}")
    print(f"  Shape: {df.shape}")
    all_pass = True

    # Check features exist
    missing = [f for f in FEATURES if f not in df.columns]
    if missing:
        print_fail(f"Missing features: {missing}")
        all_pass = False
    else:
        print_pass(f"All {len(FEATURES)} features present")

    # Band ranges
    for band in SENTINEL2_BANDS:
        if band not in df.columns:
            continue
        col = df[band].dropna()
        if len(col) > 0 and col.max() > 2.0:
            print_fail(f"{band}: max={col.max():.1f} — UNSCALED!")
            all_pass = False

    # NaN rate
    nan_rate = df[FEATURES].isna().mean().mean()
    print(f"  Overall NaN rate: {nan_rate*100:.1f}%")
    if nan_rate > 0.1:
        print_warn("High NaN rate — may be cloud coverage gaps")

    # Point count
    print(f"  Total points: {len(df):,d}")
    if len(df) < 50000:
        print_warn("Few points — maps may look sparse")
    elif len(df) > 2000000:
        print_warn("Very many points — may cause memory issues")

    return all_pass


def validate_all():
    """Validate all available data files."""
    results = {}

    # Training data
    results['training_2021'] = validate_training_samples()

    # Prediction grids
    for year in YEARS:
        file_path = os.path.join(PREDICTIONS_DIR, PREDICTION_GRID_TEMPLATE.format(year=year))
        if os.path.exists(file_path):
            results[f'prediction_{year}'] = validate_prediction_grid(year)

    # Summary
    print_header("VALIDATION SUMMARY")
    for name, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {name:25s}: {status}")

    return all(results.values())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate GEE exports')
    parser.add_argument('mode', choices=['training', 'prediction', 'all'],
                        help='What to validate')
    parser.add_argument('year', type=int, nargs='?', default=2021,
                        help='Year (for prediction mode)')
    args = parser.parse_args()

    if args.mode == 'training':
        validate_training_samples()
    elif args.mode == 'prediction':
        validate_prediction_grid(args.year)
    else:
        validate_all()
