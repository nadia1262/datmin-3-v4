# dashboard/app.py
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import *
from configs.color_palette import *

st.set_page_config(
    page_title="Dual-Driver Land Cover Dashboard",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium dark theme
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}
    
    .stApp {{
        background-color: {DASHBOARD_THEME['bg_primary']};
        color: {DASHBOARD_THEME['text_primary']};
    }}
    
    .css-1d391kg, .css-12oz5g7 {{
        background-color: {DASHBOARD_THEME['bg_secondary']} !important;
    }}
    
    div[data-testid="stMetricValue"] {{
        font-size: 2rem;
        font-weight: 700;
        color: {DASHBOARD_THEME['accent']};
    }}
    
    .stAlert {{
        background-color: {DASHBOARD_THEME['bg_secondary']} !important;
        border: 1px solid {DASHBOARD_THEME['border']} !important;
        border-radius: 8px !important;
    }}
    
    hr {{
        border-color: {DASHBOARD_THEME['border']} !important;
    }}
</style>
""", unsafe_allow_html=True)

st.title("🛰️ Dual-Driver Land Cover Transformation Dashboard")
st.subheader("Spatiotemporal Land Cover Classification in Kalimantan (2018-2024)")

st.markdown("""
---
Selamat datang di platform analitik spasial untuk **Dual-Driver Land Transformation** di Kalimantan. 
Dashboard ini menyajikan hasil dari framework klasifikasi supervised machine learning menggunakan *Sentinel-2* dan label *ESA WorldCover*.

Fokus utama penelitian ini adalah mengkuantifikasi perubahan tutupan lahan (Forest, Shrubland, Built-up, Bare, Water) dan menguji dua *driver* spasial utama:
1. **IKN Development** (Infrastructure Expansion)
2. **Mining Activities** (Extractive Land Degradation)
""")

st.info("""
**Navigasi Dashboard (Sidebar):**
- 🗺️ **Land Cover Maps**: Peta klasifikasi per tahun dengan time slider.
- 📊 **Change Detection**: Analisis transisi kelas (Forest Loss, Urban/Mining Expansion).
- 🤖 **Model Comparison**: Perbandingan 6 algoritma klasifikasi.
- 🏗️ **Driver Impact**: Pemodelan spasial IKN vs Mining.
- 🔍 **Pixel Inspector**: Fitur interaktif klik-peta untuk melihat time-series pixel.
- 🌪️ **Uncertainty**: Analisis spasial probabilitas error model.
""")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Tahun Analisis", "2018 - 2024")
with col2:
    st.metric("Algoritma ML", "6 Model")
with col3:
    st.metric("Kelas Lahan", "5 Kelas")
with col4:
    st.metric("Driver Utama", "IKN & Tambang")

st.markdown("""
---
*Project: Machine Learning-Based Land Cover Classification using Sentinel-2 Imagery and ESA WorldCover Ground Truth.*
""")
