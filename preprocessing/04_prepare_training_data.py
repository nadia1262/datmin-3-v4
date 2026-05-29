# preprocessing/04_prepare_training_data.py
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import *

def prepare_data():
    file_path = os.path.join(SAMPLES_DIR, TRAINING_SAMPLES_FILE)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None, None, None

    df = pd.read_csv(file_path)
    df = df.dropna(subset=FEATURES + [TARGET, SPATIAL_BLOCK_COL])
    
    X = df[FEATURES].values
    y = df[TARGET].values
    groups = df[SPATIAL_BLOCK_COL].values
    
    print(f"Prepared {len(df)} samples.")
    print(f"X shape: {X.shape}, y shape: {y.shape}, groups shape: {groups.shape}")
    
    return X, y, groups

if __name__ == '__main__':
    prepare_data()
