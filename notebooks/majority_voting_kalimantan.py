"""
Majority Voting — Full Kalimantan Pipeline
============================================
Script ini memproses output dari GEE script 12_majority_voting_grid.js:
1. Load sub-grid CSV (25 titik per sel 500m)
2. Classify setiap titik dengan LightGBM
3. Majority vote per sel 500m
4. Bandingkan dengan hasil centroid-only (predictions_lgbm_*.csv)
5. Hasilkan transition matrix baru

PREREQUISITE:
- GEE export sudah selesai: majority_grid_2019.csv dan majority_grid_2024.csv
- File harus diletakkan di data/predictions/
"""

import pandas as pd
import numpy as np
import joblib
import os
import sys

# ============================================================
# CONFIG
# ============================================================
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
PRED_DIR = os.path.join(BASE_DIR, 'data', 'predictions')
MODEL_DIR = os.path.join(BASE_DIR, 'results', 'classification', 'trained_models')
OUTPUT_DIR = os.path.join(BASE_DIR, 'reports')
os.makedirs(OUTPUT_DIR, exist_ok=True)

CLASS_LABELS = {
    0: 'Forest',
    1: 'Shrubland/Agriculture',
    2: 'Built-up',
    3: 'Bare/Mining-like',
    4: 'Water'
}

# Feature columns — MUST match training features exactly (10 spectral features only)
# See configs/constants.py: FEATURES = SENTINEL2_BANDS + SPECTRAL_INDICES
# Ancillary drivers (elevation, rainfall, distance_to_ikn, mining_density)
# are NOT used by the classifier — they are only for driver regression analysis.
FEATURE_COLS = ['B2', 'B3', 'B4', 'B8', 'B11', 'B12',
                'NDVI', 'NDBI', 'NDMI', 'BSI']

YEARS = [2019, 2024]

# ============================================================
# STEP 0: Check prerequisites
# ============================================================
print("=" * 60)
print("FASE 2: MAJORITY VOTING — FULL KALIMANTAN")
print("=" * 60)

import glob

# Check if majority grid files exist
missing = []
for year in YEARS:
    files = glob.glob(os.path.join(PRED_DIR, f'mv_{year}_*.csv'))
    if len(files) != 5:
        missing.append(f"Tahun {year} butuh 5 file provinsi, tapi baru ditemukan {len(files)} file (mv_{year}_*.csv)")

if missing:
    print("\n[ERROR] File berikut belum tersedia:")
    for f in missing:
        print(f"  - {f}")
    print("\nLangkah yang harus dilakukan:")
    print("1. Buka Google Earth Engine Code Editor")
    print("2. Copy-paste isi file gee_scripts/12_majority_voting_grid.js")
    print("3. Jalankan ke-10 task di tab Tasks")
    print("4. Download ke-10 CSV (mv_*.csv) dari Google Drive ke data/predictions/")
    print("5. Jalankan script ini lagi")
    sys.exit(1)

# Check if LightGBM model exists
model_path = os.path.join(MODEL_DIR, 'model_lgbm.pkl')
if not os.path.exists(model_path):
    # Try alternative paths
    alt_paths = [
        os.path.join(MODEL_DIR, 'lgbm_model.pkl'),
        os.path.join(MODEL_DIR, 'lightgbm_model.pkl'),
        os.path.join(MODEL_DIR, 'lgbm_final.pkl'),
    ]
    model_path = None
    for p in alt_paths:
        if os.path.exists(p):
            model_path = p
            break
    
    if model_path is None:
        # List available models
        if os.path.exists(MODEL_DIR):
            available = os.listdir(MODEL_DIR)
            print(f"\n[ERROR] LightGBM model tidak ditemukan.")
            print(f"File yang tersedia di {MODEL_DIR}:")
            for f in available:
                print(f"  - {f}")
        else:
            print(f"\n[ERROR] Folder models/ tidak ditemukan: {MODEL_DIR}")
        sys.exit(1)

print(f"\nModel path: {model_path}")

# ============================================================
# STEP 1: Load model
# ============================================================
print("\n[STEP 1] Loading LightGBM model...")
model = joblib.load(model_path)
print(f"  Model loaded: {type(model).__name__}")

# ============================================================
# STEP 2: Load & classify sub-grid data
# ============================================================
majority_results = {}

