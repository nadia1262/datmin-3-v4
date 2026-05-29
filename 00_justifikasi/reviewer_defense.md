# Reviewer Defense Document
## Spatial Predictive Modeling of IDM — Kalimantan

> Dokumen ini menjawab **14 serangan reviewer + 3 killer questions** secara spesifik dengan bukti empiris.

---

# 🔴 KATEGORI 1 — DATA INTEGRITY & MISSINGNESS

## Attack 1: "Kenapa 559 desa di-drop? Apakah missingness ini benar-benar random?"

**Jawaban:**

559 desa (8,5%) di-drop karena kegagalan crosswalk kode Kemendagri ↔ BPS akibat pemekaran wilayah (DOB). Ini **bukan random** dalam hal karakteristik spasial, tapi **random dalam hal target variable**.

**Bukti empiris (Mann-Whitney U Test):**

| Metrik | Kept (n=6.057) | Dropped (n=559) | Diff |
|---|---|---|---|
| Mean skor_idm | 0.7113 | 0.7089 | **0.0024** |
| Median skor_idm | 0.7019 | 0.6960 | 0.0059 |
| Std skor_idm | 0.0892 | 0.0912 | 0.0020 |
| **Mann-Whitney p-value** | | | **0.316 (p > 0.05)** |

> **Kesimpulan:** Distribusi skor IDM antara desa yang di-drop dan dipertahankan **tidak berbeda secara statistik signifikan** (U test, p=0.316). Drop ini tidak menyebabkan bias pada target variable.

**Distribusi status IDM juga hampir identik:**

| Status | Kept | Dropped | Diff |
|---|---|---|---|
| Berkembang | 45.1% | 47.9% | 2.8% |
| Maju | 32.8% | 29.0% | 3.8% |
| Mandiri | 14.3% | 15.0% | 0.8% |
| Tertinggal | 7.8% | 7.9% | 0.1% |

---

## Attack 2: "Apakah data yang di-drop menyebabkan spatial bias?"

**Jawaban jujur: YA, ada spatial bias dalam prediktor — tapi TIDAK dalam target.**

| Feature | Kept Mean | Dropped Mean | Diff% |
|---|---|---|---|
| ntl_mean_2021 | 0.2062 | **0.0000** | **100%** |
| builtup_fraction | 0.0069 | 0.0012 | 83.3% |
| pop_density | 94.63 | 30.78 | 67.5% |
| elevation_mean | 95.72 | 39.39 | 58.8% |
| evi_mean | 0.4658 | 0.4793 | 2.9% |
| lst_day_mean | 28.63 | 28.65 | 0.1% |

**Interpretasi:** Desa yang di-drop cenderung **lebih rural dan dataran rendah** (NTL = 0, pop_density rendah). Ini masuk akal — desa DOB biasanya berada di wilayah frontier yang baru dimekarkan. Namun, karena skor IDM mereka **tidak berbeda signifikan**, eliminasi ini **tidak membiaskan kemampuan prediksi model terhadap IDM**.

**Mitigasi di paper:** Acknowledge bahwa desa sangat terpencil (NTL=0) sedikit under-represented. Ini menjadi **limitation**, bukan fatal flaw.

---

## Attack 3: "Kenapa tidak menggunakan spatial join atau fuzzy matching?"

**Jawaban:**

Kami **sudah** menggunakan crosswalk multi-tahap (`build_crosswalk_v2.py`):
1. **Exact match** pada kode Kemendagri 10-digit
2. **Partial match** pada 4-digit pertama (kabupaten) + nama desa
3. Desa yang gagal di kedua tahap = genuinely unresolvable karena **kode baru dari Permendagri yang belum diadopsi BPS**

Spatial join (by coordinate/polygon overlap) **tidak feasible** karena:
- Desa yang gagal match **tidak memiliki boundary polygon** (mereka tidak ada di shapefile BPS)
- Tanpa polygon = tidak bisa di-overlay
- Fuzzy name matching rentan false positive (banyak nama desa identik antar kabupaten: "Sumber Makmur", "Sumber Jaya", dll.)

---

# 🔴 KATEGORI 2 — TEMPORAL CONSISTENCY

## Attack 4 & 5: "Bagaimana mengatasi ketidaksinkronan temporal?"

**Jawaban:**

Kami **mengkategorikan variabel berdasarkan sifat temporal** dan menerapkan prinsip **"features precede target"**:

