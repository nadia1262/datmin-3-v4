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
from theme import apply_theme, render_botanical_footer

st.set_page_config(page_title="SHAP Analysis", layout="wide")
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
st.subheader("Distribusi Nilai SHAP Global (Beeswarm Plot)")
b64_bees = load_image_base64('shap_summary.png')
if b64_bees:
    bees_alt = "SHAP beeswarm plot: setiap titik mewakili satu sampel. Warna merah = nilai fitur tinggi, biru = rendah. Posisi horizontal menunjukkan pengaruhnya terhadap keputusan model."
    st.markdown(f"""
    <div class="forest-card" style="padding: 1.25rem; margin-top: 0.75rem;">
        <div style="font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; font-weight: 700; color: #2D6A4F; text-transform: uppercase; margin-bottom: 0.6rem;">
            DENSITAS ATRIBUSI FITUR (SAMPLE-LEVEL SHAP VALUE)
        </div>
        <div style="background: #FAFCF9; border: 1px solid #E2EBDD; border-radius: 10px; padding: 1.2rem; text-align: center; box-shadow: inset 0 1px 4px rgba(0,0,0,0.02);">
            <img src="data:image/png;base64,{b64_bees}" alt="{html.escape(bees_alt)}" style="width: 100%; max-width: 960px; border-radius: 6px; display: block; margin: 0 auto;" />
        </div>
        <div style="font-size: 0.83rem; color: #4B5A50; margin-top: 0.85rem; line-height: 1.55;">
            <strong>Panduan Interpretasi Sumbu:</strong> Setiap titik mewakili 1 piksel observasi valid. Sumbu horizontal menunjukkan besaran kontribusi SHAP: nilai ke arah kanan mendorong prediksi ke kelas target, sedangkan ke arah kiri menurunkan peluangnya. Gradasi warna (merah = nilai reflektansi/indeks tinggi, biru = rendah) mengonfirmasi sensitivitas fisik kanal satelit.
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.warning("Grafik SHAP summary belum tersedia.")

# ── Per-class heatmap ──
b64_heat = load_image_base64('shap_per_class_heatmap.png')
if b64_heat:
    st.markdown("---")
    st.subheader("Diferensiasi SHAP Importance Antarkelas Tutupan Lahan")
    heat_alt = "Heatmap SHAP importance per kelas tutupan lahan per fitur spektral."
    st.markdown(f"""
    <div class="forest-card" style="padding: 1.25rem; margin-top: 0.75rem;">
        <div style="font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; font-weight: 700; color: #2D6A4F; text-transform: uppercase; margin-bottom: 0.6rem;">
            MATRIKS KONTRIBUSI SPEKTRAL PER KELAS LAHAN
        </div>
        <div style="background: #FAFCF9; border: 1px solid #E2EBDD; border-radius: 10px; padding: 1.2rem; text-align: center; box-shadow: inset 0 1px 4px rgba(0,0,0,0.02);">
            <img src="data:image/png;base64,{b64_heat}" alt="{html.escape(heat_alt)}" style="width: 100%; max-width: 960px; border-radius: 6px; display: block; margin: 0 auto;" />
        </div>
        <div style="font-size: 0.83rem; color: #4B5A50; margin-top: 0.85rem; line-height: 1.55;">
            <strong>Analisis Kelas:</strong> Menunjukkan diferensiasi peran band Sentinel-2: NDVI mendominasi identifikasi kanopi hutan, SWIR B12 dan B11 membedakan mineral tanah terbuka dan bukaan tambang dari semak belukar, serta NDBI menonjol pada pemetaan area terbangun.
        </div>
    </div>
    """, unsafe_allow_html=True)

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

render_botanical_footer()