for year in YEARS:
    print(f"\n{'='*60}")
    print(f"[STEP 2] Processing year {year}")
    print(f"{'='*60}")
    
    # Load files one by one to show progress
    files = glob.glob(os.path.join(PRED_DIR, f'mv_{year}_*.csv'))
    print(f"  Found {len(files)} province files for {year}", flush=True)
    all_dfs = []
    for f in files:
        basename = os.path.basename(f)
        print(f"  Loading {basename}...", flush=True)
        all_dfs.append(pd.read_csv(f))
    df = pd.concat(all_dfs, ignore_index=True)
    del all_dfs  # Free memory
    print(f"  Total: {len(df):,} sub-grid points from {len(files)} files", flush=True)
    
    # --- Extract coordinates ---
    if 'longitude' in df.columns:
        df.rename(columns={'longitude': 'lon', 'latitude': 'lat'}, inplace=True)
        print("  Coordinates: using longitude/latitude bands", flush=True)
    elif '.geo' in df.columns and 'lon' not in df.columns:
        import json
        print("  Extracting coordinates from .geo column...", flush=True)
        coords = df['.geo'].apply(lambda x: json.loads(x)['coordinates'] if pd.notna(x) else [np.nan, np.nan])
        df['lon'] = coords.apply(lambda c: c[0])
        df['lat'] = coords.apply(lambda c: c[1])
    
    # --- Verify feature columns exist ---
    missing_cols = [c for c in FEATURE_COLS if c not in df.columns]
    if missing_cols:
        print(f"  [ERROR] Missing feature columns: {missing_cols}")
        print(f"  Available columns: {df.columns.tolist()}")
        sys.exit(1)
    
    # --- Handle NaN ---
    X = df[FEATURE_COLS].values
    nan_mask = np.isnan(X).any(axis=1)
    if nan_mask.sum() > 0:
        print(f"  [WARN] Dropping {nan_mask.sum():,} rows with NaN ({nan_mask.mean()*100:.1f}%)", flush=True)
        df = df[~nan_mask].reset_index(drop=True)
        X = df[FEATURE_COLS].values
    
    # --- Classify with LightGBM ---
    print(f"  Classifying {len(df):,} points with LightGBM...", flush=True)
    predictions = model.predict(X)
    df['predicted_class'] = predictions
    df['predicted_label'] = df['predicted_class'].map(CLASS_LABELS)
    print(f"  Classification done!", flush=True)
    
    print(f"  Class distribution (sub-grid):")
    for cls, label in CLASS_LABELS.items():
        count = (df['predicted_class'] == cls).sum()
        pct = count / len(df) * 100
        print(f"    {label}: {count:,} ({pct:.1f}%)")
    
    # ============================================================
    # STEP 3: Majority Voting per 500m cell (FULLY VECTORIZED)
    # ============================================================
    print(f"\n[STEP 3] Majority Voting for {year}...", flush=True)
    
    # Ensure cell_id exists
    if 'cell_id' not in df.columns:
        print("  [INFO] cell_id not found, computing from coordinates...", flush=True)
        cell_size_deg = 500 / 111320
        df['cell_id'] = (
            np.floor(df['lon'] / cell_size_deg).astype(int).astype(str) + '_' +
            np.floor(df['lat'] / cell_size_deg).astype(int).astype(str)
        )
    else:
        df['cell_id'] = df['cell_id'].astype(str)
    
    # --- FULLY VECTORIZED (NO LAMBDA) ---
    print("  Computing class counts pivot table...", flush=True)
    class_counts = df.groupby(['cell_id', 'predicted_class']).size().unstack(fill_value=0)
    
    print("  Computing majority class (idxmax)...", flush=True)
    majority_class = class_counts.idxmax(axis=1).rename('majority_class')
    
    print("  Computing coordinates & stats...", flush=True)
    coords = df.groupby('cell_id')[['lon', 'lat']].mean()
    n_points = df.groupby('cell_id').size().rename('n_points')
    
    # Class proportions
    class_pcts = class_counts.div(class_counts.sum(axis=1), axis=0) * 100
    class_pcts.columns = [f'pct_{CLASS_LABELS.get(c, c)}' for c in class_pcts.columns]
    
    # Majority confidence
    majority_conf = (class_counts.max(axis=1) / class_counts.sum(axis=1) * 100).rename('majority_confidence')
    
    # Combine all
    print("  Combining results...", flush=True)
    result_df = pd.concat([majority_class, coords, n_points, majority_conf, class_pcts], axis=1).reset_index()
    result_df['majority_label'] = result_df['majority_class'].map(CLASS_LABELS)
    
    majority_results[year] = result_df
    
    print(f"  Total cells: {len(result_df):,}")
    print(f"  Avg points/cell: {result_df['n_points'].mean():.1f}")
    print(f"\n  Majority Voting class distribution:")
    for cls, label in CLASS_LABELS.items():
        count = (result_df['majority_class'] == cls).sum()
        pct = count / len(result_df) * 100
        print(f"    {label}: {count:,} ({pct:.1f}%)")
    
    # Save per-year results
    out_path = os.path.join(PRED_DIR, f'majority_voting_{year}.csv')
    result_df.to_csv(out_path, index=False)
    print(f"\n  Saved: {out_path}", flush=True)