| Kategori | Variabel | Tahun | Justifikasi |
|---|---|---|---|
| **Dynamic features** | NTL, EVI, LST, CHIRPS, PDRB | **2021** | Dipilih 1 tahun sebelum target (IDM 2022) secara **intentional** untuk mencegah data leakage dan memastikan arah prediksi temporal yang benar |
| **Slow-changing** | GHSL built-up, WorldPop | **2020** | Urbanisasi dan populasi berubah lambat (∆ < 5%/tahun). Lag 2 tahun = negligible |
| **Static/structural** | SRTM, Hansen baseline, accessibility | **2000/2015** | Topografi **tidak berubah**. Infrastruktur jalan di pedalaman Kalimantan juga relatif stabil. Ini bukan "data lama" — ini **structural constraints** yang timeless |
| **Cumulative** | Hansen forest loss | **2001-2022** | Agregasi kumulatif by design — menangkap trajectory deforestasi |

> **Kunci defense:** Kami **tidak** menggabungkan snapshot tahun berbeda secara naif. Desain temporal mengikuti prinsip: *structural variables are timeless, dynamic variables precede the target by 1-2 years to ensure predictive (not contemporaneous) validity.*

---

# 🔴 KATEGORI 3 — FEATURE ENGINEERING & REDUNDANCY

## Attack 6: "Kenapa tidak pakai PCA untuk urbanization proxies?"

**Jawaban:**

PCA **dipertimbangkan tapi tidak digunakan** karena 3 alasan:

1. **Interpretability loss**: PC1 dari NTL+builtup+pop_density akan kehilangan makna domain-specific. SHAP analysis membutuhkan fitur individual yang interpretable untuk policy recommendation
2. **VIF sudah efektif**: Setelah iterative VIF filtering (threshold=10), semua fitur memiliki VIF < 9. Multikolinearitas sudah terkontrol tanpa mengorbankan interpretability
3. **Non-linear models**: Random Forest dan XGBoost **robust terhadap multikolinearitas** — mereka memilih fitur secara kompetitif di setiap split. PCA lebih krusial untuk model linear

**Namun**, sebagai **robustness check** (future work), membandingkan performa model dengan dan tanpa PCA pada urban proxies = contribution tambahan yang valuable.

---

## Attack 7: "Model ini mengukur pembangunan desa, atau hanya derajat urbanisasi?"

**Jawaban (ini critical — harus diframing ulang):**

> **Framing yang benar:** Penelitian ini bukan mengklaim mengukur "pembangunan desa" secara holistik. Kami mengklaim bahwa **sinyal spasial yang dapat diamati dari satelit** (urbanitas, aksesibilitas, lingkungan) dapat **memprediksi variasi skor IDM** — sebuah indeks yang sendirinya merupakan proxy pembangunan.

Model ini memang menangkap **urbanization gradient** sebagai sinyal dominan. Tapi ini BUKAN kelemahan — ini **temuan substantif**:

- IDM memang **heavily correlated with urbanization** (desa urban = akses listrik, jalan, pasar, sekolah = skor tinggi)
- Kontribusi kami: **mengkuantifikasi seberapa besar** variasi IDM yang bisa dijelaskan oleh observable spatial signals, dan **mengidentifikasi desa-desa yang menyimpang** dari pattern ini (outlier analysis via residuals)

**Desa dengan IDM tinggi tapi NTL rendah** = desa yang berhasil membangun tanpa sinyal urbanisasi → **ini insight kebijakan yang genuine**.

---

## Attack 8: "Kenapa gHM dihapus, padahal itu composite yang lebih stabil?"

**Jawaban:**

Argumen "composite lebih stabil" valid secara umum, tapi **tidak berlaku** ketika komponennya sudah menjadi prediktor individual:

| gHM Component | Sudah ada sebagai fitur? |
|---|---|
| Nighttime lights | ✅ `ntl_mean_2021` |
| Built-up area | ✅ `builtup_fraction` |
| Population density | ✅ `pop_density` |
| Cropland | ❌ (tidak ada) |
| Road density | ❌ (tidak ada) |

- 3 dari 5 kategori stressor gHM sudah ter-representasi → **memasukkan gHM = meng-amplifikasi bobot 3 fitur tersebut secara tidak transparan**
- Dalam tree-based models, ini menyebabkan **feature importance yang misleading** — gHM akan "mencuri" importance dari NTL/builtup karena ia mengandung keduanya
- Korelasi empiris: gHM × pop_density = **0.65**, gHM × builtup = **0.54**

