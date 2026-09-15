"""
color_palette.py — Visual design system for Land Cover Classification Dashboard
================================================================================
Colors follow standard remote sensing conventions for land cover maps.
"""

# ============================================================
# LAND COVER CLASS COLORS (standard remote sensing convention,
# executed at hazard-grade saturation — see DASHBOARD_THEME note)
# ============================================================
CLASS_COLORS = {
    0: '#1F7A3D',  # Forest — green
    1: '#6E9A2E',  # Shrubland/Agriculture — olive-green
    2: '#C6371F',  # Built-up — red
    3: '#B87A1E',  # Bare/Mining-like — ochre
    4: '#1B5FA8',  # Water — blue
}

CLASS_COLORS_LIST = ['#1F7A3D', '#6E9A2E', '#C6371F', '#B87A1E', '#1B5FA8']

CLASS_COLORS_RGBA = {
    0: (31, 122, 61, 200),
    1: (110, 154, 46, 200),
    2: (198, 55, 31, 200),
    3: (184, 122, 30, 200),
    4: (27, 95, 168, 200),
}

# ============================================================
# MODEL COMPARISON COLORS
# ============================================================
MODEL_COLORS = {
    'logreg':  '#5B6156',  # Ink-mute gray — baseline
    'rf':      '#1F7A3D',  # Green — ensemble
    'xgboost': '#C6371F',  # Red — primary boosting
    'lgbm':    '#1B5FA8',  # Blue — fast boosting
    'svm':     '#6E4F9E',  # Purple — kernel
    'mlp':     '#B87A1E',  # Ochre — neural network
}

# ============================================================
# CHANGE DETECTION COLORS
# ============================================================
CHANGE_COLORS = {
    'forest_loss':      '#C6371F',  # Red — deforestation
    'forest_gain':      '#1F7A3D',  # Green — reforestation
    'mining_expansion': '#B87A1E',  # Ochre — mining spread
    'urban_expansion':  '#6E4F9E',  # Purple — urbanization
    'no_change':        '#D8DBD0',  # Light gray-green — stable
    'water_change':     '#1B5FA8',  # Blue — water body change
}

# ============================================================
# DRIVER IMPACT COLORS
# ============================================================
DRIVER_COLORS = {
    'ikn_dominant':     '#C6371F',  # Red — IKN driven
    'mining_dominant':  '#B87A1E',  # Ochre — mining driven
    'interaction':      '#6E4F9E',  # Purple — both drivers active
    'no_driver':        '#D8DBD0',  # Light gray-green — no significant driver
}

# ============================================================
# IKN BUFFER ZONE COLORS (gradient from center outward)
# ============================================================
IKN_BUFFER_COLORS = {
    'core':  '#7A1810',   # Deep red — IKN core
    10:      '#C6371F',   # Red — 10km buffer
    25:      '#D9612B',   # Orange-red — 25km buffer
    50:      '#E2903A',   # Orange — 50km buffer
    100:     '#EDBB6B',   # Light orange — 100km buffer
    'outside': '#F0F2ED', # Fades into background — outside influence
}

# ============================================================
# UNCERTAINTY / ERROR COLORS (diverging)
# ============================================================
UNCERTAINTY_CMAP = 'RdYlGn_r'  # Red=high uncertainty, Green=low
RESIDUAL_CMAP = 'RdBu'         # Red=overestimation, Blue=underestimation

# ============================================================
# DASHBOARD THEME — "Forest & Botanical Clean" (Inspired by PPT)
# Refined organic forest tones, clean airy canvas, soft sage borders,
# and high-contrast editorial typography.
# ============================================================
DASHBOARD_THEME = {
    'bg_primary':    '#F6F8F4',  # Soft pale moss/cream canvas
    'bg_secondary':  '#FFFFFF',  # Clean white card surface
    'bg_tertiary':   '#E8EFE5',  # Subtle sage tint (active tabs / pill tags)
    'text_primary':  '#16281C',  # Deep forest slate text
    'text_secondary':'#4B5A50',  # Muted forest moss text
    'accent':        '#1E482D',  # Deep evergreen primary
    'accent_green':  '#2D6A4F',  # Canopy emerald
    'accent_olive':  '#527853',  # Sage / olive foliage
    'accent_red':    '#B23A22',  # Terracotta / rust (forest loss / built-up)
    'accent_orange': '#C27B22',  # Warm ochre / amber (mining / bare)
    'accent_sand':   '#C4A482',  # Warm timber / sand
    'border':        '#DCE4D8',  # Soft hairline sage border
    'border_dark':   '#BAC8B4',  # Defined border for inputs
}

# ============================================================
# PLOTLY TEMPLATE & STYLING
# ============================================================
PLOTLY_TEMPLATE = 'plotly_white'
PLOTLY_PAPER_COLOR = '#FFFFFF'
PLOTLY_PLOT_COLOR = '#FFFFFF'
PLOTLY_FONT_COLOR = '#16281C'
PLOTLY_GRID_COLOR = '#E5EDE2'

# ============================================================
# MATPLOTLIB DEFAULTS
# ============================================================
FIGURE_DEFAULTS = {
    'figure.figsize': (12, 8),
    'figure.dpi': 150,
    'figure.facecolor': PLOTLY_PAPER_COLOR,
    'axes.facecolor': PLOTLY_PLOT_COLOR,
    'axes.edgecolor': DASHBOARD_THEME['border'],
    'axes.linewidth': 1.0,
    'axes.labelsize': 11,
    'axes.labelcolor': DASHBOARD_THEME['text_primary'],
    'axes.titlesize': 13,
    'text.color': DASHBOARD_THEME['text_primary'],
    'xtick.labelsize': 9.5,
    'xtick.color': DASHBOARD_THEME['text_secondary'],
    'ytick.labelsize': 9.5,
    'ytick.color': DASHBOARD_THEME['text_secondary'],
    'legend.fontsize': 9.5,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Plus Jakarta Sans', 'Inter', 'Segoe UI', 'sans-serif'],
}
