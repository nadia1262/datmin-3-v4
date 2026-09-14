# dashboard/pages/1_Land_Cover_Maps.py
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import json
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
GRID_SIZES = {
    2018: 13632, 
    2019: 1794435, 
    2020: 176624, 
    2021: 162940, 
    2022: 160261, 
    2023: 159949, 
    2024: 1530847
}

if year == 2018:
    st.warning("**Catatan:** Grid 2018 hanya memiliki 13.632 titik (vs ~155.000+ tahun lain) karena keterbatasan citra Sentinel-2 cloud-free. Proporsi tidak directly comparable.")

@st.cache_data
def load_map_data(y):
    # Coba dataset Majority Voting terbaru dulu, lalu fallback ke Centroid lama
    prefixes = [f'majority_voting_{y}', f'predictions_lgbm_{y}', f'predictions_{y}']
    file_path = None
    data_source_type = "Unknown"
    
    for prefix in prefixes:
        test_path = os.path.join(PREDICTIONS_DIR, f'{prefix}.csv')
        if os.path.exists(test_path):
            file_path = test_path
            data_source_type = "Majority Voting (500m)" if 'majority' in prefix else "Centroid (10km)"
            break
            
    if file_path:
        df_full = pd.read_csv(file_path)
        
        # Standardize column names if it's the majority voting dataset
        if 'majority_class' in df_full.columns:
            df_full = df_full.rename(columns={'majority_class': 'predicted_class', 'majority_label': 'predicted_label'})
            
        # Smart Sampling for Map Rendering (Max ~75k points for smooth browser rendering)
        # We want to preserve minority classes (mining, water, urban) which might disappear in random sampling
        if len(df_full) > 75000:
            df_map = df_full.groupby('predicted_class', group_keys=False).apply(
                lambda x: x.sample(min(len(x), 15000), random_state=42)
            )
        else:
            df_map = df_full.copy()
            
        return df_full, df_map, data_source_type
    else:
        return None, None, None

df_full, df_map, data_source_type = load_map_data(year)

if df_full is None:
    st.error("Data prediksi tidak ditemukan untuk tahun ini.")
    st.stop()

# Derive pydeck's RGB colors from the shared design-system palette
# (configs/color_palette.py) instead of a hand-duplicated dict, so the
# map and this page's own legend never drift apart.
CLASS_COLORS_RGB = {cls: list(rgba[:3]) for cls, rgba in CLASS_COLORS_RGBA.items()}

df_map['color'] = df_map['predicted_class'].map(CLASS_COLORS_RGB)

if data_source_type == "Majority Voting (500m)":
    st.info(f"📍 **Sumber Data:** Resolusi Tinggi {data_source_type} (Konsensus 25 Titik Sub-grid). Radius rendering disesuaikan.")
    render_radius = 1800
else:
    st.info(f"📍 **Sumber Data:** Resolusi Standar {data_source_type} (1 Titik per Sel). Radius rendering disesuaikan.")
    render_radius = 2500

col1, col2 = st.columns([3, 1])

with col1:
    geojson_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/external/kalimantan_boundary.geojson')
    
    layers = []

    # Border layer
    if os.path.exists(geojson_path):
        with open(geojson_path, encoding='utf-8') as f:
            boundary_geojson = json.load(f)
        border_layer = pdk.Layer(
            "GeoJsonLayer",
            data=boundary_geojson,
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
        data=df_map[['lon', 'lat', 'color', 'predicted_label']], # Only load required columns to frontend
        get_position='[lon, lat]',
        get_color='color',
        get_radius=render_radius,  # Radius dinamis bergantung tipe data
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
        map_provider="carto",
        map_style="dark",  # Carto's tokenless dark basemap — no Mapbox account needed
        tooltip={"text": "Koordinat: {lon}, {lat}\nKelas: {predicted_label}"},
    )

    st.pydeck_chart(deck)

with col2:
    st.subheader(f"Statistik {year}")
    st.caption(f"Total grid: {len(df_full):,} titik") # Gunakan panjang df_full asli
    
    counts = df_full['predicted_class'].value_counts().sort_index()
    
    for cls in range(N_CLASSES):
        count = counts.get(cls, 0)
        pct = (count / len(df_full)) * 100
        st.markdown(f"<span style='color:{CLASS_COLORS[cls]}; font-size:1.2rem;'>■</span>&ensp;**{CLASS_NAMES[cls]}**: {pct:.1f}%", unsafe_allow_html=True)

    st.markdown("---")

    # Legend
    st.markdown("**Legenda**")
    for cls in range(N_CLASSES):
        st.markdown(f"<span style='display:inline-block; width:12px; height:12px; background:{CLASS_COLORS[cls]}; border:1px solid {DASHBOARD_THEME['text_primary']}; border-radius:3px; margin-right:6px;'></span> {CLASS_NAMES[cls]}", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Titik merah besar menandakan lokasi IKN Nusantara.")
    st.caption("Peta divisualisasikan menggunakan **Stratified Smart Sampling** (hingga 60.000 titik) untuk menjaga porsi visibilitas kelas minoritas tanpa merusak performa *browser*. Statistik persentase dihitung akurat dari 100% populasi piksel grid.")
