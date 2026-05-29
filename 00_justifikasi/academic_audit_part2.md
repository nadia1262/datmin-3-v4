# AUDIT AKADEMIK ARSITEKTUR DATASET — BAGIAN 3, 4, 5
## Prediksi IDM Desa Kalimantan via Spatial ML (Lanjutan)

---

# BAGIAN 3 — IDENTIFIKASI KELEMAHAN BESAR

> [!CAUTION]
> Bagian ini ditulis dengan brutal honesty sesuai permintaan. Tidak ada sugarcoating.

## 3.1 Apakah feature set ini terlalu "remote sensing heavy"?

**YA, SECARA DEFINITIF.**

19 fitur aktif yang tersisa semuanya berasal dari raster satelit/GEE. **Zero official statistics** selain IDM (target) itu sendiri. Ini bukan inherently fatal — Jean et al. (2016) membuktikan RS-only approach bisa bekerja — tapi ini menciptakan beberapa risiko:

- Model hanya "melihat" permukaan bumi dari atas. Ia tidak tahu apakah desa punya pasar, sekolah berfungsi, atau kepala desa yang korup.
- Reviewer yang berlatar sosiologi/ekonomi pembangunan akan bertanya: **"Where is the socioeconomic context?"**
- Dari perspektif data mining murni, ini acceptable. Dari perspektif ilmu pembangunan, ini **rapuh**.

## 3.2 Apakah model berisiko hanya belajar "urbanization proxy"?

**SANGAT TINGGI RISIKONYA.**

Perhatikan pola fitur yang tersisa:

| Fitur | Sebenarnya mengukur... |
|---|---|
| `ntl_mean` | Urbanitas |
| `builtup_fraction` | Urbanitas |
| `pop_density` | Urbanitas |
| `ghm_mean` | Urbanitas (composite) |
| `time_city_mean` | Proximity to urbanity |
| `lst_day_mean` | Urban heat (inverse greenness) |

**6 dari 19 fitur (~32%) adalah proxy urbanisasi.** Model kemungkinan besar akan belajar satu pola dominan: **"desa yang lebih urban = IDM lebih tinggi"**. Ini benar secara empiris tapi **trivial secara analitis**.

SHAP analysis nanti kemungkinan besar akan menunjukkan `ntl_mean`, `builtup_fraction`, dan `time_city_mean` mendominasi. Ini bukan insight — ini common sense.

**Pertanyaan penguji sidang:** *"Jadi kesimpulan riset kamu adalah desa yang dekat kota dan terang di malam hari lebih maju? Itu perlu machine learning?"*

## 3.3 Blind spot terbesar tanpa official statistics?

1. **Kualitas governance desa** — kepala desa yang kompeten vs. tidak, ini driver IDM terbesar yang **INVISIBLE** dari satelit
2. **Dana Desa (DD) dan Alokasi Dana Desa (ADD)** — transfer fiskal pusat ke desa. Desa miskin tapi dapat dana besar bisa IDM-nya naik cepat. Satelit tidak menangkap ini
3. **Pendidikan tenaga kerja** — rata-rata tahun sekolah, % lulusan SMA. Ini komponen IKS yang krusial
4. **Akses layanan kesehatan aktual** — travel_time_healthcare proxy, tapi tidak tahu apakah puskesmas itu berfungsi atau hanya papan nama
5. **Struktur ekonomi** — apakah desa pertanian subsisten, sawit industrial, atau perikanan. Satelit tidak bisa membedakan ini dengan baik

## 3.4 Variabel penting yang belum tertangkap?

| Variabel | Pentingnya | Kenapa tidak tertangkap |
|---|---|---|
| Dana Desa per kapita | **SANGAT TINGGI** — fiscal transfer = game-changer | Tidak ada di GEE. Perlu data Kemendesa/DJPK |
| % rumah tangga miskin (P0/P1) | TINGGI — target komplementer | Data BPS, level kab minimum |
| Jarak ke ibukota kecamatan | TINGGI — lebih relevan dari kota 50k | Bisa dihitung tapi butuh data pusat kecamatan |
| Sektor ekonomi dominan | TINGGI — pertanian vs. jasa vs. tambang | Butuh PODES atau BPS |
| Akses internet/sinyal | TINGGI — digital divide = development divide | Tidak ada di GEE |

## 3.5 Risiko jika seluruh prediktor hanya dari raster satelit?

1. **Ecological fallacy** — model memprediksi "tampilan permukaan" bukan "kondisi manusia"
2. **Temporal mismatch** — GEE data tahun bervariasi (2015-2021), IDM tahun 2022. Asumsi temporal alignment tidak selalu valid
3. **Omitted variable bias** — model R² mungkin terlihat bagus (0.4-0.6) tapi residual akan terstruktur secara spasial karena missing socio-economic drivers
4. **Limited policy prescription** — "tingkatkan NTL" bukan rekomendasi kebijakan. "Bangun jalan" bisa, tapi itu butuh travel_time improvement analysis, bukan raw prediction

