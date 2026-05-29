"""
shap_classifier.py — SHAP Feature Importance Analysis
======================================================
Uses SHAP TreeExplainer to decompose model predictions
and identify which spectral features drive each class.
"""

import os
import sys
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import joblib
import shap

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import *


def run_shap_analysis(model_name, n_samples=5000):
    """Run SHAP analysis on trained model."""
    print(f"\n{'='*60}")
    print(f"  SHAP ANALYSIS: {model_name.upper()}")
    print(f"{'='*60}")

    # Output directory
    out_dir = os.path.join(SHAP_DIR, model_name)
    os.makedirs(out_dir, exist_ok=True)

    # Load model
    model_file = os.path.join(CLASSIFICATION_DIR, 'trained_models', f'model_{model_name}.pkl')
    if not os.path.exists(model_file):
        print(f"  [FAIL] Model not found: {model_file}")
        return

    model = joblib.load(model_file)
    print(f"  Loaded model: {model_file}")

    # Load training data for background
    samples_file = os.path.join(SAMPLES_DIR, TRAINING_SAMPLES_FILE)
    if not os.path.exists(samples_file):
        print(f"  [FAIL] Training data not found: {samples_file}")
        return

    df = pd.read_csv(samples_file)
    X = df[FEATURES].values
    y = df[TARGET].values

    # Subsample for SHAP (it's computationally expensive)
    if len(X) > n_samples:
        idx = np.random.RandomState(RANDOM_STATE).choice(len(X), n_samples, replace=False)
        X_sample = X[idx]
        y_sample = y[idx]
    else:
        X_sample = X
        y_sample = y

    print(f"  Using {len(X_sample)} samples for SHAP computation")

    # Choose explainer based on model type
    if model_name in MODELS_SHAP_TREE:
        print(f"  Using TreeExplainer (fast)")
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_sample)
    else:
        print(f"  Using KernelExplainer (slow, sampling 100 background)")
        bg = shap.sample(X, min(100, len(X)))
        # For models needing scaling, we'd need to apply scaler first
        scaler_file = os.path.join(CLASSIFICATION_DIR, 'trained_models', f'scaler_{model_name}.pkl')
        if os.path.exists(scaler_file):
            scaler = joblib.load(scaler_file)
            X_sample = scaler.transform(X_sample)
            bg = scaler.transform(bg)
        explainer = shap.KernelExplainer(model.predict_proba, bg)
        shap_values = explainer.shap_values(X_sample, nsamples=50)

    # SHAP values shape: list of arrays [n_classes x (n_samples, n_features)]
    # or single array for binary

    # 1. Global feature importance (mean |SHAP|)
    print(f"\n  --- Global Feature Importance (mean |SHAP|) ---")

    if isinstance(shap_values, list):
        # Multi-class list format: average across classes
        mean_abs = np.mean([np.abs(sv).mean(axis=0) for sv in shap_values], axis=0)
    elif shap_values.ndim == 3:
        # Multi-class 3D array format (samples, features, classes)
        mean_abs = np.abs(shap_values).mean(axis=(0, 2))
    else:
        # Binary or single class
        mean_abs = np.abs(shap_values).mean(axis=0)

    importance_df = pd.DataFrame({
        'feature': FEATURES,
        'mean_abs_shap': mean_abs
    }).sort_values('mean_abs_shap', ascending=False)

    print(importance_df.to_string(index=False))
    importance_df.to_csv(os.path.join(out_dir, 'shap_importance.csv'), index=False)

    # 2. Summary plot (beeswarm)
    print(f"\n  Generating SHAP summary plot...")
    fig, ax = plt.subplots(figsize=(10, 8))

    if isinstance(shap_values, list):
        # For multi-class, use mean absolute SHAP
        combined_shap = np.mean([np.abs(sv) for sv in shap_values], axis=0)
        shap.summary_plot(combined_shap, X_sample, feature_names=FEATURES, show=False,
                          plot_type='bar')
    else:
        shap.summary_plot(shap_values, X_sample, feature_names=FEATURES, show=False)

    plt.title(f'SHAP Feature Importance ({model_name.upper()})', fontsize=14, fontweight='bold')
    plt.tight_layout()
    fig_path = os.path.join(out_dir, 'shap_summary.png')
    plt.savefig(fig_path, dpi=150, bbox_inches='tight')
    plt.close('all')
    print(f"  [OK] Saved {fig_path}")

    # 3. Per-class SHAP importance
    if isinstance(shap_values, list) and len(shap_values) == N_CLASSES:
        print(f"\n  --- Per-Class SHAP Importance ---")
        per_class_rows = []
        for cls_id in range(N_CLASSES):
            cls_shap = np.abs(shap_values[cls_id]).mean(axis=0)
            for i, feat in enumerate(FEATURES):
                per_class_rows.append({
                    'class': CLASS_NAMES[cls_id],
                    'feature': feat,
                    'mean_abs_shap': cls_shap[i]
                })

        per_class_df = pd.DataFrame(per_class_rows)
        per_class_df.to_csv(os.path.join(out_dir, 'shap_per_class.csv'), index=False)

        # Heatmap
        pivot = per_class_df.pivot(index='feature', columns='class', values='mean_abs_shap')
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(pivot, annot=True, fmt='.4f', cmap='YlOrRd', ax=ax)
        ax.set_title(f'SHAP Importance per Class ({model_name.upper()})',
                     fontsize=14, fontweight='bold')
        plt.tight_layout()
        fig_path = os.path.join(out_dir, 'shap_per_class_heatmap.png')
        fig.savefig(fig_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"  [OK] Saved {fig_path}")

    # Save raw SHAP values
    np.savez_compressed(
        os.path.join(out_dir, 'shap_values.npz'),
        shap_values=shap_values if not isinstance(shap_values, list) else np.array(shap_values),
        features=X_sample,
        feature_names=FEATURES
    )

    print(f"\n  [DONE] SHAP analysis complete")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SHAP Feature Importance')
    parser.add_argument('--model', type=str, default='rf', choices=MODEL_NAMES)
    parser.add_argument('--n_samples', type=int, default=5000)
    args = parser.parse_args()

    run_shap_analysis(args.model, args.n_samples)
