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

# --- MAIN VIEW HEADER ---

def macro_decomposition_view():
    st.title("Deteksi Perubahan Tutupan Lahan (2019 → 2024)")
    st.markdown("Kuantifikasi dinamika alih fungsi lahan Pulau Kalimantan menggunakan filter konsensus spasial Majority Voting Sub-Grid Aggregation 500 meter.")

    st.markdown("---")
    st.subheader("Distribusi Spasial: Kisi Grid Majority Voting 500 Meter")
    st.markdown("Visualisasi **1.499.024 sel grid valid** (~1,5 juta titik) yang merepresentasikan konsensus modus dari 25 titik sampel berinterval 100 meter berbasis citra Sentinel-2 10 meter. Area kosong merepresentasikan perairan laut atau tutupan awan persisten yang dieleminasi demi akurasi neraca.")

    @st.cache_data(show_spinner=False)
    def load_common_domain():
        cache_parquet = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/cache/mv_footprint_sample.parquet')
        if os.path.exists(cache_parquet):
            return pd.read_parquet(cache_parquet)
        path = os.path.join(BASE_DIR, 'reports', 'majority_voting_kalimantan.csv')
        if os.path.exists(path):
            df = pd.read_csv(path, usecols=['lon_2019', 'lat_2019'])
            df = df.rename(columns={'lon_2019': 'lon', 'lat_2019': 'lat'})
            return df.iloc[::15]
        return None

    df_common_domain = load_common_domain()

    if df_common_domain is not None:
        layers = []
        
        # 1. Boundary layer outline
        geojson_path = os.path.join(BASE_DIR, 'data', 'external', 'kalimantan_boundary.geojson')
        if os.path.exists(geojson_path):
            with open(geojson_path, 'r') as f:
                boundary_data = json.load(f)
            boundary_layer = pdk.Layer(
                "GeoJsonLayer",
                data=boundary_data,
                stroked=True,
                filled=False,
                get_line_color=[30, 72, 45, 180],
                get_line_width=2200,
                pickable=False,
            )
            layers.append(boundary_layer)

        # 2. 500m Grid Points (Emerald Green)
        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=df_common_domain,
            get_position='[lon, lat]',
            get_fill_color=[34, 112, 70, 160], # Vibrant Canopy Emerald
            get_radius=2200,
            opacity=0.9,
            stroked=False,
            filled=True,
            pickable=False,
        )
        layers.append(scatter_layer)

        # 3. KIPP IKN Reference Marker (Pulsing Pin on East Kalimantan)
        ikn_pin_df = pd.DataFrame([{
            'lon': 116.705, 
            'lat': -0.965, 
            'name': 'Kawasan Inti IKN (Lokasi Sampel Validasi Mikro 10m)'
        }])
        ikn_pin_layer = pdk.Layer(
            "ScatterplotLayer",
            data=ikn_pin_df,
            get_position='[lon, lat]',
            get_fill_color=[198, 55, 31, 240], # Hazard Red Accent
            get_radius=15000,
            stroked=True,
            get_line_color=[255, 255, 255, 255],
            get_line_width=2500,
            pickable=True,
        )
        layers.append(ikn_pin_layer)
        
        view_state = pdk.ViewState(
            latitude=0.0,
            longitude=114.2,
            zoom=4.9,
            pitch=0,
        )
        
        # Render clean Light-Mode Map matching botanical PPT theme
        deck = pdk.Deck(
            layers=layers,
            initial_view_state=view_state,
            map_provider="carto",
            map_style="light",
            tooltip={"text": "{name}"}
        )
        st.pydeck_chart(deck, use_container_width=True)
        
        st.markdown("""
        <div style="display: flex; gap: 16px; align-items: center; justify-content: center; background: #F6F8F4; border: 1px solid #DCE4D8; border-radius: 20px; padding: 6px 18px; margin-top: 0.5rem; font-size: 0.8rem; color: #354738; font-weight: 600;">
            <span><span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:#227046; margin-right:6px;"></span>Kisi Grid Makro 500m (~1,5 Juta Sel Majority Voting)</span>
            <span><span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:#C6371F; border:1.5px solid white; margin-right:6px;"></span>Titik Sampel KIPP IKN (Uji Kepekaan Mikro 10m)</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Data Majority Voting tidak ditemukan.")

    st.markdown("---")

    # Load Transition Matrix & Summary
    @st.cache_data(show_spinner=False)
    def load_transition_data():
        cache_crosstab = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/cache/mv_transition_crosstab.json')
        summary_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/change_summary.json')
        if os.path.exists(cache_crosstab) and os.path.exists(summary_path):
            with open(cache_crosstab, 'r') as f:
                cm_dict = json.load(f)
            cm = pd.DataFrame(cm_dict)
            class_order = ['Forest', 'Shrubland/Agriculture', 'Built-up', 'Bare/Mining-like', 'Water']
            valid_order = [c for c in class_order if c in cm.index and c in cm.columns]
            cm = cm.reindex(index=valid_order, columns=valid_order)
            with open(summary_path, 'r') as f:
                summary_dict = json.load(f)
            return cm, summary_dict

        path = os.path.join(BASE_DIR, 'reports', 'majority_voting_kalimantan.csv')
        if os.path.exists(path):
            df = pd.read_csv(path, usecols=['majority_label_2019', 'majority_label_2024'])
            cm = pd.crosstab(df['majority_label_2019'], df['majority_label_2024'])
            
            # Reorder classes logically
            class_order = ['Forest', 'Shrubland/Agriculture', 'Built-up', 'Bare/Mining-like', 'Water']
            valid_order = [c for c in class_order if c in cm.index and c in cm.columns]
            cm = cm.reindex(index=valid_order, columns=valid_order)
            
            total = len(df)
            changed = (df['majority_label_2019'] != df['majority_label_2024']).sum()
            forest_loss = ((df['majority_label_2019'] == 'Forest') & (df['majority_label_2024'] != 'Forest')).sum()
            forest_gain = ((df['majority_label_2019'] != 'Forest') & (df['majority_label_2024'] == 'Forest')).sum()
            urbanization = ((df['majority_label_2019'] != 'Built-up') & (df['majority_label_2024'] == 'Built-up')).sum()
            mining_exp = ((df['majority_label_2019'] != 'Bare/Mining-like') & (df['majority_label_2024'] == 'Bare/Mining-like')).sum()
            
            summary_dict = {
                'total_points': total,
                'changed_points': changed,
                'change_rate_pct': round(changed / total * 100, 1),
                'forest_loss': forest_loss,
                'forest_gain': forest_gain,
                'urbanization': urbanization,
                'mining_expansion': mining_exp
            }
            return cm, summary_dict
        return None, None

    cm, summary = load_transition_data()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Matriks Transisi Spasiotemporal (2019 → 2024)")
        if cm is not None:
            fig = px.imshow(cm,
                            labels=dict(x="Kelas Tutupan Lahan 2024", y="Kelas Tutupan Lahan 2019", color="Jumlah Sel"),
                            color_continuous_scale="YlGnBu",
                            text_auto=True,
                            template=PLOTLY_TEMPLATE)
            fig.update_layout(
                paper_bgcolor=PLOTLY_PAPER_COLOR,
                plot_bgcolor=PLOTLY_PLOT_COLOR,
                font_color=PLOTLY_FONT_COLOR,
                height=420
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("File matriks transisi tidak ditemukan.")

    with col2:
        st.subheader("Ringkasan Neraca Alih Fungsi Lahan")

        if summary:
            total = summary.get('total_points', 1499024)
            changed = summary.get('changed_points', 215861)
            change_pct = summary.get('change_rate_pct', 14.4)
            forest_loss = summary.get('forest_loss', 79777)
            forest_gain = summary.get('forest_gain', 109748)
            urbanization = summary.get('urbanization', 14460)
            mining_exp = summary.get('mining_expansion', 8075)

            st.metric("Total Unit Observasi Valid", f"{total:,} Sel Grid", delta="500m Resolusi Konsensus")
            st.metric("Total Sel Mengalami Alih Fungsi", f"{changed:,} Sel", delta=f"{change_pct}% dari Luas Pulau")

            m1, m2 = st.columns(2)
            with m1:
                st.metric("Kehilangan Hutan Riil", f"{forest_loss:,} Sel", delta="-5,32% Pulau", delta_color="inverse")
                st.metric("Urbanisasi Baru", f"{urbanization:,} Sel", delta="+14.460 Titik")
            with m2:
                st.metric("Ekspansi Tambang Baru", f"{mining_exp:,} Sel", delta="+43,36% Lonjakan", delta_color="inverse")
                st.metric("Penambahan Hutan Semu", f"{forest_gain:,} Sel", delta="Efek Mixed Pixels (25 ha)", delta_color="off")

        st.markdown("""
        <div style="background:#F6F8F4; border:1px solid #DCE4D8; border-radius:10px; padding:0.9rem; margin-top:0.75rem;">
            <div style="font-size:0.8rem; color:#4B5A50; line-height:1.55;">
                <strong>Dekonstruksi Metodologis:</strong><br>
                • <strong>Gross Forest Loss (79.777 sel)</strong> membongkar deforestasi riil yang tersembunyi.<br>
                • <strong>Net Gain (+29.971 sel)</strong> terdekonstruksi secara kritis sebagai pergeseran domain fenologis (La Niña 2021 vs El Niño 2023 disusul <em>green flush</em> 2024) dan efek piksel campuran pada kanopi semak belukar tua.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Temporal Trends
    st.markdown("---")
    st.subheader("Tren Komposisi Tutupan Lahan (2019 vs 2024)")

    @st.cache_data(show_spinner=False)
    def load_temporal(matrix):
        if matrix is None: return None
        counts_19 = matrix.sum(axis=1)
        counts_24 = matrix.sum(axis=0)
        total = matrix.values.sum()
        
        data = []
        for cls in counts_19.index.union(counts_24.index):
            data.append({'year': 2019, 'class_name': cls, 'proportion': (counts_19.get(cls, 0) / total) * 100})
            data.append({'year': 2024, 'class_name': cls, 'proportion': (counts_24.get(cls, 0) / total) * 100})
        return pd.DataFrame(data)

    tc = load_temporal(cm)
    if tc is not None:
        fig = px.line(tc, x='year', y='proportion', color='class_name',
                      markers=True,
                      labels={'proportion': 'Proporsi (%)', 'year': 'Tahun Pengamatan', 'class_name': 'Kelas Tutupan Lahan'},
                      color_discrete_map={
                          'Forest': CLASS_COLORS[0],
                          'Shrubland/Agriculture': CLASS_COLORS[1],
                          'Built-up': CLASS_COLORS[2],
                          'Bare/Mining-like': CLASS_COLORS[3],
                          'Water': CLASS_COLORS[4]
                      },
                      template=PLOTLY_TEMPLATE)
        fig.update_layout(
            paper_bgcolor=PLOTLY_PAPER_COLOR,
            plot_bgcolor=PLOTLY_PLOT_COLOR,
            font_color=PLOTLY_FONT_COLOR,
            xaxis=dict(tickvals=[2019, 2024]),
            height=380
        )
        st.plotly_chart(fig, use_container_width=True)

def micro_validation_ippk_view():
    st.title("Validasi Mikro KIPP IKN: Resolusi Murni 10 Meter")
    
    st.markdown("""
    <p style="font-size:1.05rem; color:#4B5A50; line-height:1.6; margin-bottom:1.2rem;">
        Membongkar paradoks resolusi satelit: Mengapa di skala makro pulau (500 meter) tutupan hutan terkesan stabil, 
        namun pada skala mikro murni 10 meter di <strong>Kawasan Inti Pusat Pemerintahan (KIPP IKN)</strong> 
        terlihat pembukaan tutupan vegetasi nyata akibat koridor Jalan Tol Akses dan Sumbu Kebangsaan.
    </p>
    """, unsafe_allow_html=True)
    
    st.subheader("Peta Slider Swipe: Perbandingan Visual KIPP IKN (2019 vs 2024)")
    
    col_ctrl1, col_ctrl2 = st.columns([3, 2])
    with col_ctrl1:
        st.markdown("""
        <div style="font-size:0.86rem; color:#4B5A50; line-height:1.5; margin-bottom:0.5rem;">
            <strong>Interaksi Geser:</strong> Geser tuas pemisah <code>⟨ ❘ ⟩</code> di tengah peta ke arah <strong>kiri</strong> untuk membuka tutupan <strong>2024</strong> (puncak konstruksi), atau ke arah <strong>kanan</strong> untuk melihat <strong>2019</strong> (rona awal hutan alami). Peta tersinkronisasi otomatis saat digeser atau diperbesar.
        </div>
        """, unsafe_allow_html=True)
    with col_ctrl2:
        opacity_pct = st.slider("Transparansi Lapisan Klasifikasi ML (%):", min_value=30, max_value=100, value=75, step=5)
        overlay_opacity = opacity_pct / 100.0
    
    # Import and render high-performance Leaflet swipe map
    from components.kipp_swipe_map import render_kipp_swipe_map
    render_kipp_swipe_map(split_pct=50, height=560, overlay_opacity=overlay_opacity)
    
    st.markdown("---")
    st.subheader("Statistik Perubahan Lahan Mikro — Prediksi Model LightGBM (10m)")
    
    @st.cache_data(show_spinner=False)
    def load_kipp_10m_data():
        cache_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/cache/kipp_10m_stats.json')
        if os.path.exists(cache_json):
            with open(cache_json, 'r') as f:
                d = json.load(f)
            return pd.DataFrame(d['stats']), d['total_pixels']

        path_2019 = os.path.join(DATA_DIR, 'predictions', 'ikn_10m_predicted_2019.csv')
        path_2024 = os.path.join(DATA_DIR, 'predictions', 'ikn_10m_predicted_2024.csv')
        if os.path.exists(path_2019) and os.path.exists(path_2024):
            df19 = pd.read_csv(path_2019)
            df24 = pd.read_csv(path_2024)
            label_map = {0: 'Forest (Hutan)', 1: 'Shrubland (Semak)', 2: 'Built-up (Terbangun)', 3: 'Bare/Mining (Terbuka)', 4: 'Water (Air)'}
            
            counts_2019 = df19['predicted_class'].value_counts().sort_index()
            counts_2024 = df24['predicted_class'].value_counts().sort_index()
            
            all_classes = sorted(set(counts_2019.index) | set(counts_2024.index))
            stats_data = []
            for cls in all_classes:
                n19 = int(counts_2019.get(cls, 0))
                n24 = int(counts_2024.get(cls, 0))
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
            return pd.DataFrame(stats_data), len(df19)
        return None, 0
    
    df_stats, total_pixels = load_kipp_10m_data()
    
    if df_stats is not None:
        forest_row = df_stats[df_stats['Kelas Lahan'] == 'Forest (Hutan)']
        bare_row = df_stats[df_stats['Kelas Lahan'] == 'Bare/Mining (Terbuka)']
        
        forest_loss_pct = abs(forest_row['Perubahan (%)'].values[0]) if len(forest_row) > 0 else 0
        bare_increase_ha = bare_row['Delta (Ha)'].values[0] if len(bare_row) > 0 else 0
        forest_delta_ha = forest_row['Delta (Ha)'].values[0] if len(forest_row) > 0 else 0
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(
                label="KEHILANGAN HUTAN KIPP (10M)", 
                value=f"-{forest_loss_pct:.1f}%", 
                delta=f"{forest_delta_ha:+,.1f} Ha", 
                delta_color="inverse"
            )
        with c2:
            st.metric(
                label="LONJAKAN TANAH TERBUKA / TAPAK PROYEK", 
                value=f"+{bare_increase_ha:,.1f} Ha", 
                delta=f"+{abs(bare_row['Perubahan (%)'].values[0]):.0f}% Ekspansi Fisik" if len(bare_row) > 0 else "", 
                delta_color="inverse"
            )
        with c3:
            st.metric(
                label="TOTAL PIKSEL KIPP DIANALISIS",
                value=f"{total_pixels:,}",
                delta=f"~{total_pixels * 0.01:.0f} Ha Area Tapak",
                delta_color="off"
            )
        
        st.markdown("#### Distribusi Komposisi Lahan KIPP IKN (2019 vs 2024)")
        
        bar_data = []
        for _, row in df_stats.iterrows():
            bar_data.append({'Kelas': row['Kelas Lahan'], 'Tahun': '2019', 'Luas (Ha)': row['Area 2019 (Ha)']})
            bar_data.append({'Kelas': row['Kelas Lahan'], 'Tahun': '2024', 'Luas (Ha)': row['Area 2024 (Ha)']})
        
        df_bar = pd.DataFrame(bar_data)
        
        fig_bar = px.bar(
            df_bar, x='Kelas', y='Luas (Ha)', color='Tahun',
            barmode='group',
            color_discrete_map={'2019': '#2D6A4F', '2024': '#B23A22'},
            template=PLOTLY_TEMPLATE,
            labels={'Luas (Ha)': 'Luas Area (Hektar)', 'Kelas': ''}
        )
        fig_bar.update_layout(
            paper_bgcolor=PLOTLY_PAPER_COLOR,
            plot_bgcolor=PLOTLY_PLOT_COLOR,
            font_color=PLOTLY_FONT_COLOR,
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            height=400
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        with st.expander("Tabel Detail Neraca Lahan KIPP 10 Meter"):
            st.dataframe(df_stats.style.format({
                'Piksel 2019': "{:,}",
                'Piksel 2024': "{:,}",
                'Area 2019 (Ha)': "{:,.1f}",
                'Area 2024 (Ha)': "{:,.1f}",
                'Delta (Ha)': "{:+,.1f}",
                'Perubahan (%)': "{:+,.1f}%"
            }), use_container_width=True)
    else:
        st.warning("File prediksi LightGBM 10m tidak ditemukan.")
    
    st.markdown("""
    <div class="forest-card" style="margin-top: 1.5rem;">
        <span class="step-badge">SINTESIS MULTI-SKALA</span>
        <h4 style="margin: 0.3rem 0 0.5rem 0;">Resolusi Masalah MAUP dan Efek Piksel Campuran</h4>
        <div style="font-size: 0.88rem; color: #4B5A50; line-height: 1.6;">
            Perbedaan hasil antara skala makro (500 meter) dan skala mikro (10 meter) bukan merupakan kegagalan model, melainkan demonstrasi nyata dari <strong>Modifiable Areal Unit Problem (MAUP)</strong> dan <strong>Mixed-Pixel Heterogeneity</strong>. 
            Pada skala makro, kanopi semak belukar tua di tapak seluas 25 hektar menghasilkan sinyal campuran yang diklasifikasikan sebagai Forest. Sebaliknya, pada resolusi murni 10 meter di KIPP IKN di mana piksel bersifat homogen, pembukaan hutan akibat tapak gedung pemerintahan dan alur jalan tol terpetakan secara tegas dan nyata tanpa adanya artefak pemulihan semu.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# MAIN ROUTING VIA PROMINENT TABS (FAST & DIRECT)
# ============================================================
tab_micro, tab_macro = st.tabs([
    "Peta Slider Swipe Before (2019) vs After (2024) — KIPP IKN 10m",
    "Dekomposisi Makro 500m (Matriks Transisi 1,5 Juta Sel)"
])

with tab_micro:
    micro_validation_ippk_view()

with tab_macro:
    macro_decomposition_view()

