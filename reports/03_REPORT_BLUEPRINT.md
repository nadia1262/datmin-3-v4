# REPORT & RESEARCH GAP BLUEPRINT
**Project:** Spatiotemporal Land-Cover Dynamics in Kalimantan Using Sentinel-2 and Supervised Machine Learning

Dokumen ini adalah kerangka dasar (blueprint) untuk menyusun laporan akhir dan presentasi.

---

## 1. LITERATUR UNTUK LATAR BELAKANG (Referensi Kunci)

Gunakan 7 jurnal utama berikut ini untuk membangun referensi dan konteks masalah secara solid (termasuk referensi inti dari dosen pembimbing):

| No | Penulis | Tahun | Judul | Keterkaitan dengan Penelitian Ini |
|:---|:---|:---|:---|:---|
| 1 | Kurniawan, R., et al. | 2024 | *Evaluating the Impact of Ibu Kota Nusantara (IKN) Development on Land Cover Using Machine Learning-Based Sentinel-2A Satellite Image Classification* | **Referensi Utama:** Membuktikan efektivitas Sentinel-2 dan ML untuk IKN. Penelitian kita memperluasnya dengan menambahkan *Spatial Block CV*, *Common Domain* temporal, dan analisis pendorong (*drivers*). |
| 2 | Habibie, et al. | 2025 | *Integrating Sentinel-2 and ESA world cover for effective land use and land cover assessment using machine learning* | **Referensi Kerangka:** Rujukan utama untuk metodologi, penyajian hasil klasifikasi, serta komparasi antar algoritma *Machine Learning*. |
| 3 | Liu, J., et al. | 2013 | *Framing Sustainability in a Telecoupled World* | **Fondasi Teori Spasial:** Menjadi justifikasi teori *Telecoupling*—mengapa penelitian harus diuji ke *seluruh* Kalimantan (mendeteksi efek *spill-over* deforestasi). |
| 4 | Alamgir, M., et al. | 2019 | *Infrastructure expansion challenges sustainable development in globally important biodiversity hotspots* | **Urgensi Penelitian:** Membangun narasi bahwa megaproyek infrastruktur baru di Borneo berpotensi memicu *secondary deforestation*. |
| 5 | Phiri, D., et al. | 2020 | *Sentinel-2 Data for Land Cover/Use Mapping: A Review* | **Justifikasi Data:** Literatur yang mengesahkan bahwa Sentinel-2 jauh lebih superior dibanding Landsat untuk memetakan daerah tropis. |
| 6 | Meyfroidt, P., et al. | 2014 | *Multiple pathways of commodity crop expansion in tropical forest landscapes* | **Fondasi Analisis Penggerak (*Drivers*):** Menjustifikasi penggunaan regresi logistik untuk mengukur probabilitas deforestasi akibat jarak infrastruktur dan tambang. |

---

## 2. RESEARCH GAP (Celah Penelitian) & POSISI PROYEK

**Bandingkan dengan Penelitian Dosen:**  
*Robert Kurniawan — "Evaluating the Impact of Ibu Kota Nusantara (IKN) Development on Land Cover Using Machine Learning-Based Sentinel-2A Satellite Image Classification"*

### Apa yang sudah dijawab oleh penelitian sebelumnya?
1. **Perbandingan ML:** Sudah membuktikan algoritma ML mana yang terbaik untuk klasifikasi Sentinel-2.
2. **Before-After IKN:** Sudah membuat peta tutupan lahan Kaltim sebelum dan sesudah pengumuman IKN.
3. **Analisis Deskriptif:** Sudah memvisualisasikan berapa hektar hutan yang hilang di zona inti IKN.

### Apa celah (Gap) yang belum terjawab yang kita isi?
1. **The Spatial Validation Gap:** Penelitian sebelumnya sering menggunakan random split konvensional yang rentan *spatial data leakage*. **Project Kita:** Menerapkan *Spatial Block GroupKFold (0.5°)* agar akurasi model diuji tanpa bias autokorelasi spasial.
2. **The Temporal Consistency Gap:** Membandingkan peta 2019 dan 2024 secara buta sering menghasilkan *false changes* karena perbedaan liputan awan satelit. **Project Kita:** Menggunakan teknik *Common Spatial Domain*, di mana matriks transisi hanya dihitung dari 118.943 titik yang konsisten tidak tertutup awan di seluruh 6 tahun pengamatan (2019-2024).
3. **The Explanatory Driver Gap:** Penelitian sebelumnya hanya deskriptif (melihat peta berkurang/bertambah). **Project Kita:** Menggunakan *Multivariate Logistic Regression* untuk menghitung probabilitas matematis (*Odds Ratio*) dari jarak ke IKN dan tambang terhadap risiko perubahan lahan.
4. **The Scale Gap (Telecoupling):** Dampak IKN tidak hanya di Kaltim. **Project Kita:** Menguji seluruh pulau Kalimantan untuk menangkap potensi *spillover deforestation* ke provinsi lain.
5. **The Interpretability Gap:** ML sering dianggap *black-box*. **Project Kita:** Menggunakan SHAP *TreeExplainer* untuk membuktikan model beroperasi berdasarkan fisika optik yang logis (mengandalkan NDVI untuk mendeteksi klorofil hutan).

