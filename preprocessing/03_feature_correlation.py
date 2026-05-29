# preprocessing/03_feature_correlation.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import *

def check_correlation():
    file_path = os.path.join(SAMPLES_DIR, TRAINING_SAMPLES_FILE)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    df = pd.read_csv(file_path)
    X = df[FEATURES]
    
    corr = X.corr()
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt='.2f')
    plt.title('Feature Correlation Heatmap')
    plt.tight_layout()
    os.makedirs(FIGURES_DIR, exist_ok=True)
    plt.savefig(os.path.join(FIGURES_DIR, 'feature_correlation.png'))
    plt.close()
    
    # Identify highly correlated pairs
    upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
    to_drop = [column for column in upper.columns if any(upper[column].abs() > 0.9)]
    print(f"Highly correlated features (>0.9): {to_drop}")

if __name__ == '__main__':
    check_correlation()