---

# 🔴 KATEGORI 4 — METHODOLOGY

## Attack 9: "Apakah memperhitungkan spatial autocorrelation dalam residual?"

**Jawaban jujur:**

Saat ini **belum** dilakukan Moran's I test pada residual. Ini direncanakan sebagai **post-modeling diagnostic** setelah model terbaik terpilih.

**Defense:** 
- GroupKFold by kabupaten **secara implisit** memitigasi spatial autocorrelation karena memastikan kabupaten yang berdekatan tidak berada di fold yang sama (kabupaten ID berurutan secara geografis)
- Moran's I pada residual akan dilakukan sebagai **validation step** — jika signifikan, kami akan mendiskusikannya sebagai limitation dan merekomendasikan spatial error model sebagai future work

---

## Attack 10: "Apakah train-test split mempertimbangkan spatial leakage?"

**Jawaban:**

**YA.** Kami menggunakan `GroupKFold(n_splits=5)` yang dikelompokkan berdasarkan `kabupaten_id` (56 kabupaten). Ini memastikan:

1. **Seluruh desa dalam satu kabupaten** berada di fold yang sama (train ATAU test, tidak pernah keduanya)
2. Model diuji pada **kabupaten yang belum pernah dilihat** → menguji kemampuan generalisasi spasial
3. Ini **lebih ketat** dari random split dan dari stratified split — karena spatial neighbors tidak bocor antar fold

**Referensi:** Roberts et al. (2017), "Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure," *Ecography*, DOI: 10.1111/ecog.02881

---

## Attack 11: "Kenapa ML, bukan spatial econometric (SAR/SEM)?"

**Jawaban:**

| Aspek | ML (RF/XGBoost) | Spatial Econometric (SAR/SEM) |
|---|---|---|
| **Non-linearity** | ✅ Menangkap interaksi non-linear | ❌ Asumsi linear |
| **Feature interactions** | ✅ Otomatis | ❌ Harus dispecify manual |
| **Scalability** | ✅ 6.057 obs × 17 fitur = ringan | ⚠️ Spatial weight matrix 6.057×6.057 = komputasi berat |
| **Interpretability** | ✅ SHAP decomposition | ✅ Koefisien langsung |
| **Spatial structure** | ⚠️ Via GroupKFold + residual check | ✅ Built-in |

**Posisi kami:** ML dipilih karena tujuan utama adalah **predictive accuracy**, bukan causal inference. SAR/SEM lebih tepat untuk estimasi efek kausal spillover, yang bukan scope penelitian ini. Namun, perbandingan ML vs SAR/SEM merupakan **future work** yang legitimate.

---

# 🔴 KATEGORI 5 — INTERPRETATION & POLICY

## Attack 12: "Model ini untuk kebijakan, atau hanya prediksi statistik?"

**Jawaban (harus hati-hati framing):**

> Model ini adalah **alat prediksi dan screening**, bukan **alat kebijakan langsung**.

Kontribusi untuk kebijakan:
1. **Identifikasi desa underperforming**: Desa dengan prediksi IDM tinggi tapi aktual rendah → butuh investigasi lapangan
2. **Prioritisasi**: Ranking desa berdasarkan predicted IDM untuk alokasi sumber daya
3. **SHAP-based insight**: Fitur mana yang paling memengaruhi prediksi untuk kluster desa tertentu

**Yang TIDAK kami klaim:** Model ini TIDAK mengatakan "tingkatkan NTL untuk meningkatkan IDM" — itu causal claim yang butuh desain eksperimental.

---

## Attack 13: "Jika model hanya menangkap urban-rural gradient, apa kontribusi ilmiahnya?"

**Jawaban:**

Kontribusi ilmiah bukan pada **temuan bahwa desa urban = IDM tinggi** (itu trivial). Kontribusinya ada pada:

1. **Kuantifikasi**: Seberapa besar (R²) variasi IDM yang bisa diprediksi hanya dari sinyal satelit? Ini belum pernah diukur untuk IDM level desa di Kalimantan
2. **Feature importance ranking**: Fitur spasial mana yang paling prediktif? Apakah aksesibilitas > NTL > vegetasi? Ini policy-relevant
3. **Residual analysis**: Desa yang **menyimpang** dari prediksi model = **desa yang interesting secara kebijakan** (overperforming atau underperforming relatif terhadap kondisi spasialnya)
4. **Methodological template**: Pipeline GEE → VIF → GroupKFold → SHAP yang reproducible untuk seluruh Indonesia

