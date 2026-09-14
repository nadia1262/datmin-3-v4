"""
Majority Voting Proof-of-Concept: KIPP IKN
===========================================
Membandingkan klasifikasi Centroid (1 piksel) vs Majority Voting (~2500 piksel)
pada grid 500m di area KIPP IKN menggunakan data prediksi LightGBM 10m.
"""

import pandas as pd
import numpy as np
import os

# ============================================================
# CONFIG
# ============================================================
PRED_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'predictions')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'reports')
os.makedirs(OUTPUT_DIR, exist_ok=True)

CELL_SIZE_DEG = 0.0045  # ~500m at equator

CLASS_LABELS = {
    0: 'Forest',
    1: 'Shrubland/Agriculture',
    2: 'Built-up',
    3: 'Bare/Mining-like',
    4: 'Water'
}

YEARS = [2019, 2024]

# ============================================================
# STEP 1: Load 10m predicted data
# ============================================================
print("=" * 60)
print("FASE 1: MAJORITY VOTING PROOF-OF-CONCEPT — KIPP IKN")
print("=" * 60)

data = {}
for year in YEARS:
    fpath = os.path.join(PRED_DIR, f'ikn_10m_predicted_{year}.csv')
    df = pd.read_csv(fpath)
    print(f"\n[{year}] Loaded {len(df):,} pixels from {os.path.basename(fpath)}")
    print(f"  Lon: {df['lon'].min():.6f} — {df['lon'].max():.6f}")
    print(f"  Lat: {df['lat'].min():.6f} — {df['lat'].max():.6f}")
    print(f"  Classes: {df['predicted_label'].value_counts().to_dict()}")
    data[year] = df

# ============================================================
# STEP 2: Assign each 10m pixel to a 500m grid cell
# ============================================================
print("\n" + "=" * 60)
print("STEP 2: Overlaying 500m grid on 10m pixels")
print("=" * 60)

for year in YEARS:
    df = data[year]
    # Snap to grid: floor division creates cell IDs
    df['cell_col'] = np.floor(df['lon'] / CELL_SIZE_DEG).astype(int)
    df['cell_row'] = np.floor(df['lat'] / CELL_SIZE_DEG).astype(int)
    df['cell_id'] = df['cell_col'].astype(str) + '_' + df['cell_row'].astype(str)
    
    # Compute cell centroids
    df['cell_center_lon'] = (df['cell_col'] + 0.5) * CELL_SIZE_DEG
    df['cell_center_lat'] = (df['cell_row'] + 0.5) * CELL_SIZE_DEG
    
    n_cells = df['cell_id'].nunique()
    avg_pixels = len(df) / n_cells
    print(f"\n[{year}] {n_cells} cells created, avg {avg_pixels:.0f} pixels/cell")
    data[year] = df

# ============================================================
# STEP 3: Majority Voting per cell
# ============================================================
print("\n" + "=" * 60)
print("STEP 3: Majority Voting per 500m cell")
print("=" * 60)

majority_results = {}
for year in YEARS:
    df = data[year]
    
    # Group by cell and get majority class
    cell_groups = df.groupby('cell_id')
    
    rows = []
    for cell_id, group in cell_groups:
        # Majority vote
        class_counts = group['predicted_class'].value_counts()
        majority_class = class_counts.idxmax()
        majority_pct = class_counts.iloc[0] / len(group) * 100
        
        # Class proportions
        proportions = {}
        for cls_id, cls_name in CLASS_LABELS.items():
            proportions[f'pct_{cls_name}'] = (group['predicted_class'] == cls_id).sum() / len(group) * 100
        
        # Centroid simulation: pick the pixel closest to cell center
        center_lon = group['cell_center_lon'].iloc[0]
        center_lat = group['cell_center_lat'].iloc[0]
        distances = np.sqrt((group['lon'] - center_lon)**2 + (group['lat'] - center_lat)**2)
        centroid_idx = distances.idxmin()
        centroid_class = group.loc[centroid_idx, 'predicted_class']
        
        rows.append({
            'cell_id': cell_id,
            'cell_lon': center_lon,
            'cell_lat': center_lat,
            'n_pixels': len(group),
            'majority_class': majority_class,
            'majority_label': CLASS_LABELS[majority_class],
            'majority_confidence': majority_pct,
            'centroid_class': centroid_class,
            'centroid_label': CLASS_LABELS[centroid_class],
            'agree': majority_class == centroid_class,
            **proportions
        })
    
    result_df = pd.DataFrame(rows)
    majority_results[year] = result_df
    
    agree_pct = result_df['agree'].mean() * 100
    disagree = result_df[~result_df['agree']]
    
    print(f"\n[{year}] Results:")
    print(f"  Total cells: {len(result_df)}")
    print(f"  Agreement (Centroid == Majority): {agree_pct:.1f}%")
    print(f"  Disagreement: {len(disagree)} cells ({100-agree_pct:.1f}%)")
    
    if len(disagree) > 0:
        print(f"\n  Cells where Centroid != Majority Voting:")
        for _, row in disagree.iterrows():
            print(f"    {row['cell_id']}: Centroid={row['centroid_label']} -> Majority={row['majority_label']} ({row['majority_confidence']:.1f}% confidence)")

