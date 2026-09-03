"""
constants.py — Shared constants for Dual-Driver Land Cover Classification
=========================================================================
Project: Dual-Driver Spatiotemporal Land Transformation in Kalimantan
Data:    Sentinel-2 (features) + ESA WorldCover 2021 (labels)
Task:    Supervised multi-class classification (5 classes)
"""

import os

# ============================================================
# PATHS
# ============================================================
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
SAMPLES_DIR = os.path.join(DATA_DIR, 'samples')
PREDICTIONS_DIR = os.path.join(DATA_DIR, 'predictions')
EXTERNAL_DIR = os.path.join(DATA_DIR, 'external')
RESULTS_DIR = os.path.join(PROJECT_DIR, 'results')
CLASSIFICATION_DIR = os.path.join(RESULTS_DIR, 'classification')
CHANGE_DIR = os.path.join(RESULTS_DIR, 'change_maps')
DRIVER_DIR = os.path.join(RESULTS_DIR, 'driver_analysis')
SHAP_DIR = os.path.join(RESULTS_DIR, 'shap')
FIGURES_DIR = os.path.join(RESULTS_DIR, 'figures')
MAPS_DIR = os.path.join(PROJECT_DIR, 'maps')
DASHBOARD_DIR = os.path.join(PROJECT_DIR, 'dashboard')

# ============================================================
# SENTINEL-2 FEATURES (X VARIABLES — INPUT ONLY)
# ============================================================
# Raw Sentinel-2 SR Harmonized bands (6 bands)
SENTINEL2_BANDS = ['B2', 'B3', 'B4', 'B8', 'B11', 'B12']

# Derived spectral indices (4 indices)
SPECTRAL_INDICES = ['NDVI', 'NDBI', 'NDMI', 'BSI']

# Full feature set for classification (10 features)
FEATURES = SENTINEL2_BANDS + SPECTRAL_INDICES

# Band descriptions (for documentation / dashboard)
BAND_DESCRIPTIONS = {
    'B2':   'Blue (490nm, 10m)',
    'B3':   'Green (560nm, 10m)',
    'B4':   'Red (665nm, 10m)',
    'B8':   'NIR (842nm, 10m)',
    'B11':  'SWIR-1 (1610nm, 20m→10m resampled)',
    'B12':  'SWIR-2 (2190nm, 20m→10m resampled)',
    'NDVI': 'Normalized Difference Vegetation Index: (B8-B4)/(B8+B4)',
    'NDBI': 'Normalized Difference Built-up Index: (B11-B8)/(B11+B8)',
    'NDMI': 'Normalized Difference Moisture Index: (B8-B11)/(B8+B11)',
    'BSI':  'Bare Soil Index: ((B11+B4)-(B8+B2))/((B11+B4)+(B8+B2))',
}

# ============================================================
# ANCILLARY DRIVER VARIABLES (FOR DUAL-DRIVER ANALYSIS ONLY)
# These are NOT used as features in the land cover classifier.
# They are explanatory variables for the change model (Task 2/3).
# ============================================================
DRIVER_VARIABLES = [
    'distance_to_ikn',       # km — distance to IKN centroid
    'ikn_buffer_zone',       # categorical: core/10km/25km/50km/100km/outside
    'mining_density_10km',   # km² — mining area within 10km buffer
    'mining_density_25km',   # km² — mining area within 25km buffer
    'distance_to_mining',    # km — distance to nearest mining footprint
    'elevation',             # m — from SRTM
    'rainfall_annual',       # mm — from CHIRPS
]

# ============================================================
# TARGET VARIABLE (Y — GROUND TRUTH LABEL)
# Source: ESA WorldCover v200 (2021), 10m resolution
# ============================================================
TARGET = 'land_cover_class'

# Class mapping: ESA WorldCover codes → Project classes
ESA_TO_PROJECT_CLASS = {
    10: 0,   # Tree cover → Forest
    20: 1,   # Shrubland → Shrubland/Agriculture
    30: 1,   # Grassland → Shrubland/Agriculture
    40: 1,   # Cropland → Shrubland/Agriculture
    50: 2,   # Built-up → Built-up
    60: 3,   # Bare / sparse vegetation → Bare/Mining-like
    70: 3,   # Snow and Ice → Bare/Mining-like (extremely rare in Kalimantan)
    80: 4,   # Permanent water bodies → Water
    90: 0,   # Herbaceous wetland → Forest
    95: 0,   # Mangroves → Forest
    100: 1,  # Moss and lichen → Shrubland/Agriculture
}