## 3.6 Apakah model sulit dijelaskan untuk kebijakan publik?

**MEDIUM-HIGH.**

- SHAP bisa membantu interpretability teknis (fitur X penting)
- Tapi **menerjemahkan ke policy action** sulit: "NDVI turun 0.1 menyebabkan IDM turun 0.03" — policymaker tidak tahu harus berbuat apa
- Fitur seperti `elevation_mean` = exogenous, tidak bisa diubah. Jadi policy-irrelevant meskipun predictive
- **Fitur yang policy-actionable:** `time_city_mean` (bangun jalan), `builtup_fraction` (program perumahan), `loss_recent_frac` (moratorium deforestasi)

## 3.7 Feature "wow secara teknis" tapi lemah secara substantif?

| Fitur | Wow factor | Substantive weakness |
|---|---|---|
| `ghm_mean/max` | Keren — composite 13 stressor dalam 1 indeks | **Redundant** dgn fitur lain. Komponennya sudah ada di dataset |
| `rain_cv` | Novel — variabilitas iklim | Di Kalimantan humid tropical, **range variasi sangat kecil**. Kemungkinan tidak prediktif |
| `lst_night_mean` | Interesting — thermal environment | Resolusi 1km terlalu kasar. Informasi marginal di atas lst_day |
| `loss_recent_frac` | Temporal signal | Hubungan dgn IDM bisa **positif** (sawit clearing = ekonomi) atau **negatif** (degradasi) |

## 3.8 Feature yang benar-benar defensible saat sidang?

**Tier "Tidak Terbantahkan" (5 fitur):**
1. `time_city_mean` — backed by Nature 2018 paper, causal mechanism clear
2. `elevation_mean` — exogenous, robust, Nunn & Puga (2012)
3. `ntl_mean_2021` — Jean et al. (2016) Science, Elvidge et al. (2017)
4. `builtup_fraction` — JRC validated, physical infrastructure proxy
5. `cover_2000_pct` — Hansen et al. (2013) Science

**Tier "Solid" (6 fitur):**
6. `slope_mean`, 7. `pop_density`, 8. `evi_mean`, 9. `loss_cum_frac`, 10. `annual_rain_mm`, 11. `lst_day_mean`

**Tier "Questionable" (8 fitur):**
12-19: `ntl_cv`, `pop_total`, `ndvi_mean`, `loss_recent_frac`, `rain_cv`, `ghm_mean`, `ghm_max`, `lst_night_mean`

## 3.9 Kritik utama dari reviewer jurnal keras?

1. **"All predictors are remote sensing proxies of the same latent construct (urbanization/development). Your model suffers from conceptual multicollinearity even if statistical VIF is acceptable."**
2. **"The omission of fiscal transfer data (Dana Desa) is a critical gap given that it is the primary policy instrument for village development in Indonesia."**
3. **"Your spatial cross-validation with GroupKFold by kabupaten is appropriate, but have you tested for spatial autocorrelation in the residuals (Moran's I)?"**
4. **"The use of IDM as a composite index is problematic. Why not predict sub-indices (IKS, IKE, IKL) separately?"**
5. **"WorldPop population is itself a model-based estimate. Using one model's output as input to another model introduces cascading uncertainty."**

---

# BAGIAN 4 — OFFICIAL STATISTICS GAP ANALYSIS

## Apakah project ini perlu tambahan official statistics?

**YA, TAPI DENGAN CATATAN.** 

- Untuk **skripsi data mining** di STIS: feature set saat ini **sudah cukup** jika framing-nya jelas sebagai "prediksi IDM from space"
- Untuk **publikasi jurnal**: minimal 1-2 official statistics sebagai contextual control akan **sangat memperkuat** paper
- **PDRB Kabupaten** sudah direncanakan di blueprint tapi **tidak diimplementasikan** di dataset final. Ini gap yang bisa diisi.

## Rekomendasi Official Statistics

### Rekomendasi 1: PDRB per Kapita Kabupaten

| Aspek | Detail |
|---|---|
| **Nama dataset** | PDRB Atas Dasar Harga Berlaku per Kabupaten/Kota |
| **Instansi** | BPS (5 BPS Provinsi Kalimantan) |
| **Level administrasi** | Kabupaten (56 entitas) |
| **Link akses** | bps.go.id + website BPS per provinsi |
| **Effort** | **MEDIUM** — manual input 56 baris dari PDF publikasi. Estimasi: 2-3 jam |
| **Leakage risk** | **LOW** — PDRB bukan komponen IDM |
| **Expected usefulness** | **MEDIUM-HIGH** — konteks ekonomi makro, desa di kab kaya cenderung maju |
| **Worth it?** | ✅ **YA — sangat direkomendasikan.** Effort kecil, legitimasi besar |

