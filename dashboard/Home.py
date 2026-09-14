# dashboard/Home.py
import streamlit as st
import sys
import os
import base64

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import *
from configs.color_palette import *
from theme import apply_theme

st.set_page_config(
    page_title="Land Transformation Intelligence — Kalimantan",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_theme()

# Remove default padding for full-bleed hero and make header transparent (so hamburger menu stays visible)
st.markdown("""
<style>
    .block-container { padding-top: 0 !important; max-width: 100% !important; padding-left: 0 !important; padding-right: 0 !important; padding-bottom: 0 !important; }
    header[data-testid="stHeader"] { background-color: transparent !important; }
    .stMainBlockContainer { padding-top: 0 !important; padding-bottom: 0 !important; }
    
    .hero-title {
        font-family: 'Inter', sans-serif !important;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        line-height: 1.1 !important;
        margin: 0 0 1rem 0 !important;
        letter-spacing: -0.03em !important;
        text-shadow: 0 4px 30px rgba(0,0,0,0.8) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Section with Forest Background ---
hero_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'hero_kalimantan.jpg')

if os.path.exists(hero_path):
    with open(hero_path, "rb") as f:
        hero_b64 = base64.b64encode(f.read()).decode()
    
    st.markdown(f"""
    <div class="hero-wrapper" style="
        position: relative;
        width: 100vw;
        height: 100vh;
        margin-left: calc(-50vw + 50%);
        overflow: hidden;
    ">
        <img src="data:image/jpeg;base64,{hero_b64}" 
             style="width: 100%; height: 100%; object-fit: cover; display: block; filter: brightness(0.6);" />
        <div style="
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            background: radial-gradient(circle, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0) 70%);
            padding: 3rem;
        ">
            <p style="
                font-family: 'IBM Plex Mono', monospace;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.2em;
                color: rgba(255,255,255,0.75);
                margin-bottom: 1rem;
            ">Politeknik Statistika STIS — Data Mining 2025</p>
            <div class="hero-title">Land Transformation Intelligence</div>
            <p style="
                font-family: 'Inter', sans-serif;
                font-size: 1.15rem;
                color: rgba(255,255,255,0.9);
                max-width: 700px;
                line-height: 1.6;
                margin: 0 auto;
                text-shadow: 0 2px 10px rgba(0,0,0,0.5);
            ">Klasifikasi Spatiotemporal Tutupan Lahan di Kalimantan (2019 – 2024)<br>
            menggunakan Sentinel-2, ESA WorldCover, dan LightGBM.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.title("Land Transformation Intelligence")
    st.markdown("Klasifikasi Spatiotemporal Tutupan Lahan di Kalimantan (2019 – 2024)")
