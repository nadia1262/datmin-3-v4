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
from theme import apply_theme, render_botanical_footer

st.set_page_config(page_title="Land Cover Maps", page_icon="◈", layout="wide")
apply_theme()

st.title("Peta Spasiotemporal Tutupan Lahan")
st.markdown("Visualisasi klasifikasi tutupan lahan Pulau Kalimantan membandingkan kondisi rona awal (2019) dan fase puncak konstruksi fisik (2024).")

# Slider Pemilih Tahun Interaktif (2019 - 2024)
col_yr1, col_yr2 = st.columns([3, 2])
with col_yr1:
    year = st.slider(
        "Pilih Tahun Pengamatan Tutupan Lahan (Geser untuk Membandingkan):",
        min_value=2019,
        max_value=2024,
        value=2024,
        step=1
    )
    if year == 2024:
        period_desc = "Puncak Konstruksi Fisik IKN (1.530.847 sel)"
    elif year == 2019:
        period_desc = "Rona Awal Pra-IKN (1.794.435 sel)"
    else:
        period_desc = f"Fase Transisi Tahunan ({year})"
    st.markdown(f"<span style='font-size: 0.82rem; color: #2D6A4F; font-weight: 600;'>Fokus Analisis: {period_desc}</span>", unsafe_allow_html=True)

with col_yr2:
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #DCE4D8; border-radius: 10px; padding: 0.6rem 1rem; margin-top: 0.5rem;">
        <span style="font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; font-weight: 700; color: #1E482D; letter-spacing: 0.05em;">METODE AGREGASI:</span>
        <span style="font-size: 0.82rem; color: #4B5A50; margin-left: 0.4rem;">Majority Voting Sub-Grid 500m (Konsensus 25 Titik Sampel Interval 100m)</span>
    </div>
    """, unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_map_data(y):
    # Cek fast precomputed cache terlebih dahulu untuk ultra-fast load (< 15ms)
    cache_parquet = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'../data/cache/map_points_{y}.parquet')
    cache_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/cache/class_distribution.json')
    
    if os.path.exists(cache_parquet) and os.path.exists(cache_json):
        df_map = pd.read_parquet(cache_parquet)
        with open(cache_json, 'r') as f:
            all_stats = json.load(f)
        y_stats = all_stats.get(str(y), {})
        source_type = y_stats.get('source_type', 'Majority Voting (500m)')
        return None, df_map, source_type, y_stats

    # Fallback ke dataset CSV asli jika cache belum dibangun
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
        cols_to_check = ['lon', 'lat', 'predicted_class', 'predicted_label', 'majority_class', 'majority_label']
        df_sample = pd.read_csv(file_path, nrows=5)
        use_cols = [c for c in cols_to_check if c in df_sample.columns]
        
        df_full = pd.read_csv(file_path, usecols=use_cols)
        
        if 'majority_class' in df_full.columns:
            df_full = df_full.rename(columns={'majority_class': 'predicted_class', 'majority_label': 'predicted_label'})
            
        if len(df_full) > 50000:
            df_map = df_full.groupby('predicted_class', group_keys=False).apply(
                lambda x: x.sample(min(len(x), 10000), random_state=42)
            )
        else:
            df_map = df_full.copy()
            
        counts = df_full['predicted_label'].value_counts().to_dict()
        y_stats = {
            'total': len(df_full),
            'counts': counts,
            'percentages': {k: (v / len(df_full)) * 100 for k, v in counts.items()}
        }
            
        return df_full, df_map, data_source_type, y_stats
    else:
        return None, None, None, None

df_full, df_map, data_source_type, y_stats = load_map_data(year)
if df_map is None:
    st.error("Data prediksi tidak ditemukan untuk tahun ini.")
    st.stop()

# Derive pydeck's RGB colors
CLASS_COLORS_RGB = {cls: list(rgba[:3]) for cls, rgba in CLASS_COLORS_RGBA.items()}
df_map['color'] = df_map['predicted_class'].map(CLASS_COLORS_RGB)
render_radius = 1900 if data_source_type == "Majority Voting (500m)" else 2600

col1, col2 = st.columns([3, 1])

with col1:
    geojson_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/external/kalimantan_boundary.geojson')
    
    layers = []
    
    if os.path.exists(geojson_path):
        with open(geojson_path, 'r') as f:
            boundary_data = json.load(f)
            
        boundary_layer = pdk.Layer(
            "GeoJsonLayer",
            data=boundary_data,
            stroked=True,
            filled=False,
            get_line_color=[100, 116, 139, 200],
            get_line_width=2500,
            pickable=False,
        )
        layers.append(boundary_layer)

    # Scatter points layer (using stratified sampled points for smooth 60fps rendering)
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_map[['lon', 'lat', 'color', 'predicted_label']],
        get_position='[lon, lat]',
        get_color='color',
        get_radius=render_radius,
        pickable=True,
        opacity=0.9,
        stroked=False,
        filled=True,
    )
    layers.append(scatter_layer)

    # IKN marker
    ikn_layer = pdk.Layer(
        "ScatterplotLayer",
        data=pd.DataFrame([{'lon': IKN_CENTER['lon'], 'lat': IKN_CENTER['lat']}]),
        get_position='[lon, lat]',
        get_color='[255, 0, 0, 255]',
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
        map_style="dark",
        tooltip={"text": "Koordinat: {lon}, {lat}\nKelas: {predicted_label}"},
    )

    st.pydeck_chart(deck, use_container_width=True)

with col2:
    total_pop = y_stats.get('total', len(df_full) if df_full is not None else len(df_map))
    st.markdown(f"""
    <div style="background: #FFFFFF; border: 1px solid {DASHBOARD_THEME['border']}; border-radius: 12px; padding: 1.2rem; box-shadow: 0 2px 8px rgba(22, 40, 28, 0.03);">
        <p style="font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; color: {DASHBOARD_THEME['accent_green']}; margin-bottom: 0.25rem;">PROPORSI KELAS</p>
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.2rem;">Statistik {year}</h3>
        <p style="font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; color: {DASHBOARD_THEME['text_secondary']}; margin-bottom: 1rem;">
            Total Populasi: <strong>{total_pop:,}</strong> sel
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    for cls in range(N_CLASSES):
        cls_name = CLASS_NAMES[cls]
        pct = y_stats.get('percentages', {}).get(cls_name, 0.0)
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; background: #FFFFFF; border: 1px solid {DASHBOARD_THEME['border']}; border-radius: 8px; padding: 0.5rem 0.75rem; margin-bottom: 0.35rem;">
            <div style="display: flex; align-items: center;">
                <span style="display: inline-block; width: 12px; height: 12px; background: {CLASS_COLORS[cls]}; border-radius: 3px; margin-right: 8px;"></span>
                <span style="font-size: 0.85rem; font-weight: 600; color: {DASHBOARD_THEME['text_primary']};">{cls_name}</span>
            </div>
            <span style="font-family: 'IBM Plex Mono', monospace; font-size: 0.82rem; font-weight: 700; color: {DASHBOARD_THEME['text_primary']};">{pct:.1f}%</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top: 1rem; padding: 0.8rem; background: #F6F8F4; border-radius: 8px; border: 1px solid #DCE4D8;">
        <div style="font-size: 0.78rem; color: #4B5A50; line-height: 1.5;">
            • Titik merah beradius besar menandakan sentroid KIPP IKN.<br>
            • Peta dirender via <em>Stratified Spatial Sampling</em> untuk fluiditas browser, statistik dihitung dari 100% data populasi.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Botanical Footer
render_botanical_footer()