### Rekomendasi 2: Tingkat Kemiskinan Kabupaten (P0)

| Aspek | Detail |
|---|---|
| **Nama dataset** | Persentase Penduduk Miskin per Kabupaten |
| **Instansi** | BPS |
| **Level administrasi** | Kabupaten |
| **Link akses** | bps.go.id → Kemiskinan → Tabel Dinamis |
| **Effort** | **LOW** — tersedia langsung di website BPS sebagai tabel |
| **Leakage risk** | **MEDIUM** — kemiskinan berkorelasi dengan IDM, tapi bukan input langsung. Level kabupaten (bukan desa) mengurangi leakage |
| **Expected usefulness** | **HIGH** — menambah dimensi socio-economic yang sangat absen |
| **Worth it?** | ⚠️ **CONDITIONAL** — worth it jika bisa justify bahwa level kabupaten = bukan leakage. Diskusikan dengan dosen pembimbing |

### Rekomendasi 3: Rasio Elektrisitas Kabupaten

| Aspek | Detail |
|---|---|
| **Nama dataset** | Persentase Rumah Tangga dengan Akses Listrik |
| **Instansi** | BPS / PLN |
| **Level administrasi** | Kabupaten |
| **Link akses** | SUSENAS via bps.go.id |
| **Effort** | LOW-MEDIUM |
| **Leakage risk** | **MEDIUM-HIGH** — akses listrik = sub-indikator IKS dalam IDM! **Ini leakage** |
| **Expected usefulness** | Tinggi secara prediktif tapi... |
| **Worth it?** | ❌ **TIDAK — LEAKAGE.** Jangan gunakan |

### Rekomendasi 4: IPM (Indeks Pembangunan Manusia) Kabupaten

| Aspek | Detail |
|---|---|
| **Nama dataset** | IPM per Kabupaten/Kota |
| **Instansi** | BPS |
| **Level administrasi** | Kabupaten |
| **Link akses** | bps.go.id → IPM |
| **Effort** | **LOW** — data siap pakai |
| **Leakage risk** | **MEDIUM** — IPM mengukur konsep mirip (pembangunan) tapi komponen berbeda (pendidikan, kesehatan, pengeluaran). Bukan input IDM langsung |
| **Expected usefulness** | MEDIUM |
| **Worth it?** | ⚠️ **OPSIONAL** — bisa dipakai sebagai robustness check, bukan fitur utama |

> [!IMPORTANT]
> **Verdict pada full-GEE approach:** Secara teknis sangat kuat dan novel. Tapi terasa "terlalu artificial" untuk reviewer ilmu sosial. **Minimal tambahkan PDRB per kapita kabupaten** (effort: 2-3 jam) untuk memberikan 1 variabel sosio-ekonomi anchor.

---

# BAGIAN 5 — FINAL RECOMMENDATION

## 5.1 Final Recommended Feature Architecture

### WAJIB (11 fitur) — Core yang tidak boleh dibuang

| # | Fitur | Alasan |
|---|---|---|
| 1 | `ntl_mean_2021` | Proxy ekonomi #1, backed by Science paper |
| 2 | `elevation_mean` | Exogenous geography, zero leakage |
| 3 | `slope_mean` | Physical constraint pembangunan |
| 4 | `builtup_fraction` | Proxy urbanisasi fisik tervalidasi |
| 5 | `pop_density` | Demand-side proxy fundamental |
| 6 | `evi_mean` | Vegetasi (superior di tropics) |
| 7 | `time_city_mean` | Aksesibilitas — backed by Nature paper |
| 8 | `cover_2000_pct` | Baseline ekologi, Hansen Science paper |
| 9 | `loss_cum_frac` | Degradasi lingkungan kumulatif |
| 10 | `lst_day_mean` | Thermal environment / UHI proxy |
| 11 | `annual_rain_mm` | Exogenous climate control |

### OPTIONAL (5 fitur) — Keep if VIF allows

| # | Fitur | Catatan |
|---|---|---|
| 12 | `ntl_cv_2021` | Informatif tapi noisy di desa gelap |
| 13 | `pop_total` | Overlap dgn density, tapi masih lolos VIF |
| 14 | `loss_recent_frac` | Relasi ambiguous (sawit vs. degradasi) |
| 15 | `rain_cv` | Mungkin tidak prediktif di humid Kalimantan |
| 16 | `lst_night_mean` | Marginal information over day LST |

### SEBAIKNYA DIBUANG (3 fitur)

| # | Fitur | Alasan |
|---|---|---|
| 17 | `ndvi_mean` | **Redundant dgn EVI.** VIF keduanya near-threshold. Drop NDVI, keep EVI |
| 18 | `ghm_mean` | **Conceptually redundant.** Komponennya sudah ada sebagai fitur terpisah |
| 19 | `ghm_max` | Sama dgn ghm_mean — double-counting |

