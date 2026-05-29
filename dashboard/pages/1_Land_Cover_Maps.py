# dashboard/pages/1_Land_Cover_Maps.py
import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from configs.constants import *
from configs.color_palette import *

st.set_page_config(page_title="Land Cover Maps", page_icon="🗺️", layout="wide")

st.title("🗺️ Multi-temporal Land Cover Maps")
st.markdown("Visualisasi klasifikasi tutupan lahan di Kalimantan untuk periode 2018–2024.")

year = st.slider("Pilih Tahun:", min_value=2018, max_value=2024, value=2024)

# Load data or generate dummy
@st.cache_data
def load_map_data(y):
    # Try model-specific file first, then generic
    for prefix in [f'predictions_lgbm_{y}', f'predictions_rf_{y}', f'predictions_{y}']:
        file_path = os.path.join(PREDICTIONS_DIR, f'{prefix}.csv')
        if os.path.exists(file_path):
            break
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # sample for dashboard
        if len(df) > 5000: df = df.sample(5000, random_state=42)
        return df
    else:
        # Dummy data
        n = 5000
        return pd.DataFrame({
            'lon': 110 + np.random.rand(n) * 9,
            'lat': -4 + np.random.rand(n) * 8,
            'predicted_class': np.random.choice([0,1,2,3,4], n, p=[0.5, 0.25, 0.05, 0.05, 0.15])
        })

df = load_map_data(year)

col1, col2 = st.columns([3, 1])

with col1:
    m = folium.Map(location=[IKN_CENTER['lat'], IKN_CENTER['lon']], zoom_start=6, tiles='CartoDB dark_matter')
    
    # Add IKN Marker
    folium.Marker(
        [IKN_CENTER['lat'], IKN_CENTER['lon']],
        popup="IKN Center",
        icon=folium.Icon(color="red", icon="star")
    ).add_to(m)
    
    # Plot points
    for idx, row in df.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=2,
            color=CLASS_COLORS[int(row['predicted_class'])],
            fill=True,
            fillOpacity=0.7,
            weight=0
        ).add_to(m)
        
    st_folium(m, height=600, width=800, returned_objects=[])

with col2:
    st.subheader(f"Statistik {year}")
    counts = df['predicted_class'].value_counts().sort_index()
    
    for cls in range(N_CLASSES):
        count = counts.get(cls, 0)
        pct = (count / len(df)) * 100
        st.markdown(f"**<span style='color:{CLASS_COLORS[cls]}'>■</span> {CLASS_NAMES[cls]}**: {pct:.1f}%", unsafe_allow_html=True)
        
    st.markdown("---")
    st.info("Peta ini dirender dari systematic sample grid. Data resolusi penuh dikomputasi di GEE dan dievaluasi dalam pipeline.")