# ============================================================
# STEP 4: Transition Matrix — Majority Voting
# ============================================================
print(f"\n{'='*60}")
print("[STEP 4] Transition Matrix — Majority Voting (2019 -> 2024)")
print(f"{'='*60}")

# Merge on cell_id
merged = majority_results[2019].merge(
    majority_results[2024],
    on='cell_id',
    suffixes=('_2019', '_2024')
)
print(f"\nCommon cells: {len(merged):,}")

# Majority Voting transition
mv_trans = pd.crosstab(
    merged['majority_label_2019'],
    merged['majority_label_2024'],
    margins=True
)
print("\n--- MAJORITY VOTING Transition Matrix ---")
print(mv_trans)

# ============================================================
# STEP 5: Compare with Centroid results
# ============================================================
print(f"\n{'='*60}")
print("[STEP 5] Comparison: Centroid vs Majority Voting")
print(f"{'='*60}")

# Load original centroid predictions
centroid_data = {}
for year in YEARS:
    fpath = os.path.join(PRED_DIR, f'predictions_lgbm_{year}.csv')
    if os.path.exists(fpath):
        centroid_data[year] = pd.read_csv(fpath, usecols=['lon', 'lat', 'predicted_label'])
        print(f"\n[Centroid {year}] Loaded {len(centroid_data[year]):,} points")

if len(centroid_data) == 2:
    print("\n--- CENTROID Transition Summary ---")
    for year in YEARS:
        print(f"\n  [{year}] Class counts:")
        print(centroid_data[year]['predicted_label'].value_counts().to_string())
    
    print("\n--- MAJORITY VOTING Transition Summary ---")
    for year in YEARS:
        print(f"\n  [{year}] Class counts:")
        print(majority_results[year]['majority_label'].value_counts().to_string())

# ============================================================
# STEP 6: Forest Loss comparison
# ============================================================
print(f"\n{'='*60}")
print("[STEP 6] Forest Loss: Centroid vs Majority Voting")
print(f"{'='*60}")

methods = {
    'CENTROID (1 piksel/sel)': centroid_data if len(centroid_data) == 2 else None,
    'MAJORITY VOTING (25 piksel/sel)': majority_results
}

for method_name, method_data in methods.items():
    if method_data is None:
        continue
    
    if method_name.startswith('CENTROID'):
        forest_19 = (method_data[2019]['predicted_label'] == 'Forest').sum()
        forest_24 = (method_data[2024]['predicted_label'] == 'Forest').sum()
        total = len(method_data[2019])
    else:
        forest_19 = (method_data[2019]['majority_label'] == 'Forest').sum()
        forest_24 = (method_data[2024]['majority_label'] == 'Forest').sum()
        total = len(method_data[2019])
    
    delta = forest_24 - forest_19
    pct = delta / forest_19 * 100 if forest_19 > 0 else 0
    
    print(f"\n  {method_name}")
    print(f"  {'='*50}")
    print(f"  Forest 2019:  {forest_19:>8,} / {total:,} ({forest_19/total*100:.1f}%)")
    print(f"  Forest 2024:  {forest_24:>8,} / {total:,} ({forest_24/total*100:.1f}%)")
    print(f"  Delta:        {delta:>+8,} ({pct:+.1f}%)")

# Save final comparison
output_path = os.path.join(OUTPUT_DIR, 'majority_voting_kalimantan.csv')
merged.to_csv(output_path, index=False)
print(f"\n[DONE] Full comparison saved to: {output_path}")
