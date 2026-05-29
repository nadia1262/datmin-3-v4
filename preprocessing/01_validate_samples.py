# preprocessing/01_validate_samples.py
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import *

def validate_samples():
    file_path = os.path.join(SAMPLES_DIR, TRAINING_SAMPLES_FILE)
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}. Please create a dummy file for now or download from GEE.")
        # Create a dummy dataset for testing if not exists
        os.makedirs(SAMPLES_DIR, exist_ok=True)
        print("Generating synthetic dummy data for testing pipeline...")
        n_samples = 1000
        df = pd.DataFrame({
            'B2': np.random.rand(n_samples), 'B3': np.random.rand(n_samples),
            'B4': np.random.rand(n_samples), 'B8': np.random.rand(n_samples),
            'B11': np.random.rand(n_samples), 'B12': np.random.rand(n_samples),
            'NDVI': np.random.uniform(-1, 1, n_samples),
            'NDBI': np.random.uniform(-1, 1, n_samples),
            'NDMI': np.random.uniform(-1, 1, n_samples),
            'BSI': np.random.uniform(-1, 1, n_samples),
            'land_cover_class': np.random.choice(list(CLASS_NAMES.keys()), n_samples),
            'spatial_block_id': np.random.randint(1, 20, n_samples),
            'elevation': np.random.uniform(0, 2000, n_samples),
            'rainfall_annual': np.random.uniform(1000, 4000, n_samples),
            'distance_to_ikn': np.random.uniform(0, 500, n_samples),
            'mining_density_10km': np.random.uniform(0, 100, n_samples),
            'distance_to_mining': np.random.uniform(0, 100, n_samples),
            '.geo': '{"type":"Point","coordinates":[114.0,-1.0]}'
        })
        df.to_csv(file_path, index=False)
        print(f"Dummy data generated at {file_path}")

    print(f"Loading {file_path}...")
    df = pd.read_csv(file_path)

    print("\n--- Validation Report ---")
    
    # 1. Check Missing Values
    missing = df.isnull().sum().sum()
    print(f"Total missing values: {missing}")
    if missing > 0:
        print(df.isnull().sum())

    # 2. Check Features
    missing_feats = [f for f in FEATURES if f not in df.columns]
    print(f"Missing features: {missing_feats if missing_feats else 'None'}")

    # 3. Class Distribution
    print("\nClass Distribution:")
    class_counts = df[TARGET].value_counts().sort_index()
    for cls, count in class_counts.items():
        print(f"  Class {cls} ({CLASS_NAMES.get(cls, 'Unknown')}): {count} samples")

    # 4. Spatial Blocks
    n_blocks = df[SPATIAL_BLOCK_COL].nunique()
    print(f"\nTotal spatial blocks: {n_blocks}")

if __name__ == '__main__':
    validate_samples()
