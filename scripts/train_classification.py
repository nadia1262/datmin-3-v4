"""
train_classification.py — Multi-Model Land Cover Classification
================================================================
Trains 6 ML models with Spatial Block GroupKFold Cross-Validation.
Models: Logistic Regression, Random Forest, XGBoost, LightGBM, SVM, MLP.
"""

import os
import sys
import time
import json
import argparse
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (accuracy_score, f1_score, cohen_kappa_score,
                             confusion_matrix, classification_report)

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import *

warnings.filterwarnings('ignore', category=FutureWarning)


def get_model_and_params(model_name):
    """Return model instance and hyperparameter grid."""
    if model_name == 'logreg':
        return LogisticRegression(max_iter=1000, random_state=RANDOM_STATE), \
               {'C': [0.1, 1, 10]}

    elif model_name == 'rf':
        return RandomForestClassifier(random_state=RANDOM_STATE, n_jobs=-1), \
               {'n_estimators': [200, 500], 'max_depth': [None, 20], 'min_samples_leaf': [1, 2]}

    elif model_name == 'xgboost':
        import xgboost as xgb
        return xgb.XGBClassifier(random_state=RANDOM_STATE, eval_metric='mlogloss',
                                 use_label_encoder=False, n_jobs=-1), \
               {'n_estimators': [200, 500], 'max_depth': [6, 10], 'learning_rate': [0.05, 0.1]}

    elif model_name == 'lgbm':
        import lightgbm as lgb
        return lgb.LGBMClassifier(random_state=RANDOM_STATE, verbose=-1, n_jobs=-1), \
               {'n_estimators': [200, 500], 'max_depth': [10, 20], 'learning_rate': [0.05, 0.1]}

    elif model_name == 'svm':
        return SVC(random_state=RANDOM_STATE, probability=True), \
               {'C': [1, 10], 'kernel': ['rbf']}

    elif model_name == 'mlp':
        return MLPClassifier(random_state=RANDOM_STATE, max_iter=500, early_stopping=True), \
               {'hidden_layer_sizes': [(128, 64), (256, 128)], 'learning_rate_init': [0.001, 0.01]}


def quick_cv_score(model, X, y, groups, params):
    """Quick 3-fold CV to find best hyperparameters."""
    from sklearn.model_selection import ParameterGrid

    best_score = -1
    best_params = None
    gkf = GroupKFold(n_splits=3)

    for p in ParameterGrid(params):
        scores = []
        for train_idx, val_idx in gkf.split(X, y, groups):
            m = model.__class__(**{**model.get_params(), **p})
            m.fit(X[train_idx], y[train_idx])
            scores.append(accuracy_score(y[val_idx], m.predict(X[val_idx])))
        mean_score = np.mean(scores)
        if mean_score > best_score:
            best_score = mean_score
            best_params = p

    return best_params, best_score


