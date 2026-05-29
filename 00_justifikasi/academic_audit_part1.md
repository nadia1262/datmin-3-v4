# AUDIT AKADEMIK ARSITEKTUR DATASET — BAGIAN 1 & 2
## Prediksi IDM Desa Kalimantan via Spatial ML

> **Auditor:** Antigravity AI | **Tanggal:** 17 Mei 2026
> **Scope:** 19 fitur aktif di `merged_imputed_vif.csv` (post-VIF) + arsitektur keseluruhan

---

# BAGIAN 1 — AUDIT AKADEMIK FEATURE SET

## Tabel Audit Per-Fitur

### A. Nighttime Lights (NTL)

| Aspek | `ntl_mean_2021` | `ntl_cv_2021` |
|---|---|---|
| **Dataset asal** | VIIRS DNB Annual V21 | VIIRS DNB Annual V21 (derived) |
| **Fenomena yang diukur** | Intensitas aktivitas ekonomi malam hari rata-rata per desa | Heterogenitas spasial cahaya dalam polygon desa |
| **Mekanisme kausal → IDM** | Cahaya malam = elektrisitas + aktivitas komersial → proxy IKE (ekonomi). Desa terang = infrastruktur listrik + pasar aktif | CV tinggi = desa "dual economy" (ada cluster terang + area gelap). Menangkap inequality internal yang mean saja tidak bisa |
| **Kenapa masuk akal** | Studi Jean et al. (2016, *Science*), Elvidge et al. (2017) menunjukkan NTL = proxy GDP paling robust secara global | CV menambah dimensi distribusi yang mean tidak punya. Akademis novel untuk village level |
| **Risiko leakage** | **LOW** — NTL bukan komponen IDM. IDM menggunakan data survei akses listrik (biner), bukan radiance | **LOW** — derived dari NTL, tidak overlap IDM |
| **Risiko proxy redundancy** | Moderat — korelasi tinggi dengan `builtup_fraction`, `pop_density`, `ghm_mean` karena semua proxy urbanisasi | Rendah — CV relatif unik |
| **Risiko spurious correlation** | **MEDIUM** — gas flare Kaltim bisa bikin desa hutan terlihat "terang" padahal miskin | LOW |
| **Risiko noisy di Kalimantan** | **TINGGI di Kaltim** — gas flare. Mitigasi: pakai band `average_masked` | Noise amplified di desa gelap (division near-zero) |
| **Layak dipertahankan?** | ✅ **YA — WAJIB.** Fitur paling defensible secara literatur | ✅ **YA** — tapi acknowledging limitasi noise |

---

### B. Built-Up & Population

| Aspek | `builtup_fraction` | `pop_total` | `pop_density` |
|---|---|---|---|
| **Dataset asal** | JRC GHSL R2023A | WorldPop 100m | WorldPop 100m / village_area |
| **Fenomena yang diukur** | Fraksi lahan terbangun fisik | Estimasi jumlah penduduk | Konsentrasi penduduk per km² |
| **Mekanisme kausal → IDM** | Built-up = infrastruktur fisik (rumah, jalan, fasilitas). Langsung relevan untuk IKE & IKL | Populasi = demand side untuk layanan. Desa banyak penduduk = perlu lebih banyak sekolah, klinik | Density = intensitas penggunaan lahan. Density tinggi = urban = akses layanan lebih baik |
| **Kenapa masuk akal** | GHSL R2023 = state-of-art global built-up detection. Validated di Pesaresi et al. (2016, *ISPRS*) | WorldPop = gold standard gridded population. Digunakan UN, World Bank | Density = proxy urbanitas yang robust |
| **Risiko leakage** | **LOW** — built-up bukan komponen IDM | **LOW** — populasi bukan input IDM langsung | **LOW** |
| **Risiko proxy redundancy** | Tinggi dgn NTL, pop_density, ghm_mean | **TINGGI dgn pop_density** — pop_total = density × area. VIF menunjukkan masih <10 tapi perlu monitoring | Tinggi dgn pop_total, NTL, builtup |
| **Risiko noisy di Kalimantan** | Underestimation di settlement tradisional kayu yang tidak terdeteksi radar | WorldPop = estimasi model, bukan sensus. Bisa disagree dgn BPS | Sama dgn pop_total |
| **Layak dipertahankan?** | ✅ **YA** | ⚠️ **CONDITIONAL** — keep both pop_total & pop_density hanya jika VIF aman | ✅ **YA** |

