# dashboard/pages/5_Spatiotemporal_Heatmap.py
import streamlit as st
import pandas as pd
import pydeck as pdk
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from configs.constants import *
from configs.color_palette import *

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from theme import apply_theme, render_botanical_footer

st.set_page_config(page_title="Spatiotemporal Heatmap", layout="wide")
apply_theme()

st.markdown("""
<div style="margin-bottom: 1.2rem;">
    <span class="step-badge">MODUL 05</span>
    <h2 style="font-family: 'Plus Jakarta Sans', sans-serif; font-weight: 800; color: #16281C; margin-top: 0.4rem; margin-bottom: 0.2rem;">
        3D Spatiotemporal Heatmap (2019–2024)
    </h2>
    <p style="color: #4B5A50; font-size: 0.95rem; margin-bottom: 0;">
        Visualisasi heksagonal 3D interaktif yang mengagregasikan densitas spasial pergeseran tutupan lahan: <b>Deforestasi Riil</b>, <b>Urbanisasi</b>, dan <b>Ekspansi Tambang</b>.
    </p>
</div>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_change_data():
    cache_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/cache/change_points_active.parquet')
    if os.path.exists(cache_path):
        return pd.read_parquet(cache_path)
    path = os.path.join(CHANGE_DIR_V2, 'change_points_2019_2024.csv')
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Compute indicator columns dynamically
        df['is_changed'] = (df['predicted_label_2019'] != df['predicted_label_2024']).astype(int)
        df['forest_loss'] = ((df['predicted_label_2019'] == 'Forest') & (df['predicted_label_2024'] != 'Forest')).astype(int)
        df['urbanization'] = ((df['predicted_label_2019'] != 'Built-up') & (df['predicted_label_2024'] == 'Built-up')).astype(int)
        df['mining_expansion'] = ((df['predicted_label_2019'] != 'Bare/Mining-like') & (df['predicted_label_2024'] == 'Bare/Mining-like')).astype(int)
        return df
    return None

df = load_change_data()

if df is not None:
    # Filter only changed points
    df_changed = df[df['is_changed'] == 1].copy()

    col_ctrl, col_map = st.columns([1, 3])
    
    with col_ctrl:
        st.markdown('<div class="forest-card">', unsafe_allow_html=True)
        st.markdown("<h4 style='color: #1E482D; margin-top: 0;'>Parameter Visualisasi</h4>", unsafe_allow_html=True)
        
        metric_choice = st.radio(
            "Pilih Metrik Perubahan Spasial:",
            ("Forest Loss (Deforestasi)", "Urbanisasi (Built-up)", "Ekspansi Tambang / Terbuka")
        )
        
        radius = st.slider("Radius Heksagon (meter)", min_value=2000, max_value=25000, value=7000, step=1000)
        elevation = st.slider("Skala Elevasi 3D", min_value=20, max_value=500, value=180, step=20)

        # Mapping choice to column and botanical color ramp
        if metric_choice.startswith("Forest Loss"):
            filter_col = "forest_loss"
            metric_title = "Deforestasi"
            color_range = [
                [254, 224, 210],
                [252, 187, 161],
                [252, 146, 114],
                [251, 106, 74],
                [222, 45, 38],
                [165, 15, 21]
            ]
        elif metric_choice.startswith("Urbanisasi"):
            filter_col = "urbanization"
            metric_title = "Urbanisasi"
            color_range = [
                [239, 243, 255],
                [198, 219, 239],
                [158, 202, 225],
                [107, 174, 214],
                [49, 130, 189],
                [8, 81, 156]
            ]
        else:
            filter_col = "mining_expansion"
            metric_title = "Ekspansi Tambang"
            color_range = [
                [254, 237, 222],
                [253, 208, 162],
                [253, 174, 107],
                [253, 141, 60],
                [230, 85, 13],
                [166, 54, 3]
            ]

        # Filter the active points
        df_plot = df_changed[df_changed[filter_col] == 1][['lon', 'lat']].copy()
        
        st.markdown(f"""
        <div style="background: #F6F8F4; border: 1px solid #DCE4D8; border-radius: 8px; padding: 0.75rem; margin-top: 1rem;">
            <div style="font-size: 0.75rem; color: #5A6E5F; text-transform: uppercase; font-weight: 700;">Titik Sampel Terdeteksi</div>
            <div style="font-size: 1.6rem; font-weight: 800; color: #1E482D; font-family: 'IBM Plex Mono', monospace;">
                {len(df_plot):,} <span style="font-size: 0.85rem; font-weight: 500; color: #5A6E5F;">titik</span>
            </div>
            <div style="font-size: 0.78rem; color: #5A6E5F; margin-top: 0.2rem;">
                Proporsi: <b>{(len(df_plot) / len(df) * 100):.2f}%</b> dari {len(df):,} total observasi bridge dataset.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="font-size: 0.8rem; color: #5A6E5F; margin-top: 1.2rem; line-height: 1.5;">
            <b>Kontrol Navigasi 3D:</b><br/>
            • <b>Pan:</b> Tahan Klik Kiri + Geser<br/>
            • <b>Tilt 3D:</b> Tahan Klik Kanan + Geser (atau Ctrl + Drag)<br/>
            • <b>Zoom:</b> Scroll Mouse
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_map:
        if len(df_plot) > 0:
            # PyDeck Layer
            layer = pdk.Layer(
                "HexagonLayer",
                data=df_plot,
                get_position="[lon, lat]",
                radius=radius,
                elevation_scale=elevation,
                elevation_range=[0, 3500],
                pickable=True,
                extruded=True,
                color_range=color_range,
                coverage=0.92
            )
            
            # Viewport Kalimantan
            view_state = pdk.ViewState(
                longitude=115.0,
                latitude=-0.5,
                zoom=5.6,
                min_zoom=4,
                max_zoom=12,
                pitch=42,
                bearing=-8
            )
            
            # Render with light clean map style that fits botanical canvas
            r = pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip={"text": f"Kerapatan {metric_title}: {{elevationValue}} titik"},
                map_style="light"
            )
            
            st.pydeck_chart(r, use_container_width=True, height=620)
        else:
            st.warning("Tidak ada titik perubahan yang terdeteksi untuk metrik ini.")

    st.markdown("""
    <div class="forest-card" style="margin-top: 0.8rem;">
        <div class="card-title">Interpretasi Agregasi Spasial 3D</div>
        <p class="card-desc">
            Elevasi kolom heksagonal merepresentasikan konsentrasi titik pergeseran tutupan lahan dalam radius tertentu.
            Pola kolom tertinggi pada <b>Forest Loss</b> terkonsentrasi di koridor perbatasan Kalimantan Timur dan Kalimantan Tengah sepanjang jalur logistik dan konsesi perkebunan/HPH,
            sedangkan <b>Ekspansi Tambang</b> membentuk gugus terisolasi namun tajam di lingkar luar IKN (Kutai Kartanegara dan Paser).
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("Data transisi (change_points_2019_2024.csv) tidak ditemukan. Pastikan pipeline deteksi perubahan sudah dijalankan.")

render_botanical_footer()
