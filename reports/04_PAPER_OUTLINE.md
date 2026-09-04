# Outline Penulisan Paper (Berdasarkan Gaya Habibie et al., 2025)

Berikut adalah struktur detail untuk menulis *paper* atau laporan akhir Anda. Struktur ini 100% mengikuti *flow* dari paper Habibie et al. (2025), namun telah disisipkan sub-bab khusus untuk mengakomodasi analisis Seri Waktu (*Spatiotemporal*) dan Regresi Logistik yang menjadi keunggulan project Anda.

---

### **Abstrak**
*   **Paragraf 1:** Latar belakang (Pembangunan IKN di Kalimantan dan pentingnya pemantauan tutupan lahan).
*   **Paragraf 2:** Metode Utama (Integrasi Sentinel-2, ESA WorldCover 2021, *Machine Learning*, dan *Spatial Block CV*).
*   **Paragraf 3:** Hasil (SVM memiliki akurasi spasial tertinggi 83.99%, namun LightGBM (83.32%) dipilih sebagai model operasional terbaik karena efisiensi waktu komputasinya yang 6.5x lebih cepat).
*   **Paragraf 4:** Analisis Lanjutan (Transisi lahan 2019-2024 via *Common Domain*, analisis faktor pendorong/regresi, dan interpretasi SHAP).
*   **Kata Kunci:** Sentinel-2; ESA WorldCover; Machine Learning; Spatiotemporal Analysis; IKN; Land Cover Classification; Explainable AI (SHAP).

---

### **1. Pendahuluan**
*   **1.1. Latar Belakang Lingkungan:** Pentingnya pemantauan tutupan lahan global dan peran Kalimantan sebagai paru-paru dunia.
*   **1.2. Konteks Pembangunan IKN:** Ancaman deforestasi, urbanisasi, dan ekspansi infrastruktur/tambang akibat pemindahan ibu kota ke Kalimantan Timur.
*   **1.3. Peran Remote Sensing & ML:** Mengapa satelit (Sentinel-2) dan Algoritma ML lebih superior dari metode tradisional. Keterbatasan penelitian sebelumnya (misal: hanya melihat 1 tahun, skala terlalu kecil, validasi bias).
*   **1.4. Tujuan Penelitian:**
    1. Mengevaluasi akurasi 6 algoritma ML dalam memetakan tutupan lahan menggunakan pendekatan *Spatial Cross-Validation*.
    2. Mendeteksi perubahan tutupan lahan di seluruh Kalimantan (2019-2024) menggunakan *Common Spatial Domain*.
    3. Mengukur pengaruh faktor IKN, pertambangan, dan alam terhadap deforestasi.
    4. Menginterpretasikan model menggunakan SHAP *Analysis*.

---

### **2. Materi dan Metode**
*   **2.1. Wilayah Studi:** Deskripsi Pulau Kalimantan (Luas, iklim tropis, signifikansi ekologis, dan posisi IKN).
*   **2.2. Metodologi:** Penjelasan umum kerangka kerja (*Flowchart* dari GEE hingga interpretasi SHAP).
*   **2.3. Pengumpulan dan Persiapan Data**
    *   *2.3.1. Data Satelit (Sentinel-2):* Proses komposit median tahunan dan masking awan (QA60).
    *   *2.3.2. Data Topografi dan Lingkungan:* Penggunaan SRTM (Elevasi) dan curah hujan.
    *   *2.3.3. Indeks Lingkungan:* Formula dan tujuan penggunaan indeks (NDVI, NDBI, NDMI, BSI).
    *   *2.3.4. ESA WorldCover:* Justifikasi penggunaan peta 2021 sebagai *Ground Truth* tunggal untuk ekstraksi sampel (30.000 titik). Konsep *Temporal Transferability*.
*   **2.4. Pemrosesan dan Ekspor Data:** Pemrosesan di GEE dan pengeksporan *prediction grid* berskala 500m (mempertimbangkan batas komputasi memori).
*   **2.5. Pelatihan Model ML dan Optimasi Hyperparameter:** Deskripsi 6 model yang diuji (SVM, LightGBM, XGBoost, Random Forest, MLP/ANN, Logistic Regression).
*   **2.6. Proses Optimasi & Validasi Spasial:** Penjelasan penggunaan Optuna dan **Spatial Block GroupKFold CV (0.5°)** untuk mencegah kebocoran spasial (*spatial data leakage*). *(Ini nilai jual utama Anda!)*
*   **2.7. Metrik Evaluasi Model:** Rumus OA, F1-Score, Precision, Recall.
*   **2.8. Deteksi Perubahan Temporal & Analisis Penggerak:**
    *   Konsep *Common Spatial Domain* (118.943 titik) untuk melacak tren 2019-2024 tanpa *noise* awan.
    *   Penggunaan *Logistic Regression* (Odds Ratio) untuk menganalisis pendorong deforestasi.
*   **2.9. Analisis SHAP:** Penjelasan SHAP (SHapley Additive exPlanations) untuk melihat seberapa besar pengaruh setiap fitur terhadap keputusan model ML.

