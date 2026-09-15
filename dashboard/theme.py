# dashboard/theme.py
"""
Shared theme module for consistent elegant styling across all dashboard pages.
Adopts 'Forest & Botanical Clean' design system inspired by the presentation aesthetic:
- Off-white / pale moss canvas (#F6F8F4)
- Deep evergreen headings and accents (#16281C, #1E482D, #2D6A4F)
- Elegant white cards with soft sage hairline borders (#DCE4D8) and 12px border-radius
- Clean typography (Plus Jakarta Sans & IBM Plex Mono)
- Zero generic AI clutter, zero cheap emojis
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.color_palette import DASHBOARD_THEME


def apply_theme():
    """Inject Forest & Botanical Clean CSS into the current Streamlit page."""
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

        /* ── Base Canvas ── */
        html, body, [class*="css"] {{
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
            color: {DASHBOARD_THEME['text_primary']};
        }}

        .stApp {{
            background-color: {DASHBOARD_THEME['bg_primary']};
            color: {DASHBOARD_THEME['text_primary']};
        }}

        header[data-testid="stHeader"] {{
            background-color: {DASHBOARD_THEME['bg_primary']} !important;
            border-bottom: 1px solid {DASHBOARD_THEME['border']} !important;
        }}

        /* ── Sidebar: Botanical Navigation Rail ── */
        section[data-testid="stSidebar"] {{
            background-color: #EEF3EB !important;
            border-right: 1px solid {DASHBOARD_THEME['border']} !important;
        }}

        section[data-testid="stSidebar"] .stMarkdown p,
        section[data-testid="stSidebar"] .stMarkdown span {{
            color: {DASHBOARD_THEME['text_secondary']};
            font-size: 0.88rem;
        }}

        [data-testid="stSidebarNav"] ul {{
            counter-reset: navstep;
            padding-top: 0.5rem;
        }}

        [data-testid="stSidebarNav"] li {{
            counter-increment: navstep;
            margin-bottom: 0.25rem;
        }}

        [data-testid="stSidebarNav"] li a {{
            border-radius: 8px !important;
            padding: 0.5rem 0.75rem !important;
            font-size: 0.84rem !important;
            font-weight: 500 !important;
            color: {DASHBOARD_THEME['text_secondary']} !important;
            transition: all 0.15s ease-in-out !important;
            border-left: 3px solid transparent !important;
        }}

        [data-testid="stSidebarNav"] li a:hover {{
            background-color: {DASHBOARD_THEME['bg_tertiary']} !important;
            color: {DASHBOARD_THEME['accent']} !important;
        }}

        [data-testid="stSidebarNav"] li a::before {{
            content: counter(navstep, decimal-leading-zero) " ";
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.72rem;
            font-weight: 600;
            color: {DASHBOARD_THEME['accent_green']};
            margin-right: 0.5rem;
        }}

        [data-testid="stSidebarNav"] li a[aria-current="page"] {{
            border-left: 3px solid {DASHBOARD_THEME['accent_green']} !important;
            background-color: #E2EBDD !important;
            color: {DASHBOARD_THEME['accent']} !important;
            font-weight: 700 !important;
        }}

        /* ── Headings & Titles ── */
        h1 {{
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 800 !important;
            letter-spacing: -0.025em !important;
            color: {DASHBOARD_THEME['text_primary']} !important;
            padding-bottom: 0.4rem;
            margin-bottom: 1.2rem !important;
        }}

        h2, h3 {{
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.015em !important;
            color: {DASHBOARD_THEME['text_primary']} !important;
            margin-top: 1.25rem !important;
            margin-bottom: 0.75rem !important;
        }}

        h4 {{
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            color: {DASHBOARD_THEME['text_primary']} !important;
        }}

        /* ── Metric Cards: Crisp Botanical Readouts ── */
        div[data-testid="stMetric"] {{
            background: {DASHBOARD_THEME['bg_secondary']} !important;
            border: 1px solid {DASHBOARD_THEME['border']} !important;
            border-radius: 12px !important;
            padding: 1.1rem 1.3rem !important;
            box-shadow: 0 2px 8px rgba(22, 40, 28, 0.03) !important;
            border-top: 3px solid {DASHBOARD_THEME['accent_green']} !important;
        }}

        div[data-testid="stMetricLabel"] {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.72rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: {DASHBOARD_THEME['text_secondary']} !important;
        }}

        div[data-testid="stMetricValue"] {{
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 1.65rem !important;
            font-weight: 800 !important;
            color: {DASHBOARD_THEME['text_primary']} !important;
            letter-spacing: -0.02em !important;
        }}

        div[data-testid="stMetricDelta"] {{
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
        }}

        /* ── Modern Tabs ── */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.5rem;
            border-bottom: 1px solid {DASHBOARD_THEME['border']};
            margin-bottom: 1.25rem;
        }}

        .stTabs [data-baseweb="tab"] {{
            padding: 0.65rem 1.4rem;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.85rem;
            font-weight: 600;
            color: {DASHBOARD_THEME['text_secondary']};
            border-radius: 8px 8px 0 0;
            border-bottom: 2px solid transparent;
            transition: all 0.2s ease;
        }}

        .stTabs [aria-selected="true"] {{
            color: {DASHBOARD_THEME['accent']} !important;
            border-bottom: 3px solid {DASHBOARD_THEME['accent_green']} !important;
            background-color: transparent !important;
        }}

        /* ── DataFrames & Tables ── */
        .stDataFrame {{
            border: 1px solid {DASHBOARD_THEME['border']};
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(22, 40, 28, 0.02);
        }}

        /* ── Plotly Charts ── */
        .stPlotlyChart {{
            border: 1px solid {DASHBOARD_THEME['border']};
            border-radius: 12px;
            overflow: hidden;
            padding: 0.75rem;
            background-color: {DASHBOARD_THEME['bg_secondary']};
            box-shadow: 0 2px 10px rgba(22, 40, 28, 0.03);
        }}

        /* ── Informational / Alert Boxes ── */
        .stAlert {{
            background-color: #F1F6EE !important;
            border: 1px solid {DASHBOARD_THEME['border']} !important;
            border-radius: 10px !important;
            border-left: 4px solid {DASHBOARD_THEME['accent_green']} !important;
            color: {DASHBOARD_THEME['text_primary']} !important;
        }}

        /* ── Horizontal Rules ── */
        hr {{
            border-color: {DASHBOARD_THEME['border']} !important;
            margin: 1.8rem 0 !important;
        }}

        /* ── Forest Editorial Custom Classes ── */
        .forest-card {{
            background: #FFFFFF;
            border: 1px solid {DASHBOARD_THEME['border']};
            border-radius: 14px;
            padding: 1.4rem 1.6rem;
            box-shadow: 0 4px 16px rgba(22, 40, 28, 0.04);
            margin-bottom: 1.25rem;
            position: relative;
            overflow: hidden;
        }}

        .forest-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #1E482D 0%, #4A7C59 50%, #C4A482 100%);
        }}

        .step-badge {{
            display: inline-block;
            background-color: {DASHBOARD_THEME['accent']};
            color: #FFFFFF;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
            margin-bottom: 0.6rem;
            letter-spacing: 0.05em;
        }}

        .step-badge-outline {{
            display: inline-block;
            border: 1.5px solid {DASHBOARD_THEME['accent_green']};
            color: {DASHBOARD_THEME['accent_green']};
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.72rem;
            font-weight: 700;
            padding: 0.15rem 0.55rem;
            border-radius: 20px;
            margin-bottom: 0.6rem;
            letter-spacing: 0.05em;
        }}

        .stat-pill {{
            background: #F1F6EE;
            border: 1px solid {DASHBOARD_THEME['border']};
            border-radius: 8px;
            padding: 0.4rem 0.75rem;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.8rem;
            color: {DASHBOARD_THEME['text_primary']};
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            margin-right: 0.5rem;
        }}

        .leaf-tag {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.7rem;
            font-weight: 600;
            color: {DASHBOARD_THEME['accent_green']};
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 0.35rem;
        }}
    </style>
    """, unsafe_allow_html=True)