---

### C. Vegetation

| Aspek | `ndvi_mean` | `evi_mean` |
|---|---|---|
| **Dataset asal** | MODIS MOD13Q1 V6.1 | MODIS MOD13Q1 V6.1 |
| **Fenomena yang diukur** | Kehijauan/tutupan vegetasi rata-rata | Kehijauan vegetasi (corrected for atmosphere & soil) |
| **Mekanisme kausal → IDM** | NDVI tinggi = hutan/pertanian sehat → relevan IKL. NDVI rendah = lahan degraded atau urban | EVI lebih sensitif di hutan lebat Kalimantan. Menangkap gradasi yang NDVI saturate |
| **Kenapa masuk akal** | Digunakan di hampir semua poverty mapping paper. Yeh et al. (2020) mengkonfirmasi predictive power | EVI > NDVI untuk tropical dense canopy. Huete et al. (2002, *RSE*) |
| **Risiko leakage** | **LOW** — vegetasi bukan komponen IDM (IKL mengukur bencana & lingkungan via survei, bukan greenness) | **LOW** |
| **Risiko proxy redundancy** | **SANGAT TINGGI dgn EVI** — VIF saat ini 8.4 (NDVI) dan 9.7 (EVI). Keduanya di ambang batas | **SANGAT TINGGI dgn NDVI** |
| **Risiko spurious correlation** | MEDIUM — desa terpencil di hutan bisa punya NDVI tinggi tapi IDM rendah. Hubungannya **non-linear** | Sama |
| **Risiko noisy di Kalimantan** | Cloud contamination tropis, tapi annual composite mengurangi ini | Lebih baik dari NDVI di kondisi cloudy |
| **Layak dipertahankan?** | ⚠️ **PERTIMBANGKAN DROP SALAH SATU.** VIF keduanya near-threshold. Rekomendasi: keep EVI (lebih superior di Kalimantan), drop NDVI | ✅ **YA — keep EVI** sebagai perwakilan vegetasi |

---

### D. Accessibility

| Aspek | `time_city_mean` |
|---|---|
| **Dataset asal** | Oxford/MAP Accessibility to Cities 2015 |
| **Fenomena yang diukur** | Waktu tempuh (menit) ke kota terdekat ≥50k populasi |
| **Mekanisme kausal → IDM** | Aksesibilitas = determinan fundamental pembangunan. Desa jauh dari kota = sulit akses layanan, pasar, informasi → IDM rendah |
| **Kenapa masuk akal** | **FITUR TERKUAT SECARA TEORI.** Weiss et al. (2018, *Nature*, DOI: 10.1038/nature25181) = paper landmark. Friction surface memperhitungkan topografi, road network, land cover |
| **Risiko leakage** | **LOW** — travel time bukan komponen IDM. IDM mengukur akses via survei biner (ada/tidak jalan), bukan waktu tempuh |
| **Risiko proxy redundancy** | Moderat dgn elevation, slope (daerah tinggi biasanya jauh dari kota) |
| **Risiko spurious correlation** | LOW — hubungan kausal jelas dan well-established |
| **Risiko noisy di Kalimantan** | LOW — Oxford/MAP product well-validated. Tapi data 2015, bisa outdated di beberapa area dengan jalan baru |
| **Layak dipertahankan?** | ✅ **YA — WAJIB. Ini salah satu fitur paling defensible di seluruh dataset** |

---

### E. Terrain (Topografi)

