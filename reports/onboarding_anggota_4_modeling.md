# 📋 PANDUAN ONBOARDING ANGGOTA 4
# Peran: Penulis BAB III — Bagian Modeling & Statistik

---

## 🎯 Tujuan Dokumen Ini
Tugasmu menjelaskan cara kerja model Machine Learning dan model statistik yang dipakai. Kamu harus bisa menjelaskan: "Model ini dilatih dengan cara apa? Dievaluasi dengan cara apa? Hyperparameter terbaiknya apa?"

---

## 📚 STEP 1: Baca file-file ini

1. **`scripts/train_classification.py`** — Script Python utama training. Baca baris demi baris, pahami alurnya.
2. **`configs/constants.py`** — Lihat `FEATURE_COLS`, `CLASS_NAMES`, `PARAM_GRIDS`
3. **`scripts/dual_driver_analysis.py`** — Regresi Logistik untuk driver analysis
4. **`scripts/shap_classifier.py`** — Analisis SHAP
5. **`reports/audit_teknis_final.md`** Bab 1.1–1.2 — Hasil model yang sudah ada

---

## 🔍 STEP 2: Audit Mandiri — Buka dan Amati Output Nyata

Jalankan Python di terminal untuk melihat hasil aktual:

```bash
python -c "
import pandas as pd, json
# Model comparison
mc = pd.read_csv('results/classification/model_comparison.csv')
print(mc[['model','accuracy','f1_macro','kappa','time_s']])
"
```

Setelah melihat output, jawab pertanyaan ini:
1. **Berapa Overall Accuracy model LightGBM kita?** (catat angkanya: 83.xx%)
2. **Berapa Kappa Cohen-nya?** (catat angkanya: 0.7xxx) Apa artinya secara kualitatif? (Hint: 0.6–0.8 = substantial agreement)
3. **Kelas mana yang paling sulit diklasifikasikan?** (lihat per-class accuracy — mana yang paling rendah?)
4. **Berapa hyperparameter final LightGBM?** (n_estimators, learning_rate, num_leaves)
5. **Apa itu GridSearchCV dan mengapa kita menggunakannya?** (bukan asal tebak hyperparameter)
6. **Apa itu SHAP value?** (jelaskan dalam 1 kalimat — ini mengukur kontribusi tiap fitur terhadap satu prediksi)

---

## 🖥️ STEP 3: Lihat Output Visual

1. Buka `results/classification/confusion_matrices/cm_lgbm.png` — Confusion Matrix LGBM
2. Buka `results/shap/lgbm/shap_summary.png` — SHAP beeswarm plot
3. Di dashboard Streamlit, buka halaman **3_Model_Comparison** dan **7_SHAP_Analysis**

**Pertanyaan setelah melihat:**
- Di confusion matrix, kelas mana yang sering "tertukar" dengan kelas lain?
- Di SHAP plot, fitur mana yang paling berpengaruh (baris paling atas)?

---

## ✅ STEP 4: Checklist sebelum mulai nulis

- [ ] Saya tahu hyperparameter final dari setiap model (ada di `results/classification/summary_lgbm.json`)
- [ ] Saya bisa membaca confusion matrix dan menghitung Producer's vs User's Accuracy
- [ ] Saya tahu apa yang dimaksud dengan SHAP global feature importance
- [ ] Saya paham konsep Spatial Block CV (bukan random split)

---

## 📝 Kerangka yang harus kamu tulis (setengah dari BAB III):

```
3.6 Feature Engineering
    - 6 raw bands + 4 spectral indices = 10 fitur prediktor
    - Justifikasi ilmiah tiap fitur (gunakan reports/variabel_penelitian.md)

3.7 Algoritma Machine Learning
    - LightGBM (arsitektur, hyperparameter akhir)
    - Random Forest
    - XGBoost
    - SVM (kernel RBF)
    - MLP (layer: 128-64-5)
    - Logistic Regression (baseline)

3.8 Hyperparameter Tuning (GridSearchCV)
    - Grid yang dicoba per model
    - Metrik optimasi: F1-Macro (bukan accuracy, karena class imbalance)

3.9 Evaluasi Model
    - Overall Accuracy
    - F1-Score Macro & Weighted
    - Cohen's Kappa (interpretasi: 0.6-0.8 = substantial)
    - Confusion Matrix (per kelas: Producer's & User's Accuracy)

3.10 Change Detection
    - Metode: direct comparison antar tahun
    - Matriks transisi n×n
    - Definisi operasional: deforestasi, urbanisasi, ekspansi tambang

3.11 Regresi Logistik Dual-Driver
    - Model: P(Y=1) = logit(β₀ + β₁·dist_ikn + β₂·mining + β₃·elevation + β₄·rainfall)
    - Interpretasi: Odds Ratio, P-Value, signifikansi α=0.05

3.12 SHAP Analysis
    - Shapley value: dari teori game theory
    - Global importance vs. local explanation
```

**Angka penting yang WAJIB ada di bagian ini:**
- LGBM: `n_estimators=500, learning_rate=0.01, num_leaves=63`
- Training time: LGBM 116s vs SVM 14.343s (justifikasi efisiensi)
- Kappa 0.7795 = "Substantial agreement" (kutip skala Landis & Koch 1977)
