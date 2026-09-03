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
from theme import apply_theme

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
                 color_discrete_map={'Signifikan (p<0.05)': '#00E676', 'Tidak Signifikan': '#6C757D'},
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
    **Interpretasi:**
    - `distance_to_ikn` negatif & signifikan (p=0.0015): Semakin **dekat** ke IKN → risiko deforestasi **lebih tinggi**.
    - `mining_density_10km` positif & signifikan (p=0.0006): Area padat tambang → risiko deforestasi **lebih tinggi**.
    - Pseudo R² = 0.0056 → variabel ini menjelaskan asosiasi spasial, bukan kausalitas penuh.
    """)

with tab2:
    df_urb = load_driver_data('urbanization')
    plot_coefficients(df_urb, "Pendorong Urbanisasi (Non-Built → Built)")
    st.markdown("""
    **Interpretasi:**
    - `distance_to_ikn` **TIDAK signifikan** (p=0.272): Efek urbanisasi IKN belum terukur dalam periode 2018–2024.
    - `mining_density_10km` signifikan (p=0.033): Urbanisasi lebih terkait aktivitas tambang.
    - Temuan ini menunjukkan konstruksi IKN masih terlokalisir, belum terjadi *sprawl effect*.
    """)

with tab3:
    df_min = load_driver_data('mining')
    plot_coefficients(df_min, "Pendorong Ekspansi Tambang (Non-Bare → Bare)")
    st.markdown("""
    **Interpretasi:**
    - `distance_to_ikn` **positif** & signifikan (p=0.038): Ekspansi tambang terjadi **jauh dari** IKN.
    - `mining_density_10km` signifikan (p<0.001): Tambang cenderung berkluster (spatial clustering).
    """)
    st.warning("**Catatan:** Hanya 26 kasus positif dari 9.624 observasi. Temuan ini bersifat eksploratif dan tidak memenuhi minimum sample untuk regresi logistik yang robust (rule of thumb: 10 events per predictor × 4 variabel = 40).")

st.markdown("---")
st.info("**Catatan Metodologis:** Analisis ini menggunakan regresi logistik dengan variabel yang di-standardize. Odds Ratio <1 berarti penurunan peluang, >1 berarti peningkatan peluang, per 1 standar deviasi perubahan variabel.")

# Driver effects plot
st.subheader("Visualisasi: Deforestation Rate vs Drivers")
driver_img = os.path.join(DRIVER_DIR, 'driver_effects.png')
if os.path.exists(driver_img):
    st.image(driver_img, use_container_width=True)
else:
    st.caption("Plot driver effects belum tersedia.")
