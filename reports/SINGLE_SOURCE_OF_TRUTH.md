# 📌 SINGLE SOURCE OF TRUTH — Semua Angka Final Project
## Terakhir diupdate: 30 Agustus 2026

> **ATURAN: Semua anggota tim WAJIB mengambil angka dari dokumen ini.**
> **JANGAN hitung sendiri, JANGAN ambil dari file lain.**
> **Jika ada angka yang tidak ada di sini, minta coding lead untuk menambahkan.**

---

## 1. DATA

| Item | Nilai | Sumber |
|------|-------|--------|
| Total training samples | 30,000 | `data/samples/training_samples_2021.csv` |
| Training tahun | 2021 | ESA WorldCover v200 |
| Training resolution | 10m | GEE script 07 |
| Prediction resolution | 500m | GEE script 09, `PREDICTION_SCALE = 500` |
| Jumlah fitur input (X) | 10 | 6 band + 4 indeks |
| Fitur input | B2, B3, B4, B8, B11, B12, NDVI, NDBI, NDMI, BSI | `configs/constants.py` |
| Jumlah kelas (Y) | 5 | Forest, Shrubland/Agri, Built-up, Bare/Mining, Water |
| Spatial blocks | 279 | GroupKFold blocks dari 0.5° grid |
| CV folds | 5 | GroupKFold |

### Distribusi Kelas Training
| Kelas | ID | Jumlah |
|-------|---|--------|
| Forest | 0 | 10,000 |
| Shrubland/Agriculture | 1 | 8,000 |
| Built-up | 2 | 5,000 |
| Bare/Mining-like | 3 | 3,000 |
| Water | 4 | 4,000 |

### Grid Prediksi Per Tahun
| Tahun | Titik | Ukuran File |
|-------|-------|-------------|
| **2018** | **13,632** | **3.3 MB** |
| 2019 | 175,384 | 42.2 MB |
| 2020 | 176,624 | 42.5 MB |
| 2021 | 162,940 | 39.2 MB |
| 2022 | 160,261 | 38.5 MB |
| 2023 | 159,949 | 38.5 MB |
| 2024 | 154,137 | 37.1 MB |

---

## 2. PERFORMA MODEL

| Rank | Model | OA | F1-Macro | F1-Weighted | Kappa | Time (s) | n_samples |
|------|-------|----|----------|-------------|-------|----------|-----------|
| 🥇 | **LightGBM** | **0.8332** | **0.8347** | **0.8336** | **0.7795** | 116.6 | 30,000 |
| 2 | XGBoost | 0.8320 | 0.8337 | 0.8323 | 0.7777 | 189.3 | 30,000 |
| 3 | SVM | 0.8320 | 0.8371 | 0.8323 | 0.7789 | 14,343.7 | **10,000** ⚠️ |
| 4 | MLP | 0.8285 | 0.8328 | 0.8286 | 0.7742 | 340.6 | **10,000** ⚠️ |
| 5 | Random Forest | 0.8253 | 0.8267 | 0.8258 | 0.7690 | 449.5 | 30,000 |
| 6 | Logistic Regression | 0.7936 | 0.7931 | 0.7931 | 0.7263 | 14.6 | 30,000 |

> ⚠️ SVM dan MLP di-CV pada 10,000 subset. Perbandingan tidak 100% fair.
> ⚠️ SVM F1-macro (0.8371) sebenarnya tertinggi, tapi pada subset yang lebih kecil.

### Per-Class Accuracy (LightGBM)
| Kelas | Producer's Acc | User's Acc | IoU |
|-------|---------------|------------|-----|
| Forest | 84.12% | 85.85% | 73.88% |
| Shrubland/Agriculture | 77.55% | 76.58% | 62.74% |
| Built-up | 83.47% | 81.43% | 70.16% |
| Bare/Mining-like | 78.32% | 77.71% | 64.05% |
| Water | 94.90% | 94.96% | 90.37% |

### Best Hyperparameters (LightGBM)
- n_estimators: 500
- max_depth: -1 (unlimited)
- learning_rate: 0.01
- num_leaves: 63

---

## 3. KOMPOSISI TUTUPAN LAHAN (Model: LGBM, Common Domain)

> **Catatan Penting**: Angka ini dihitung HANYA pada *common spatial domain* (118,943 titik) yang memiliki coverage konsisten sepanjang 2019–2024.

| Tahun | Forest (%) | Shrubland (%) | Built-up (%) | Bare/Mining (%) | Water (%) | N titik |
|-------|-----------|---------------|-------------|-----------------|---------|---------|
| 2019 | 75.33 | 18.06 | 1.83 | 0.49 | 4.29 | 118,943 |
| 2020 | 76.01 | 17.86 | 1.41 | 0.50 | 4.22 | 118,943 |
| 2021 | 76.43 | 16.92 | 1.40 | 0.48 | 4.77 | 118,943 |
| 2022 | 79.68 | 13.62 | 1.25 | 0.81 | 4.64 | 118,943 |
| 2023 | 77.16 | 14.86 | 2.10 | 1.11 | 4.77 | 118,943 |
| 2024 | 76.60 | 16.27 | 1.81 | 0.56 | 4.75 | 118,943 |

