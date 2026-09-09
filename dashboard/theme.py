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
    """Inject Instrument Panel CSS into the current Streamlit page.

    Hard-edged, light, hazard-grade — see dashboard/design-demos/direction-approved.md
    for the chosen direction and dashboard/design-demos/3-instrument-panel.html
    for the source mockup this structure is carried from.
    """
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');

        /* ── Base ── */
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background-color: {DASHBOARD_THEME['bg_primary']};
            color: {DASHBOARD_THEME['text_primary']};
        }}

        header[data-testid="stHeader"] {{
            background-color: {DASHBOARD_THEME['bg_primary']} !important;
        }}

        /* ── Sidebar: numbered instrument rail ── */
        section[data-testid="stSidebar"] {{
            background-color: {DASHBOARD_THEME['bg_secondary']};
            border-right: 1px solid {DASHBOARD_THEME['text_primary']};
        }}

        section[data-testid="stSidebar"] .stMarkdown p,
        section[data-testid="stSidebar"] .stMarkdown span {{
            color: {DASHBOARD_THEME['text_secondary']};
            font-size: 0.9rem;
        }}

        [data-testid="stSidebarNav"] ul {{
            counter-reset: navstep;
        }}

        [data-testid="stSidebarNav"] li {{
            counter-increment: navstep;
        }}

        [data-testid="stSidebarNav"] li a {{
            border-left: 3px solid transparent;
            font-size: 0.85rem;
        }}

        [data-testid="stSidebarNav"] li a::before {{
            content: counter(navstep, decimal-leading-zero) " ";
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.7rem;
            color: {DASHBOARD_THEME['text_secondary']};
            margin-right: 0.4rem;
        }}

        [data-testid="stSidebarNav"] li a[aria-current="page"] {{
            border-left-color: {DASHBOARD_THEME['accent']};
            background-color: {DASHBOARD_THEME['bg_tertiary']} !important;
        }}

        /* ── Headings ── */
        h1 {{
            font-weight: 700 !important;
            letter-spacing: -0.01em !important;
            color: {DASHBOARD_THEME['text_primary']} !important;
            border-bottom: 2px solid {DASHBOARD_THEME['text_primary']};
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem !important;
        }}

        h2, h3 {{
            font-weight: 600 !important;
            letter-spacing: -0.005em !important;
            color: {DASHBOARD_THEME['text_primary']} !important;
        }}

        /* ── Metric Cards: flat instrument readout ── */
        div[data-testid="stMetric"] {{
            background: {DASHBOARD_THEME['bg_secondary']};
            border: 1px solid {DASHBOARD_THEME['text_primary']};
            border-radius: 8px;
            padding: 1rem 1.25rem;
        }}

        div[data-testid="stMetricLabel"] {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.7rem !important;
            font-weight: 500 !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: {DASHBOARD_THEME['text_secondary']} !important;
        }}

        div[data-testid="stMetricValue"] {{
            font-size: 1.6rem !important;
            font-weight: 700 !important;
            color: {DASHBOARD_THEME['text_primary']} !important;
        }}

        /* ── Info / Alert Boxes ── */
        .stAlert {{
            background-color: {DASHBOARD_THEME['bg_secondary']} !important;
            border: 1px solid {DASHBOARD_THEME['border']} !important;
            border-radius: 8px !important;
            border-left: 4px solid {DASHBOARD_THEME['accent_orange']} !important;
        }}

        /* ── Tabs ── */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0;
            border-bottom: 2px solid {DASHBOARD_THEME['text_primary']};
        }}

        .stTabs [data-baseweb="tab"] {{
            padding: 0.75rem 1.5rem;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            font-weight: 500;
            color: {DASHBOARD_THEME['text_secondary']};
            border-bottom: 3px solid transparent;
            transition: color 0.15s ease;
        }}

        .stTabs [aria-selected="true"] {{
            color: {DASHBOARD_THEME['text_primary']} !important;
            border-bottom: 3px solid {DASHBOARD_THEME['accent']} !important;
            background-color: transparent !important;
        }}

        /* ── DataFrames ── */
        .stDataFrame {{
            border: 1px solid {DASHBOARD_THEME['text_primary']};
            border-radius: 8px;
            overflow: hidden;
        }}

        /* ── Horizontal Rules ── */
        hr {{
            border-color: {DASHBOARD_THEME['border']} !important;
            margin: 2rem 0 !important;
        }}

        /* ── Plotly Charts ── */
        .stPlotlyChart {{
            border: 1px solid {DASHBOARD_THEME['text_primary']};
            border-radius: 8px;
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
            font-family: 'IBM Plex Mono', monospace;
            font-style: normal;
            font-size: 0.78rem !important;
        }}

        /* ── Subtle section label ── */
        .section-label {{
            font-family: 'IBM Plex Mono', monospace;
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