# Project class definitions
N_CLASSES = 5
CLASS_NAMES = {
    0: 'Forest',
    1: 'Shrubland/Agriculture',
    2: 'Built-up',
    3: 'Bare/Mining-like',
    4: 'Water',
}
CLASS_LABELS = list(CLASS_NAMES.values())

# ============================================================
# STUDY AREA
# ============================================================
# Kalimantan bounding box (approximate)
KALIMANTAN_BOUNDS = {
    'west': 108.5,
    'east': 119.5,
    'south': -4.2,
    'north': 4.5,
}

# IKN (Ibu Kota Nusantara) center coordinates
IKN_CENTER = {
    'lat': -1.128,
    'lon': 116.847,
}

# IKN buffer zones (km)
IKN_BUFFER_ZONES = [10, 25, 50, 100]

# Provinces in Kalimantan
PROVINCES = [
    'Kalimantan Timur',
    'Kalimantan Selatan',
    'Kalimantan Tengah',
    'Kalimantan Barat',
    'Kalimantan Utara',
]

# ============================================================
# SPATIAL SAMPLING & VALIDATION
# ============================================================
# Spatial block grid size (degrees) — ~55km at equator
BLOCK_GRID_SIZE = 0.5

# Spatial block CV
SPATIAL_BLOCK_COL = 'spatial_block_id'
N_FOLDS = 5

# Stratified sampling target per class
SAMPLING_TARGET = {
    0: 10000,  # Forest (dominant — capped)
    1:  8000,  # Shrubland/Agriculture
    2:  5000,  # Built-up (minority — oversampled)
    3:  3000,  # Bare/Mining-like (rare — oversampled)
    4:  4000,  # Water
}
TOTAL_SAMPLES = sum(SAMPLING_TARGET.values())  # 30,000

# ============================================================
# MACHINE LEARNING MODELS
# ============================================================
RANDOM_STATE = 42

MODEL_NAMES = ['logreg', 'rf', 'xgboost', 'lgbm', 'svm', 'mlp']

MODEL_DISPLAY_NAMES = {
    'logreg':  'Logistic Regression',
    'rf':      'Random Forest',
    'xgboost': 'XGBoost',
    'lgbm':    'LightGBM',
    'svm':     'Support Vector Machine',
    'mlp':     'Neural Network (MLP)',
}

# Models that require feature scaling
MODELS_NEED_SCALING = {'logreg', 'svm', 'mlp'}

# Models that support SHAP TreeExplainer
MODELS_SHAP_TREE = {'rf', 'xgboost', 'lgbm'}

# ============================================================
# TEMPORAL CONFIGURATION
# ============================================================
# Primary temporal window: 2019–2024 (Option B — 2018 excluded)
# 2018 has only 13,632 points (7.8% of 2019's 175,384) with
# shorter latitude range, making it non-comparable.
PRIMARY_YEARS = [2019, 2020, 2021, 2022, 2023, 2024]
EXCLUDED_YEARS = [2018]  # Kept as supplementary/descriptive only
YEARS = PRIMARY_YEARS  # Default to primary years for all scripts
LABEL_YEAR = 2021  # Year with ground truth labels (ESA WorldCover v200)
BASELINE_YEAR = 2019
ENDLINE_YEAR = 2024

# Common spatial domain file (118,943 matched points across 2019-2024)
COMMON_DOMAIN_FILE = os.path.join(PREDICTIONS_DIR, 'common_domain_2019_2024.csv')
CHANGE_DIR_V2 = os.path.join(RESULTS_DIR, 'change_maps_v2')
DRIVER_DIR_V2 = os.path.join(RESULTS_DIR, 'driver_analysis_v2')

# ============================================================
# EVALUATION METRICS
# ============================================================
METRICS = [
    'overall_accuracy',
    'macro_f1',
    'weighted_f1',
    'cohens_kappa',
    'iou_per_class',
]

# ============================================================
# GEE CONFIGURATION
# ============================================================
GEE_COLLECTIONS = {
    'sentinel2': 'COPERNICUS/S2_SR_HARMONIZED',
    'worldcover': 'ESA/WorldCover/v200',
    'srtm': 'USGS/SRTMGL1_003',
    'chirps': 'UCSB-CHG/CHIRPS/DAILY',
}

SENTINEL2_CLOUD_THRESHOLD = 20  # Max cloud cover percentage
SENTINEL2_SCALE = 10  # Output resolution in meters

# ============================================================
# FILE NAMING CONVENTIONS
# ============================================================
TRAINING_SAMPLES_FILE = 'training_samples_2021.csv'
PREDICTION_GRID_TEMPLATE = 'prediction_grid_{year}.csv'
SPATIAL_BLOCKS_FILE = 'spatial_blocks.csv'
