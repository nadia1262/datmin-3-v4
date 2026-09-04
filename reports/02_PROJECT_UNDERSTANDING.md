# PROJECT UNDERSTANDING
**Project:** Spatiotemporal Land-Cover Dynamics in Kalimantan Using Sentinel-2 and Supervised Machine Learning

---

## 1. GAMBARAN BESAR PROJECT (PIPELINE)

Proyek ini bertujuan memetakan dan menganalisis perubahan tutupan lahan di Kalimantan selama 6 tahun (2019-2024), serta mengeksplorasi hubungan antara perubahan tersebut dengan pembangunan IKN dan aktivitas tambang.

**Alur Sederhana:**
Data satelit diambil → diekstrak menjadi data latih → model Machine Learning dilatih → model memprediksi peta se-Kalimantan → peta dibandingkan antar tahun untuk mencari perubahan → perubahan tersebut diuji korelasinya dengan lokasi IKN dan tambang → dashboard menampilkan hasilnya.

### Rincian per Tahapan:

1. **Pengumpulan Data Latih (Sampling Training)**
   - **Input:** Citra satelit Sentinel-2 (2021) & Peta tutupan lahan ESA WorldCover (2021).
   - **Proses:** Diambil 30.000 titik koordinat secara acak dari seluruh Kalimantan. Untuk setiap titik, dicatat warna/pantulan satelitnya (sebagai "X") dan jenis lahannya menurut ESA (sebagai "Y").
   - **Output:** `training_samples_2021.csv`.
   - **Tujuan:** Mengajari algoritma Machine Learning cara membedakan hutan, tambang, bangunan, dll dari warna satelitnya.

2. **Pembuatan Grid Prediksi (Se-Kalimantan)**
   - **Input:** Citra satelit Sentinel-2 (2019 hingga 2024).
   - **Proses:** Membuat jaring-jaring (grid) berjarak 500 meter menutupi seluruh Kalimantan. Didapatkan ~155.000 hingga 176.000 titik setiap tahunnya.
   - **Output:** `prediction_grid_2019.csv` sampai `prediction_grid_2024.csv`.
   - **Tujuan:** Menyiapkan kanvas kosong yang akan diwarnai oleh Machine Learning.

3. **Pelatihan Model (Model Training & Selection)**
   - **Input:** `training_samples_2021.csv`.
   - **Proses:** Mengadu 6 algoritma (SVM, LightGBM, Random Forest, dll) untuk menebak tutupan lahan. Pengujian dilakukan dengan "Spatial Block Cross-Validation", yakni membagi peta menjadi kotak-kotak 55km agar pengujiannya jujur (tidak ada kebocoran data tetangga).
   - **Output:** Model terbaik (`model_lgbm.pkl`) & metrik akurasi (`model_comparison.csv`).
   - **Tujuan:** Mendapatkan "otak" AI yang paling akurat dan efisien. (SVM paling akurat 83.99%, tapi LightGBM dipilih karena sangat cepat dengan akurasi 83.32%).

4. **Prediksi (Prediction)**
   - **Input:** Grid Prediksi (semua tahun) + Model AI (`model_lgbm.pkl`).
   - **Proses:** Model menebak kelas tutupan lahan pada ratusan ribu titik di seluruh Kalimantan untuk setiap tahun.
   - **Output:** Peta tutupan lahan tahunan (`predictions_lgbm_2019.csv` dst).
   - **Tujuan:** Menghasilkan peta tutupan lahan kita sendiri.

5. **Deteksi Perubahan (Change Detection)**
   - **Input:** Peta Prediksi 2019-2024.
   - **Proses:** Mengambil hanya 118.943 titik yang lokasinya konsisten ada di semua tahun (disebut *Common Spatial Domain*). Kemudian membandingkan kelasnya di tahun 2019 dengan 2024.
   - **Output:** Matriks transisi & data titik berubah (`change_points_2019_2024.csv`).
   - **Tujuan:** Mengetahui secara pasti di mana hutan hilang (deforestasi) atau tambang muncul.

6. **Analisis Pendorong (Driver Analysis)**
   - **Input:** Data titik berubah + Jarak ke IKN + Kepadatan Tambang + Elevasi + Curah hujan.
   - **Proses:** Menggunakan uji statistik Regresi Logistik untuk melihat apakah daerah yang dekat IKN atau tambang memiliki peluang deforestasi/urbanisasi yang lebih besar.
   - **Output:** Angka Odds Ratio dan P-value (`driver_deforestation.csv` dst).
   - **Tujuan:** Menjawab hipotesis: "Apakah IKN/Tambang berhubungan dengan hilangnya hutan?".

