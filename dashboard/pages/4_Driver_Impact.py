# dashboard/pages/4_Driver_Impact.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from configs.constants import *
from configs.color_palette import *

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from theme import apply_theme, render_botanical_footer

st.set_page_config(page_title="Dual-Driver Impact", page_icon="◈", layout="wide")
apply_theme()

st.title("Dual-Driver Analysis: IKN × Mining")
st.markdown("Mengukur asosiasi spasial antara kedekatan IKN dan kepadatan tambang terhadap probabilitas perubahan tutupan lahan.")

DASH_DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

@st.cache_data
def load_driver_data(analysis_type):
    path = os.path.join(DASH_DATA, f'driver_{analysis_type}.csv')
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

tab1, tab2, tab3 = st.tabs(["Deforestasi", "Urbanisasi", "Ekspansi Tambang"])

def plot_coefficients(df, title):
    if df is None:
        st.warning(f"Data {title} tidak tersedia.")
        return

    df_plot = df[df['variable'] != 'intercept'].copy()
    df_plot['significance'] = df_plot['significant'].map({True: 'Signifikan (p<0.05)', False: 'Tidak Signifikan'})

    fig = px.bar(df_plot, x='coefficient', y='variable', orientation='h',
                 color='significance',
                 color_discrete_map={'Signifikan (p<0.05)': DASHBOARD_THEME['accent'], 'Tidak Signifikan': DASHBOARD_THEME['text_secondary']},
                 pattern_shape='significance',
                 pattern_shape_map={'Signifikan (p<0.05)': '', 'Tidak Signifikan': '/'},
                 title=title,
                 template=PLOTLY_TEMPLATE,
                 hover_data=['p_value', 'odds_ratio'])
    fig.update_layout(
        paper_bgcolor=PLOTLY_PAPER_COLOR,
        plot_bgcolor=PLOTLY_PLOT_COLOR,
        font_color=PLOTLY_FONT_COLOR,
        yaxis_title="",
        xaxis_title="Koefisien (Standardized)"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Detail table
    st.dataframe(
        df_plot[['variable', 'coefficient', 'p_value', 'odds_ratio', 'significant']].style.format({
            'coefficient': '{:.4f}',
            'p_value': '{:.4f}',
            'odds_ratio': '{:.4f}'
        }),
        use_container_width=True
    )

with tab1:
    df_def = load_driver_data('deforestation')
    plot_coefficients(df_def, "Pendorong Deforestasi (Forest Loss)")
    st.markdown("""
    <div class="forest-card" style="margin-top: 1rem;">
        <span class="step-badge">TEMUAN TELECOUPLING DEFORESTASI</span>
        <h4 style="margin: 0.2rem 0 0.4rem 0;">Mekanisme Alih Fungsi & Efek Rembesan (Spillover)</h4>
        <div style="font-size: 0.88rem; color: #4B5A50; line-height: 1.6;">
            • <strong>Jarak ke Sentroid IKN (OR = 1,114; p < 0,001):</strong> Berasosiasi positif signifikan. Setiap kenaikan jarak standar meningkatkan peluang deforestasi sebesar 11,4%. Hal ini membuktikan bekerjanya <em>spatial telecoupling</em>: penjagaan super ketat di zona inti KIPP IKN berhasil mencegah deforestasi langsung di pusat pemerintahan, namun mendesak aktivitas pembukaan lahan ke koridor penyangga luar (radius 10–50 km).<br>
            • <strong>Kepadatan Tambang 10 km (OR = 1,093; p < 0,001):</strong> Menjadi akselerator degradasi lahan. Area di sekitar konsesi tambang batubara aktif mengalami risiko deforestasi 9,3% lebih tinggi.<br>
            • <strong>Faktor Mitigasi Alami:</strong> Elevasi topografi tinggi (OR = 0,462) dan curah hujan tahunan (OR = 0,906) bertindak sebagai benteng alami yang signifikan menahan laju pembukaan lahan.
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    df_urb = load_driver_data('urbanization')
    plot_coefficients(df_urb, "Pendorong Urbanisasi (Non-Built → Built)")
    st.markdown("""
    <div class="forest-card" style="margin-top: 1rem;">
        <span class="step-badge">TEMUAN URBANISASI</span>
        <h4 style="margin: 0.2rem 0 0.4rem 0;">Dinamika Pertumbuhan Area Terbangun</h4>
        <div style="font-size: 0.88rem; color: #4B5A50; line-height: 1.6;">
            • <strong>Jarak ke IKN (p = 0,087; Tidak Signifikan):</strong> Pembangunan IKN belum memberikan efek limpahan urbanisasi masif pada kota-kota penyangga di luar radius proyek dalam kurun waktu 2019–2024.<br>
            • <strong>Kepadatan Tambang (OR = 1,268; p < 0,001):</strong> Menjadi pendorong utama urbanisasi di Kalimantan. Wilayah lingkar tambang secara aktif menarik pembangunan perumahan pekerja, permukiman spontan, dan fasilitas logistik pendukung.
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    df_min = load_driver_data('mining')
    plot_coefficients(df_min, "Pendorong Ekspansi Tambang (Non-Bare → Bare)")
    st.markdown("""
    <div class="forest-card" style="margin-top: 1rem;">
        <span class="step-badge">TEMUAN EKSPANSI TAMBANG</span>
        <h4 style="margin: 0.2rem 0 0.4rem 0;">Aglomerasi Pertambangan Batubara</h4>
        <div style="font-size: 0.88rem; color: #4B5A50; line-height: 1.6;">
            • <strong>Kepadatan Tambang Historis (OR = 1,302; p < 0,001):</strong> Memiliki efek multiplikasi terkuat. Konsesi tambang yang telah ada memicu pembukaan lubang tambang baru (open pit) dan jalan angkut batubara di sekitarnya (+30,2% peluang ekspansi per unit standar deviasi).
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div style="background: #F6F8F4; border: 1px solid #DCE4D8; border-radius: 10px; padding: 1rem 1.2rem;">
    <div style="font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; font-weight: 700; color: #1E482D; text-transform: uppercase; margin-bottom: 0.3rem;">
        CATATAN INTEGRITAS STATISTIK (BRIDGE DATASET)
    </div>
    <div style="font-size: 0.82rem; color: #4B5A50; line-height: 1.55;">
        1. <strong>Mitigasi Pseudo-Replication:</strong> Model regresi logistik dievaluasi pada <strong>Bridge Dataset (122.478 titik sampel spasial independen)</strong> berjarak ~10 km, bukan pada 1,5 juta sel bertetangga, demi memenuhi asumsi independensi observasi dan mencegah inflasi derajat bebas semu.<br>
        2. <strong>Ground-Truth Tambang Independen:</strong> Variabel kepadatan tambang dihitung menggunakan dataset terverifikasi internasional (Maus et al., 2022) dan Minerba ESDM, mengeliminasi risiko circular reasoning.
    </div>
</div>
""", unsafe_allow_html=True)

# Botanical Footer
render_botanical_footer()