| Aspek | `elevation_mean` | `slope_mean` |
|---|---|---|
| **Dataset asal** | SRTM 30m | SRTM 30m (derived) |
| **Fenomena yang diukur** | Ketinggian rata-rata desa (m dpl) | Kemiringan lereng rata-rata (derajat) |
| **Mekanisme kausal → IDM** | Elevasi = constraint fisik aksesibilitas & pertanian. Dataran tinggi Kalimantan = terisolasi | Slope = hambatan konstruksi infrastruktur. Slope >15° = sangat sulit bangun jalan/bangunan |
| **Kenapa masuk akal** | Riley et al. (1999), Nunn & Puga (2012, *Review of Economics and Statistics*) — ruggedness menghambat pembangunan secara sistematik | Terrain sebagai exogenous geography instrument = sangat kuat secara kausalitas |
| **Risiko leakage** | **ZERO** — topografi = fully exogenous, tidak bisa dimanipulasi kebijakan | **ZERO** |
| **Risiko proxy redundancy** | Tinggi dgn slope (r~0.7+). **`ruggedness_mean` sudah di-drop VIF (80.57!)** — keputusan tepat | Moderat dgn elevation |
| **Risiko noisy** | Very low — SRTM = static, well-validated, 30m resolution | Very low |
| **Layak dipertahankan?** | ✅ **YA — WAJIB.** Exogenous variable = best instrument | ✅ **YA** |

---

### F. Forest Change

| Aspek | `cover_2000_pct` | `loss_cum_frac` | `loss_recent_frac` |
|---|---|---|---|
| **Dataset asal** | Hansen GFC v1.11 | Hansen GFC v1.11 (derived) | Hansen GFC v1.11 (derived) |
| **Fenomena yang diukur** | Baseline tutupan hutan tahun 2000 (%) | Fraksi kehilangan hutan kumulatif 2001-2022 | Fraksi kehilangan hutan 2018-2022 |
| **Mekanisme kausal → IDM** | Tutupan hutan = modal ekologi. Relevan utk IKL | Deforestasi kumulatif = degradasi lingkungan jangka panjang | Deforestasi terkini = sinyal transformasi lahan aktif (bisa positif [sawit] atau negatif [degradasi]) |
| **Kenapa masuk akal** | Hansen et al. (2013, *Science*) — dataset deforestasi paling banyak dikutip di dunia | Kalimantan = hotspot deforestasi global. Konteks sangat relevan | Recent loss lebih actionable untuk prediksi IDM kontemporer |
| **Risiko leakage** | **LOW** | **LOW** | **LOW** |
| **Risiko spurious** | MEDIUM — deforestasi untuk sawit bisa meningkatkan ekonomi lokal (IKE naik) tapi menurunkan ekologi (IKL turun). **Hubungan ambiguous** | Sama | Sama, bahkan lebih kuat |
| **Noisy di Kalimantan** | LOW — 30m resolution sangat baik | LOW | LOW |
| **Layak dipertahankan?** | ✅ **YA** | ✅ **YA** — tapi acknowledge relasi non-linear | ✅ **YA** |

---

### G. Climate

| Aspek | `annual_rain_mm` | `rain_cv` |
|---|---|---|
| **Dataset asal** | CHIRPS Monthly | CHIRPS Monthly (derived) |
| **Fenomena yang diukur** | Total curah hujan tahunan (mm) | Variabilitas curah hujan intra-annual |
| **Mekanisme kausal → IDM** | Curah hujan → produktivitas pertanian → IKE. Terlalu sedikit = kekeringan, terlalu banyak = banjir | CV tinggi = iklim tidak stabil → risiko gagal panen, bencana |
| **Kenapa masuk akal** | Funk et al. (2015, *Scientific Data*) — CHIRPS = standard utk analisis agroklimat | Rain variability = climate risk yang mempengaruhi ketahanan ekonomi rural |
| **Risiko leakage** | **ZERO** — curah hujan = fully exogenous | **ZERO** |
| **Risiko proxy redundancy** | LOW — curah hujan relatif independen dari fitur lain | LOW |
| **Risiko spurious** | MEDIUM — Kalimantan relatif homogen curah hujannya (humid tropical). **Variasi mungkin terlalu kecil untuk prediktif** | Lebih informatif dari total |
| **Noisy di Kalimantan** | MEDIUM — resolusi 5.5km kasar. Kalimantan flat = OK, tapi mountain areas bisa bias | Sama |
| **Layak dipertahankan?** | ⚠️ **MARGINAL.** Secara teori kuat tapi di Kalimantan humid tropical, range variasi kecil. Mungkin tidak prediktif. Keep tapi jangan surprised kalau importance rendah | ✅ **YA** — rain_cv lebih informatif dari total |

