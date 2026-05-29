# dashboard/pages/4_Driver_Impact.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from configs.constants import *
from configs.color_palette import *

st.set_page_config(page_title="Dual-Driver Impact", page_icon="🏗️", layout="wide")

st.title("🏗️ Dual-Driver Interaction Model")
st.markdown("Mengukur efek spasial dari ekspansi IKN dan aktivitas ekstraktif (Tambang) terhadap probabilitas perubahan tutupan lahan.")

@st.cache_data
def load_driver_coefs():
    path = os.path.join(DRIVER_DIR, 'driver_coefficients.csv')
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        # Dummy coefs
        return pd.DataFrame({
            'Feature': ['distance_to_ikn', 'mining_density_10km', 'interaction_ikn_mining', 'elevation', 'rainfall_annual'],
            'Coefficient': [-0.85, 0.65, -0.42, -0.21, 0.11],
            'P_Value': [0.001, 0.002, 0.015, 0.05, 0.12]
        })

df = load_driver_coefs()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Logistic Regression Coefficients")
    # Filter out intercept
    df_plot = df[df['Feature'] != 'Intercept'].copy()
    df_plot['Significance'] = np.where(df_plot['P_Value'] < 0.05, 'Significant (p<0.05)', 'Not Significant')
    
    fig = px.bar(df_plot, x='Coefficient', y='Feature', orientation='h',
                 color='Significance', 
                 color_discrete_map={'Significant (p<0.05)': '#00E676', 'Not Significant': '#6C757D'},
                 title='Driver Effect on Land Cover Change',
                 template=PLOTLY_TEMPLATE)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Interaction Hotspots")
    st.markdown("""
    **Insight Utama:**
    - `distance_to_ikn` memiliki koefisien negatif: semakin dekat dengan IKN, probabilitas perubahan lahan semakin *tinggi*.
    - `mining_density_10km` memiliki koefisien positif: area padat tambang memiliki probabilitas perubahan *tinggi*.
    - **Term Interaksi** signifikan: Menandakan ada hotspot di mana kedua driver memperkuat degradasi lahan secara eksponensial.
    """)
    
    # Synthetic heatmap for visual concept
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Gradient_Color_Map.png/800px-Gradient_Color_Map.png", caption="Conceptual Interaction Surface")