# ============================================================
# STEP 4: Transition Matrix comparison
# ============================================================
print("\n" + "=" * 60)
print("STEP 4: Transition Matrix — Centroid vs Majority Voting")
print("=" * 60)

# Merge 2019 and 2024 on cell_id
merged = majority_results[2019].merge(
    majority_results[2024], 
    on='cell_id', 
    suffixes=('_2019', '_2024')
)

print(f"\nCommon cells: {len(merged)}")

# --- Centroid-based transition ---
print("\n--- CENTROID-BASED Transition Matrix (2019 → 2024) ---")
centroid_trans = pd.crosstab(
    merged['centroid_label_2019'], 
    merged['centroid_label_2024'],
    margins=True
)
print(centroid_trans)

# --- Majority Voting-based transition ---
print("\n--- MAJORITY VOTING Transition Matrix (2019 → 2024) ---")
majority_trans = pd.crosstab(
    merged['majority_label_2019'], 
    merged['majority_label_2024'],
    margins=True
)
print(majority_trans)

# ============================================================
# STEP 5: Forest Loss comparison
# ============================================================
print("\n" + "=" * 60)
print("STEP 5: Forest Loss Comparison")
print("=" * 60)

for method in ['centroid', 'majority']:
    label_19 = f'{method}_label_2019'
    label_24 = f'{method}_label_2024'
    
    forest_19 = (merged[label_19] == 'Forest').sum()
    forest_24 = (merged[label_24] == 'Forest').sum()
    delta = forest_24 - forest_19
    pct_change = (delta / forest_19 * 100) if forest_19 > 0 else 0
    
    bare_19 = (merged[label_19] == 'Bare/Mining-like').sum()
    bare_24 = (merged[label_24] == 'Bare/Mining-like').sum()
    built_19 = (merged[label_19] == 'Built-up').sum()
    built_24 = (merged[label_24] == 'Built-up').sum()
    
    method_name = "CENTROID (1 piksel)" if method == 'centroid' else "MAJORITY VOTING (~2500 piksel)"
    print(f"\n{'='*50}")
    print(f"  {method_name}")
    print(f"{'='*50}")
    print(f"  Forest:          {forest_19:3d} → {forest_24:3d}  (delta: {delta:+d}, {pct_change:+.1f}%)")
    print(f"  Bare/Mining:     {bare_19:3d} → {bare_24:3d}  (delta: {bare_24-bare_19:+d})")
    print(f"  Built-up:        {built_19:3d} → {built_24:3d}  (delta: {built_24-built_19:+d})")

# ============================================================
# STEP 6: Soft classification detail (proportion changes)
# ============================================================
print("\n" + "=" * 60)
print("STEP 6: Soft Classification — Forest Proportion per Cell")
print("=" * 60)

forest_pct_19 = merged['pct_Forest_2019']
forest_pct_24 = merged['pct_Forest_2024']
forest_pct_delta = forest_pct_24 - forest_pct_19

print(f"\n  Average forest proportion per cell:")
print(f"    2019: {forest_pct_19.mean():.1f}%")
print(f"    2024: {forest_pct_24.mean():.1f}%")
print(f"    Delta: {forest_pct_delta.mean():+.1f} percentage points")
print(f"\n  Cells where forest proportion DECREASED: {(forest_pct_delta < 0).sum()} / {len(merged)}")
print(f"  Cells where forest proportion INCREASED: {(forest_pct_delta > 0).sum()} / {len(merged)}")
print(f"  Average decrease magnitude: {forest_pct_delta[forest_pct_delta < 0].mean():+.1f} pp")

# Save results
output_path = os.path.join(OUTPUT_DIR, 'majority_voting_comparison.csv')
merged.to_csv(output_path, index=False)
print(f"\n✓ Detailed comparison saved to: {output_path}")

print("\n" + "=" * 60)
print("DONE — Majority Voting Proof-of-Concept Complete")
print("=" * 60)
