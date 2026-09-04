# BAB III: Variabel Penelitian dan Justifikasi Ilmiah

Dalam penelitian ini, pemodelan dilakukan dalam dua tahap utama: (1) Klasifikasi Tutupan Lahan menggunakan *Machine Learning*, dan (2) Analisis Regresi Penggerak (*Driver Analysis*). Masing-masing tahap memiliki variabel prediktor dan variabel target yang spesifik.

---

## 3.1. Tahap 1: Model Klasifikasi Tutupan Lahan (Land Cover Classification)

Model *Machine Learning* (LightGBM) dilatih untuk mengenali jenis tutupan lahan berdasarkan sifat fisika optik pantulan permukaan bumi yang direkam oleh satelit Sentinel-2.

### 3.1.1. Variabel Target (Dependent Variable)
Variabel yang diprediksi oleh algoritma adalah kelas tutupan lahan. Label aktual (*ground truth*) diekstraksi dari dataset **ESA WorldCover 2021** yang direklasifikasi menjadi 5 kelas utama yang relevan dengan fokus penelitian:
1. **Forest (Hutan):** Area dengan tutupan tajuk pohon rapat (termasuk lahan basah berhutan dan mangrove).
2. **Shrubland / Agriculture (Semak/Pertanian):** Lahan vegetasi rendah, padang rumput, semak belukar, dan lahan pertanian aktif.
3. **Built-up (Area Terbangun):** Infrastruktur buatan manusia, jalan aspal, beton, dan pemukiman (fokus urbanisasi IKN).
4. **Bare / Mining-like (Tanah Terbuka):** Lahan kosong tanpa vegetasi yang terekspos, yang di Kalimantan sangat berkorelasi dengan lubang galian tambang terbuka (*open-pit mining*).
5. **Water (Badan Air):** Laut, danau, dan sungai besar.

### 3.1.2. Variabel Prediktor (Independent Variables)
Alih-alih menggunakan koordinat spasial murni, model diberikan **10 fitur spektral** (Sifat Fisika Optik Bumi) sebagai prediktor. Pendekatan ini memastikan model tidak "menghafal lokasi", melainkan mempelajari karakteristik pantulan material di permukaan, sehingga model dapat memprediksi secara akurat untuk tahun-tahun yang berbeda (2019–2024).

#### A. Raw Sentinel-2 Bands (Spektrum Mentah)
Satelit Sentinel-2 merekam gelombang elektromagnetik dari spektrum *visible* hingga *infrared*.
1. **B2 (Blue - 490nm), B3 (Green - 560nm), B4 (Red - 665nm):** Spektrum cahaya tampak (*visible spectrum*). Berguna untuk membedakan objek berpigmen kontras (seperti air laut vs daratan).
2. **B8 (Near-Infrared / NIR - 842nm):** Gelombang Inframerah Dekat. Klorofil pada daun memantulkan gelombang NIR secara sangat ekstrem. Piksel dengan pantulan B8 yang tinggi secara mutlak mengindikasikan keberadaan vegetasi sehat.
3. **B11 (SWIR 1 - 1610nm) & B12 (SWIR 2 - 2190nm):** *Shortwave-Infrared*. Gelombang ini mampu menembus asbut/kabut tipis dan sangat peka terhadap kandungan air dalam tanah serta mineral batuan. Band ini adalah **kunci utama** dalam membedakan tanah galian tambang (pantulan SWIR sangat tinggi) dengan beton area terbangun.

#### B. Spectral Indices (Indeks Kalkulasi Matematis)
Untuk menstimulasi akurasi model, band mentah dikombinasikan menjadi indeks spektral khusus yang menonjolkan ( *enhance*) kelas lahan tertentu secara tajam:
4. **NDVI (*Normalized Difference Vegetation Index*):** Mengkuantifikasi biomassa vegetasi dengan rasio NIR dan Red. Ini adalah pemisah utama antara **Hutan** (nilai mendekati +1) dengan area non-vegetasi.
5. **NDBI (*Normalized Difference Built-up Index*):** Menggunakan rasio SWIR dan NIR untuk mendeteksi dominasi material infrastruktur buatan manusia (beton, atap). Sangat krusial untuk melacak **Pembangunan Infrastruktur IKN**.
6. **BSI (*Bare Soil Index*):** Mengkombinasikan SWIR, Red, NIR, dan Blue untuk menonjolkan paparan mineral tanah mentah. Indeks ini merupakan indikator terkuat untuk mendeteksi bukaan lahan baru akibat **Ekspansi Pertambangan**.
7. **NDMI (*Normalized Difference Moisture Index*):** Mengukur tingkat kelembaban kanopi dan permukaan. Berguna untuk memisahkan rawa/badan air dari daratan yang teduh.

---

## 3.2. Tahap 2: Model Analisis Penggerak (Dual-Driver Analysis)

Setelah peta tutupan lahan 2019–2024 terbentuk dari model di atas, penelitian berlanjut ke pengujian hipotesis spasial menggunakan Regresi Logistik untuk menjawab: *"Apakah IKN dan Tambang adalah pendorong utama konversi lahan tersebut?"*

### 3.2.1. Variabel Target (Binary Response)
Variabel target di sini adalah probabilitas terjadinya perubahan ekstrem (transisi lahan) dari tahun 2019 ke 2024:
1. **Forest Loss (Deforestasi):** 1 jika Hutan (2019) berubah menjadi non-Hutan (2024), 0 jika tetap Hutan.
2. **Urban Expansion:** 1 jika lahan non-Bangunan (2019) berubah menjadi Bangunan (2024), 0 jika sebaliknya.
3. **Mining Expansion:** 1 jika lahan non-Tanah Terbuka (2019) berubah menjadi Tanah Terbuka (2024), 0 jika sebaliknya.

### 3.2.2. Variabel Prediktor Spasial (Drivers)
1. **Distance to IKN (km):** Jarak Euclidean dari setiap piksel observasi menuju titik pusat Ibu Kota Nusantara. Menjadi proksi untuk pengaruh tarikan urbanisasi sentripetal.
2. **Mining Density 10km (%):** Kepadatan area galian tambang dalam radius 10 kilometer di sekitar titik observasi. Menjadi proksi untuk tingkat degradasi lingkungan akibat aktivitas ekstraktif.
3. **Elevation (m) & Annual Rainfall (mm):** (Variabel Kontrol). Ketinggian dari SRTM dan curah hujan dari CHIRPS dimasukkan ke dalam model agar hasil analisis statistik (*P-Value* dan *Odds Ratio*) dari pengaruh IKN dan Tambang tidak bias oleh faktor topografi dan iklim lokal.
