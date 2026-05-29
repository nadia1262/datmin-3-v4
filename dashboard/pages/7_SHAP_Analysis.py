import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="SHAP Analysis", page_icon="🧠", layout="wide")

st.title("🧠 Interpretability with SHAP (Feature Importance)")
st.markdown("""
Bagaimana model Machine Learning kita (LightGBM) mengenali pola "Hutan", "Tambang", atau "Bangunan" dari sekadar data pantulan cahaya satelit? 
Melalui analisis **SHAP (SHapley Additive exPlanations)**, kita membedah "otak" model untuk melihat fitur spektral mana yang paling krusial dalam klasifikasi tutupan lahan.
""")

SHAP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../results/shap/lgbm')

def load_image(filename):
    path = os.path.join(SHAP_DIR, filename)
    if os.path.exists(path):
        return Image.open(path)
    return None

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Global Importance (Beeswarm Summary)")
    st.info("Setiap titik adalah satu lokasi sampel. Posisi di sumbu X menunjukkan seberapa besar fitur tersebut mendorong prediksi model ke arah kelas tertentu.")
    img_bees = load_image('shap_summary.png')
    if img_bees:
        st.image(img_bees, use_container_width=True)
    else:
        st.warning("Grafik SHAP summary belum tersedia. Pastikan script shap_classifier.py sudah dijalankan.")

with col2:
    st.subheader("Feature Importance per Class")
    st.info("Heatmap ini menunjukkan rata-rata dampak setiap fitur spektral terhadap masing-masing kelas tutupan lahan.")
    img_heat = load_image('shap_per_class_heatmap.png')
    if img_heat:
        st.image(img_heat, use_container_width=True)
    else:
        st.warning("Grafik SHAP heatmap belum tersedia.")

st.markdown("""
---
### 💡 Insights dari Analisis Spektral
1. **NDVI (Normalized Difference Vegetation Index)**: Variabel mutlak terpenting. Model menggunakannya secara eksklusif untuk memisahkan vegetasi lebat (Hutan) dari area terbuka (Tambang/Bangunan).
2. **SWIR (Band 11 & Band 12)**: *Shortwave Infrared* terbukti sangat krusial. Band ini menembus kabut tipis dan sangat sensitif terhadap kelembaban tanah dan mineral batuan, sehingga model sangat bergantung pada B11/B12 untuk mengenali **Tanah Terbuka (Bare/Mining-like)**.
3. **NDBI (Normalized Difference Built-up Index)**: Sesuai teori *Remote Sensing*, NDBI menjadi fitur kunci kedua setelah SWIR untuk mendeteksi infrastruktur beton dan aspal di area IKN.
""")