> **Pesan Kunci untuk Dosen:** "Kami tidak sekadar melatih algoritma atau membuat dashboard. Kami berfokus pada **kekokohan validasi spasial**, **konsistensi temporal (Common Domain)**, dan **kuantifikasi probabilitas pendorong (driver analysis)** yang belum disentuh oleh studi sebelumnya."

---

## 3. OUTLINE LAPORAN (BAB 1 - 5)

Gunakan struktur ini untuk mulai menyicil laporan. Jangan memasukkan hasil yang belum di-generate!

### BAB 1 — Pendahuluan
- **Latar Belakang:** Status Kalimantan sebagai kawasan konservasi global vs ancaman megaproyek IKN dan ekstraksi tambang. Kebutuhan monitoring satelit (*Alamgir 2019, Liu 2013*).
- **Rumusan Masalah:** Bagaimana dinamika perubahan tutupan lahan di Kalimantan (2019-2024)? Faktor apa yang secara probabilitas berasosiasi dengan deforestasi dan urbanisasi?
- **Research Gap:** (Ambil dari Poin 2 di atas).
- **Tujuan & Kontribusi:** Menghasilkan pipeline ML dengan validasi yang ketat dan analisis pendorong.

### BAB 2 — Data dan Metodologi
- **Area Studi:** Seluruh provinsi di Pulau Kalimantan.
- **Data Satelit:** Sentinel-2 SR Harmonized (B2, B3, B4, B8, B11, B12, NDVI, NDBI, NDMI, BSI). Grid prediksi 500m.
- **Label:** ESA WorldCover 2021 (30.000 sampel stratified). 11 kelas diciutkan menjadi 5 kelas (Forest, Shrubland, Built-up, Bare/Mining, Water).
- **Algoritma ML:** LightGBM, XGBoost, RF, SVM, MLP, LogReg.
- **Validasi:** Spatial Block GroupKFold (ukuran blok 0.5°).
- **Change Detection:** Konsep *Common Spatial Domain*.
- **Driver Analysis:** Regresi Logistik (IKN distance, Mining density, Elevation, Rainfall).
- **Interpretability:** Konsep SHAP.

### BAB 3 — Hasil Analisis
- **Perbandingan Model:** SVM paling akurat (83.99%), tapi LightGBM dipilih (83.32%) demi efisiensi skala besar.
- **Peta Klasifikasi:** Tren komposisi 2019-2024 didominasi Forest (~77%).
- **Deteksi Perubahan:** Forest gain (10,187 titik) vs Forest loss (6,800 titik). 
- **Analisis Pendorong (Driver):** 
  - Elevasi berasosiasi negatif kuat dengan deforestasi.
  - Jarak ke IKN berasosiasi (meningkatkan odds deforestasi di sekitarnya).
- **Analisis SHAP:** NDVI (0.938) adalah fitur penentu utama, diikuti SWIR B12 (0.470).

### BAB 4 — Pembahasan (Discussion)
- **Mengapa Forest Gain > Loss?** Bahas kemungkinan ini adalah revegetasi semak belukar yang berubah menjadi hutan sekunder (Shrubland → Forest), atau sekadar osilasi spektral klasifikasi musiman.
- **Dampak IKN:** Mengapa urbanisasi skala pulau sangat kecil (0.92%)? Karena dampak IKN saat ini secara spasial masih terpusat di Penajam Paser Utara, belum memicu *urban sprawl* skala Kalimantan secara agregat.
- **Keterbatasan Penelitian (WAJIB ADA):**
  - Prediksi pada 500m vs Training 10m (isiko *mixed pixel*).
  - Regresi logistik menunjukkan **asosiasi**, bukan kausalitas (sebab-akibat) murni.
  - *Rare events*: Kasus ekspansi tambang hanya 421 titik, regresi mungkin kurang robust.
  - Penggunaan label tahun 2021 untuk memprediksi 2019-2024.

### BAB 5 — Kesimpulan
- **Kesimpulan 1:** Pendekatan Spatial CV memberikan akurasi (83%) yang lebih konservatif namun jauh lebih jujur dibanding random split.
- **Kesimpulan 2:** Pembangunan IKN memiliki asosiasi spasial terhadap kehilangan hutan di area sekitarnya, namun secara proporsi pulau, dinamika hutan Kalimantan masih didominasi transisi natural/perkebunan (Forest ↔ Shrubland).
- **Rekomendasi:** Penelitian ke depan disarankan menggunakan resolusi grid lebih rapat (misal 50m) dan metode *Causal Inference* untuk membuktikan sebab-akibat IKN secara definitif.
