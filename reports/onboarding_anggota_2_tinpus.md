# 📋 PANDUAN ONBOARDING ANGGOTA 2
# Peran: Penulis BAB II (Tinjauan Pustaka)

---

## 🎯 Tujuan Dokumen Ini
Tugasmu adalah menulis teori di balik semua yang kita lakukan. Kamu harus memahami mengapa setiap pilihan teknis (Sentinel-2, LightGBM, NDVI, dll) ada justifikasi ilmiahnya — bukan karena asal pilih.

---

## 📚 STEP 1: Baca file-file ini dulu

1. **`00_justifikasi/algorithm_justification.md`** — Ini adalah goldmine-mu. Berisi justifikasi ilmiah setiap algoritma.
2. **`reports/variabel_penelitian.md`** — Penjelasan 10 variabel prediktor dan dasar ilmiahnya
3. **`00_justifikasi/literature_mapping_IDM_spatial_ML.md`** — Peta literatur ML spasial
4. **`configs/constants.py`** — Lihat daftar `FEATURE_COLS` dan `CLASS_NAMES` (baris 1-30 saja)

---

## 🔍 STEP 2: Audit Mandiri — Uji Pemahaman Teknis

Tanpa melihat catatan, jawab:

1. **Apa itu Sentinel-2?** (siapa yang mengoperasikan, resolusi berapa meter, berapa hari sekali melewati satu titik?)
2. **Apa perbedaan band NIR (B8) dengan band SWIR (B11)?** (secara fisika, apa yang dibedakan dari kemampuan deteksinya?)
3. **Apa itu NDVI dan bagaimana rumus matematisnya?** (`(NIR - Red) / (NIR + Red)`)
4. **Mengapa Random Forest disebut "ensemble method"?** (jelaskan konsep voting dari banyak pohon keputusan)
5. **Apa perbedaan LightGBM dengan XGBoost?** (Hint: cara membangun tree-nya berbeda — leaf-wise vs level-wise)
6. **Apa itu Cohen's Kappa dan mengapa lebih baik dari sekedar akurasi?** (Hint: kappa memperhitungkan peluang menebak secara kebetulan)
7. **Apa itu ESA WorldCover 2021?** (dataset apa ini, siapa yang membuatnya, resolusi berapa?)

---

## 🖥️ STEP 3: Lihat Hasil Nyata di Dashboard

1. Buka halaman **3_Model_Comparison** di Streamlit
2. Amati grafik perbandingan 6 model
3. **Pertanyaan:** Mengapa Logistic Regression jauh di bawah model tree-based? Apa yang membuat perbedaan akurasi itu?

---

## ✅ STEP 4: Checklist sebelum mulai nulis BAB II

- [ ] Saya bisa menjelaskan cara kerja LightGBM dengan analogi sederhana
- [ ] Saya tahu rumus NDVI, NDBI, NDMI, BSI
- [ ] Saya tahu apa itu ESA WorldCover dan mengapa dijadikan ground truth
- [ ] Saya paham perbedaan Producer's Accuracy vs User's Accuracy di confusion matrix

---

## 📝 Kerangka BAB II yang harus kamu tulis:

```
BAB II TINJAUAN PUSTAKA
2.1 Remote Sensing & Citra Satelit
    - Pengertian remote sensing
    - Sentinel-2: karakteristik teknis (13 band, resolusi 10m, revisit time 5 hari)
    - Keunggulan vs Landsat (resolusi lebih tinggi, lebih baru)
2.2 Indeks Spektral
    - NDVI (vegetasi)
    - NDBI (bangunan)
    - NDMI (kelembaban)
    - BSI (tanah terbuka)
2.3 Machine Learning untuk Klasifikasi Tutupan Lahan
    - Decision Tree → Random Forest → Gradient Boosting (XGBoost/LightGBM)
    - Support Vector Machine (SVM)
    - Multi-layer Perceptron (MLP)
    - Logistic Regression (baseline)
2.4 Evaluasi Model Klasifikasi
    - Overall Accuracy, F1-Score, Cohen's Kappa
    - Confusion Matrix: Producer's vs User's Accuracy
2.5 Land Use/Land Cover Change (LULCC)
    - Definisi change detection
    - Matriks transisi antar kelas
2.6 Regresi Logistik Biner untuk Analisis Spasial
    - Logit model, Odds Ratio, interpretasi koefisien
    - Pseudo R² (McFadden)
2.7 IKN dan Konteks Kebijakan
    - Lokasi, skala investasi, timeline konstruksi
    - Potensi dampak ekologi
2.8 Kajian Penelitian Terdahulu (minimal 5 paper)
```

**Minimal 10 referensi yang harus dicari di Google Scholar:**
- "Sentinel-2 land cover classification machine learning"
- "LightGBM remote sensing image classification"
- "LULCC Kalimantan Borneo deforestation"
- "Spatial cross-validation remote sensing"
- "IKN Nusantara environmental impact"