---

### **3. Hasil**
*   **3.1. Distribusi Tutupan Lahan dan Korelasi Fitur:** Statistik deskriptif dari 30.000 data *training* (Tabel frekuensi dan matriks korelasi antar fitur satelit).
*   **3.2. Analisis Distribusi dan Potensi Outlier:** Boxplot dari nilai indeks spektral (NDVI, BSI, dll) per kelas tutupan lahan.
*   **3.3. Perbandingan Kinerja Model:** Tabel raksasa berisi Akurasi, F1, Waktu Latih dari keenam model ML. Perlihatkan bahwa SVM memenangkan Akurasi (83.99%), tetapi LightGBM menang secara operasional (116.6 detik vs 759.9 detik).
*   **3.4. Dashboard Optimasi:** Visualisasi kurva tuning parameter (Optuna/GridSearch).
*   **3.5. Kinerja Model Machine Learning:**
    *   *3.5.1. LightGBM:* (Model yang diplilih untuk operasional/prediksi seri waktu, detailkan *confusion matrix*-nya).
    *   *3.5.2. SVM:* (Bahas tingginya akurasi namun harganya yang mahal di waktu komputasi).
    *   *3.5.3. XGBoost, Random Forest, ANN, dan Linear Models:* (Model perbandingan lainnya).
*   **3.6. Kepentingan Fitur (*Feature Importance*):** *Bar chart* fitur terpenting bawaan algoritma ML.
*   **3.7. Analisis SHAP:** *Summary Plot* SHAP. Tunjukkan bagaimana NDVI dan Elevasi sangat mendominasi arah keputusan model.
*   **3.8. Deteksi Perubahan Spatiotemporal (2019-2024):**
    *   Tabel Matriks Transisi 2019 ke 2024.
    *   Angka total Forest Loss (6.800) vs Forest Gain (10.187).
*   **3.9. Pemetaan Skala Mikro (10m) Kawasan Inti IKN:**
    *   Menampilkan visualisasi prediksi 10m khusus di zona KIPP untuk membuktikan kemampuan resolusi tinggi dari model.
*   **3.10. Pendorong Spasial Deforestasi:**
    *   Tabel hasil Regresi Logistik (Nilai P-Value, Koefisien, Odds Ratio).
    *   Temuan bahwa jarak ke IKN atau kepadatan tambang memiliki efek (signifikan/tidak), dikontrol oleh elevasi.

---

### **4. Pembahasan**
*   **4.1. Interpretasi Kinerja Model ML:** Mengapa akurasi berada di kisaran 83-84% (bahas kejujuran validasi *Spatial CV* dibanding *random split*). Bahas juga *trade-off* antara Akurasi (SVM) vs Efisiensi (LightGBM).
*   **4.2. Dinamika Tutupan Lahan & Efek Kelas Campuran (*Mixed Pixels*):** Membahas anomali tingginya *Forest Gain*. Jelaskan secara kritis bahwa ini kemungkinan adalah artefak algoritma (batas spektral yang mirip antara *Forest* dan *Shrubland* pada resolusi 500m), bukan murni reforestasi fisik.
*   **4.3. Dampak Pembangunan IKN dan Penambangan (*Telecoupling*):** Membahas temuan dari regresi logistik. Apakah deforestasi berkumpul di dekat IKN atau menyebar di seluruh pulau?
*   **4.4. Keterbatasan Penelitian:** Mengakui limitasi resolusi 500m yang memicu efek *mixed pixels*, namun menjustifikasinya dengan bukti kemampuan prediksi skala mikro 10m di IKN. Serta rasionalisasi penggunaan label tahun 2021 (*Temporal Transferability*).

---

### **5. Kesimpulan**
*   Kesimpulan 1: Secara teoritis SVM (83.99%) merupakan algoritma paling tangguh, namun LightGBM (83.32%) adalah kombinasi paling efektif dan cepat untuk prediksi operasional di skala pulau Kalimantan.
*   Kesimpulan 2: Fitur spektral (NDVI) dan topografi (elevasi) jauh lebih penting sebagai pembeda dibanding curah hujan.
*   Kesimpulan 3: Pembangunan di Kalimantan memicu transisi lahan yang kompleks, di mana deteksi *machine learning* sering kesulitan membedakan hutan dan semak belukar sekunder pada resolusi 500m.
*   Rekomendasi: Peneliti selanjutnya disarankan menggunakan data *Time-Series/Phenology* (bukan hanya *single-composite*) untuk membedakan lahan dengan lebih akurat.

---

### **Ketersediaan Data**
Menjelaskan bahwa *script* GEE, data *training*, dan *dashboard* interaktif tersedia secara publik (Sertakan tautan Streamlit atau repositori Anda).

### **Ucapan Terima Kasih**
Ucapan terima kasih kepada instansi, dosen pembimbing, ESA (European Space Agency), dan Copernicus Sentinel Hub atas penyediaan data gratis.

### **Daftar Pustaka**
Daftar referensi akademik (termasuk referensi ke Habibie et al., konsep Telecoupling, dan metode Temporal Transferability).
