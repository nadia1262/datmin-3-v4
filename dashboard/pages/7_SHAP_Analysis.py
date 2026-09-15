# dashboard/pages/7_SHAP_Analysis.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
import base64
import html
from io import BytesIO
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

@st.cache_data(show_spinner=False)
def load_image_base64(filename):
    path = os.path.join(SHAP_DIR, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
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
                     color_continuous_scale=[DASHBOARD_THEME['bg_tertiary'], DASHBOARD_THEME['accent'], DASHBOARD_THEME['text_primary']],
                     template=PLOTLY_TEMPLATE,
                     text='Mean |SHAP|')
        fig.update_traces(texttemplate='%{text:.3f}', textposition='outside', cliponaxis=False)
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
                .bar(subset=['Mean |SHAP|'], color=DASHBOARD_THEME['accent'], vmin=0),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.caption("Data SHAP importance belum tersedia.")

# ── SHAP Summary Beeswarm Plot ──
st.markdown("---")
st.subheader("SHAP Summary Plot (Beeswarm)")
b64_bees = load_image_base64('shap_summary.png')
if b64_bees:
    bees_alt = "SHAP beeswarm plot: setiap titik mewakili satu sampel. Warna merah = nilai fitur tinggi, biru = rendah. Posisi horizontal menunjukkan pengaruhnya terhadap keputusan model."
    st.markdown(
        f'<img src="data:image/png;base64,{b64_bees}" alt="{html.escape(bees_alt)}" style="width:100%; max-width:100%">',
        unsafe_allow_html=True
    )
    st.caption(bees_alt)
else:
    st.warning("Grafik SHAP summary belum tersedia.")

# ── Per-class heatmap ──
b64_heat = load_image_base64('shap_per_class_heatmap.png')
if b64_heat:
    st.markdown("---")
    st.subheader("SHAP Importance per Kelas")
    heat_alt = "Heatmap SHAP importance per kelas tutupan lahan (Forest, Shrubland/Agriculture, Built-up, Bare/Mining-like, Water) per fitur spektral."
    st.markdown(
        f'<img src="data:image/png;base64,{b64_heat}" alt="{html.escape(heat_alt)}" style="width:100%; max-width:100%">',
        unsafe_allow_html=True
    )
    st.caption(heat_alt)

st.markdown("---")
st.markdown("""
<div class="forest-card" style="margin-top: 1rem;">
    <span class="step-badge">SINTESIS FISIKA OPTIK SPEKTRAL</span>
    <h4 style="margin: 0.2rem 0 0.6rem 0;">Tiga Temuan Utama Fisika Penginderaan Jauh</h4>
    <div style="font-size: 0.88rem; color: #4B5A50; line-height: 1.65;">
        • <strong>NDVI (Mean |SHAP| = 0,938):</strong> Variabel spektral paling dominan. Menjadi pemisah utama antara kanopi vegetasi lebat (Hutan/Semak) dengan lanskap non-vegetasi.<br>
        • <strong>Pasangan SWIR B12 & B11 (Mean |SHAP| = 0,470 & 0,443):</strong> Sangat sensitif terhadap kadar air kanopi dan pantulan mineral tanah terbuka. Kombinasi kanal inframerah gelombang pendek ini menjadi kunci utama LightGBM dalam mendeteksi bukaan tambang batubara aktif dan alur infrastruktur jalan.<br>
        • <strong>NDBI (0,178) vs NDMI (0,046):</strong> Membuktikan temuan multikolinearitas sempurna (r = -1,000). Nilai SHAP terbagi di antara kedua indeks spektral komplementer ini.
    </div>
    <div style="margin-top: 0.8rem; padding-top: 0.6rem; border-top: 1px solid #DCE4D8; font-size: 0.8rem; color: #6E7D73;">
        <em>Catatan Interpretabilitas:</em> Nilai SHAP menguantifikasi kontribusi fitur terhadap keputusan prediksi algoritma (bagaimana model membedakan spektral), bukan hubungan kausalitas lingkungan.
    </div>
</div>
""", unsafe_allow_html=True)
