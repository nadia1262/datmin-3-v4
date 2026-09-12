# Definisi Operasional Variabel Penelitian

Penelitian ini memiliki dua tahapan analitik yang berbeda, yaitu (1) Pemodelan Spasial *Machine Learning* untuk Klasifikasi Tutupan Lahan dan (2) Pemodelan Ekonometrika Spasial untuk Analisis Asosiasi *Dual-Driver*. Oleh karena itu, arsitektur variabel independen (X) dan dependen (Y) dibagi menjadi dua kerangka kerja yang terpisah.

---

## TAHAP 1: Pemodelan Spasial *Machine Learning* (LightGBM)
*Fase ini bertujuan untuk mengekstraksi dan mengklasifikasikan piksel citra satelit menjadi kategori tutupan lahan secara diskrit.*

### Variabel Dependen (Y)
Variabel Y pada tahap ini adalah **Kelas Tutupan Lahan (*Land Cover Class*)**. Data referensi (*ground truth/reference label*) diekstrak dari produk **ESA WorldCover 2021** yang disederhanakan secara semantik ke dalam 5 kelas diskrit:
1. **Forest:** Hutan primer, hutan sekunder lebat, dan kanopi pohon tertutup.
2. **Shrubland/Agriculture:** Semak belukar, padang rumput, perkebunan (termasuk kelapa sawit), dan lahan pertanian.
3. **Built-up:** Area terbangun, infrastruktur, jalan aspal, dan permukiman (kota/desa).
4. **Bare/Mining-like:** Lahan terbuka tanpa vegetasi, area pembukaan lahan (*land clearing*), dan poligon ekstraktif/pertambangan.
5. **Water:** Badan air permanen (laut, danau, sungai besar).

### Variabel Independen (X)
Variabel X merupakan *input features* yang digunakan algoritma untuk membedakan karakteristik masing-masing piksel. Terdiri atas 12 variabel multivariat:
1. **Pita Spektral Satelit (Sentinel-2 Surface Reflectance):**
   - $X_1$ = Band 2 (Blue)
   - $X_2$ = Band 3 (Green)
   - $X_3$ = Band 4 (Red)
   - $X_4$ = Band 8 (Near-Infrared / NIR)
   - $X_5$ = Band 11 (Short-Wave Infrared 1 / SWIR1)
   - $X_6$ = Band 12 (Short-Wave Infrared 2 / SWIR2)
2. **Indeks Spektral Turunan:**
   - $X_7$ = **NDVI** (*Normalized Difference Vegetation Index*): Pengukur kerapatan dan kesehatan vegetasi.
   - $X_8$ = **NDBI** (*Normalized Difference Built-up Index*): Pengukur densitas material bangunan/infrastruktur.
   - $X_9$ = **NDMI** (*Normalized Difference Moisture Index*): Pengukur kelembaban tajuk/kanopi air.
   - $X_{10}$ = **BSI** (*Bare Soil Index*): Pengukur tingkat keterbukaan tanah dan material mineral (krusal untuk mendeteksi tambang).
3. **Variabel Lingkungan Tambahan:**
   - $X_{11}$ = **Elevasi (SRTM)**: Ketinggian permukaan tanah (mdpl).
   - $X_{12}$ = **Curah Hujan Tahunan (CHIRPS)**: Akumulasi presipitasi tahunan.

---

## TAHAP 2: Analisis Asosiasi *Dual-Driver* (*Multivariate Logistic Regression*)
*Fase ini bertujuan untuk menginvestigasi probabilitas kejadian kerusakan lingkungan yang disebabkan oleh IKN dibandingkan dengan industri pertambangan.*

### Variabel Dependen (Y)
Variabel Y pada tahap ini bertransformasi dari sekadar peta menjadi **Kejadian Perubahan Tutupan Lahan (*Land Cover Change Outcome*)**. Variabel ini bersifat dikotomi/biner (0 atau 1) yang disintesis dari Matriks Transisi antara peta prediksi tahun 2019 dan 2024:
1. **$Y_1$ (Deforestasi / *Forest Loss*):**
   - Bernilai **1** jika piksel pada 2019 adalah *Forest* dan berubah menjadi kelas non-vegetasi (contoh: *Bare/Built-up*) pada 2024.
   - Bernilai **0** jika tidak terjadi deforestasi.
2. **$Y_2$ (Urbanisasi):**
   - Bernilai **1** jika piksel pada 2019 adalah non-terbangun dan berubah menjadi kelas *Built-up* pada 2024.
   - Bernilai **0** jika tidak terjadi urbanisasi.
3. **$Y_3$ (Ekspansi Tambang / *Mining Expansion*):**
   - Bernilai **1** jika piksel pada 2019 adalah non-terbuka dan berubah menjadi kelas *Bare/Mining-like* pada 2024.
   - Bernilai **0** jika tidak terjadi pembukaan lahan.

### Variabel Independen (X)
Variabel X merupakan prediktor atau pendorong (*driver*) yang diuji pengaruhnya secara statistik terhadap kejadian-kejadian di atas:
1. **Prediktor Utama (Variabel Uji):**
   - $X_1$ = **Jarak ke IKN (*Distance to IKN*)**: Jarak *Euclidean* absolut dari titik koordinat piksel menuju titik pusat/Nol Ibu Kota Nusantara (dalam satuan derajat/km). Digunakan untuk menguji hipotesis *Spillover Effect*.
   - $X_2$ = **Kepadatan Tambang (*Mining Density 10 km*)**: Kepadatan poligon area tambang eksisting (berdasarkan data eksternal global *Maus et al., 2022*) dalam radius 10 kilometer dari piksel tersebut. Digunakan untuk menguji hipotesis *Telecoupling Ekstraktif*.
2. **Variabel Kontrol (Kovariat Topografi & Iklim):**
   - $X_3$ = **Elevasi**: Untuk mengontrol fakta spasial bahwa manusia cenderung membangun atau menebang hutan di dataran rendah yang landai.
   - $X_4$ = **Curah Hujan Tahunan**: Untuk mengontrol kondisi agroklimat daerah ekologis.

---

**Sintesis Kerangka Pikir:**
*Pipeline* data pada penelitian ini beroperasi secara sekuensial. Keberhasilan **Variabel Y pada Tahap 1** (peta klasifikasi yang dihasilkan oleh LightGBM) difilter melalui metode *Common Spatial Domain* (penghapusan awan), yang kemudian bermutasi menjadi bahan baku utama bagi **Variabel Y pada Tahap 2** (perhitungan logistik transisi probabilitas spasial).
