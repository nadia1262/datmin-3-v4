"""
color_palette.py — Visual design system for Land Cover Classification Dashboard
================================================================================
Colors follow standard remote sensing conventions for land cover maps.
"""

# ============================================================
# LAND COVER CLASS COLORS (standard remote sensing palette)
# ============================================================
CLASS_COLORS = {
    0: '#1B7837',  # Forest — dark green
    1: '#A6D96A',  # Shrubland/Agriculture — light green
    2: '#E31A1C',  # Built-up — red
    3: '#C4A35A',  # Bare/Mining-like — tan/brown
    4: '#2166AC',  # Water — blue
}

CLASS_COLORS_LIST = ['#1B7837', '#A6D96A', '#E31A1C', '#C4A35A', '#2166AC']

CLASS_COLORS_RGBA = {
    0: (27, 120, 55, 200),
    1: (166, 217, 106, 200),
    2: (227, 26, 28, 200),
    3: (196, 163, 90, 200),
    4: (33, 102, 172, 200),
}

# ============================================================
# MODEL COMPARISON COLORS
# ============================================================
MODEL_COLORS = {
    'logreg':  '#6C757D',  # Gray — baseline
    'rf':      '#28A745',  # Green — ensemble
    'xgboost': '#FD7E14',  # Orange — primary boosting
    'lgbm':    '#20C997',  # Teal — fast boosting
    'svm':     '#6610F2',  # Purple — kernel
    'mlp':     '#E83E8C',  # Pink — neural network
}

# ============================================================
# CHANGE DETECTION COLORS
# ============================================================
CHANGE_COLORS = {
    'forest_loss':      '#D73027',  # Red — deforestation
    'forest_gain':      '#1A9850',  # Green — reforestation
    'mining_expansion': '#FEE08B',  # Yellow — mining spread
    'urban_expansion':  '#FC4E2A',  # Orange-red — urbanization
    'no_change':        '#F0F0F0',  # Light gray — stable
    'water_change':     '#4575B4',  # Blue — water body change
}

# ============================================================
# DRIVER IMPACT COLORS
# ============================================================
DRIVER_COLORS = {
    'ikn_dominant':     '#FF6B6B',  # Coral red — IKN driven
    'mining_dominant':  '#FFD93D',  # Gold — mining driven
    'interaction':      '#C44DFF',  # Purple — both drivers active
    'no_driver':        '#E8E8E8',  # Light gray — no significant driver
}

# ============================================================
# IKN BUFFER ZONE COLORS (gradient from center outward)
# ============================================================
IKN_BUFFER_COLORS = {
    'core':  '#800026',   # Deep red — IKN core
    10:      '#BD0026',   # Red — 10km buffer
    25:      '#FC4E2A',   # Orange-red — 25km buffer
    50:      '#FEB24C',   # Orange — 50km buffer
    100:     '#FED976',   # Light orange — 100km buffer
    'outside': '#FFFFCC', # Pale yellow — outside influence
}

# ============================================================
# UNCERTAINTY / ERROR COLORS (diverging)
# ============================================================
UNCERTAINTY_CMAP = 'RdYlGn_r'  # Red=high uncertainty, Green=low
RESIDUAL_CMAP = 'RdBu'         # Red=overestimation, Blue=underestimation

# ============================================================
# DASHBOARD THEME (Custom 3-Color Palette)
# ============================================================
DASHBOARD_THEME = {
    'bg_primary':    '#FEFDE2',  # Cream background
    'bg_secondary':  '#F5F4D9',  # Slightly darker cream for cards
    'bg_tertiary':   '#EAE8C9',  # Hover/active background
    'text_primary':  '#2E332F',  # Dark text for readability on cream
    'text_secondary':'#606A62',  # Muted text
    'accent':        '#799368',  # Sage Green (primary interactive elements)
    'accent_green':  '#799368',  # Sage Green
    'accent_red':    '#EB8B4A',  # Orange (used for contrast/highlights)
    'accent_orange': '#EB8B4A',  # Orange
    'border':        '#D9D7BF',  # Borders
}

# ============================================================
# MATPLOTLIB DEFAULTS
# ============================================================
FIGURE_DEFAULTS = {
    'figure.figsize': (12, 8),
    'figure.dpi': 150,
    'figure.facecolor': '#FFFFFF',
    'axes.facecolor': '#FFFFFF',
    'axes.edgecolor': '#333333',
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Inter', 'Arial', 'DejaVu Sans'],
}

# ============================================================
# PLOTLY TEMPLATE
# ============================================================
PLOTLY_TEMPLATE = 'plotly_white'
PLOTLY_PAPER_COLOR = '#FEFDE2'
PLOTLY_PLOT_COLOR = '#F5F4D9'
PLOTLY_FONT_COLOR = '#2E332F'
PLOTLY_GRID_COLOR = '#D9D7BF'