---

## Attack 14: "Bagaimana memastikan model tidak hanya belajar proxy ekonomi makro?"

**Jawaban:**

Kami menguji ini melalui **ablation study** (direncanakan post-modeling):
- Model A: Full features (17)
- Model B: Tanpa NTL (proxy ekonomi utama)
- Model C: Hanya variabel lingkungan (EVI, elevation, forest, rain)
- Jika Model C masih memiliki R² > 0: variabel lingkungan memberikan informasi **independen** dari proxy ekonomi

Tambahan: PDRB per kapita kabupaten telah ditambahkan sebagai **explicit macro-economic control**. Jika NTL masih significant setelah mengontrol PDRB → NTL menangkap **variasi intra-kabupaten** yang PDRB tidak bisa.

---

# 💀 KILLER QUESTIONS

## Killer 1: "R-Square kamu cuma 25%, ini artinya ML kamu gagal dan kita tetap butuh survei kan?"

**Jawaban (Gunakan framing "Auditor", BUKAN "Pengganti"):**

> "Tepat sekali, Bapak/Ibu. Dan itu adalah **temuan terpenting** dari riset kami. 
> 
> Pertama, ini membuktikan secara empiris bahwa survei Kementerian Desa tidak bisa diganti oleh satelit, karena 75% aspek pembangunan (seperti tata kelola, gotong royong, keberadaan bidan) bersifat non-fisik dan *irreplaceable*. Jika kami mengklaim R² 90%, kami justru membohongi metodologi.
> 
> Kedua, **25% variasi fisik** yang tertangkap satelit (jalan, terang lampu, kepadatan) ini BUKAN untuk menggantikan survei, melainkan kami gunakan sebagai **baseline audit (alat anti-fraud)**. Jika prediksi fisik dari model ML kami sangat tinggi (desanya terang dan padat), tapi skor yang dilaporkan Kades sangat rendah (Tertinggal), model kami berhasil mengidentifikasi **anomali/red-flag** bahwa data survei di lapangan kemungkinan dimanipulasi untuk mendapatkan Dana Desa lebih besar. 
> 
> Jadi, model ini bukan pengganti, melainkan **auditor tata kelola spasial yang objektif dan tidak bisa dibohongi**."

## Killer 2: "Apakah IDM bisa diprediksi dari remote sensing variables?"

**Jawaban:**

Ini adalah **research question**, bukan asumsi. Penelitian ini **menguji hipotesis** apakah observable spatial signals berkorelasi cukup kuat dengan IDM untuk menghasilkan prediksi bermakna. R² 25% adalah jawaban empiris dari pertanyaan tersebut — itu merupakan **temuan negatif yang sangat informatif dan publishable** ("IDM didominasi oleh dimensi sosial pembangunan yang memerlukan data survei tradisional, namun 25% footprint fisiknya dapat digunakan sebagai alat cross-validation").

## Killer 3: "Menjelaskan pembangunan, atau hanya memetakan korelasi spasial?"

**Jawaban:**

> Kami secara eksplisit memposisikan penelitian ini sebagai **spatial predictive modeling**, bukan causal explanation.

Kami **TIDAK** mengklaim menjelaskan *mengapa* desa A lebih maju dari desa B. Kami menunjukkan bahwa *observable spatial patterns* dapat **memprediksi** posisi relatif desa pada skala IDM. Ini valid dan useful tanpa perlu klaim kausalitas.

## Killer 4: "Jika semua RS features dihapus, apakah model masih bermakna?"

**Jawaban:**

Tanpa RS features, model hanya punya PDRB per kapita (1 variabel level kabupaten). Model ini akan berfungsi sebagai **naive baseline** dengan R² yang jauh lebih rendah — karena ia hanya membedakan antar kabupaten, bukan antar desa. **Perbedaan R² antara model full vs. PDRB-only** menunjukkan **added value** dari remote sensing features untuk prediksi granular level desa.

---

# ✅ REFRAME KONTRIBUSI FINAL

| ❌ Jangan bilang | ✅ Bilang ini |
|---|---|
| "Model pembangunan desa" | "Spatial predictive model for village development index" |
| "Fitur satelit menjelaskan pembangunan" | "Observable spatial signals predict IDM variation" |
| "Rekomendasi kebijakan" | "Screening tool for identifying underperforming villages" |
| "NTL menyebabkan IDM tinggi" | "NTL is the strongest spatial predictor of IDM" |
