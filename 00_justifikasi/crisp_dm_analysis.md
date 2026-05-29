# Analisis CRISP-DM: Prediksi Indeks Desa Membangun (IDM) Berbasis Geospasial

Proyek ini dibangun di atas landasan akademik yang sangat solid. Pendekatan konvensional yang memprediksi kemajuan desa menggunakan data PODES (Potensi Desa) seringkali terjebak dalam **tautologi** (memprediksi suatu indeks menggunakan komponen pembentuk indeks itu sendiri). Proyek ini menghindari jebakan tersebut dengan menggunakan fitur spasial yang 100% eksternal (independen) dari formula IDM.

Berikut adalah analisis proyek dari kacamata *Cross-Industry Standard Process for Data Mining* (**CRISP-DM**).

---

## 1. Business Understanding (Pemahaman Masalah)

### Latar Belakang & Urgensi
Setiap tahun, pemerintah menyalurkan triliunan Rupiah Dana Desa berdasarkan skor Indeks Desa Membangun (IDM). Saat ini, IDM dihitung melalui kuesioner mandiri (*self-reported*) oleh aparatur desa. Metode ini memiliki kelemahan:
1. **Subjektivitas & Risiko Bias:** Desa bisa melaporkan kondisi lebih buruk agar statusnya tetap rendah demi mendapat bantuan dana lebih besar.
2. **Mahal & Lambat:** Butuh berbulan-bulan untuk mensurvei puluhan ribu desa di lokasi terpencil.

### Tujuan Proyek
Membangun model Machine Learning untuk mengestimasi skor IDM secara objektif menggunakan sinyal satelit (*Remote Sensing*) yang tersedia secara terbuka, gratis, dan *real-time*. Model ini dapat digunakan sebagai alat kalibrasi dan deteksi anomali bagi pembuat kebijakan.

### Kenapa Kalimantan?
Kalimantan adalah laboratorium spasial yang sempurna. Ada disparitas ekstrem antara kota metropolitan (seperti Balikpapan), desa yang didominasi tambang/sawit berskala besar, hingga desa pedalaman hutan yang terisolasi total. Kehadiran mega-proyek IKN (Ibu Kota Nusantara) juga membuat dinamika wilayah ini sangat penting dipantau.

---

## 2. Data Understanding (Pemahaman Data & Justifikasi Literatur)

Sinyal satelit tidak mengukur kemiskinan secara langsung, melainkan menangkap **sinyal proksi** (gejala fisik) dari aktivitas manusia. Berikut adalah justifikasi akademik mengapa variabel-variabel GEE ini sangat vital:

| Dimensi | Fitur (Variabel) | Justifikasi Literatur & Rasionalisasi |
|---|---|---|
| **Ekonomi Makro & Kelistrikan** | `ntl_mean` (Nighttime Lights/Cahaya Malam) | **(Henderson et al., 2012)** membuktikan bahwa intensitas cahaya malam berkorelasi sangat kuat dengan PDB wilayah dan infrastruktur listrik. Desa yang terang dari luar angkasa hampir dipastikan memiliki akses listrik dan aktivitas ekonomi komersial (IKE) yang baik. |
| **Fisik & Permukiman** | `builtup_fraction` (GHSL) | Mengukur luasan fisik bangunan (beton/atap seng). Pembangunan infrastruktur desa yang masif akan terekam sebagai ekspansi *built-up area*. Ini parameter esensial untuk membedakan desa agraris dengan desa yang mulai mengarah ke semi-urban. |
| **Demografi** | `pop_total`, `pop_density` (WorldPop) | Kemajuan fasilitas sosial (IKS) seperti keberadaan puskesmas dan sekolah sangat terikat dengan besarnya *demand* atau kepadatan penduduk. Desa yang populasinya terlalu kecil akan sulit mencapai skala ekonomi yang memadai untuk pembangunan fasilitas publik. |
| **Hambatan Alam** | `elevation_mean`, `slope_mean` (SRTM DEM) | Faktor biaya. Menggelar aspal atau membangun puskesmas di daerah berbukit terjal (*slope* curam) menelan biaya eksponensial lebih mahal daripada di dataran rendah. Elevasi ekstrem adalah penentu mutlak isolasi struktural pembangunan. |
| **Isolasi Spasial** | `time_city_mean` (Accessibility MAP) | **(Weiss et al., 2018)**. Mengukur waktu tempuh rata-rata (dalam hitungan menit/jam) menggunakan moda transportasi darat menuju pusat layanan rujukan terdekat. Mengisolasi desa dari rantai pasok ekonomi adalah rintangan terbesar kemajuan daerah pedalaman. |
| **Pertanian & Ekologi** | `ndvi_mean`, `lst_day_mean` (MODIS) | Indeks Kehijauan (NDVI) dan Suhu Permukaan Bumi (LST). Di Kalimantan, desa yang transisi lahan dari kanopi hutan padat (NDVI tinggi, LST sejuk) menjadi area terbuka tambang/permukiman (NDVI rendah, LST panas) mengindikasikan adanya sentuhan aktivitas industri ekstraktif yang mengubah pola ekonomi wilayah tersebut. |
| **Gangguan Lingkungan** | `ghm_mean` (Global Human Modification) | Seberapa parah intervensi dan eksploitasi manusia terhadap suatu kawasan alam. Fitur ini sangat potensial menjadi penentu kuat dalam memprediksi skor Ketahanan Lingkungan (IKL) suatu desa. |
| **Cuaca Ekstrem** | `annual_rain_mm`, `rain_cv` (CHIRPS) | Curah hujan total dan variabilitas curah hujan berkaitan kuat dengan kerentanan bencana hidrometeorologi (banjir/longsor). Bencana menghambat Indeks Ketahanan Lingkungan. |

