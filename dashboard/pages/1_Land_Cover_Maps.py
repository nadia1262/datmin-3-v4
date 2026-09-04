# dashboard/pages/1_Land_Cover_Maps.py
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from configs.constants import *
from configs.color_palette import *

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from theme import apply_theme

st.set_page_config(page_title="Land Cover Maps", page_icon="◈", layout="wide")
apply_theme()

st.title("Multi-temporal Land Cover Maps")
st.markdown("Visualisasi klasifikasi tutupan lahan di Kalimantan untuk periode 2018–2024.")

year = st.slider("Pilih Tahun:", min_value=2018, max_value=2024, value=2024)

# Grid size info
GRID_SIZES = {2018: 13632, 2019: 175384, 2020: 176624, 2021: 162940, 2022: 160261, 2023: 159949, 2024: 154137}

if year == 2018:
    st.warning("**Catatan:** Grid 2018 hanya memiliki 13.632 titik (vs ~155.000+ tahun lain) karena keterbatasan citra Sentinel-2 cloud-free. Proporsi tidak directly comparable.")

@st.cache_data
def load_map_data(y):
    for prefix in [f'predictions_lgbm_{y}', f'predictions_rf_{y}', f'predictions_{y}']:
        file_path = os.path.join(PREDICTIONS_DIR, f'{prefix}.csv')
        if os.path.exists(file_path):
            break
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        if len(df) > 8000:
            df = df.sample(8000, random_state=42)
        return df
    else:
        return None

df = load_map_data(year)

if df is None:
    st.error("Data prediksi tidak ditemukan untuk tahun ini.")
    st.stop()

# Convert class to RGBA colors for pydeck
CLASS_COLORS_RGB = {
    0: [34, 139, 34],    # Forest — vibrant green
    1: [204, 255, 102],  # Shrubland/Agriculture — bright lime green
    2: [255, 51, 51],    # Built-up — bright red
    3: [255, 204, 102],  # Bare/Mining-like — bright tan/gold
    4: [51, 153, 255],   # Water — bright blue
}

df['color'] = df['predicted_class'].map(CLASS_COLORS_RGB)

col1, col2 = st.columns([3, 1])

with col1:
    geojson_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/external/kalimantan_boundary.geojson')
    
    layers = []
    
    # Border layer
    if os.path.exists(geojson_path):
        border_layer = pdk.Layer(
            "GeoJsonLayer",
            data=geojson_path,
            opacity=0.8,
            stroked=True,
            filled=False,
            extruded=False,
            get_line_color=[255, 255, 255, 150], # White outline
            get_line_width=3000,
        )
        layers.append(border_layer)

    # Scatter layer
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[lon, lat]',
        get_color='color',
        get_radius=2200,  # Lebar agar solid
        pickable=True,
        opacity=0.9,      # Sedikit transparan agar tumpukan terlihat
        stroked=False,
        filled=True,
    )
    layers.append(scatter_layer)

    # IKN marker
    ikn_layer = pdk.Layer(
        "ScatterplotLayer",
        data=pd.DataFrame([{'lon': IKN_CENTER['lon'], 'lat': IKN_CENTER['lat']}]),
        get_position='[lon, lat]',
        get_color='[255, 0, 0, 255]', # Solid red
        get_radius=8000,
        pickable=True,
    )
    layers.append(ikn_layer)

    view_state = pdk.ViewState(
        latitude=IKN_CENTER['lat'],
        longitude=IKN_CENTER['lon'] - 1.5,
        zoom=5.2,
        pitch=0,
    )

    deck = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/dark-v11',  # Dark mode map agar warna titik pop-up dan tegas
        tooltip={"text": "Koordinat: {lon}, {lat}\nKelas: {predicted_label}"},
    )

    st.pydeck_chart(deck)

with col2:
    st.subheader(f"Statistik {year}")
    st.caption(f"Total grid: {GRID_SIZES.get(year, 'N/A'):,} titik")
    
    counts = df['predicted_class'].value_counts().sort_index()
    
    for cls in range(N_CLASSES):
        count = counts.get(cls, 0)
        pct = (count / len(df)) * 100
        st.markdown(f"<span style='color:{CLASS_COLORS[cls]}; font-size:1.2rem;'>■</span>&ensp;**{CLASS_NAMES[cls]}**: {pct:.1f}%", unsafe_allow_html=True)

    st.markdown("---")

    # Legend
    st.markdown("**Legenda**")
    for cls in range(N_CLASSES):
        st.markdown(f"<span style='display:inline-block; width:12px; height:12px; background:{CLASS_COLORS[cls]}; border-radius:2px; margin-right:6px;'></span> {CLASS_NAMES[cls]}", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Titik merah besar menandakan lokasi IKN Nusantara.")
    st.caption("Peta dirender dari systematic sample grid. Data resolusi penuh dikomputasi di GEE.")