### TAMBAHKAN (1 fitur) — LOW EFFORT, HIGH IMPACT

| # | Fitur | Sumber | Effort |
|---|---|---|---|
| 20 | `pdrb_kab_perkapita` | BPS manual | 2-3 jam |

## 5.2 Jumlah Fitur Ideal

- **Untuk skripsi undergraduate:** **12-16 fitur** = sweet spot
  - Terlalu sedikit (<10): model underpowered
  - Terlalu banyak (>25): overfitting risk + sulit dijelaskan
  - **Saat ini 19 fitur = sedikit terlalu banyak.** Drop 3 redundant → **16 fitur = ideal

## 5.3 Kombinasi Terbaik

| Dimensi | Penilaian | Catatan |
|---|---|---|
| **Methodological Rigor** | ⭐⭐⭐⭐ (4/5) | GroupKFold spatial CV = excellent. VIF filtering = good. Missing: Moran's I residual test, sub-index decomposition |
| **Interpretability** | ⭐⭐⭐ (3/5) | SHAP planned = good. Tapi RS-only features sulit ditranslasi ke policy. Tambahkan PDRB untuk grounding |
| **Novelty** | ⭐⭐⭐⭐ (4/5) | "Predicting village development from satellite imagery at Kalimantan scale" = novel di konteks Indonesia. Tapi bukan globally novel (Jean et al. sudah ada) |
| **Feasibility** | ⭐⭐⭐⭐⭐ (5/5) | Semua data open access, pipeline sudah jalan, scripts sudah tested. Excellent |

## 5.4 Kelayakan Publikasi

### Skripsi STIS
✅ **SANGAT CUKUP.** Bahkan **di atas rata-rata** untuk skripsi S1. Feature engineering + spatial CV + SHAP = impressive untuk undergraduate. Pastikan:
- Framing jelas: "Can satellite-derived features predict IDM?"
- Acknowledge limitations (RS-only, no fiscal data)
- Discuss sub-index prediction sebagai future work

### Publikasi SINTA (Nasional)
✅ **LAYAK** untuk SINTA 2-3 jika:
- Tulis dalam Bahasa Indonesia
- Tambahkan minimal PDRB sebagai control
- Bandingkan model dgn dan tanpa spatial CV
- Jurnal target: *Jurnal Statistika STIS*, *Media Statistik*, *Jurnal Matematika MANTIK*

### Publikasi Scopus
⚠️ **BELUM CUKUP TANPA PERBAIKAN.** Untuk Scopus Q3-Q4 butuh:
1. **Tambah official statistics** (PDRB minimum)
2. **Prediksi sub-index** (IKS, IKE, IKL terpisah) — ini bisa jadi novel contribution
3. **Spatial residual analysis** (Moran's I, LISA map) — show spatial structure of errors
4. **Benchmark vs. census-based approach** — bandingkan RS-only vs. RS+survey
5. Target jurnal: *Sustainability* (MDPI, Q2), *Applied Geography* (Elsevier, Q1), *IJDE* (Taylor & Francis, Q2)

Untuk Scopus Q1-Q2 (RSE, ISPRS): **BELUM.** Butuh deep learning component, higher resolution imagery, dan/atau methodological innovation yang belum ada.

---

## RINGKASAN EKSEKUTIF

| Aspek | Status |
|---|---|
| **Feature set secara teknis** | ✅ Solid — well-curated GEE pipeline |
| **Feature set secara akademik** | ⚠️ Adequate for thesis, **needs 1-2 official stats for journal** |
| **Kelemahan terbesar** | Over-reliance on urbanization proxies; no fiscal/governance data |
| **Quick win terbesar** | Tambahkan PDRB kabupaten (effort: 2-3 jam, impact: tinggi) |
| **Fitur yang harus di-drop** | `ndvi_mean` (redundant dgn EVI), `ghm_mean` + `ghm_max` (redundant dgn NTL/builtup) |
| **Kelayakan skripsi** | ✅ Di atas rata-rata |
| **Kelayakan SINTA** | ✅ Layak |
| **Kelayakan Scopus** | ⚠️ Perlu perbaikan signifikan |

> [!NOTE]
> **Pesan penutup:** Project ini secara teknis sangat impresif untuk mahasiswa S1 — pipeline GEE lengkap, spatial CV, VIF filtering, imputation pipeline. Kelemahan utamanya bukan di teknis, tapi di **framing akademis**: model ini memprediksi "tampilan bumi dari atas", bukan "kondisi pembangunan manusia". Satu variabel sosio-ekonomi (PDRB) akan **dramatically improve** kredibilitas akademisnya tanpa effort signifikan.
