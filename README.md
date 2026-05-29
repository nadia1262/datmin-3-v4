# Spatiotemporal Land Cover Transformation in Kalimantan (2018–2024)
## Dual-Driver Analysis: IKN Development × Mining Expansion

> Supervised machine learning classification of Sentinel-2 imagery using ESA WorldCover ground truth labels, with spatiotemporal change detection and dual-driver spatial analysis.

---

## Quick Start

### 1. GEE Data Export
Open [Google Earth Engine Code Editor](https://code.earthengine.google.com/) and run:
1. `gee_scripts/07_stratified_sampling.js` → exports `training_samples_2021.csv`
2. `gee_scripts/09_prediction_grid.js` → exports `prediction_grid_{year}.csv` (×7 years)

Download CSVs from Google Drive to:
- `data/samples/training_samples_2021.csv`
- `data/predictions/prediction_grid_{year}.csv`

### 2. Validate GEE Exports
```bash
python preprocessing/validate_gee_export.py training
python preprocessing/validate_gee_export.py prediction 2021
```

### 3. Train Models
```bash
python scripts/train_classification.py --all      # Train all 6 models
python scripts/train_classification.py --compare   # Compare results
```

### 4. Predict All Years
```bash
python scripts/predict_all_years.py --model rf     # Using Random Forest
python scripts/predict_all_years.py --all          # Using all models
```

### 5. Temporal Validation
```bash
python scripts/temporal_consistency_check.py
```

### 6. Change Detection
```bash
python scripts/change_detection.py --model rf --full-temporal
```

### 7. SHAP Analysis
```bash
python scripts/shap_classifier.py --model lgbm --n_samples 5000
```

### 8. Dual-Driver Analysis
```bash
python scripts/dual_driver_analysis.py --model rf
```

### 9. Prepare & Launch Dashboard
```bash
python scripts/prepare_dashboard_data.py --model rf
streamlit run dashboard/app.py
```

---

## Project Structure

```
Kelompok_3_v4/
├── configs/
│   ├── constants.py          # All project constants (features, classes, paths)
│   └── color_palette.py      # Visual design system
├── gee_scripts/
│   ├── 00_utils.js           # Master utility functions (SINGLE SOURCE OF TRUTH)
│   ├── 01_sentinel2_composite.js
│   ├── 07_stratified_sampling.js   # Training data export
│   └── 09_prediction_grid.js      # Prediction grid export (per year)
├── preprocessing/
│   └── validate_gee_export.py     # Data quality validation
├── scripts/
│   ├── train_classification.py    # 6-model training pipeline
│   ├── predict_all_years.py       # Temporal prediction (2018-2024)
│   ├── change_detection.py        # Transition matrices + hotspot detection
│   ├── shap_classifier.py         # SHAP explainability (multiclass)
│   ├── dual_driver_analysis.py    # IKN × Mining driver analysis
│   ├── temporal_consistency_check.py  # Distributional drift detection
│   └── prepare_dashboard_data.py  # Dashboard data pre-computation
├── dashboard/
│   ├── app.py                     # Streamlit main app
│   └── pages/                     # Dashboard pages
├── data/
│   ├── samples/                   # Training samples (from GEE)
│   ├── predictions/               # Prediction grids + outputs
│   └── external/                  # External datasets
├── results/
│   ├── classification/            # Models, confusion matrices, metrics
│   ├── change_maps/               # Transition matrices, hotspots
│   ├── driver_analysis/           # Regression coefficients
│   └── shap/                      # SHAP plots and values
└── figures/                       # Publication-quality maps
```

## Pipeline Architecture

```
GEE Export ──→ Validate ──→ Train (6 models) ──→ Predict (7 years)
                                                      │
                              ┌────────────────────────┤
                              ▼                        ▼
                      Change Detection         SHAP Analysis
                              │                        │
                              ▼                        ▼
                      Driver Analysis          Dashboard Prep
                              │                        │
                              └────────┬───────────────┘
                                       ▼
                               Streamlit Dashboard
```

## Models

| # | Model | Type | Scaling |
|---|-------|------|---------|
| 1 | Logistic Regression | Linear baseline | StandardScaler |
| 2 | Random Forest | Ensemble (bagging) | None |
| 3 | XGBoost | Ensemble (boosting) | None |
| 4 | LightGBM | Ensemble (boosting) | None |
| 5 | SVM (RBF) | Kernel method | StandardScaler |
| 6 | MLP | Neural network | StandardScaler |

## Land Cover Classes

| ID | Class | Color | ESA WorldCover Source |
|----|-------|-------|----------------------|
| 0 | Forest | 🟢 `#1B7837` | Tree cover, Wetland, Mangrove |
| 1 | Shrubland/Agriculture | 🟩 `#A6D96A` | Shrubland, Grassland, Cropland |
| 2 | Built-up | 🔴 `#E31A1C` | Built-up |
| 3 | Bare/Mining-like | 🟤 `#C4A35A` | Bare/sparse vegetation |
| 4 | Water | 🔵 `#2166AC` | Permanent water bodies |

## Validation Strategy

- **Spatial Block Cross-Validation**: 5-fold GroupKFold using 0.5° grid blocks
- **Metrics**: Overall Accuracy, F1-macro, F1-weighted, Cohen's Kappa, IoU, Producer's/User's Accuracy per class

## Key Configuration

All constants are centralized in `configs/constants.py`:
- `FEATURES`: 10 input features (6 bands + 4 indices)
- `TARGET`: `land_cover_class` (0-4)
- `YEARS`: [2018, 2019, 2020, 2021, 2022, 2023, 2024]
- `LABEL_YEAR`: 2021 (ESA WorldCover v200)
- `RANDOM_STATE`: 42

## Team

POLSTAT STIS — Kelompok 3, Semester 6, Data Mining

---

## Critical Notes

> ⚠️ **Cloud Masking**: ALL GEE scripts MUST use the `maskS2clouds()` function from `00_utils.js` (QA60 bitmask + divide by 10000). Without this, band values will be in DN (0-10000) instead of reflectance (0-1), causing model failure.

> ⚠️ **Temporal Transfer**: Models are trained on 2021 data only. Predictions for other years assume stable spectral-class relationships. Run `temporal_consistency_check.py` to verify.
