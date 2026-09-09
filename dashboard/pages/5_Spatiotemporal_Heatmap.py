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
from theme import apply_theme

st.set_page_config(page_title="Spatiotemporal Heatmap", page_icon="◈", layout="wide")
apply_theme()

st.title("3D Spatiotemporal Heatmap (2019-2024)")
st.markdown("Visualisasi 3D beresolusi tinggi dari area yang mengalami **Deforestasi**, **Urbanisasi**, dan **Ekspansi Tambang**.")

@st.cache_data
def load_data():
    path = os.path.join(CHANGE_DIR_V2, 'change_points_2019_2024.csv')
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

df = load_data()

if df is not None:
    # Filter only changed points to save memory
    df_changed = df[df['is_changed'] == 1].copy()

    col1, col2 = st.columns([1, 3])
    with col1:
        st.subheader("Filter Peta")
        metric_choice = st.radio(
            "Pilih Metrik Perubahan:",
            ("Forest Loss (Deforestasi)", "Urbanisasi", "Ekspansi Tambang")
        )
        
        radius = st.slider("Radius Heksagon (meter)", min_value=1000, max_value=20000, value=5000, step=1000)
        elevation = st.slider("Skala Ketinggian 3D", min_value=10, max_value=500, value=150, step=10)

        # Mapping choice to column and color
        if metric_choice == "Forest Loss (Deforestasi)":
            filter_col = "forest_loss"
            # Red/Orange heatmap for forest loss
            color_range = [
                [255, 255, 178],
                [254, 204, 92],
                [253, 141, 60],
                [240, 59, 32],
                [189, 0, 38],
                [128, 0, 38]
            ]
        elif metric_choice == "Urbanisasi":
            filter_col = "urbanization"
            # Purple/Blue for urbanization
            color_range = [
                [224, 236, 244],
                [191, 211, 230],
                [158, 188, 218],
                [140, 150, 198],
                [136, 86, 167],
                [129, 15, 124]
            ]
        else:
            filter_col = "mining_expansion"
            # Red/Pink color for mining
            color_range = [
                [254, 235, 226],
                [252, 197, 192],
                [250, 159, 181],
                [247, 104, 161],
                [197, 27, 138],
                [122, 1, 119]
            ]

        # Filter the active points
        df_plot = df_changed[df_changed[filter_col] == 1][['lon', 'lat']]
        
        st.metric("Total Titik Terdeteksi", f"{len(df_plot):,}")
        st.caption("**Navigasi 3D:**")
        st.caption("- Geser (Pan): Tahan Klik Kiri + Geser")
        st.caption("- Miringkan (Tilt): Tahan Klik Kanan + Geser (atau Ctrl/Cmd + Drag)")
        st.caption("- Perbesar (Zoom): Scroll Mouse")

    with col2:
        if len(df_plot) > 0:
            # PyDeck Layer
            layer = pdk.Layer(
                "HexagonLayer",
                data=df_plot,
                get_position="[lon, lat]",
                radius=radius,
                elevation_scale=elevation,
                elevation_range=[0, 3000],
                pickable=True,
                extruded=True,
                color_range=color_range,
                coverage=1
            )
            
            # Set viewport to Kalimantan
            view_state = pdk.ViewState(
                longitude=114.5,
                latitude=0.5,
                zoom=5.5,
                min_zoom=4,
                max_zoom=12,
                pitch=45,
                bearing=-10
            )
            
            # Render
            r = pdk.Deck(
                layers=[layer],
                initial_view_state=view_state,
                tooltip={"text": "Jumlah Titik: {elevationValue}"},
                map_style=pdk.map_styles.DARK
            )
            
            st.pydeck_chart(r, use_container_width=True, height=600)
        else:
            st.warning("Tidak ada titik perubahan yang terdeteksi untuk metrik ini.")

else:
    st.error("Data transisi (change_points_2019_2024.csv) tidak ditemukan. Pastikan pipeline deteksi perubahan sudah dijalankan.")
