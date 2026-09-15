# scripts/build_dashboard_cache.py
import os
import json
import pandas as pd
import numpy as np
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')
from configs.constants import PREDICTIONS_DIR

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'dashboard', 'data', 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)

CLASS_MAP = {
    0: 'Forest',
    1: 'Shrubland/Agriculture',
    2: 'Built-up',
    3: 'Bare/Mining-like',
    4: 'Water'
}

def process_all_years():
    class_distributions = {}
    years = [2019, 2020, 2021, 2022, 2023, 2024]
    
    for y in years:
        print(f"Processing year {y}...")
        # Check files
        mv_path = os.path.join(PREDICTIONS_DIR, f'majority_voting_{y}.csv')
        lgbm_path = os.path.join(PREDICTIONS_DIR, f'predictions_lgbm_{y}.csv')
        
        file_path = None
        source_type = "Majority Voting (500m)"
        if os.path.exists(mv_path):
            file_path = mv_path
        elif os.path.exists(lgbm_path):
            file_path = lgbm_path
            source_type = "LightGBM Centroid"
        else:
            print(f"No prediction file for {y}, skipping.")
            continue
            
        # Inspect columns
        header = pd.read_csv(file_path, nrows=2)
        cols = header.columns.tolist()
        
        class_col = 'majority_class' if 'majority_class' in cols else 'predicted_class'
        label_col = 'majority_label' if 'majority_label' in cols else 'predicted_label'
        
        usecols = ['lon', 'lat', class_col]
        if label_col in cols:
            usecols.append(label_col)
            
        df = pd.read_csv(file_path, usecols=usecols)
        
        # Standardize column names
        df = df.rename(columns={class_col: 'predicted_class'})
        if label_col in df.columns:
            df = df.rename(columns={label_col: 'predicted_label'})
        else:
            df['predicted_label'] = df['predicted_class'].map(CLASS_MAP)
            
        total_rows = len(df)
        counts = df['predicted_label'].value_counts().to_dict()
        pcts = {k: (v / total_rows) * 100 for k, v in counts.items()}
        
        class_distributions[str(y)] = {
            'total': int(total_rows),
            'source_type': source_type,
            'counts': {k: int(v) for k, v in counts.items()},
            'percentages': {k: round(float(v), 2) for k, v in pcts.items()}
        }
        
        # Stratified sample of ~40,000 points for smooth, instant 60fps PyDeck rendering
        sample_dfs = []
        for cls_name, group in df.groupby('predicted_label'):
            # allocate sample size: proportional with min guarantee
            target_n = min(len(group), max(1200, int(len(group) / total_rows * 40000)))
            sample_dfs.append(group.sample(target_n, random_state=42))
            
        df_sample = pd.concat(sample_dfs, ignore_index=True)
        # Keep only lon, lat, predicted_class, predicted_label
        out_parquet = os.path.join(CACHE_DIR, f'map_points_{y}.parquet')
        df_sample.to_parquet(out_parquet, index=False)
        print(f"Year {y}: Total {total_rows} -> Sample {len(df_sample)} saved to {out_parquet}")
        
    # Save class distribution
    summary_json = os.path.join(CACHE_DIR, 'class_distribution.json')
    with open(summary_json, 'w') as f:
        json.dump(class_distributions, f, indent=2)
    print(f"Saved distribution summary to {summary_json}")

if __name__ == '__main__':
    process_all_years()
