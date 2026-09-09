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
# DASHBOARD THEME — "Instrument Panel"
# Light, hard-edged, hazard-grade saturation. Chosen over the
# previous cream/sage palette because the subject (deforestation,
# mining degradation) needs a register that reads as a monitoring
# instrument, not a calm lifestyle app — see
# dashboard/design-demos/direction-approved.md.
# ============================================================
DASHBOARD_THEME = {
    'bg_primary':    '#F0F2ED',  # Light gray-green background
    'bg_secondary':  '#FFFFFF',  # White panel/card surface
    'bg_tertiary':   '#EAF0E3',  # Active/selected background (nav rail)
    'text_primary':  '#171A15',  # Near-black text
    'text_secondary':'#5B6156',  # Muted ink
    'accent':        '#1F7A3D',  # Forest green (primary interactive elements)
    'accent_green':  '#1F7A3D',
    'accent_red':    '#C6371F',  # Built-up red (urgency/warning)
    'accent_orange': '#B87A1E',  # Bare/mining ochre (secondary warning)
    'border':        '#C7CDBD',  # Hard-edge borders (no shadows, no radius)
}

# ============================================================
# PLOTLY TEMPLATE
# ============================================================
PLOTLY_TEMPLATE = 'plotly_white'
PLOTLY_PAPER_COLOR = '#FFFFFF'
PLOTLY_PLOT_COLOR = '#FFFFFF'
PLOTLY_FONT_COLOR = '#171A15'
PLOTLY_GRID_COLOR = '#C7CDBD'

# ============================================================
# MATPLOTLIB DEFAULTS
# ============================================================
FIGURE_DEFAULTS = {
    'figure.figsize': (12, 8),
    'figure.dpi': 150,
    'figure.facecolor': PLOTLY_PAPER_COLOR,
    'axes.facecolor': PLOTLY_PLOT_COLOR,
    'axes.edgecolor': DASHBOARD_THEME['text_primary'],
    'axes.linewidth': 1.2,
    'axes.labelsize': 12,
    'axes.labelcolor': DASHBOARD_THEME['text_primary'],
    'axes.titlesize': 14,
    'text.color': DASHBOARD_THEME['text_primary'],
    'xtick.labelsize': 10,
    'xtick.color': DASHBOARD_THEME['text_primary'],
    'ytick.labelsize': 10,
    'ytick.color': DASHBOARD_THEME['text_primary'],
    'legend.fontsize': 10,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Inter', 'Arial', 'DejaVu Sans'],
}
