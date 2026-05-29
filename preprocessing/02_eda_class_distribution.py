# preprocessing/02_eda_class_distribution.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import *
from configs.color_palette import CLASS_COLORS_LIST

def run_eda():
    file_path = os.path.join(SAMPLES_DIR, TRAINING_SAMPLES_FILE)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    df = pd.read_csv(file_path)
    os.makedirs(FIGURES_DIR, exist_ok=True)

    # 1. Class Distribution Bar Chart
    plt.figure(figsize=(10, 6))
    class_counts = df[TARGET].value_counts().sort_index()
    sns.barplot(x=[CLASS_NAMES[i] for i in class_counts.index], y=class_counts.values, palette=CLASS_COLORS_LIST)
    plt.title('Class Distribution in Training Data')
    plt.ylabel('Number of Samples')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGURES_DIR, 'class_distribution.png'))
    plt.close()

    # 2. Feature distributions per class (Boxplots)
    for feature in SPECTRAL_INDICES:
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=TARGET, y=feature, data=df, palette=CLASS_COLORS_LIST)
        plt.title(f'{feature} Distribution by Class')
        plt.xticks(ticks=range(N_CLASSES), labels=[CLASS_NAMES[i] for i in range(N_CLASSES)], rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(FIGURES_DIR, f'boxplot_{feature}.png'))
        plt.close()

    print(f"EDA plots saved to {FIGURES_DIR}")

if __name__ == '__main__':
    run_eda()