---

### H. Human Modification

| Aspek | `ghm_mean` | `ghm_max` |
|---|---|---|
| **Dataset asal** | CSP Global Human Modification | CSP gHM |
| **Fenomena yang diukur** | Indeks kumulatif modifikasi manusia (0-1), rata-rata per desa | Nilai modifikasi maksimum dalam polygon |
| **Mekanisme kausal → IDM** | gHM = composite 13 stressor (NTL, built-up, roads, cropland, dll). Proxy holistik intensitas manusia | Max = titik paling termodifikasi, mungkin pusat desa |
| **Kenapa masuk akal** | Kennedy et al. (2019, *Global Change Biology*, DOI: 10.1111/gcb.14549) | Melengkapi mean dengan informasi hotspot |
| **Risiko leakage** | **LOW** | **LOW** |
| **Risiko proxy redundancy** | **TINGGI — ini MASALAH TERBESAR gHM.** gHM = composite dari NTL + built-up + roads + cropland. Kita sudah punya NTL, builtup_fraction, pop_density sebagai fitur terpisah. **gHM = "double-counting" secara definitif** | Sama |
| **Risiko spurious** | LOW — tapi karena redundancy, koefisien bisa misleading | Sama |
| **Layak dipertahankan?** | ⚠️ **PERTIMBANGKAN DROP.** gHM_mean VIF=6.5 masih aman tapi secara konseptual redundant. Saat sidang, penguji bisa tanya: "kenapa pakai composite yang komponennya sudah jadi fitur terpisah?" | ⚠️ **DROP ghm_max** kalau ingin parsimoni. Keep salah satu saja |

---

### I. Land Surface Temperature

| Aspek | `lst_day_mean` | `lst_night_mean` |
|---|---|---|
| **Dataset asal** | MODIS MOD11A2 V6.1 | MODIS MOD11A2 V6.1 |
| **Fenomena yang diukur** | Suhu permukaan siang hari (°C) | Suhu permukaan malam hari (°C) |
| **Mekanisme kausal → IDM** | LST siang = urban heat island + degradasi lahan. Desa urban/gundul = LST tinggi | LST malam = thermal mass. Lebih stabil, proxy material bangunan & kepadatan |
| **Kenapa masuk akal** | LST digunakan dalam studi urban-rural gradient. Clinton & Gong (2013, *RSE*) | LST malam lebih predictive untuk poverty (Steele et al., 2017) |
| **Risiko leakage** | **LOW** | **LOW** |
| **Risiko proxy redundancy** | MEDIUM — korelasi dgn NDVI (inverse), elevation (inverse) | MEDIUM — korelasi dgn LST day |
| **Risiko noisy** | MEDIUM — resolusi 1km kasar untuk desa kecil | Sama |
| **Layak dipertahankan?** | ✅ **YA** — menambah dimensi thermalenvironment yang unik | ⚠️ **CONDITIONAL** — jika VIF stabil, keep. Kalau ingin parsimoni, drop night dan keep day saja |

---

# BAGIAN 2 — VALIDASI LITERATUR

## 2.1 Nighttime Lights

| # | Paper | Tahun | Jurnal | DOI | Prediksi | Level | Mendukung? |
|---|---|---|---|---|---|---|---|
| 1 | Jean et al., "Combining satellite imagery and ML to predict poverty" | 2016 | *Science* | `10.1126/science.aaf7894` | Asset wealth, consumption | Village/cluster | ✅ Strongly supports |
| 2 | Elvidge et al., "VIIRS night-time lights" | 2017 | *Int. J. Remote Sensing* | `10.1080/01431161.2017.1342050` | Socioeconomic activity | Sub-national | ✅ Technical foundation |
| 3 | Henderson et al., "Measuring Economic Growth from Outer Space" | 2012 | *American Economic Review* | `10.1257/aer.102.2.994` | GDP growth | National/sub-national | ✅ Seminal economics paper |

## 2.2 Built-Up (GHSL)

