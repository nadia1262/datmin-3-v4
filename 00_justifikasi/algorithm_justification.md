# Justifikasi 6 Algoritma Supervised Learning
## Spatial Predictive Modeling — IDM Desa Kalimantan

> **Konteks:** Regresi tabular, 6.057 observasi × 17 prediktor, target kontinu (skor_idm 0–1), fitur geospasial + socio-economic.

---

## Model 1: Ridge Regression
### *Kategori: Linear / Regularized Model*

**Intuisi:** Ridge = OLS dengan penalti L2 pada koefisien. Dirancang khusus untuk dataset dengan multikolinearitas — persis masalah dataset kita (NTL ↔ builtup ↔ pop_density). Ridge menstabilkan estimasi koefisien yang volatil akibat fitur berkorelasi tinggi.

### Justifikasi Akademik

| Paper | Jean, N. et al. (2016). "Combining satellite imagery and machine learning to predict poverty." |
|---|---|
| **Jurnal** | ***Science***, 353(6301), 790–794 |
| **DOI** | [`10.1126/science.aaf7894`](https://doi.org/10.1126/science.aaf7894) |
| **Kontribusi** | Menggunakan Ridge Regression sebagai final-stage predictor setelah CNN feature extraction untuk poverty prediction di 5 negara Afrika. R² hingga 0.75 untuk asset wealth. **Paper paling berpengaruh** di bidang satellite-based poverty prediction |

### Strength & Weakness (Context IDM)

| ✅ Strength | ❌ Weakness |
|---|---|
| Robust terhadap multikolinearitas (VIF ~8.85 elevation) | Asumsi linearitas — tidak menangkap hubungan non-linear NTL↔IDM |
| Interpretable — koefisien langsung menunjukkan arah & magnitude | Tidak menangkap interaksi antar fitur (elev × accessibility) |
| Sangat cepat, reproducible, deterministic | Underfit jika hubungan sebenarnya curved/threshold-based |
| Baseline yang **wajib ada** untuk pembanding | Performance biasanya kalah dari tree-based models |

### Computational Consideration

| Complexity | **LOW** — O(np²) training, O(np) prediction |
|---|---|
| Waktu training | < 1 detik untuk 6.057 × 17 |
| Scalability | Sangat baik untuk dataset besar |
| Tuning | Minimal — hanya 1 hyperparameter (α) |

---

## Model 2: K-Nearest Neighbors Regression (KNN-R)
### *Kategori: Instance-Based Learning*

**Intuisi:** KNN memprediksi IDM desa berdasarkan rata-rata (weighted) skor desa-desa yang paling "mirip" dalam feature space. Untuk data spasial, ini intuitif: desa dengan NTL, elevasi, dan aksesibilitas serupa kemungkinan punya IDM serupa. KNN secara implisit menangkap **spatial autocorrelation** dalam feature space (bukan geographic space).

### Justifikasi Akademik

| Paper | Ahmed, M. et al. (2023). "Nonparametric prediction for spatial data" |
|---|---|
| **Jurnal** | *Journal of Spatial Econometrics*, 4, Article 7 |
| **DOI** | [`10.1007/s43071-023-00041-2`](https://doi.org/10.1007/s43071-023-00041-2) |
| **Kontribusi** | Memperkenalkan "double nearest neighbor" rule yang mengintegrasikan spatial proximity ke dalam KNN prediction. Menunjukkan KNN efektif untuk nonparametric prediction pada data spatial |

### Strength & Weakness (Context IDM)

| ✅ Strength | ❌ Weakness |
|---|---|
| Non-parametric — **tidak ada asumsi distribusi** | Sensitif terhadap skala fitur → wajib standardize |
| Menangkap non-linearitas dan cluster lokal secara alami | **Curse of dimensionality** — 17 fitur masih aman tapi borderline |
| Intuitif untuk stakeholder: "desa ini mirip desa X, Y, Z" | Lambat saat prediksi (harus hitung jarak ke semua training points) |
| Detector natural untuk **outlier desa** | Tidak menghasilkan feature importance |

### Computational Consideration

| Complexity | **MEDIUM** — O(1) training, O(n × d) prediction per instance |
|---|---|
| Waktu training | Instant (lazy learner) |
| Waktu prediksi | ~2-5 detik untuk 6.057 desa (manageable) |
| Tuning | `k` (jumlah neighbors), distance metric, weighting |

---

## Model 3: Support Vector Regression (SVR)
### *Kategori: Kernel Method*

**Intuisi:** SVR memetakan fitur ke high-dimensional space menggunakan kernel function, menemukan hyperplane optimal yang memaksimalkan margin di ε-tube. Dengan kernel RBF, SVR menangkap hubungan non-linear yang kompleks — seperti threshold effect dimana IDM naik cepat setelah NTL melewati nilai tertentu, lalu saturasi.

### Justifikasi Akademik

| Paper | Wibawa, F. et al. (2023). "Predicting Poverty Percentage Based on Satellite Imagery and POI Using SVR and RF Regression" |
|---|---|
| **Jurnal** | *Journal of Information Systems Engineering and Business Intelligence*, 9(2), 146–157 |
| **DOI** | [`10.20473/jisebi.9.2.146-157`](https://doi.org/10.20473/jisebi.9.2.146-157) |
| **Kontribusi** | Membandingkan SVR vs RF untuk poverty prediction di Jawa Tengah menggunakan NTL, NDVI, dan POI. **Konteks Indonesia langsung** — paling dekat dengan setup kita |

| Paper pendukung | Puttanapong, N. et al. (2022). "Predicting Poverty Using Geospatial Data in Thailand" |
|---|---|
| **Jurnal** | *Sustainability (MDPI)*, 14(9), 5317 |
| **DOI** | [`10.3390/su14095317`](https://doi.org/10.3390/su14095317) |
| **Kontribusi** | Benchmark komprehensif SVR vs RF vs NN untuk spatial poverty prediction. SVR kompetitif pada dataset kecil |

### Strength & Weakness (Context IDM)

| ✅ Strength | ❌ Weakness |
|---|---|
| Kernel trick → menangkap non-linearitas tanpa feature engineering manual | Hyperparameter tuning (C, ε, γ) **sensitif dan mahal** |
| Robust terhadap outlier (ε-insensitive loss) | **Tidak scalable** — O(n²) hingga O(n³) untuk training |
| Bagus untuk dataset medium (6k = sweet spot) | Black-box — sulit interpretasi |
| Validated di konteks poverty prediction Indonesia | Tidak memberikan feature importance natively |

### Computational Consideration

| Complexity | **HIGH** — O(n² · d) hingga O(n³) tergantung kernel cache |
|---|---|
| Waktu training | ~30-120 detik untuk 6.057 × 17 (RBF kernel) |
| Tuning | Grid search 3D (C × ε × γ) = paling mahal dari 6 model |
| Tip | Gunakan `StandardScaler` wajib; mulai dari default sklearn |

---

## Model 4: Random Forest Regression
### *Kategori: Tree-Based (Bagging)*

**Intuisi:** Ensemble dari ratusan decision trees, masing-masing dilatih pada bootstrap sample dan random subset fitur. RF secara alami menangkap: (1) non-linearitas, (2) interaksi fitur (elevation × accessibility), (3) threshold effects. Ini model "workhorse" untuk tabular data.

### Justifikasi Akademik

| Paper | Breiman, L. (2001). "Random Forests." |
|---|---|
| **Jurnal** | *Machine Learning*, 45(1), 5–32 |
| **DOI** | [`10.1023/A:1010933404324`](https://doi.org/10.1023/A:1010933404324) |
| **Kontribusi** | **Paper foundational** yang memperkenalkan Random Forest. >100.000 sitasi. Membuktikan bagging + random feature selection → variance reduction tanpa meningkatkan bias. Menjadi gold standard untuk tabular ML |

### Strength & Weakness (Context IDM)

| ✅ Strength | ❌ Weakness |
|---|---|
| **Robust terhadap multikolinearitas** — fitur redundan hanya mengurangi importance, tidak merusak prediksi | Cenderung **overfit pada data spatial** jika tree depth tidak dikontrol |
| Built-in **feature importance** (MDI & permutation) → langsung untuk SHAP | Tidak bisa extrapolate di luar range training data |
| Robust terhadap outlier dan skewed features | Memory-heavy untuk forest besar (>1000 trees) |
| Tidak perlu feature scaling | Prediksi = average of trees → bias towards mean |
| **Paling sering digunakan** di poverty/development mapping literature | |

### Computational Consideration

| Complexity | **MEDIUM** — O(n · d · n_trees · log n) |
|---|---|
| Waktu training | ~5-15 detik (500 trees, 6.057 × 17) |
| Parallelism | Embarrassingly parallel (`n_jobs=-1`) |
| Tuning | `n_estimators`, `max_depth`, `min_samples_leaf`, `max_features` |

---

## Model 5: XGBoost (Extreme Gradient Boosting)
### *Kategori: Tree-Based Boosting*

**Intuisi:** Sequential ensemble dimana setiap tree memperbaiki **residual error** tree sebelumnya. XGBoost menambahkan regularisasi (L1+L2 pada leaf weights) untuk mencegah overfitting. Ini model paling dominan di kompetisi tabular ML dan benchmark akademik karena kemampuannya menangkap interaksi non-linear yang sangat kompleks.

### Justifikasi Akademik

| Paper | Chen, T. & Guestrin, C. (2016). "XGBoost: A Scalable Tree Boosting System." |
|---|---|
| **Jurnal** | Proc. 22nd ACM SIGKDD International Conference (KDD '16), 785–794 |
| **DOI** | [`10.1145/2939672.2939785`](https://doi.org/10.1145/2939672.2939785) |
| **Kontribusi** | Memperkenalkan XGBoost dengan sparsity-aware split finding dan weighted quantile sketch. **>40.000 sitasi.** De facto standard untuk tabular prediction. Digunakan di >50% winning Kaggle solutions 2015-2020 DAN di ratusan peer-reviewed spatial/socioeconomic papers |

### Strength & Weakness (Context IDM)

| ✅ Strength | ❌ Weakness |
|---|---|
| **Akurasi tertinggi** untuk tabular data secara konsisten | Lebih rentan **overfit** daripada RF tanpa tuning yang baik |
| Built-in regularization (α, λ) → spatial overfitting control | Hyperparameter space lebih besar dari RF |
| Handles missing values natively (meskipun kita sudah impute) | Sequential training → tidak se-parallel RF |
| SHAP integration langsung (`shap.TreeExplainer`) | Butuh early stopping via validation set |
| **Expected: model terbaik di pipeline ini** | |

### Computational Consideration

| Complexity | **MEDIUM-HIGH** — O(n · d · n_rounds · depth) |
|---|---|
| Waktu training | ~10-30 detik (500 rounds, 6.057 × 17) |
| Tuning | `n_estimators`, `max_depth`, `learning_rate`, `subsample`, `colsample_bytree`, `reg_alpha`, `reg_lambda` |
| GPU support | ✅ (tapi tidak perlu untuk dataset ini) |

---

## Model 6: LightGBM (Light Gradient Boosting Machine)
### *Kategori: Advanced Boosting / Ensemble*

**Intuisi:** Evolusi dari XGBoost dengan 2 inovasi kunci: (1) **GOSS** (Gradient-based One-Side Sampling) — mengurangi data points saat training, (2) **EFB** (Exclusive Feature Bundling) — mengurangi fitur efektif. Hasilnya: **2-10× lebih cepat** dari XGBoost dengan akurasi setara atau lebih baik.

### Justifikasi Akademik

| Paper | Ke, G. et al. (2017). "LightGBM: A Highly Efficient Gradient Boosting Decision Tree." |
|---|---|
| **Jurnal** | *Advances in Neural Information Processing Systems 30* (NeurIPS 2017) |
| **Link** | [NeurIPS Proceedings](https://proceedings.neurips.cc/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html) |
| **Kontribusi** | Menunjukkan GOSS + EFB menghasilkan speedup signifikan tanpa kehilangan akurasi. Menjadi alternatif XGBoost yang **lebih efisien** pada dataset besar. **>15.000 sitasi** |

### Strength & Weakness (Context IDM)

| ✅ Strength | ❌ Weakness |
|---|---|
| **Paling cepat** di antara semua boosting models | Untuk dataset kecil (6k), speed advantage **tidak signifikan** |
| Leaf-wise growth → akurasi lebih tinggi pada dataset heterogen | Leaf-wise bisa overfit lebih agresif pada data kecil |
| Handles categorical features natively | Kurang stable dari XGBoost pada dataset kecil |
| Sering menang di benchmark tabular terbaru | API sedikit berbeda dari sklearn convention |

### Computational Consideration

| Complexity | **MEDIUM** — lebih efisien dari XGBoost |
|---|---|
| Waktu training | ~3-10 detik (lebih cepat dari XGBoost) |
| Memory | Lebih hemat dari XGBoost |
| Tuning | Mirip XGBoost + `num_leaves`, `min_child_samples` |

---

# BONUS ANALYSIS

## A. Rekomendasi Pipeline Strategy

```
┌─────────────────────────────────────────────────────┐
│              PIPELINE STRATEGY                       │
│                                                     │
│  BASELINE          → Ridge Regression               │
│  (benchmarks)        (linear reference point)       │
│                    → KNN Regression                  │
│                      (non-parametric reference)     │
│                                                     │
│  MAIN MODELS       → Random Forest  ← workhorse    │
│  (performance)     → XGBoost        ← expected best│
│                    → LightGBM       ← speed check  │
│                                                     │
│  INTERPRETABILITY  → SHAP on XGBoost/RF             │
│  (post-hoc)        → Koefisien Ridge (sanity check) │
│                                                     │
│  STRESS TEST       → SVR (kernel method diversity)  │
│  (robustness)                                       │
└─────────────────────────────────────────────────────┘
```

| Role | Model | Tujuan |
|---|---|---|
| **Linear Baseline** | Ridge | Menetapkan floor: "seberapa baik model linear?" |
| **Non-parametric Baseline** | KNN | Benchmark tanpa asumsi parametrik |
| **Main Model** | XGBoost | Expected best performer, SHAP analysis |
| **Validation Model** | Random Forest | Apakah bagging ≈ boosting? Robustness check |
| **Speed Benchmark** | LightGBM | Apakah lebih cepat = sama baik? |
| **Kernel Diversity** | SVR | Satu-satunya non-tree non-linear model |

## B. Risk Analysis

### Spatial Leakage Risk

| Risk | Level | Mitigasi |
|---|---|---|
| Train-test kontaminasi | **LOW** | GroupKFold by kabupaten_id |
| Spatial autocorrelation residual | **MEDIUM** | Post-hoc Moran's I test planned |
| Neighboring kabupaten similarity | **LOW-MEDIUM** | Kabupaten ID grouping implicitly separates geographic clusters |

### Overfitting Risk per Model

| Model | Risk | Kenapa | Mitigasi |
|---|---|---|---|
| Ridge | **VERY LOW** | L2 regularization built-in | α via CV |
| KNN | **LOW** | Non-parametric, tapi k controls complexity | k via CV |
| SVR | **MEDIUM** | Kernel complexity + hyperparameter sensitivity | Careful C/γ tuning |
| Random Forest | **MEDIUM** | Deep trees memorize spatial patterns | Limit `max_depth`, `min_samples_leaf` |
| XGBoost | **MEDIUM-HIGH** | Sequential fitting pada residuals → overfitting on noise | Early stopping, `reg_alpha/lambda` |
| LightGBM | **HIGH** | Leaf-wise growth aggressive pada dataset kecil | `num_leaves` constraint, `min_child_samples` |

### Multicollinearity Sensitivity

| Model | Sensitivity | Catatan |
|---|---|---|
| Ridge | **Designed for it** ✅ | L2 menstabilkan koefisien berkorelasi |
| KNN | **Immune** | Distance-based, tidak estimate koefisien |
| SVR | **Low** (kernel) | Kernel mapping menghindari kolinearitas langsung |
| Random Forest | **Very Low** | Fitur bersaing di setiap split, tidak saling merusak |
| XGBoost | **Very Low** | Sama dgn RF |
| LightGBM | **Very Low** | Sama dgn RF |

## C. Computational Ranking (ringan → berat)

| Rank | Model | Est. Training Time | Est. CV Time (5-fold) |
|---|---|---|---|
| 1 🟢 | **Ridge** | < 1 detik | < 3 detik |
| 2 🟢 | **KNN** | Instant | ~10 detik |
| 3 🟢 | **LightGBM** | ~5 detik | ~30 detik |
| 4 🟡 | **Random Forest** | ~10 detik | ~60 detik |
| 5 🟡 | **XGBoost** | ~15 detik | ~90 detik |
| 6 🔴 | **SVR** | ~60 detik | ~5-8 menit |

**Total estimated pipeline time:** ~15-20 menit untuk seluruh 6 model × 5-fold CV.

---

## Referensi Lengkap (BibTeX-ready)

| # | Paper | DOI |
|---|---|---|
| 1 | Jean et al. (2016), *Science* | `10.1126/science.aaf7894` |
| 2 | Ahmed et al. (2023), *J. Spatial Econometrics* | `10.1007/s43071-023-00041-2` |
| 3 | Wibawa et al. (2023), *JISEBI* | `10.20473/jisebi.9.2.146-157` |
| 4 | Breiman (2001), *Machine Learning* | `10.1023/A:1010933404324` |
| 5 | Chen & Guestrin (2016), *KDD* | `10.1145/2939672.2939785` |
| 6 | Ke et al. (2017), *NeurIPS* | NeurIPS Proceedings 2017 |
| 7 | Puttanapong et al. (2022), *Sustainability* | `10.3390/su14095317` |