---

## 3. Data Preparation (Persiapan Data)

Proses yang sangat krusial, meliputi langkah-langkah yang sebagian besar sudah kita tuntaskan:
1. **Administrasi:** Pembuatan *Crosswalk ID* untuk merekonsiliasi perbedaan kode wilayah antara poligon BPS dengan dataset Kemendagri (IDM target).
2. **Spatial Reduction (Zonal Statistics):** Agregasi triliunan piksel data berformat *raster* dari Google Earth Engine menjadi format *tabular* berbasis batas desa (rata-rata, varians, deviasi standar).
3. **Data Cleaning:** Imputasi *missing values* bagi desa-desa yang letaknya *borderline* atau tutupan datanya berlubang akibat gumpalan awan.
4. **Seleksi Fitur & Reduksi Dimensi:** Pengecekan *Variance Inflation Factor* (VIF) untuk membuang metrik yang overlap atau multikolinier.

---

## 4. Modeling (Pemodelan)

Kita memformulasikan persoalan ini sebagai tipe pembelajaran **Supervised Regresi** (memprediksi angka *continue* 0 sampai 1 pada Skor IDM). Pendekatannya bersifat *Multi-Algorithm* untuk mengeksplorasi topologi masalah:

1. **Model Linier (Baseline):**
   *Linear Regression* dan *Ridge Regression*. Sebagai patokan kasar. Asumsinya: semakin terang cahaya malam, maka skor kemandirian desa linier naik secara proporsional. Mudah diinterpretasikan.
2. **Model Tree-Based & Ensemble:**
   *Random Forest* dan algoritma Boosting (*Gradient Boosting*, *XGBoost*). Andal dan kokoh (*robust*) menangkap kerumitan spasial nonlinearitas. (Contoh interaksi: "Jika akses jalan buruk, tapi nilai cahayanya terang akibat konsesi tambang, maka nilai ekonomi tinggi namun lingkungan rusak").
3. **Model Kernel:**
   *Support Vector Regression (SVR)*. Efektif menangani *noise* multidimensi pada dataset geospasial padat batas desa beririsan tinggi.

---

## 5. Evaluation (Evaluasi)

Algoritma dinilai tidak hanya melalui akurasinya, tetapi stabilitas strukturalnya di hadapan data geospasial:
- **Metrik Tradisional:** $R^2$ (Daya perwakilan varians IDM), *Root Mean Squared Error* (RMSE), dan *Mean Absolute Error* (MAE).
- **Spatial Cross-Validation:** Memecah data *validation* berdasarkan klaster wilayah atau *Kabupaten* (menggunakan *GroupKFold*). Jika hanya menggunakan *Random Split* konvensional, model bisa berbuat curang (*Spatial Leakage*) dengan "menghafal" pola desa yang letaknya persis bertetanggaan, membuat tingkat keakurasiannya tampak artifisial.
- **Interpretabilitas Model:** Melibatkan metode SHAP (*SHapley Additive exPlanations*) untuk membongkar "black box" model. Mengapa model menetapkan suatu prediksi? Sinyal spasial manakah yang paling kuat menarik skor suatu desa, serta bagaimana perbedaan fiturnya antara desa di pesisir pesat industri vs. desa lereng pegunungan.

---

## 6. Deployment (Pemanfaatan & Rekomendasi)

Untuk kebutuhan analitika akademik dan pemerintahan, *output* terpenting bukanlah *software endpoint*, melainkan **Policy Targeting Framework**:
1. **Analisis Spatial Residual (Anomali Pemodelan):**
   Memvisualisasikan *gap* yang terjadi ketika skor IDM asli di lapangan dinilai tinggi padahal sinyal infrastrukturnya dari antariksa terbilang parah, *atau sebaliknya*. 
2. Desa dengan aset fisik mumpuni namun skor pembangunannya tersendat secara persisten akan dikategorikan sebagai *underperforming villages*, menjadi target mutlak evaluasi dan pemantauan khusus akibat kemungkinan anomali alokasi pendanaan.
