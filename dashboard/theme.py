# dashboard/theme.py
"""
Shared theme module for consistent elegant styling across all dashboard pages.
Adopts 'Forest & Botanical Clean' design system inspired by the presentation aesthetic:
- Deep evergreen botanical sidebar (#07190F to #133924) with crisp white/mint typography
- Off-white / pale moss canvas (#F6F8F4)
- Deep evergreen headings and accents (#16281C, #1E482D, #2D6A4F)
- Elegant white cards with soft sage hairline borders (#DCE4D8) and 12px border-radius
- Clean typography (Plus Jakarta Sans & IBM Plex Mono)
- Rolling mossy hills footer and live botanical accents
"""
import streamlit as st
import sys
import os
import base64

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.color_palette import DASHBOARD_THEME


def apply_theme():
    """Inject Forest & Botanical Clean CSS into the current Streamlit page."""

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap');

        /* ── Base Canvas & Global Container ── */
        html, body, [class*="css"] {{
            font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
            color: {DASHBOARD_THEME['text_primary']};
        }}

        .stApp {{
            background-color: {DASHBOARD_THEME['bg_primary']};
            color: {DASHBOARD_THEME['text_primary']};
            overflow-x: hidden !important;
        }}

        /* ── Generous Container Margins & Padding (No Cramped Edges) ── */
        .block-container,
        [data-testid="stAppViewContainer"] .main .block-container,
        .stMainBlockContainer {{
            max-width: 1320px !important;
            margin-left: auto !important;
            margin-right: auto !important;
            padding-top: 1rem !important;
            padding-bottom: 2.5rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }}

        @media (max-width: 1024px) {{
            .block-container,
            [data-testid="stAppViewContainer"] .main .block-container,
            .stMainBlockContainer {{
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }}
        }}

        header[data-testid="stHeader"] {{
            background-color: {DASHBOARD_THEME['bg_primary']} !important;
            border-bottom: 1px solid {DASHBOARD_THEME['border']} !important;
        }}

        /* ── Sidebar: Natural Deep Evergreen Slate ── */
        section[data-testid="stSidebar"] {{
            background-color: #0E1F15 !important;
            background-image: linear-gradient(180deg, #102418 0%, #0A1710 100%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: 1px 0 6px rgba(0, 0, 0, 0.08) !important;
        }}

        section[data-testid="stSidebar"] > div {{
            background: transparent !important;
        }}

        section[data-testid="stSidebar"] .stMarkdown p,
        section[data-testid="stSidebar"] .stMarkdown span,
        section[data-testid="stSidebar"] .stCaption {{
            color: #C5D6CC !important;
            font-size: 0.86rem;
        }}

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4 {{
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            letter-spacing: -0.015em;
        }}

        section[data-testid="stSidebar"] strong {{
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }}

        /* ── Sidebar Navigation Header & Items ── */
        [data-testid="stSidebarNav"] {{
            padding-top: 0.8rem;
            position: relative;
        }}

        [data-testid="stSidebarNav"]::before {{
            content: "BORNEO OBSERVATORY";
            display: block;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.16em;
            color: #7DA88D;
            text-transform: uppercase;
            padding: 0.4rem 0.5rem 0.65rem 0.5rem;
            margin-bottom: 0.85rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }}

        [data-testid="stSidebarNav"] ul {{
            counter-reset: navstep;
            padding: 0;
            margin: 0;
        }}

        [data-testid="stSidebarNav"] li {{
            counter-increment: navstep;
            margin-bottom: 0.25rem;
            list-style: none !important;
        }}

        [data-testid="stSidebarNav"] li a {{
            border-radius: 8px !important;
            padding: 0.55rem 0.75rem !important;
            font-size: 0.86rem !important;
            font-weight: 500 !important;
            background: transparent !important;
            border: 1px solid transparent !important;
            transition: all 0.18s ease-in-out !important;
            text-decoration: none !important;
            display: flex !important;
            align-items: center !important;
        }}

        [data-testid="stSidebarNav"] li a,
        [data-testid="stSidebarNav"] li a *,
        [data-testid="stSidebarNav"] li a span,
        [data-testid="stSidebarNav"] li a div,
        [data-testid="stSidebarNav"] a span {{
            color: #C2D2C7 !important;
            -webkit-text-fill-color: #C2D2C7 !important;
            font-weight: 500 !important;
        }}

        [data-testid="stSidebarNav"] li a:hover {{
            background: rgba(255, 255, 255, 0.05) !important;
            border-color: rgba(255, 255, 255, 0.07) !important;
        }}

        [data-testid="stSidebarNav"] li a:hover * {{
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }}

        [data-testid="stSidebarNav"] li a::before {{
            content: counter(navstep, decimal-leading-zero);
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.72rem;
            font-weight: 600;
            color: #6FA382 !important;
            -webkit-text-fill-color: #6FA382 !important;
            margin-right: 0.75rem;
            opacity: 0.85;
            display: inline-block;
            line-height: 1;
        }}

        [data-testid="stSidebarNav"] li a[aria-current="page"] {{
            background: rgba(45, 106, 79, 0.35) !important;
            border-left: 3px solid #52B788 !important;
            border-top: 1px solid rgba(82, 183, 136, 0.25) !important;
            border-right: 1px solid rgba(82, 183, 136, 0.12) !important;
            border-bottom: 1px solid rgba(82, 183, 136, 0.12) !important;
        }}

        [data-testid="stSidebarNav"] li a[aria-current="page"] * {{
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            font-weight: 600 !important;
        }}

        [data-testid="stSidebarNav"] li a[aria-current="page"]::before {{
            color: #74C69D !important;
            -webkit-text-fill-color: #74C69D !important;
            opacity: 1;
        }}

        /* ── Sidebar Form Widgets (Selectbox, Slider, Radio) ── */
        section[data-testid="stSidebar"] [data-baseweb="select"] > div {{
            background-color: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.14) !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
        }}
        section[data-testid="stSidebar"] [data-baseweb="select"] * {{
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }}
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stSlider label,
        section[data-testid="stSidebar"] .stRadio label,
        section[data-testid="stSidebar"] .stMultiSelect label {{
            color: #E2EBDD !important;
            -webkit-text-fill-color: #E2EBDD !important;
            font-weight: 600 !important;
            font-size: 0.84rem !important;
            letter-spacing: 0.01em;
            margin-bottom: 0.35rem;
        }}
        section[data-testid="stSidebar"] hr {{
            border-color: rgba(255, 255, 255, 0.08) !important;
        }}

        button[kind="header"] {{
            color: #C2D2C7 !important;
        }}
        button[kind="header"]:hover {{
            color: #FFFFFF !important;
            background: rgba(255, 255, 255, 0.08) !important;
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
            margin-top: 0.8rem !important;
            margin-bottom: 0.5rem !important;
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
            padding: 0.9rem 1rem !important;
            box-shadow: none !important;
            border-top: 2px solid {DASHBOARD_THEME['accent_green']} !important;
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
            margin: 1.2rem 0 !important;
        }}

        /* ── Forest Editorial Custom Classes ── */
        .forest-card {{
            background: #FFFFFF;
            border: 1px solid {DASHBOARD_THEME['border']};
            border-radius: 14px;
            padding: 1rem 1.2rem;
            box-shadow: none;
            margin-bottom: 0.8rem;
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

    # Render rich botanical branding card and mossy hills in sidebar
    _render_sidebar_botanical()


def _render_sidebar_botanical():
    """Renders a single cohesive, organic botanical card grounded by the rolling hills."""
    with st.sidebar:
        hills_html = "<div style='line-height: 0; margin-top: 0.5rem; background: #0A1710; border-top: 1px solid rgba(255, 255, 255, 0.05);'><img src='app/static/mossy_hills_transparent.png' style='width: 100%; display: block; opacity: 0.85; filter: contrast(1.05);' alt='Rolling Hills' /></div>"
        st.markdown(f"""
        <div style="
            margin-top: 2rem;
            margin-bottom: 1rem;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        ">
            <div style="padding: 1rem 1rem 0.6rem 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <span style="
                        font-family: 'IBM Plex Mono', monospace;
                        font-size: 0.68rem;
                        font-weight: 700;
                        color: #74C69D;
                        letter-spacing: 0.12em;
                        text-transform: uppercase;
                    ">POLSTAT STIS • KEL. 3</span>
                    <span style="
                        font-family: 'IBM Plex Mono', monospace;
                        font-size: 0.62rem;
                        background: rgba(82, 183, 136, 0.15);
                        color: #A7D7C5;
                        padding: 0.15rem 0.4rem;
                        border-radius: 4px;
                    ">Majority Voting</span>
                </div>
                <p style="font-size: 0.78rem; color: #B5C9BC; line-height: 1.45; margin: 0 0 0.75rem 0;">
                    Observatori spatiotemporal Sentinel-2 (2019–2024) membedah interaksi IKN & hegemoni tambang.
                </p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.45rem; font-family: 'IBM Plex Mono', monospace;">
                    <div style="background: rgba(0, 0, 0, 0.22); padding: 0.5rem; border-radius: 6px; border: 1px solid rgba(255, 255, 255, 0.04);">
                        <div style="font-size: 0.60rem; color: #7B9B85; text-transform: uppercase;">Domain Spasial</div>
                        <div style="font-size: 0.82rem; font-weight: 700; color: #FFFFFF;">1,5 Juta Sel</div>
                    </div>
                    <div style="background: rgba(0, 0, 0, 0.22); padding: 0.5rem; border-radius: 6px; border: 1px solid rgba(255, 255, 255, 0.04);">
                        <div style="font-size: 0.60rem; color: #7B9B85; text-transform: uppercase;">Model Akurasi</div>
                        <div style="font-size: 0.82rem; font-weight: 700; color: #74C69D;">83,32% OA</div>
                    </div>
                </div>
            </div>
            {hills_html}
        </div>
        """, unsafe_allow_html=True)


def render_botanical_footer():
    """Renders a grounded, elegant institutional footer card matching the presentation design system."""
    st.markdown("""
    <div style="
        margin-top: 2.5rem;
        margin-bottom: 1rem;
        padding: 1.2rem 1.5rem;
        background: #F2F6EF;
        border: 1px solid #D5E0D2;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(16, 36, 24, 0.02);
    ">
        <div style="display: inline-flex; align-items: center; gap: 0.6rem; margin-bottom: 0.45rem;">
            <span style="display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #2D6A4F;"></span>
            <span style="
                font-family: 'IBM Plex Mono', monospace;
                font-weight: 700;
                color: #1E482D;
                letter-spacing: 0.1em;
                font-size: 0.8rem;
                text-transform: uppercase;
            ">POLITEKNIK STATISTIKA STIS • DATA MINING 2025/2026</span>
            <span style="display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #2D6A4F;"></span>
        </div>
        <div style="font-size: 0.84rem; color: #4B5A50; line-height: 1.6; max-width: 820px; margin: 0 auto; font-family: 'Plus Jakarta Sans', sans-serif;">
            Sistem Pemantauan Alih Fungsi Lahan Spatiotemporal Kalimantan (2019–2024)<br/>
            <span style="font-size: 0.76rem; color: #6F8274; font-family: 'IBM Plex Mono', monospace;">
                Sentinel-2 Surface Reflectance • Majority Voting Sub-Grid 500m (1,5 Juta Sel) • LightGBM Multi-Skala • Spatial Telecoupling
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
