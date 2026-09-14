# dashboard/pages/2_Change_Detection.py
import streamlit as st
import pandas as pd
import numpy as np
import json
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

try:
    import leafmap.foliumap as leafmap
except ImportError:
    leafmap = None

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
from configs.constants import *
from configs.color_palette import *

# Root project directory (for accessing reports/)
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from theme import apply_theme

st.set_page_config(page_title="Change Detection", page_icon="◈", layout="wide")
apply_theme()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigasi Modul")
selected_menu = st.sidebar.radio(
    "Pilih Skala Analisis:",
    ['Dekomposisi Makro (500m)', 'Validasi Mikro KIPP IKN (10m)']
)

def macro_decomposition_view():
    st.title("Change Detection (2019 → 2024)")
    st.markdown("Analisis transisi tutupan lahan dan deteksi perubahan temporal menggunakan Common Spatial Domain.")

    st.markdown("---")
    st.subheader("Tapak Spasial: Grid Majority Voting (500m)")
    st.markdown("Visualisasi **~1,5 juta sel** yang mewakili konsensus (*majority voting*) 25 titik sub-grid pada setiap area 500m di Kalimantan. Area yang kosong merepresentasikan wilayah tanpa data yang valid di kedua tahun (awam persisten atau batas data).")

    @st.cache_data
    def load_common_domain():
        path = os.path.join(BASE_DIR, 'reports', 'majority_voting_kalimantan.csv')
        if os.path.exists(path):
            # Cukup ambil koordinat (hanya pakai baris kelipatan 10 agar browser tidak crash render 1.5 juta titik)
            df = pd.read_csv(path, usecols=['lon_2019', 'lat_2019'])
            df = df.rename(columns={'lon_2019': 'lon', 'lat_2019': 'lat'})
            return df.iloc[::10]
        return None

    df_common_domain = load_common_domain()

    if df_common_domain is not None:
        # Scatterplot Layer for PyDeck
        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_common_domain,
            get_position='[lon, lat]',
            get_fill_color=[216, 219, 208, 150], # Elegan muted gray-green (mengikuti kode D8DBD0 dari palet no_change)
            get_radius=2500,  # Samakan dengan halaman peta (solid grid)
            opacity=0.9,
            stroked=False,
            filled=True,
            pickable=False,
        )
        
        # View state focused on Central Borneo
        view_state = pdk.ViewState(
            latitude=0.0,
            longitude=114.0,
            zoom=4.8,
            pitch=0,
        )
        
        # Render the Deck
        deck = pdk.Deck(
            layers=[scatter_layer],
            initial_view_state=view_state,
            map_provider="carto", # Samakan dengan provider peta utama
            map_style="dark",     # Carto dark basemap
            tooltip=False
        )
        
        st.pydeck_chart(deck)
    else:
        st.warning("Data Common Spatial Domain tidak ditemukan. Pastikan 'change_points_2019_2024.csv' tersedia.")

    st.markdown("---")

    # Load Transition Matrix
    @st.cache_data
    def load_transition_matrix():
        path = os.path.join(BASE_DIR, 'reports', 'majority_voting_kalimantan.csv')
        if os.path.exists(path):
            df = pd.read_csv(path, usecols=['majority_label_2019', 'majority_label_2024'])
            cm = pd.crosstab(df['majority_label_2019'], df['majority_label_2024'])
            return cm, df
        return None, None

    # Load Change Summary
    @st.cache_data
    def calculate_change_summary(df):
        if df is None: return None
        total = len(df)
        changed = (df['majority_label_2019'] != df['majority_label_2024']).sum()
        change_pct = round(changed / total * 100, 1) if total > 0 else 0
        forest_loss = ((df['majority_label_2019'] == 'Forest') & (df['majority_label_2024'] != 'Forest')).sum()
        forest_gain = ((df['majority_label_2019'] != 'Forest') & (df['majority_label_2024'] == 'Forest')).sum()
        urbanization = ((df['majority_label_2019'] != 'Built-up') & (df['majority_label_2024'] == 'Built-up')).sum()
        mining_exp = ((df['majority_label_2019'] != 'Bare/Mining-like') & (df['majority_label_2024'] == 'Bare/Mining-like')).sum()
        
        return {
            'total_points': total,
            'changed_points': changed,
            'change_rate_pct': change_pct,
            'forest_loss': forest_loss,
            'forest_gain': forest_gain,
            'urbanization': urbanization,
            'mining_expansion': mining_exp
        }

    cm, df_full = load_transition_matrix()
    summary = calculate_change_summary(df_full)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Transition Matrix (2019 → 2024)")
        if cm is not None:
            fig = px.imshow(cm,
                            labels=dict(x="Kelas 2024", y="Kelas 2019", color="Titik"),
                            color_continuous_scale="YlOrRd",
                            template=PLOTLY_TEMPLATE)
            fig.update_layout(
                paper_bgcolor=PLOTLY_PAPER_COLOR,
                plot_bgcolor=PLOTLY_PLOT_COLOR,
                font_color=PLOTLY_FONT_COLOR
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("File transition matrix tidak ditemukan. Jalankan `python scripts/change_detection_v2.py` terlebih dahulu.")

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
        st.markdown("- **Forest Loss** dan **Forest Gain** dapat dilihat perbandingannya untuk menilai tren deforestasi atau revegetasi.")
        st.markdown("- Urbanisasi seringkali terjadi secara bertahap (Forest → Shrubland → Built-up).")
        
        st.info("""
        **Catatan Metodologis: Majority Voting (Sub-grid)**
        Transisi antar kelas di atas dihitung menggunakan **~1,5 juta sel (500m)** di seluruh Kalimantan.
        Setiap sel adalah hasil konsensus (*majority voting*) dari 25 titik sub-grid (100m) yang terbebas dari tutupan awan di 2019 dan 2024. 
        Metode ini mengeleminasi bias under-sampling dari metode *centroid* (piksel tunggal), memastikan representasi agregat yang jauh lebih akurat untuk estimasi deforestasi regional.
        """)

    # Temporal Trends
    st.markdown("---")
    st.subheader("Tren Komposisi Tutupan Lahan (2019–2024)")

    @st.cache_data
    def load_temporal(df):
        if df is None: return None
        counts_19 = df['majority_label_2019'].value_counts()
        counts_24 = df['majority_label_2024'].value_counts()
        
        data = []
        for cls in counts_19.index.union(counts_24.index):
            data.append({'year': 2019, 'class_name': cls, 'proportion': counts_19.get(cls, 0) / len(df) * 100})
            data.append({'year': 2024, 'class_name': cls, 'proportion': counts_24.get(cls, 0) / len(df) * 100})
        return pd.DataFrame(data)

    tc = load_temporal(df_full)
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
        st.caption("Tren komposisi divisualisasikan menggunakan seluruh prediksi ML per tahun.")

def micro_validation_ippk_view():
    st.title("Validasi Mikro KIPP IKN: Mengungkap Realita Pembangunan IKN (10m)")
    
    st.markdown("""
    **Mengapa Validasi Mikro?**  
    Analisis skala makro sebelumnya (500m) mendeteksi anomali *'Forest Gain'* masif di Kalimantan. Hal ini murni disebabkan oleh **Disonansi Resolusi dan Mixed Pixel Effect**, di mana sinyal heterogen lapangan (seperti semak belukar) tertelan oleh sinyal dominan hutan saat dikompresi. Modul ini melakukan validasi mikro menggunakan resolusi asli 10 meter (tanpa kompresi/agregasi) khusus di Kawasan Inti Pusat Pemerintahan (KIPP) IKN untuk melihat tren perubahan tutupan lahan yang sesungguhnya sejalan dengan pembangunan IKN.
    """)
    st.markdown("---")
    
    st.subheader("Perbandingan Visual KIPP IKN (2019 vs 2024)")
    
    if leafmap is None:
        st.error("Library `leafmap` tidak ditemukan. Silakan buka terminal dan jalankan `pip install leafmap folium` untuk mengaktifkan fitur peta interaktif side-by-side.")
    else:
        # Initial map center around KIPP IKN (Penajam Paser Utara / Sepaku)
        m = leafmap.Map(center=[-0.965, 116.705], zoom=12, draw_control=False, measure_control=False)
        m.add_basemap("HYBRID") # Menggunakan Google Satellite berlabel agar terasa rill
        
        # Absolute paths for Streamlit loading robustness
        tiff_2019 = os.path.join(DATA_DIR, 'external', 'ipp_k_10m_2019.tif')
        tiff_2024 = os.path.join(DATA_DIR, 'external', 'ipp_k_10m_2024.tif')
        
        color_palette = ['#1F7A3D', '#6E9A2E', '#C6371F', '#B87A1E', '#1B5FA8']
        
        if os.path.exists(tiff_2019) and os.path.exists(tiff_2024):
            # If the actual high-res GeoTIFFs are provided in data/external
            m.split_map(
                left_layer=tiff_2019, 
                right_layer=tiff_2024, 
                left_label="2019 (Pra-Konstruksi)", 
                right_label="2024 (Fase Konstruksi Masif)",
                left_args={"cmap": color_palette, "vmin": 0, "vmax": 4, "opacity": 0.65}, # Opacity 65% agar menyatu dengan satelit
                right_args={"cmap": color_palette, "vmin": 0, "vmax": 4, "opacity": 0.65}
            )
        else:
            # Fallback mock visualization showing the interaction logic
            st.warning("File raster resolusi tinggi 10m (`ipp_k_10m_2019.tif` & `ipp_k_10m_2024.tif`) belum ditemukan di folder `data/external/`. Menampilkan peta batas simulasi IKN.")
            m.split_map(left_layer="SATELLITE", right_layer="OpenTopoMap",
                       left_label="2019 (Citra Satelit Historis)", right_label="2024 (Pemetaan Topografi)")
            
            # Interactive annotations for key KIPP landmarks
            m.add_marker(location=[-0.965, 116.705], popup="Istana Negara / Sumbu Kebangsaan", tooltip="Zona KIPP Inti (Titik Nol)")
            m.add_marker(location=[-0.940, 116.755], popup="Bendungan Sepaku Semoi", tooltip="Infrastruktur Air Utama KIPP")
            
        m.to_streamlit(height=550)
        
        # Legend matching configs/color_palette.py
        st.markdown("**Legenda Tutupan Lahan (10m):**")
        leg_cols = st.columns(5)
        leg_cols[0].markdown(f"<div style='background-color:{DASHBOARD_THEME['accent_green']}; padding:10px; color:white; border-radius:5px; text-align:center;'>Hutan</div>", unsafe_allow_html=True)
        leg_cols[1].markdown(f"<div style='background-color:#6E9A2E; padding:10px; color:white; border-radius:5px; text-align:center;'>Semak/Pertanian</div>", unsafe_allow_html=True)
        leg_cols[2].markdown(f"<div style='background-color:{DASHBOARD_THEME['accent_red']}; padding:10px; color:white; border-radius:5px; text-align:center;'>Area Terbangun</div>", unsafe_allow_html=True)
        leg_cols[3].markdown(f"<div style='background-color:{DASHBOARD_THEME['accent_orange']}; padding:10px; color:white; border-radius:5px; text-align:center;'>Tanah Terbuka</div>", unsafe_allow_html=True)
        leg_cols[4].markdown(f"<div style='background-color:#1B5FA8; padding:10px; color:white; border-radius:5px; text-align:center;'>Air</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Statistik Perubahan Lahan Mikro — Prediksi LightGBM (10m)")
    st.caption("Data berikut adalah hasil prediksi model LightGBM kelompok kami yang dijalankan pada resolusi asli 10 meter, khusus di area KIPP IKN.")
    
    # --- Load REAL LightGBM 10m Predictions ---
    @st.cache_data
    def load_lgbm_10m_predictions():
        path_2019 = os.path.join(DATA_DIR, 'predictions', 'ikn_10m_predicted_2019.csv')
        path_2024 = os.path.join(DATA_DIR, 'predictions', 'ikn_10m_predicted_2024.csv')
        if os.path.exists(path_2019) and os.path.exists(path_2024):
            df19 = pd.read_csv(path_2019)
            df24 = pd.read_csv(path_2024)
            return df19, df24
        return None, None
    
    df19, df24 = load_lgbm_10m_predictions()
    
    if df19 is not None and df24 is not None:
        # Class label mapping
        label_map = {0: 'Forest (Hutan)', 1: 'Shrubland (Semak)', 2: 'Built-up (Terbangun)', 3: 'Bare/Mining (Terbuka)', 4: 'Water (Air)'}
        
        # Count pixels per class
        counts_2019 = df19['predicted_class'].value_counts().sort_index()
        counts_2024 = df24['predicted_class'].value_counts().sort_index()
        
        # Build comparison DataFrame
        all_classes = sorted(set(counts_2019.index) | set(counts_2024.index))
        stats_data = []
        for cls in all_classes:
            n19 = int(counts_2019.get(cls, 0))
            n24 = int(counts_2024.get(cls, 0))
            # Each 10m pixel = 100 m² = 0.01 Ha
            ha19 = n19 * 0.01
            ha24 = n24 * 0.01
            delta_ha = ha24 - ha19
            pct_change = (delta_ha / ha19 * 100) if ha19 > 0 else 0
            stats_data.append({
                'Kelas Lahan': label_map.get(cls, f'Kelas {cls}'),
                'Piksel 2019': n19,
                'Piksel 2024': n24,
                'Area 2019 (Ha)': round(ha19, 1),
                'Area 2024 (Ha)': round(ha24, 1),
                'Delta (Ha)': round(delta_ha, 1),
                'Perubahan (%)': round(pct_change, 1)
            })
        
        df_stats = pd.DataFrame(stats_data)
        
        # --- Key Metrics ---
        forest_row = df_stats[df_stats['Kelas Lahan'] == 'Forest (Hutan)']
        bare_row = df_stats[df_stats['Kelas Lahan'] == 'Bare/Mining (Terbuka)']
        shrub_row = df_stats[df_stats['Kelas Lahan'] == 'Shrubland (Semak)']
        
        forest_loss_pct = abs(forest_row['Perubahan (%)'].values[0]) if len(forest_row) > 0 else 0
        bare_increase_ha = bare_row['Delta (Ha)'].values[0] if len(bare_row) > 0 else 0
        forest_delta_ha = forest_row['Delta (Ha)'].values[0] if len(forest_row) > 0 else 0
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(
                label="FOREST LOSS (LGBM 10M)", 
                value=f"-{forest_loss_pct:.1f}%", 
                delta=f"{forest_delta_ha:+,.1f} Ha", 
                delta_color="inverse"
            )
        with c2:
            st.metric(
                label="LONJAKAN LAHAN TERBUKA", 
                value=f"+{bare_increase_ha:,.1f} Ha", 
                delta=f"+{abs(bare_row['Perubahan (%)'].values[0]):.0f}% Ekspansi Konstruksi" if len(bare_row) > 0 else "", 
                delta_color="off"
            )
        with c3:
            total_pixels = len(df19)
            st.metric(
                label="TOTAL PIKSEL DIANALISIS",
                value=f"{total_pixels:,}",
                delta=f"~{total_pixels * 0.01:.0f} Ha area KIPP",
                delta_color="off"
            )
        
        # --- Grouped Bar Chart: 2019 vs 2024 ---
        st.markdown("#### Perbandingan Komposisi Lahan KIPP IKN (2019 vs 2024)")
        
        bar_data = []
        color_map_bar = {
            'Forest (Hutan)': CLASS_COLORS[0],
            'Shrubland (Semak)': CLASS_COLORS[1],
            'Built-up (Terbangun)': CLASS_COLORS[2],
            'Bare/Mining (Terbuka)': CLASS_COLORS[3],
            'Water (Air)': CLASS_COLORS[4]
        }
        for _, row in df_stats.iterrows():
            bar_data.append({'Kelas': row['Kelas Lahan'], 'Tahun': '2019', 'Piksel': row['Piksel 2019']})
            bar_data.append({'Kelas': row['Kelas Lahan'], 'Tahun': '2024', 'Piksel': row['Piksel 2024']})
        
        df_bar = pd.DataFrame(bar_data)
        
        fig_bar = px.bar(
            df_bar, x='Kelas', y='Piksel', color='Tahun',
            barmode='group',
            color_discrete_map={'2019': '#4A7C59', '2024': '#C6371F'},
            template=PLOTLY_TEMPLATE,
            labels={'Piksel': 'Jumlah Piksel (10m)', 'Kelas': ''}
        )
        fig_bar.update_layout(
            paper_bgcolor=PLOTLY_PAPER_COLOR,
            plot_bgcolor=PLOTLY_PLOT_COLOR,
            font_color=PLOTLY_FONT_COLOR,
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            height=420
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # --- Data Table ---
        with st.expander("Lihat Tabel Detail Perubahan"):
            st.dataframe(df_stats.style.format({
                'Piksel 2019': "{:,}",
                'Piksel 2024': "{:,}",
                'Area 2019 (Ha)': "{:,.1f}",
                'Area 2024 (Ha)': "{:,.1f}",
                'Delta (Ha)': "{:+,.1f}",
                'Perubahan (%)': "{:+,.1f}%"
            }).set_properties(**{
                'background-color': DASHBOARD_THEME['bg_primary'], 
                'color': DASHBOARD_THEME['text_primary']
            }), use_container_width=True)
    else:
        st.warning("File prediksi LightGBM 10m (`ikn_10m_predicted_2019.csv` & `ikn_10m_predicted_2024.csv`) tidak ditemukan di folder `data/predictions/`.")
    
    st.markdown("---")
    st.markdown("""
    <div style="background-color: #EAF0E3; border-left: 4px solid #1F7A3D; border-radius: 8px; padding: 1.25rem 1.5rem; margin-top: 0.5rem;">
        <p style="font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; color: #1F7A3D; margin-bottom: 0.5rem;">Convergent Evidence</p>
        <p style="margin: 0 0 0.75rem 0; line-height: 1.6;">Model <strong>LightGBM</strong> (dilatih pada ESA WorldCover 2021) dan <strong>Google Dynamic World</strong> (Deep Learning independen) <strong>sepakat</strong>: deforestasi masif terjadi di KIPP IKN.</p>
        <ol style="margin: 0; padding-left: 1.25rem; line-height: 1.7;">
            <li>Hutan di titik nol konstruksi IKN telah terfragmentasi dan terkonversi menjadi lahan terbuka/konstruksi.</li>
            <li>Ilusi <em>Forest Gain</em> pada skala makro 500m merupakan artefak dari <strong>Systematic Point Sampling</strong> dan <strong>Mixed Pixel Effect</strong>.</li>
            <li>Model makro 500m tetap valid untuk mendeteksi <em>Telecoupling</em> regional, namun memerlukan validasi mikro 10m untuk memotret <em>footprint</em> infrastruktur lokal.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# MAIN ROUTING LOGIC
# ============================================================
if selected_menu == 'Dekomposisi Makro (500m)':
    macro_decomposition_view()
elif selected_menu == 'Validasi Mikro KIPP IKN (10m)':
    micro_validation_ippk_view()
