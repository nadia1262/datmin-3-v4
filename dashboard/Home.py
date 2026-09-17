# dashboard/Home.py
import streamlit as st
import sys
import os
import base64

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from configs.constants import *
from configs.color_palette import *
from theme import apply_theme, render_botanical_footer

st.set_page_config(
    page_title="Land Transformation Intelligence — Kalimantan",
    page_icon="K",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()

# Custom style overrides for Home page
st.markdown("""
<style>
    .hero-showcase {
        position: relative;
        border-radius: 20px;
        overflow: hidden;
        margin-bottom: 1.8rem;
        border: 1px solid #DCE4D8;
        box-shadow: 0 10px 30px rgba(16, 36, 24, 0.08);
        min-height: 430px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #0E1F15;
    }
    .hero-title {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        line-height: 1.32 !important;
        margin: 0 0 0.85rem 0 !important;
        letter-spacing: -0.02em !important;
        text-shadow: 0 3px 20px rgba(0,0,0,0.85) !important;
        text-transform: uppercase;
    }
    @media (max-width: 768px) {
        .hero-title {
            font-size: 1.35rem !important;
            line-height: 1.25 !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- Hero Section with Dynamic Video Footage Background ---
st.markdown("""
<div class="hero-showcase">
    <video autoplay loop muted playsinline poster="app/static/hero_kalimantan.jpg" 
           style="position: absolute; top:0; left:0; width: 100%; height: 100%; object-fit: cover; display: block; filter: brightness(0.80) contrast(1.05);">
        <source src="app/static/Footage.mp4" type="video/mp4">
    </video>
    <div style="position: absolute; top:0; left:0; width: 100%; height: 100%; background: linear-gradient(180deg, rgba(8, 20, 13, 0.20) 0%, rgba(6, 16, 10, 0.65) 100%); pointer-events: none;"></div>
    <div style="
        position: relative;
        z-index: 2;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 3.8rem 2.8rem;
        max-width: 960px;
    ">
        <h1 class="hero-title">
            TRANSFORMASI TUTUPAN LAHAN DAN SPATIAL TELECOUPLING PEMBANGUNAN IKN SERTA EKSPANSI PERTAMBANGAN DI KALIMANTAN: PENDEKATAN MACHINE LEARNING MULTI-SKALA
        </h1>
        <div style="
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 1.15rem;
            font-weight: 700;
            color: #74C69D;
            letter-spacing: -0.01em;
            margin-bottom: 1.1rem;
            line-height: 1.45;
            text-shadow: 0 2px 14px rgba(0,0,0,0.85);
        ">
            Komparasi Spasial Rona Awal dan Puncak Konstruksi Menggunakan Citra Multispektral Sentinel-2
        </div>
        <p style="
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 0.94rem;
            font-weight: 400;
            color: rgba(255,255,255,0.94);
            max-width: 820px;
            line-height: 1.6;
            margin: 0 auto;
            text-shadow: 0 2px 10px rgba(0,0,0,0.8);
        ">
            Investigasi Spatiotemporal Rona Awal (2019) Menuju Puncak Konstruksi IKN (2024): 
            Membedah Efek Spillover IKN vs Hegemoni Pertambangan Menggunakan Citra Multispektral Sentinel-2, Agregasi Majority Voting 1,5 Juta Sel, dan Analisis Spatial Telecoupling.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Section di Bawah Hero: Methodology Header ---
st.markdown("""
<div style="text-align: center; margin: 0.8rem auto 1.5rem auto; max-width: 780px;">
    <p style="font-family: 'IBM Plex Mono', monospace; font-size: 0.74rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.16em; color: #2D6A4F; margin-bottom: 0.35rem;">
        KERANGKA KERJA ILMIAH TERPADU
    </p>
    <h2 style="font-size: 2.1rem; font-weight: 800; color: #16281C; margin: 0 0 0.6rem 0; letter-spacing: -0.02em;">
        Metodologi Sekuensial Tiga Tahap
    </h2>
    <p style="color: #4B5A50; line-height: 1.6; font-size: 0.94rem; margin: 0;">
        Menjembatani resolusi satelit multi-skala untuk mengatasi bias tutupan awan khatulistiwa dan mengevaluasi interaksi spasial kebijakan pemindahan ibu kota.
    </p>
</div>
""", unsafe_allow_html=True)

# 3 Methodology Pillars (Adopting Slide 3 from PPT)
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="forest-card" style="height: 100%;">
        <span class="step-badge">TAHAP 01</span>
        <h3 style="font-size: 1.15rem; margin: 0 0 0.5rem 0; color: #16281C;">Klasifikasi Machine Learning</h3>
        <p style="color: #4B5A50; font-size: 0.88rem; line-height: 1.55; margin-bottom: 1rem;">
            Evaluasi kompetitif 6 algoritma <em>supervised learning</em> pada <strong>30.000 sampel murni</strong> berbasis 10 fitur optik Sentinel-2 dengan validasi spasial independen.
        </p>
        <div style="background: #F6F8F4; border-radius: 8px; padding: 0.75rem; font-size: 0.82rem; color: #16281C;">
            <div style="font-weight: 700; color: #1E482D; margin-bottom: 0.2rem;">Model Terpilih: LightGBM</div>
            <div>• Overall Accuracy: <strong>83,32%</strong></div>
            <div>• Macro F1-Score: <strong>0,8347</strong></div>
            <div>• Waktu Latih: <strong>116,6 detik</strong> (vs SVM 760s)</div>
            <div>• Protokol: <strong>Spatial Block GroupKFold 5-Fold</strong></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="forest-card" style="height: 100%;">
        <span class="step-badge">TAHAP 02</span>
        <h3 style="font-size: 1.15rem; margin: 0 0 0.5rem 0; color: #16281C;">Deteksi Perubahan Majority Voting</h3>
        <p style="color: #4B5A50; font-size: 0.88rem; line-height: 1.55; margin-bottom: 1rem;">
            Agregasi spasial pada kisi sel 500m x 500m (didukung 25 titik sub-grid interval 100m) untuk mengeliminasi bias <em>cloud dropout</em> pada penginderaan jauh khatulistiwa.
        </p>
        <div style="background: #F6F8F4; border-radius: 8px; padding: 0.75rem; font-size: 0.82rem; color: #16281C;">
            <div style="font-weight: 700; color: #1E482D; margin-bottom: 0.2rem;">Cakupan & Dinamika Riil:</div>
            <div>• Sel Grid Valid: <strong>1.499.024 sel</strong> (~1,5 juta titik)</div>
            <div>• Deforestasi Riil: <strong>79.777 sel</strong> (5,32% pulau)</div>
            <div>• Ekspansi Tambang: <strong>8.075 sel</strong> (+43,4%)</div>
            <div>• Resolusi Mikro: <strong>10 meter KIPP IKN</strong></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="forest-card" style="height: 100%;">
        <span class="step-badge">TAHAP 03</span>
        <h3 style="font-size: 1.15rem; margin: 0 0 0.5rem 0; color: #16281C;">Inferensi Telecoupling Spasial</h3>
        <p style="color: #4B5A50; font-size: 0.88rem; line-height: 1.55; margin-bottom: 1rem;">
            Pemodelan faktor pendorong alih fungsi lahan menggunakan <em>Bridge Dataset</em> untuk mencegah bias autokorelasi spasial dan <em>pseudo-replication</em>.
        </p>
        <div style="background: #F6F8F4; border-radius: 8px; padding: 0.75rem; font-size: 0.82rem; color: #16281C;">
            <div style="font-weight: 700; color: #1E482D; margin-bottom: 0.2rem;">Temuan Ekonometrika Spasial:</div>
            <div>• Titik Sampel Independen: <strong>122.478 titik</strong> (~10 km)</div>
            <div>• Jarak ke IKN: <strong>OR = 1,114</strong> (p < 0,001, rembesan)</div>
            <div>• Kepadatan Tambang: <strong>OR = 1,093</strong> (p < 0,001)</div>
            <div>• Faktor Mitigasi: <strong>Elevasi Topografi & Hujan</strong></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- Key Vital Metrics Bar ---
st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric(label="SEL GRID MAKRO DIANALISIS", value="1.499.024", delta="100% Bebas Bias Awan")
with m2:
    st.metric(label="KEHILANGAN HUTAN RIIL", value="79.777 Sel", delta="-5,32% Tapak Daratan", delta_color="inverse")
with m3:
    st.metric(label="LONJAKAN TAMBANG TERBUKA", value="+43,36%", delta="+8.075 Sel Tambang Baru", delta_color="inverse")
with m4:
    st.metric(label="PREDIKSI MIKRO KIPP IKN", value="10 Meter", delta="Sentinel-2 Resolusi Murni")

# --- Quick Navigation Modules ---
st.markdown("""
<div style="margin: 2rem 0 0.8rem 0;">
    <p style="font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.14em; color: #2D6A4F; margin-bottom: 0.25rem;">
        MODUL INTERAKTIF
    </p>
    <h3 style="font-size: 1.45rem; font-weight: 800; color: #16281C; margin: 0 0 0.8rem 0; letter-spacing: -0.015em;">
        Eksplorasi Data dan Analisis Geospasial
    </h3>
</div>
""", unsafe_allow_html=True)

nav1, nav2, nav3 = st.columns(3)
with nav1:
    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #DCE4D8; border-radius:10px; padding:1.2rem; margin-bottom:0.75rem;">
        <span class="step-badge-outline">01 PETA TUTUPAN LAHAN</span>
        <h4 style="margin: 0.4rem 0 0.3rem 0; font-size:1rem;">Land Cover Maps</h4>
        <p style="font-size:0.84rem; color:#4B5A50; margin:0;">Visualisasi spasial pulau Kalimantan membandingkan kondisi rona awal 2019 vs puncak konstruksi 2024.</p>
    </div>
    <div style="background:#FFFFFF; border:1px solid #DCE4D8; border-radius:10px; padding:1.2rem;">
        <span class="step-badge-outline">02 DETEKSI PERUBAHAN</span>
        <h4 style="margin: 0.4rem 0 0.3rem 0; font-size:1rem;">Change Detection</h4>
        <p style="font-size:0.84rem; color:#4B5A50; margin:0;">Matriks transisi 1,5 juta sel Majority Voting dan validasi mikro 10m koridor KIPP IKN.</p>
    </div>
    """, unsafe_allow_html=True)

with nav2:
    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #DCE4D8; border-radius:10px; padding:1.2rem; margin-bottom:0.75rem;">
        <span class="step-badge-outline">03 KOMPARASI MODEL</span>
        <h4 style="margin: 0.4rem 0 0.3rem 0; font-size:1rem;">Model Comparison</h4>
        <p style="font-size:0.84rem; color:#4B5A50; margin:0;">Benchmark komparatif 6 algoritma Machine Learning dengan Spatial Block GroupKFold CV.</p>
    </div>
    <div style="background:#FFFFFF; border:1px solid #DCE4D8; border-radius:10px; padding:1.2rem;">
        <span class="step-badge-outline">04 ANALISIS PENDORONG</span>
        <h4 style="margin: 0.4rem 0 0.3rem 0; font-size:1rem;">Driver Impact</h4>
        <p style="font-size:0.84rem; color:#4B5A50; margin:0;">Regresi logistik spasial multivariat memodelkan asosiasi jarak IKN dan kepadatan tambang.</p>
    </div>
    """, unsafe_allow_html=True)

with nav3:
    st.markdown("""
    <div style="background:#FFFFFF; border:1px solid #DCE4D8; border-radius:10px; padding:1.2rem; margin-bottom:0.75rem;">
        <span class="step-badge-outline">05 HEATMAP SPASIOTEMPORAL</span>
        <h4 style="margin: 0.4rem 0 0.3rem 0; font-size:1rem;">3D Spatiotemporal Heatmap</h4>
        <p style="font-size:0.84rem; color:#4B5A50; margin:0;">Pemetaan densitas heksagon 3D untuk hotspot deforestasi, urbanisasi, dan tambang.</p>
    </div>
    <div style="background:#FFFFFF; border:1px solid #DCE4D8; border-radius:10px; padding:1.2rem;">
        <span class="step-badge-outline">06 INTERPRETABILITAS AI</span>
        <h4 style="margin: 0.4rem 0 0.3rem 0; font-size:1rem;">SHAP Analysis</h4>
        <p style="font-size:0.84rem; color:#4B5A50; margin:0;">Transparansi model LightGBM: atribusi fitur spektral satelit (NDVI, SWIR, NDBI).</p>
    </div>
    """, unsafe_allow_html=True)

# Botanical Rolling Hills Footer
render_botanical_footer()