def train_model(model_name):
    """Train a single model with full pipeline."""
    print(f"\n{'='*60}")
    print(f"  TRAINING: {model_name.upper()}")
    print(f"{'='*60}")

    # Load data
    samples_file = os.path.join(SAMPLES_DIR, TRAINING_SAMPLES_FILE)
    df = pd.read_csv(samples_file)

    X = df[FEATURES].values
    y = df[TARGET].values
    groups = df[SPATIAL_BLOCK_COL].values

    n_blocks = len(np.unique(groups))
    class_dist = dict(zip(*np.unique(y, return_counts=True)))
    print(f"  Loaded {len(df)} samples, {n_blocks} spatial blocks")
    print(f"  Class distribution: {class_dist}")

    # Scale if needed
    scaler = None
    if model_name in MODELS_NEED_SCALING:
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

    # SVM subsampling (too slow on 30k)
    if model_name == 'svm' and len(X) > 10000:
        idx = np.random.RandomState(RANDOM_STATE).choice(len(X), 10000, replace=False)
        X_train = X[idx]
        y_train = y[idx]
        groups_train = groups[idx]
        print(f"  [SVM] Subsampled to {len(X_train)} for tractability")
    else:
        X_train = X
        y_train = y
        groups_train = groups

    # Step 1: Quick hyperparameter search
    base_model, param_grid = get_model_and_params(model_name)
    print(f"  Step 1: Hyperparameter search...")

    best_params, quick_score = quick_cv_score(base_model, X_train, y_train, groups_train, param_grid)
    print(f"  Best params: {best_params} (Quick CV Acc: {quick_score:.4f})")

    # Step 2: Final 5-fold GroupKFold CV with best params
    print(f"\n  Step 2: Final {N_FOLDS}-fold GroupKFold CV...")
    start_time = time.time()

    final_model = base_model.__class__(**{**base_model.get_params(), **best_params})
    gkf = GroupKFold(n_splits=N_FOLDS)

    fold_results = []
    overall_cm = np.zeros((N_CLASSES, N_CLASSES), dtype=int)
    all_preds = []
    all_true = []

    for fold, (train_idx, test_idx) in enumerate(gkf.split(X_train, y_train, groups_train)):
        model = base_model.__class__(**{**base_model.get_params(), **best_params})
        model.fit(X_train[train_idx], y_train[train_idx])
        preds = model.predict(X_train[test_idx])

        acc = accuracy_score(y_train[test_idx], preds)
        f1_mac = f1_score(y_train[test_idx], preds, average='macro', zero_division=0)
        f1_wt = f1_score(y_train[test_idx], preds, average='weighted', zero_division=0)
        kappa = cohen_kappa_score(y_train[test_idx], preds)

        fold_results.append({
            'fold': fold, 'accuracy': acc, 'f1_macro': f1_mac,
            'f1_weighted': f1_wt, 'kappa': kappa
        })

        overall_cm += confusion_matrix(y_train[test_idx], preds, labels=range(N_CLASSES))
        all_preds.extend(preds)
        all_true.extend(y_train[test_idx])

        print(f"    Fold {fold}: OA={acc:.4f}  F1m={f1_mac:.4f}  kappa={kappa:.4f}")

    train_time = time.time() - start_time
    results_df = pd.DataFrame(fold_results)

    # Mean metrics
    mean_acc = results_df['accuracy'].mean()
    mean_f1m = results_df['f1_macro'].mean()
    mean_f1w = results_df['f1_weighted'].mean()
    mean_kappa = results_df['kappa'].mean()

    print(f"\n  MEAN: OA={mean_acc:.4f}  F1m={mean_f1m:.4f}  kappa={mean_kappa:.4f}")
    print(f"  Training time: {train_time:.1f}s")

    # Step 3: Train final model on ALL data
    print(f"\n  Step 3: Training final model on all data...")
    final_model = base_model.__class__(**{**base_model.get_params(), **best_params})
    final_model.fit(X, y)  # Use all data (not subsampled)

    # Save outputs
    os.makedirs(os.path.join(CLASSIFICATION_DIR, 'trained_models'), exist_ok=True)
    os.makedirs(os.path.join(CLASSIFICATION_DIR, 'confusion_matrices'), exist_ok=True)

    # Model
    model_path = os.path.join(CLASSIFICATION_DIR, 'trained_models', f'model_{model_name}.pkl')
    joblib.dump(final_model, model_path)
    print(f"  Saved model: {model_path}")

    # Scaler
    if scaler is not None:
        scaler_path = os.path.join(CLASSIFICATION_DIR, 'trained_models', f'scaler_{model_name}.pkl')
        joblib.dump(scaler, scaler_path)

    # CV results
    results_df.to_csv(os.path.join(CLASSIFICATION_DIR, f'cv_results_{model_name}.csv'), index=False)

    # Confusion matrix
    cm_df = pd.DataFrame(overall_cm, index=CLASS_LABELS, columns=CLASS_LABELS)
    cm_df.to_csv(os.path.join(CLASSIFICATION_DIR, 'confusion_matrices', f'cm_{model_name}.csv'))

    # Plot confusion matrix
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(cm_df, annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_title(f'Confusion Matrix: {model_name.upper()} (5-Fold Spatial CV)', fontweight='bold')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    plt.tight_layout()
    fig.savefig(os.path.join(CLASSIFICATION_DIR, 'confusion_matrices', f'cm_{model_name}.png'), dpi=150)
    plt.close()

    # Feature importance (for tree models)
    if hasattr(final_model, 'feature_importances_'):
        fi = pd.DataFrame({
            'feature': FEATURES,
            'importance': final_model.feature_importances_
        }).sort_values('importance', ascending=False)
        fi.to_csv(os.path.join(CLASSIFICATION_DIR, f'feature_importance_{model_name}.csv'), index=False)
    elif model_name == 'logreg':
        # Use absolute coefficient mean across classes
        coefs = np.abs(final_model.coef_).mean(axis=0)
        fi = pd.DataFrame({
            'feature': FEATURES,
            'importance': coefs
        }).sort_values('importance', ascending=False)
        fi.to_csv(os.path.join(CLASSIFICATION_DIR, f'feature_importance_{model_name}.csv'), index=False)

    # Per-class metrics
    per_class = {}
    for cls_id, cls_name in CLASS_NAMES.items():
        tp = overall_cm[cls_id, cls_id]
        fn = overall_cm[cls_id, :].sum() - tp
        fp = overall_cm[:, cls_id].sum() - tp
        tn = overall_cm.sum() - tp - fn - fp
        pa = tp / (tp + fn) if (tp + fn) > 0 else 0
        ua = tp / (tp + fp) if (tp + fp) > 0 else 0
        iou = tp / (tp + fn + fp) if (tp + fn + fp) > 0 else 0
        per_class[cls_name] = {
            'producers_accuracy': pa, 'users_accuracy': ua, 'iou': iou
        }

    # Summary JSON
    summary = {
        'model': model_name,
        'best_params': best_params,
        'time_s': round(train_time, 1),
        'n_samples': len(df),
        'accuracy': round(mean_acc, 4),
        'f1_macro': round(mean_f1m, 4),
        'f1_weighted': round(mean_f1w, 4),
        'kappa': round(mean_kappa, 4),
        'per_class': per_class
    }
    with open(os.path.join(CLASSIFICATION_DIR, f'summary_{model_name}.json'), 'w') as f:
        json.dump(summary, f, indent=2, default=str)

    # Predictions on full training set (for diagnostics)
    full_preds = final_model.predict(X)
    pred_df = df[['lon', 'lat'] if 'lon' in df.columns else []].copy() if 'lon' in df.columns else pd.DataFrame()
    if '.geo' in df.columns:
        pred_df['.geo'] = df['.geo']
    pred_df['true_class'] = y
    pred_df['predicted_class'] = full_preds
    if hasattr(final_model, 'predict_proba'):
        try:
            proba = final_model.predict_proba(X)
            for i, cls_name in CLASS_NAMES.items():
                if i < proba.shape[1]:
                    pred_df[f'prob_{cls_name}'] = proba[:, i]
        except Exception:
            pass
    pred_df.to_csv(os.path.join(CLASSIFICATION_DIR, f'predictions_{model_name}.csv'), index=False)

    print(f"\n  [DONE] {model_name.upper()} training complete")
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train Land Cover Classifiers')
    parser.add_argument('--model', type=str, default=None, choices=MODEL_NAMES,
                        help='Train a specific model')
    parser.add_argument('--all', action='store_true', help='Train all models')
    args = parser.parse_args()

    if args.all:
        summaries = []
        for m in MODEL_NAMES:
            try:
                s = train_model(m)
                if s:
                    summaries.append(s)
            except Exception as e:
                print(f"  [FAIL] {m}: {e}")

        # Print comparison table
        if summaries:
            print(f"\n{'='*70}")
            print(f"  MODEL COMPARISON")
            print(f"{'='*70}")
            print(f"  {'Model':<12s} {'OA':>8s} {'F1-macro':>10s} {'Kappa':>8s} {'Time':>8s}")
            print(f"  {'-'*46}")
            for s in sorted(summaries, key=lambda x: x['accuracy'], reverse=True):
                print(f"  {s['model']:<12s} {s['accuracy']:>8.4f} {s['f1_macro']:>10.4f} {s['kappa']:>8.4f} {s['time_s']:>7.1f}s")
    elif args.model:
        train_model(args.model)
    else:
        print("Specify --model NAME or --all")
