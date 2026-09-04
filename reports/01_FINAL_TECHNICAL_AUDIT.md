# FINAL TECHNICAL AUDIT (UPDATED)
**Project:** Spatiotemporal Land-Cover Dynamics in Kalimantan Using Sentinel-2 and Supervised Machine Learning  
**Tanggal Audit:** 3 September 2026  
**Status Keseluruhan:** ✅ **YES WITH MINOR FIXES** — Pipeline siap masuk laporan

---

## BAGIAN 1 — GAMBARAN BESAR PROJECT (PIPELINE)

```
[Google Earth Engine]
  Sentinel-2 SR Harmonized (2019-2024) + ESA WorldCover 2021
     ↓
  07_stratified_sampling.js → training_samples_2021.csv (30K titik, 10m)
  09_prediction_grid.js     → prediction_grid_{year}.csv (155K+ titik, 500m)
     ↓
[Python - Classification]
  train_classification.py  → 6 model ML + Spatial Block CV
     ↓
  predict_all_years.py     → predictions_lgbm_{year}.csv (2019-2024)
     ↓
[Python - Analysis V2]
  change_detection_v2.py   → Common Domain 118,943 titik + Matriks Transisi
     ↓
  driver_analysis_v2.py    → Logistic Regression (IKN × Mining)
     ↓
  shap_classifier.py       → SHAP Feature Importance
     ↓
[Dashboard]
  prepare_dashboard_data.py → JSON/CSV ringkasan
  streamlit run dashboard/app.py → 5 halaman interaktif
```

---

## BAGIAN 5 — AUDIT METODOLOGI

### D. Machine Learning (6 Model — Updated)
| Model | N Sampel | OA | F1-Macro | Kappa | Waktu |
|---|---|---|---|---|---|
| **SVM** | 30,000 | **0.8399** | **0.8423** | **0.7884** | 759.9s |
| LightGBM | 30,000 | 0.8332 | 0.8347 | 0.7795 | 116.6s |
| XGBoost | 30,000 | 0.8320 | 0.8337 | 0.7777 | 189.3s |
| MLP | 10,000 | 0.8285 | 0.8328 | 0.7742 | 340.6s |
| RF | 30,000 | 0.8253 | 0.8267 | 0.7690 | 449.5s |
| LogReg | 30,000 | 0.7936 | 0.7931 | 0.7263 | 14.6s |

> SVM tertinggi tetapi LightGBM dipilih karena 6.5× lebih cepat (selisih 0.67%).

---

## BAGIAN 6 — AUDIT HASIL

| Metrik | Nilai | Sumber |
|---|---|---|
| Best OA | 0.8399 (SVM) | `summary_svm.json` |
| Final Model OA | 0.8332 (LightGBM) | `summary_lgbm.json` |
| Common Domain | 118,943 titik | `change_summary.json` |
| Titik Berubah | 19,483 (16.38%) | `change_summary.json` |
| Forest Loss | 6,800 | `change_summary.json` |
| Forest Gain | 10,187 | `change_summary.json` |
| Urbanization | 1,095 | `change_summary.json` |
| Mining Expansion | 421 | `change_summary.json` |
| Top SHAP | NDVI (0.938) | `shap_importance.csv` |

### Temuan Menarik:
- **Forest Gain > Forest Loss** (10,187 vs 6,800) — perlu dibahas
- **Urbanisasi rendah** (0.92%) — dampak IKN masih terlokalisir
- **Mining expansion rare** (421 titik) — interpretasi hati-hati

---

## BAGIAN 7 — RISK REGISTER (UPDATED)

| Masalah | Status | Risiko |
|---|---|---|
| ~~Dashboard output V1~~ | ✅ DIPERBAIKI | 🔴 P0 |
| ~~Teks hardcoded~~ | ✅ DIPERBAIKI | 🔴 P0 |
| ~~SVM subsample 10K~~ | ✅ DIPERBAIKI | 🟠 P1 |
| ~~model_comparison.csv outdated~~ | ✅ DIPERBAIKI | 🔴 P0 |
| ~~Model Comparison caption salah~~ | ✅ DIPERBAIKI | 🔴 P0 |
| Resolusi 10m ≠ 500m | Akui di laporan | 🟠 P1 |
| Asosiasi ≠ Kausal | Gunakan kata "berasosiasi" | 🔴 P0 |
| NDMI redundan | Akui di laporan | 🟢 P2 |
| MLP subsample 10K | Akui di laporan | 🟢 P2 |
| Mining rare events | Akui di laporan | 🟠 P1 |

---

## BAGIAN 12 — EXECUTIVE VERDICT

### ✅ YES WITH MINOR FIXES — Pipeline siap masuk laporan

### 5 Hal Terpenting Dalam 1 Minggu:
1. Mulai tulis draft laporan BAB 1-5
2. Akui keterbatasan: resolusi, asosiasi ≠ kausal, rare events
3. Ganti semua kata "menyebabkan" → "berasosiasi dengan"
4. Screenshot dashboard untuk lampiran
5. Semua anggota pahami: Spatial CV, Common Domain, SHAP

### Ceritakan Project dalam 10 Kalimat:
> "Proyek ini memetakan perubahan tutupan lahan di Kalimantan 2019-2024 menggunakan Sentinel-2. Kami melatih 6 model ML menggunakan 30.000 titik berlabel dari ESA WorldCover 2021. Validasi menggunakan Spatial Block CV agar tidak ada kebocoran spasial. LightGBM terpilih dengan OA 83.32%. Model memprediksi ~155.000 titik per tahun. Analisis perubahan menggunakan 118.943 titik Common Domain. Forest gain (10.187) melebihi forest loss (6.800). Urbanisasi dan tambang relatif rendah. Regresi logistik menunjukkan elevasi berasosiasi negatif terkuat dengan deforestasi. SHAP mengungkap NDVI sebagai fitur paling krusial bagi model."