| # | Paper | Tahun | Jurnal | DOI | Level | Mendukung? |
|---|---|---|---|---|---|---|
| 4 | Pesaresi et al., "Operating procedure for production of built-up area..." | 2016 | *IEEE JSTARS* | `10.1109/JSTARS.2015.2467734` | Global | ✅ Technical validation |
| 5 | Corbane et al., "Automated global delineation of human settlements..." | 2019 | *Int. J. Digital Earth* | `10.1080/17538947.2018.1550804` | Global | ✅ Methodology |

## 2.3 Vegetation (NDVI/EVI)

| # | Paper | Tahun | Jurnal | DOI | Level | Mendukung? |
|---|---|---|---|---|---|---|
| 6 | Huete et al., "Overview of the radiometric and biophysical performance of MODIS vegetation indices" | 2002 | *Remote Sens. Environ.* | `10.1016/S0034-4257(02)00096-2` | Global | ✅ EVI > NDVI for tropical |
| 7 | Yeh et al., "Using publicly available satellite imagery and DL to understand economic well-being in Africa" | 2020 | *Nature Communications* | `10.1038/s41467-020-16185-w` | Village | ✅ Multi-spectral features incl. vegetation |

## 2.4 Accessibility

| # | Paper | Tahun | Jurnal | DOI | Level | Mendukung? |
|---|---|---|---|---|---|---|
| 8 | Weiss et al., "A global map of travel time to cities..." | 2018 | ***Nature*** | `10.1038/nature25181` | Global/pixel | ✅ **Landmark paper** — strongest citation |
| 9 | Nelson et al., "A suite of global accessibility indicators" | 2019 | *Scientific Data* | `10.1038/s41597-019-0265-5` | Global | ✅ Healthcare accessibility |

## 2.5 Terrain

| # | Paper | Tahun | Jurnal | DOI | Level | Mendukung? |
|---|---|---|---|---|---|---|
| 10 | Nunn & Puga, "Ruggedness: The Blessing of Bad Geography in Africa" | 2012 | *Rev. Econ. & Statistics* | `10.1162/REST_a_00161` | National/sub-national | ✅ Terrain = exogenous instrument |
| 11 | Riley et al., "A Terrain Ruggedness Index..." | 1999 | *Intermountain J. Sciences* | N/A (pre-DOI) | Regional | ✅ TRI methodology |

## 2.6 Forest Change

| # | Paper | Tahun | Jurnal | DOI | Level | Mendukung? |
|---|---|---|---|---|---|---|
| 12 | Hansen et al., "High-Resolution Global Maps of 21st-Century Forest Cover Change" | 2013 | ***Science*** | `10.1126/science.1244693` | Global/30m | ✅ Dataset foundation |
| 13 | Gaveau et al., "Rapid conversions and avoided deforestation..." | 2016 | *PNAS* | `10.1073/pnas.1522411113` | Kalimantan | ✅ Direct Kalimantan context |

## 2.7 Climate (CHIRPS)

| # | Paper | Tahun | Jurnal | DOI | Level | Mendukung? |
|---|---|---|---|---|---|---|
| 14 | Funk et al., "The climate hazards infrared precipitation with stations..." | 2015 | ***Scientific Data*** | `10.1038/sdata.2015.66` | Global/5km | ✅ Dataset foundation |

## 2.8 Human Modification (gHM)

| # | Paper | Tahun | Jurnal | DOI | Level | Mendukung? |
|---|---|---|---|---|---|---|
| 15 | Kennedy et al., "Managing the middle: A shift in conservation priorities..." | 2019 | *Global Change Biology* | `10.1111/gcb.14549` | Global/1km | ⚠️ Supports conservation use, **NOT poverty prediction** |

> [!WARNING]
> **Catatan Kritis Literatur:** Tidak ada satu pun paper di atas yang secara spesifik menggunakan **IDM** sebagai target dengan **exact feature set** ini di level **desa Kalimantan**. Paper terdekat adalah studi ADB/STIS yang menggunakan NTL + Sentinel untuk prediksi IDM, tapi dengan metodologi berbeda (CNN, bukan tabular ML). Ini berarti project ini memiliki **novelty** tapi juga berarti **belum ada validasi langsung** — ini harus diakui di paper.


