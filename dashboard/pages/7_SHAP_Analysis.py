# dashboard/pages/7_SHAP_Analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from configs.color_palette import *
from configs.constants import BAND_DESCRIPTIONS

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

# ── Load SHAP Importance Data ──
importance_path = os.path.join(SHAP_DIR, 'shap_importance.csv')
df_imp = None
if os.path.exists(importance_path):
    df_imp = pd.read_csv(importance_path)
    df_imp.columns = ['Feature', 'Mean |SHAP|']

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Global Feature Importance (Bar Chart)")
    if df_imp is not None:
        df_plot = df_imp.sort_values('Mean |SHAP|', ascending=True)
        fig = px.bar(df_plot, x='Mean |SHAP|', y='Feature', orientation='h',
                     color='Mean |SHAP|',
                     color_continuous_scale=['#EAE8C9', '#799368', '#4a6b3a'],
                     template=PLOTLY_TEMPLATE,
                     text='Mean |SHAP|')
        fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        fig.update_layout(
            paper_bgcolor=PLOTLY_PAPER_COLOR,
            plot_bgcolor=PLOTLY_PLOT_COLOR,
            font_color=PLOTLY_FONT_COLOR,
            yaxis_title='', xaxis_title='Mean |SHAP Value|',
            showlegend=False, coloraxis_showscale=False,
            height=450
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Data SHAP importance belum tersedia. Jalankan `python scripts/shap_classifier.py` terlebih dahulu.")

with col2:
    st.subheader("Feature Importance (Tabel)")
    if df_imp is not None:
        df_table = df_imp.copy()
        df_table['Rank'] = range(1, len(df_table) + 1)
        df_table['Deskripsi'] = df_table['Feature'].map(BAND_DESCRIPTIONS)
        df_table = df_table[['Rank', 'Feature', 'Mean |SHAP|', 'Deskripsi']]
        st.dataframe(
            df_table.style.format({'Mean |SHAP|': '{:.4f}'})
                .bar(subset=['Mean |SHAP|'], color='#799368', vmin=0),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.caption("Data SHAP importance belum tersedia.")

# ── SHAP Summary Beeswarm Plot ──
st.markdown("---")
st.subheader("SHAP Summary Plot (Beeswarm)")
st.caption("Setiap titik mewakili satu sampel. Warna merah = nilai fitur tinggi, biru = rendah. Posisi horizontal menunjukkan pengaruhnya terhadap keputusan model.")
img_bees = load_image('shap_summary.png')
if img_bees:
    st.image(img_bees, use_container_width=True)
else:
    st.warning("Grafik SHAP summary belum tersedia.")

# ── Per-class heatmap ──
img_heat = load_image('shap_per_class_heatmap.png')
if img_heat:
    st.markdown("---")
    st.subheader("SHAP Importance per Kelas")
    st.image(img_heat, use_container_width=True)

st.markdown("""
---
### Insights dari Analisis Spektral

| Peringkat | Fitur | Mean \|SHAP\| | Interpretasi |
|---|---|---|---|
| 🥇 1 | **NDVI** | 0.938 | Variabel mutlak terpenting. Model mengandalkannya untuk memisahkan vegetasi lebat (Hutan) dari area terbuka. |
| 🥈 2 | **B12 (SWIR-2)** | 0.470 | Sangat sensitif terhadap kelembaban tanah dan mineral, kunci mengenali tambang dan tanah terbuka. |
| 🥉 3 | **B11 (SWIR-1)** | 0.443 | Komplemen dari B12. Bersama-sama, pasangan SWIR mendominasi deteksi area non-vegetasi. |
| 4 | **B3 (Green)** | 0.217 | Membantu membedakan jenis vegetasi (hijau vs kering). |
| 5 | **NDBI** | 0.178 | Fitur kunci untuk mendeteksi infrastruktur beton dan aspal (*built-up*). |
| ... | **NDMI** | 0.046 | Hampir tidak berkontribusi — secara matematis identik dengan negasi NDBI (NDMI ≈ −NDBI). |

> **Catatan Penting:** SHAP menjelaskan **bagaimana model membuat keputusan** (interpretabilitas), bukan **mengapa** suatu lahan berubah (kausalitas). 
> SHAP value tinggi pada NDVI berarti model sangat mengandalkan NDVI saat mengklasifikasi, bukan berarti NDVI menyebabkan perubahan lahan.
""")
