# dashboard/pages/2_Change_Detection.py
import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from configs.constants import *
from configs.color_palette import *

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from theme import apply_theme

st.set_page_config(page_title="Change Detection", page_icon="◈", layout="wide")
apply_theme()

st.title("Change Detection (2018 → 2024)")
st.markdown("Analisis transisi tutupan lahan dan deteksi perubahan temporal.")

# Load Transition Matrix
@st.cache_data
def load_transition_matrix():
    path = os.path.join(CHANGE_DIR, 'transition_matrix_2018_2024.csv')
    if os.path.exists(path):
        cm = pd.read_csv(path, index_col=0)
        # Remove margins if present
        cm = cm.drop('All', axis=0, errors='ignore').drop('All', axis=1, errors='ignore')
        return cm
    return None

# Load Change Summary
@st.cache_data
def load_change_summary():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'change_summary.json')
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None

cm = load_transition_matrix()
summary = load_change_summary()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Transition Matrix (2018 → 2024)")
    if cm is not None:
        fig = px.imshow(cm,
                        labels=dict(x="Kelas 2024", y="Kelas 2018", color="Titik"),
                        color_continuous_scale="YlOrRd",
                        template=PLOTLY_TEMPLATE)
        fig.update_layout(
            paper_bgcolor=PLOTLY_PAPER_COLOR,
            plot_bgcolor=PLOTLY_PLOT_COLOR,
            font_color=PLOTLY_FONT_COLOR
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("File transition matrix tidak ditemukan. Jalankan `python scripts/change_detection.py --model lgbm --full-temporal` terlebih dahulu.")

with col2:
    st.subheader("Ringkasan Perubahan")

    if summary:
        total = summary.get('total_points', 0)
        changed = summary.get('changed_points', 0)
        change_pct = summary.get('change_rate_pct', 0)
        forest_loss = summary.get('forest_loss', 0)
        forest_gain = summary.get('forest_gain', 0)
        urbanization = summary.get('urbanization', 0)
        mining_exp = summary.get('mining_expansion', 0)

        st.metric("Total Matched Points", f"{total:,}")
        st.metric("Titik Berubah", f"{changed:,} ({change_pct}%)")

        m1, m2 = st.columns(2)
        with m1:
            st.metric("Forest Loss", f"{forest_loss:,} titik")
            st.metric("Urbanisasi", f"{urbanization:,} titik")
        with m2:
            st.metric("Forest Gain", f"{forest_gain:,} titik")
            st.metric("Mining Expansion", f"{mining_exp:,} titik")
    else:
        st.warning("File change_summary.json tidak ditemukan.")

    st.markdown("### Interpretasi")
    st.markdown("- **Forest → Shrubland** (791 titik) adalah transisi terbesar — menunjukkan degradasi bertahap.")
    st.markdown("- **Shrubland → Built-up** (93 titik) lebih banyak dari Forest → Built-up (56) — pola urbanisasi bertahap.")
    st.markdown("- Forest gain (889) sedikit lebih banyak dari forest loss (858) — perlu analisis lebih lanjut apakah ini revegetasi nyata atau artefak resolusi.")

# Temporal Trends
st.markdown("---")
st.subheader("Tren Komposisi Tutupan Lahan (2018–2024)")

@st.cache_data
def load_temporal():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'temporal_composition.csv')
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

tc = load_temporal()
if tc is not None:
    fig = px.line(tc, x='year', y='proportion', color='class_name',
                  markers=True,
                  labels={'proportion': 'Proporsi (%)', 'year': 'Tahun', 'class_name': 'Kelas'},
                  template=PLOTLY_TEMPLATE)
    fig.update_layout(
        paper_bgcolor=PLOTLY_PAPER_COLOR,
        plot_bgcolor=PLOTLY_PLOT_COLOR,
        font_color=PLOTLY_FONT_COLOR
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Data 2018 memiliki grid yang jauh lebih kecil (13K vs 155K+ titik), sehingga proporsinya tidak directly comparable.")
