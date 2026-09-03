# dashboard/pages/3_Model_Comparison.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from configs.constants import *
from configs.color_palette import *

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from theme import apply_theme

st.set_page_config(page_title="Model Comparison", page_icon="◈", layout="wide")
apply_theme()

st.title("Algorithmic Comparison")
st.markdown("Evaluasi 6 model Supervised Machine Learning dengan Spatial Block GroupKFold.")

@st.cache_data
def load_metrics():
    path = os.path.join(CLASSIFICATION_DIR, 'model_comparison.csv')
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

df_metrics = load_metrics()

if df_metrics is None:
    st.error("File model_comparison.csv tidak ditemukan.")
    st.stop()

# Show subset warning for SVM/MLP
st.subheader("Performance Metrics Table")
st.caption("SVM dan MLP dievaluasi pada subset 10.000 sampel (bukan 30.000 seperti model lain) karena keterbatasan komputasi.")
st.dataframe(df_metrics.style.highlight_max(subset=['accuracy', 'f1_macro', 'kappa'], color='darkgreen'))

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(df_metrics, x='model', y='accuracy', 
                 color='model', color_discrete_map=MODEL_COLORS,
                 title='Overall Accuracy by Model',
                 template=PLOTLY_TEMPLATE)
    fig.update_layout(yaxis_range=[0.5, 1.0],
                      paper_bgcolor=PLOTLY_PAPER_COLOR,
                      plot_bgcolor=PLOTLY_PLOT_COLOR,
                      font_color=PLOTLY_FONT_COLOR)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(df_metrics, x='model', y='f1_macro', 
                 color='model', color_discrete_map=MODEL_COLORS,
                 title='Macro F1-Score by Model',
                 template=PLOTLY_TEMPLATE)
    fig.update_layout(yaxis_range=[0.5, 1.0],
                      paper_bgcolor=PLOTLY_PAPER_COLOR,
                      plot_bgcolor=PLOTLY_PLOT_COLOR,
                      font_color=PLOTLY_FONT_COLOR)
    st.plotly_chart(fig, use_container_width=True)
    
st.info("**LightGBM** mencapai Overall Accuracy tertinggi (83.32%) dengan waktu training paling efisien (116 detik). SVM memiliki F1-macro sedikit lebih tinggi (0.837) tetapi membutuhkan waktu ~4 jam dan dievaluasi pada subset 10K sampel.")