> ⚠️ **2018 DIKELUARKAN** dari analisis utama karena spatial coverage-nya hanya 7.8% dari coverage 2019, sehingga secara fundamental tidak *comparable*.

---

## 4. CHANGE DETECTION (2019→2024, Model: LGBM, Common Domain)

| Metrik | Nilai |
|--------|-------|
| Total matched points | 118,943 |
| Changed points | 19,483 |
| Change rate | 16.38% |
| Forest loss | 6,800 titik |
| Forest gain | 10,187 titik |
| Urbanization | 1,095 titik |
| Mining expansion | 421 titik |

### Transisi Utama
| Dari → Ke | Jumlah | Persen |
|-----------|--------|--------|
| Shrubland → Forest | 9,694 | 8.15% |
| Forest → Shrubland | 6,215 | 5.23% |
| Built-up → Shrubland | 1,081 | 0.91% |
| Shrubland → Built-up | 623 | 0.52% |
| Forest → Built-up | 409 | 0.34% |
| Built-up → Forest | 372 | 0.31% |

---

## 5. DRIVER ANALYSIS (Regresi Logistik, 2019→2024)

### A. Deforestation Model (n=118,943, n_positive=6,800)
| Variabel | Koefisien | P-Value | Odds Ratio | Signifikan? |
|----------|-----------|---------|------------|------------|
| Intercept | -2.996 | <0.001 | 0.050 | ✅ |
| distance_to_ikn | +0.103 | <0.001 | 1.108 | ✅ *** |
| mining_density_10km | +0.065 | <0.001 | 1.068 | ✅ *** |
| elevation | -0.777 | <0.001 | 0.460 | ✅ *** |
| rainfall_annual | -0.097 | <0.001 | 0.908 | ✅ *** |
| **Pseudo R²** | **0.0321** | | | |

### B. Urbanization Model (n=118,943, n_positive=1,095)
| Variabel | Koefisien | P-Value | Odds Ratio | Signifikan? |
|----------|-----------|---------|------------|------------|
| Intercept | -4.883 | <0.001 | 0.008 | ✅ |
| distance_to_ikn | -0.058 | 0.087 | 0.944 | ❌ |
| mining_density_10km | +0.195 | <0.001 | 1.215 | ✅ *** |
| elevation | -0.491 | <0.001 | 0.612 | ✅ *** |
| rainfall_annual | -0.251 | <0.001 | 0.778 | ✅ *** |
| **Pseudo R²** | **0.0414** | | | |

### C. Mining Expansion Model (n=118,943, n_positive=421)
| Variabel | Koefisien | P-Value | Odds Ratio | Signifikan? |
|----------|-----------|---------|------------|------------|
| Intercept | -5.921 | <0.001 | 0.003 | ✅ |
| distance_to_ikn | -0.243 | <0.001 | 0.784 | ✅ *** |
| mining_density_10km | +0.232 | <0.001 | 1.261 | ✅ *** |
| elevation | -0.261 | 0.001 | 0.770 | ✅ *** |
| rainfall_annual | -0.316 | <0.001 | 0.729 | ✅ *** |
| **Pseudo R²** | **0.0664** | | | |

---

## 6. SHAP FEATURE IMPORTANCE (LightGBM)

| Rank | Feature | Mean |SHAP| |
|------|---------|---------------|
| 1 | **NDVI** | **0.938** |
| 2 | B12 | 0.470 |
| 3 | B11 | 0.443 |
| 4 | B3 | 0.217 |
| 5 | NDBI | 0.178 |
| 6 | B2 | 0.166 |
| 7 | BSI | 0.159 |
| 8 | B4 | 0.154 |
| 9 | B8 | 0.140 |
| 10 | NDMI | 0.046 |

> NDVI sangat dominan (2x runner-up). NDMI hampir tidak berkontribusi karena redundan dengan NDBI.

---

## 7. FITUR KORELASI TINGGI (>0.9)

| Feature A | Feature B | Correlation |
|-----------|-----------|-------------|
| NDBI | NDMI | **-1.000** ⚠️ identik |
| B2 | B3 | 0.974 |
| B3 | B4 | 0.960 |
| B2 | B4 | 0.932 |
| B11 | B12 | 0.928 |

---

## 8. KONFIGURASI TEKNIS

| Parameter | Nilai |
|-----------|-------|
| Random Seed | 42 |
| Sentinel-2 Collection | COPERNICUS/S2_SR_HARMONIZED |
| Cloud Threshold | 20% |
| Label Source | ESA WorldCover v200 (2021) |
| Study Area | Kalimantan bbox (108.5°-119.5°E, 4.5°N-4.2°S) |
| IKN Center | -1.128°S, 116.847°E |
| Spatial Block Size | 0.5° (~55 km) |
| Python | 3.10+ |