7. **Interpretabilitas Model (SHAP)**
   - **Input:** Model AI + sebagian data.
   - **Proses:** Menganalisis bagaimana cara kerja otak model menggunakan metode SHAP.
   - **Output:** Grafik pentingnya fitur spektral (`shap_importance.csv`).
   - **Tujuan:** Membuktikan bahwa model kita pintar (mengandalkan indeks vegetasi/NDVI untuk hutan), bukan sekadar menebak acak.

---

## 2. DATA LINEAGE / PERJALANAN DATA

| Tahap | Input | Script | Proses | Output | Digunakan Oleh |
|---|---|---|---|---|---|
| **GEE Export** | Sentinel-2 + ESA WC | `gee_scripts/07...js` | Ekstrak sampel latih | `training_samples_2021.csv` | `train_classification.py` |
| **GEE Export** | Sentinel-2 (19-24) | `gee_scripts/09...js` | Ekstrak grid 500m | `prediction_grid_{year}.csv` | `predict_all_years.py` |
| **Model Training** | `training_samples...csv`| `train_classification.py` | Latih 6 algoritma | `model_lgbm.pkl` | `predict_all_years.py`, SHAP |
| **Prediction** | `model_lgbm.pkl` + grids | `predict_all_years.py` | Tebak kelas per grid | `predictions_lgbm_{year}.csv` | `change_detection_v2.py` |
| **Change Detec.**| `predictions_lgbm...csv`| `change_detection_v2.py`| Filter common domain | `change_points_2019_2024.csv` | `driver_analysis_v2.py` |
| **Driver Analys.**| `change_points...csv` | `driver_analysis_v2.py`| Logistic Regression | `logistic_forest_loss...csv` | Dashboard |
| **Dashboard Prep**| Semua output akhir | `prepare_dashboard...py`| Agregasi ke JSON/CSV | `dashboard/data/*.json` | Streamlit Dashboard |

---

## 3. AUDIT FILE SCRIPT (YANG BENAR-BENAR DIJALANKAN)

Berikut adalah daftar file yang **benar-benar membentuk pipeline akhir**. Urutan ini adalah urutan eksekusi aktual:

1. **`gee_scripts/07_stratified_sampling.js`**
   - *Sebenarnya ngapain?* Berjalan di GEE, menarik 30.000 titik koordinat secara cerdas (tidak ngumpul di satu tempat) lalu mengekspor spektral satelitnya.
2. **`gee_scripts/09_prediction_grid.js`**
   - *Sebenarnya ngapain?* Berjalan di GEE, membuat jaring-jaring 500m menutupi Kalimantan dan menarik data satelit untuk tiap jaring dari 2019-2024.
3. **`scripts/train_classification.py`**
   - *Sebenarnya ngapain?* Otaknya proyek. Script ini melatih 6 model AI, membagi-bagi peta menjadi blok 55km (agar ujiannya tidak curang/bocor), mencatat rapor tiap AI, dan menyimpan AI yang menang (`model_lgbm.pkl`).
4. **`scripts/predict_all_years.py`**
   - *Sebenarnya ngapain?* Script ini "mempekerjakan" AI yang menang tadi untuk melihat ratusan ribu titik jaring dari tahun ke tahun dan menuliskan tebakannya (Hutan, Air, dll).
5. **`scripts/change_detection_v2.py`**
   - *Sebenarnya ngapain?* Membandingkan hasil tebakan tahun 2019 dan 2024. Pintarnya script ini, ia membuang titik-titik yang tertutup awan di salah satu tahun (sehingga hanya tersisa 118,943 titik "Common Domain") agar perbandingannya 100% adil.
6. **`scripts/driver_analysis_v2.py`**
   - *Sebenarnya ngapain?* Mengambil titik-titik yang berubah (misal Hutan → Tambang), lalu melakukan uji statistik Regresi Logistik. Ia mengecek: "Apakah titik yang berubah ini lokasinya dekat IKN atau tidak?".
7. **`scripts/shap_classifier.py`**
   - *Sebenarnya ngapain?* Membedah otak model LightGBM untuk melihat rumus spektral mana yang paling ia percaya (ternyata NDVI).
8. **`scripts/prepare_dashboard_data.py`**
   - *Sebenarnya ngapain?* Mengambil file-file raksasa (jutaan baris) dari proses di atas, menyaring intisarinya, dan mengubahnya menjadi file super kecil (`.json`/`.csv`) agar website dashboard tidak lemot.

*File `change_detection.py` (lama) dan `dual_driver_analysis.py` (lama) sebaiknya diabaikan dari penulisan metode.*
