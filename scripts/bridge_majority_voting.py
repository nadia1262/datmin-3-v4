import os
import sys
import pandas as pd
from scipy.spatial import cKDTree

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import *

def main():
    print("============================================================")
    print("BRIDGE SCRIPT: MAJORITY VOTING (PHASE 2) -> DRIVERS (PHASE 3)")
    print("============================================================")
    
    # 1. Load the 1.5M Majority Voting output (Phase 2)
    mv_path = os.path.join(RESULTS_DIR, '..', 'reports', 'majority_voting_kalimantan.csv')
    if not os.path.exists(mv_path):
        print(f"[FAIL] Majority voting results not found at {mv_path}")
        sys.exit(1)
        
    print("Loading Majority Voting results (~1.5M points)...")
    df_mv = pd.read_csv(mv_path)
    
    # 2. Load the 175k driver anchors from 2019 predictions (Phase 3 Anchor)
    driver_path = os.path.join(PREDICTIONS_DIR, 'predictions_lgbm_2019.csv')
    print("Loading Driver Anchors (10km grid, ~175k points)...")
    df_driver = pd.read_csv(driver_path)
    
    # We only care about matching valid land points, and df_driver serves as the spatial template
    print(f"Driver anchors count: {len(df_driver):,}")
    print(f"Majority voting count: {len(df_mv):,}")
    
    # 3. Build cKDTree for fast spatial joining
    print("Building spatial index (cKDTree)...")
    tree = cKDTree(df_mv[['lon_2019', 'lat_2019']].values)
    
    # 4. Query the nearest majority voting cell for each driver anchor
    print("Querying nearest neighbors (Spatial Intersection)...")
    distances, indices = tree.query(df_driver[['lon', 'lat']].values)
    
    print(f"Average spatial distance (degrees): {distances.mean():.6f}")
    
    # Set a strict distance threshold (~2km max) to avoid merging points across oceans
    threshold = 0.02 # degrees
    valid_mask = distances < threshold
    print(f"Valid matches within threshold: {valid_mask.sum():,} / {len(df_driver):,}")
    
    # Filter the anchors to valid matches
    df_driver_matched = df_driver[valid_mask].copy()
    valid_indices = indices[valid_mask]
    
    # Grab the corresponding rows from Majority Voting
    matched_mv_rows = df_mv.iloc[valid_indices].reset_index(drop=True)
    
    # 5. Build the change points format expected by Phase 3
    print("Constructing change_points format...")
    df_change = pd.DataFrame({
        'lon': df_driver_matched['lon'].round(4),
        'lat': df_driver_matched['lat'].round(4),
        'predicted_label_2019': matched_mv_rows['majority_label_2019'].values,
        'predicted_label_2024': matched_mv_rows['majority_label_2024'].values
    })
    
    # Add 'changed' boolean column
    df_change['changed'] = df_change['predicted_label_2019'] != df_change['predicted_label_2024']
    
    # 6. Save to CHANGE_DIR_V2 (Overwriting the old centroid-based change points)
    os.makedirs(CHANGE_DIR_V2, exist_ok=True)
    out_path = os.path.join(CHANGE_DIR_V2, 'change_points_2019_2024.csv')
    df_change.to_csv(out_path, index=False)
    
    print(f"\n[SUCCESS] Saved {len(df_change):,} accurate samples to: {out_path}")
    print("You can now safely run 'scripts/dual_driver_analysis.py' and 'scripts/shap_classifier.py'!")

if __name__ == '__main__':
    main()
