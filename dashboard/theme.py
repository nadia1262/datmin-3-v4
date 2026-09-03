# dashboard/theme.py
"""
Shared theme module for consistent elegant styling across all dashboard pages.
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.color_palette import DASHBOARD_THEME


def apply_theme():
    """Inject elegant CSS into the current Streamlit page."""
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* ── Base ── */
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background-color: {DASHBOARD_THEME['bg_primary']};
            color: {DASHBOARD_THEME['text_primary']};
        }}

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {{
            background-color: {DASHBOARD_THEME['bg_secondary']};
            border-right: 1px solid {DASHBOARD_THEME['border']};
        }}

        section[data-testid="stSidebar"] .stMarkdown p,
        section[data-testid="stSidebar"] .stMarkdown span {{
            color: {DASHBOARD_THEME['text_secondary']};
            font-size: 0.9rem;
        }}

        /* ── Headings ── */
        h1 {{
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
            color: {DASHBOARD_THEME['text_primary']} !important;
            border-bottom: 2px solid {DASHBOARD_THEME['accent']};
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem !important;
        }}

        h2, h3 {{
            font-weight: 600 !important;
            letter-spacing: -0.01em !important;
            color: {DASHBOARD_THEME['text_primary']} !important;
        }}

        /* ── Metric Cards ── */
        div[data-testid="stMetric"] {{
            background: linear-gradient(135deg, {DASHBOARD_THEME['bg_secondary']} 0%, {DASHBOARD_THEME['bg_tertiary']} 100%);
            border: 1px solid {DASHBOARD_THEME['border']};
            border-radius: 12px;
            padding: 1rem 1.25rem;
            transition: border-color 0.2s ease, transform 0.15s ease;
        }}

        div[data-testid="stMetric"]:hover {{
            border-color: {DASHBOARD_THEME['accent']};
            transform: translateY(-1px);
        }}

        div[data-testid="stMetricLabel"] {{
            font-size: 0.8rem !important;
            font-weight: 500 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: {DASHBOARD_THEME['text_secondary']} !important;
        }}

        div[data-testid="stMetricValue"] {{
            font-size: 1.75rem !important;
            font-weight: 700 !important;
            color: {DASHBOARD_THEME['accent']} !important;
        }}

        /* ── Info / Alert Boxes ── */
        .stAlert {{
            background-color: {DASHBOARD_THEME['bg_secondary']} !important;
            border: 1px solid {DASHBOARD_THEME['border']} !important;
            border-radius: 10px !important;
            border-left: 3px solid {DASHBOARD_THEME['accent']} !important;
        }}

        /* ── Tabs ── */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0;
            border-bottom: 1px solid {DASHBOARD_THEME['border']};
        }}

        .stTabs [data-baseweb="tab"] {{
            padding: 0.75rem 1.5rem;
            font-weight: 500;
            color: {DASHBOARD_THEME['text_secondary']};
            border-bottom: 2px solid transparent;
            transition: all 0.2s ease;
        }}

        .stTabs [aria-selected="true"] {{
            color: {DASHBOARD_THEME['accent']} !important;
            border-bottom: 2px solid {DASHBOARD_THEME['accent']} !important;
            background-color: transparent !important;
        }}

        /* ── DataFrames ── */
        .stDataFrame {{
            border: 1px solid {DASHBOARD_THEME['border']};
            border-radius: 10px;
            overflow: hidden;
        }}

        /* ── Horizontal Rules ── */
        hr {{
            border-color: {DASHBOARD_THEME['border']} !important;
            margin: 2rem 0 !important;
        }}

        /* ── Plotly Charts ── */
        .stPlotlyChart {{
            border: 1px solid {DASHBOARD_THEME['border']};
            border-radius: 10px;
            overflow: hidden;
            padding: 0.5rem;
            background-color: {DASHBOARD_THEME['bg_secondary']};
        }}

        /* ── Slider ── */
        .stSlider > div > div {{
            color: {DASHBOARD_THEME['text_secondary']};
        }}

        /* ── Caption ── */
        .stCaption {{
            color: {DASHBOARD_THEME['text_secondary']} !important;
            font-style: italic;
        }}

        /* ── Subtle section label ── */
        .section-label {{
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: {DASHBOARD_THEME['text_secondary']};
            margin-bottom: 0.25rem;
        }}

        .accent-text {{
            color: {DASHBOARD_THEME['accent']};
            font-weight: 600;
        }}

        .muted-text {{
            color: {DASHBOARD_THEME['text_secondary']};
            font-size: 0.9rem;
        }}
    </style>
    """, unsafe_allow_html=True)
