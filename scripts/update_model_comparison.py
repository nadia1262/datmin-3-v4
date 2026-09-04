"""
update_model_comparison.py - Update model_comparison.csv with fresh data from summary JSONs
"""
import os, sys, json, csv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/..')
from configs.constants import CLASSIFICATION_DIR, MODEL_NAMES

model_names = ['lgbm', 'xgboost', 'svm', 'mlp', 'rf', 'logreg']
rows = []

for m in model_names:
    path = os.path.join(CLASSIFICATION_DIR, f'summary_{m}.json')
    if os.path.exists(path):
        with open(path) as f:
            s = json.load(f)
        rows.append({
            'model': s['model'],
            'best_params': str(s['best_params']),
            'time_s': s['time_s'],
            'n_samples': s['n_samples'],
            'accuracy': s['accuracy'],
            'f1_macro': s['f1_macro'],
            'f1_weighted': s['f1_weighted'],
            'kappa': s['kappa'],
            'per_class': str(s['per_class'])
        })
        print(f"  [OK] {m}: acc={s['accuracy']}, n={s['n_samples']}, time={s['time_s']}s")
    else:
        print(f"  [MISSING] {path}")

out_path = os.path.join(CLASSIFICATION_DIR, 'model_comparison.csv')
fieldnames = ['model','best_params','time_s','n_samples','accuracy','f1_macro','f1_weighted','kappa','per_class']
with open(out_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"\n[DONE] Rebuilt {out_path} with {len(rows)} models.")
