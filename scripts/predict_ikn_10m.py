"""
predict_ikn_10m.py — Apply trained LGBM model to 10m IKN grids and generate maps
================================================================================
Uses the trained LightGBM model to predict the 10m high-resolution grid for the
IKN core zone (KIPP) and exports high-quality PNG maps.
"""

import os
import sys
import json
import time
import numpy as np
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import *

def parse_geo(geo_str):
    try:
        coords = json.loads(geo_str)['coordinates']
        return coords[0], coords[1]
    except:
        return np.nan, np.nan

def main():
    print(f"\n{'='*60}")
    print(f"  PREDICTING MICRO-SCALE (10m) IKN ZONE")
    print(f"{'='*60}")

    # Load LGBM Model
    model_name = 'lgbm'
    model_file = os.path.join(CLASSIFICATION_DIR, 'trained_models', f'model_{model_name}.pkl')
    if not os.path.exists(model_file):
        print(f"  [FAIL] Model not found: {model_file}")
        sys.exit(1)

    model = joblib.load(model_file)
    print(f"  Loaded model: {model_file}")

    # Color Mapping for the 5 classes
    # 0: Forest (DarkGreen), 1: Shrubland (YellowGreen), 2: Built-up (Red), 3: Bare (Gray), 4: Water (Blue)
    colors = ['darkgreen', 'yellowgreen', 'red', 'gray', 'blue']
    cmap = mcolors.ListedColormap(colors)
    
    # Process 2019 and 2024
    for year in [2019, 2024]:
        t0 = time.time()
        input_csv = os.path.join(PREDICTIONS_DIR, f'ikn_10m_grid_{year}.csv')
        output_csv = os.path.join(PREDICTIONS_DIR, f'ikn_10m_predicted_{year}.csv')
        map_out = os.path.join(CLASSIFICATION_DIR, f'ikn_10m_map_{year}.png')
        
        if not os.path.exists(input_csv):
            print(f"  [SKIP] {input_csv} not found")
            continue
            
        print(f"\n  Processing Year: {year}")
        df = pd.read_csv(input_csv)
        print(f"  Loaded {len(df)} points at 10m resolution")
        
        # Extract coordinates
        if '.geo' in df.columns:
            coords = df['.geo'].apply(parse_geo)
            df['lon'] = [c[0] for c in coords]
            df['lat'] = [c[1] for c in coords]
        else:
            print(f"  [FAIL] No .geo column found in {year}")
            continue
            
        # Check features
        available_features = [f for f in FEATURES if f in df.columns]
        if len(available_features) < len(FEATURES):
            print(f"  [FAIL] Missing features. Needed: {FEATURES}")
            continue
            
        # Prepare X
        X = df[FEATURES].values
        
        # Handle NaNs (drop rows with NaN)
        nan_mask = np.isnan(X).any(axis=1)
        if nan_mask.sum() > 0:
            print(f"  [WARN] Dropping {nan_mask.sum()} rows with NaN features")
            df = df[~nan_mask].copy()
            X = df[FEATURES].values
            
        # Predict
        print(f"  Predicting using {model_name.upper()}...")
        preds = model.predict(X)
        df['predicted_class'] = preds
        df['predicted_label'] = [CLASS_NAMES.get(int(p), 'Unknown') for p in preds]
        
        # Save CSV (Optional: dropping raw features to save space)
        export_df = df[['lon', 'lat', 'predicted_class', 'predicted_label']]
        export_df.to_csv(output_csv, index=False)
        print(f"  Saved predictions to {os.path.basename(output_csv)}")
        
        # Generate Map
        print(f"  Generating High-Res Map for {year}...")
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Scatter plot (s=2 makes dots slightly larger for 190k points on a 10x10 figure)
        scatter = ax.scatter(df['lon'], df['lat'], c=df['predicted_class'], 
                             cmap=cmap, vmin=0, vmax=4, s=2, marker='s', edgecolors='none')
        
        # Create legend
        handles = [plt.Line2D([0], [0], marker='s', color='w', markerfacecolor=c, markersize=10) for c in colors]
        ax.legend(handles, [CLASS_NAMES[i] for i in range(5)], title="Land Cover", loc='upper right')
        
        ax.set_title(f"IKN Core Zone (KIPP) - 10m Resolution Land Cover ({year})", fontsize=16, pad=15)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        
        # Ensure aspect ratio is equal so the map isn't distorted
        ax.set_aspect('equal', 'box')
        
        plt.tight_layout()
        plt.savefig(map_out, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"  Saved Map to {os.path.basename(map_out)}")
        print(f"  Done {year} in {time.time()-t0:.1f}s")
        
    print(f"\n  [ALL DONE]")

if __name__ == '__main__':
    main()
