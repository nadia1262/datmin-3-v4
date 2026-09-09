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
    - Kepadatan Tambang (`mining_density_10km`) **positif dan signifikan** (p<0.001), menunjukkan bahwa area yang berdekatan dengan tambang *baseline* 2019 memiliki risiko deforestasi yang konsisten lebih tinggi.
    - Jarak IKN (`distance_to_ikn`) memiliki koefisien positif, yang berarti semakin **jauh** dari IKN, probabilitas deforestasi justru sedikit lebih tinggi. Ini mengindikasikan deforestasi di Kalimantan lebih didominasi oleh aktivitas industri (tambang/kebun) di wilayah pedalaman ketimbang radius langsung IKN.
    - Elevasi dan curah hujan berasosiasi negatif (area tinggi/curah hujan tinggi lebih sedikit mengalami deforestasi).
    """)

with tab2:
    df_urb = load_driver_data('urbanization')
    plot_coefficients(df_urb, "Pendorong Urbanisasi (Non-Built → Built)")
    st.markdown("""
    **Interpretasi:**
    - **`distance_to_ikn` ternyata TIDAK SIGNIFIKAN** (p > 0.05). Artinya, efek limpahan (*spillover effect*) dari pembangunan IKN terhadap urbanisasi wilayah sekitarnya belum terukur/belum terjadi secara masif dalam kerangka waktu 2019–2024.
    - Sebaliknya, **`mining_density_10km` positif dan sangat signifikan**. Wilayah padat tambang secara konsisten menarik pertumbuhan area terbangun (kemungkinan untuk pemukiman pekerja dan infrastruktur logistik pendukung).
    """)

with tab3:
    df_min = load_driver_data('mining')
    plot_coefficients(df_min, "Pendorong Ekspansi Tambang (Non-Bare → Bare)")
    st.markdown("""
    **Interpretasi:**
    - Ekspansi tambang baru berasosiasi kuat dengan: (1) Jarak yang semakin dekat dengan IKN (mungkin karena kemudahan logistik), dan (2) Kepadatan tambang historis yang tinggi (*clustering effect*).
    """)

st.markdown("---")
st.info("""
**Catatan Metodologis (PENTING):** 
1. **Bukan Causal Inference:** Regresi logistik ini mengukur *asosiasi spasial*, bukan hubungan sebab-akibat absolut.
2. **Data Kepadatan Tambang:** Untuk menghindari *circular reasoning* (memprediksi tambang menggunakan tebakan ML), variabel tambang (`mining_density_10km`) dihitung secara geospasial menggunakan observasi *ground-truth* independen dari **"Global polygons of surface mining area v2" (Maus et al., 2022)**.
""")

# Driver effects plot (always deforestation-scoped — see note below)
st.markdown("---")
st.subheader("Visualisasi Tambahan: Forest Loss Rate vs Drivers (Deforestasi)")
st.caption("Plot ini selalu menampilkan analisis deforestasi, terlepas dari tab yang aktif di atas — belum tersedia visualisasi setara untuk urbanisasi/ekspansi tambang.")
driver_img = os.path.join(DRIVER_DIR_V2, 'driver_effects.png')
if os.path.exists(driver_img):
    st.image(
        driver_img,
        use_container_width=True,
        caption="Deforestation rate binned by distance to IKN and by mining density — see scripts/dual_driver_analysis.py",
    )
else:
    st.caption("Plot driver effects belum tersedia. Jalankan `python scripts/dual_driver_analysis.py` untuk membuatnya.")
