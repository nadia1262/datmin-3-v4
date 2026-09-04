# dashboard/app.py
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import *
from configs.color_palette import *
from theme import apply_theme

st.set_page_config(
    page_title="Dual-Driver Land Cover Dashboard",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()

st.title("Dual-Driver Land Cover Transformation Dashboard")
st.markdown("Klasifikasi Spatiotemporal Tutupan Lahan di Kalimantan (2019–2024)", 
            help=None)

st.markdown("""
---
Selamat datang di platform analitik spasial untuk **Dual-Driver Land Transformation** di Kalimantan. 
Dashboard ini menyajikan hasil dari framework klasifikasi supervised machine learning menggunakan *Sentinel-2* dan label *ESA WorldCover*.

Fokus utama penelitian ini adalah mengkuantifikasi perubahan tutupan lahan (Forest, Shrubland, Built-up, Bare, Water) dan menguji dua *driver* spasial utama:
1. **IKN Development** — Infrastructure Expansion
2. **Mining Activities** — Extractive Land Degradation
""")

st.info("""
**Navigasi Dashboard (Sidebar):**
- **Land Cover Maps** — Peta klasifikasi per tahun dengan time slider.
- **Change Detection** — Analisis transisi kelas dan tren temporal.
- **Model Comparison** — Perbandingan 6 algoritma klasifikasi.
- **Driver Impact** — Analisis dual-driver IKN vs Mining.
- **SHAP Analysis** — Interpretabilitas fitur model.
""")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Tahun Analisis", "2019 – 2024")
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
