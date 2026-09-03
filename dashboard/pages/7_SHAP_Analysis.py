# dashboard/pages/7_SHAP_Analysis.py
import streamlit as st
import pandas as pd
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from configs.color_palette import *

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from theme import apply_theme

st.set_page_config(page_title="SHAP Analysis", page_icon="◈", layout="wide")
apply_theme()

st.title("Interpretability with SHAP")
st.markdown("""
Bagaimana model Machine Learning kita (LightGBM) mengenali pola "Hutan", "Tambang", atau "Bangunan" dari sekadar data pantulan cahaya satelit? 
Melalui analisis **SHAP (SHapley Additive exPlanations)**, kita membedah "otak" model untuk melihat fitur spektral mana yang paling krusial dalam klasifikasi tutupan lahan.
""")

SHAP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../results/shap/lgbm')

def load_image(filename):
    path = os.path.join(SHAP_DIR, filename)
    if os.path.exists(path):
        return Image.open(path)
    return None

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Global Feature Importance")
    st.caption("Bar chart menunjukkan rata-rata |SHAP value| per fitur — semakin tinggi, semakin besar kontribusi fitur terhadap keputusan model.")
    img_bees = load_image('shap_summary.png')
    if img_bees:
        st.image(img_bees, use_container_width=True)
    else:
        st.warning("Grafik SHAP summary belum tersedia. Pastikan script shap_classifier.py sudah dijalankan.")

with col2:
    st.subheader("Feature Importance (Tabel)")
    # Load importance from CSV
    importance_path = os.path.join(SHAP_DIR, 'shap_importance.csv')
    if os.path.exists(importance_path):
        df_imp = pd.read_csv(importance_path)
        df_imp.columns = ['Feature', 'Mean |SHAP|']
        df_imp['Rank'] = range(1, len(df_imp) + 1)
        df_imp = df_imp[['Rank', 'Feature', 'Mean |SHAP|']]
        st.dataframe(
            df_imp.style.format({'Mean |SHAP|': '{:.4f}'}).bar(subset=['Mean |SHAP|'], color='#00D4FF', vmin=0),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.caption("Data SHAP importance belum tersedia.")

    # Show heatmap if available
    img_heat = load_image('shap_per_class_heatmap.png')
    if img_heat:
        st.subheader("Importance per Class")
        st.image(img_heat, use_container_width=True)

st.markdown("""
---
### Insights dari Analisis Spektral
1. **NDVI (Normalized Difference Vegetation Index)** — Variabel mutlak terpenting. Model menggunakannya untuk memisahkan vegetasi lebat (Hutan) dari area terbuka (Tambang/Bangunan).
2. **SWIR (Band 11 & Band 12)** — *Shortwave Infrared* sangat sensitif terhadap kelembaban tanah dan mineral batuan, sehingga model bergantung pada B11/B12 untuk mengenali area terbuka (Bare/Mining-like).
3. **NDBI (Normalized Difference Built-up Index)** — Fitur kunci untuk mendeteksi infrastruktur beton dan aspal.
4. **NDMI** (Mean |SHAP| = 0.046) — Hampir tidak berkontribusi karena secara matematis merupakan negasi dari NDBI (NDMI = −NDBI). Ini merupakan keterbatasan dalam desain fitur yang perlu diakui.
""")
