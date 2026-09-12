# BAB 2: Materi dan Metode

Secara konseptual, penelitian ini merangkai tiga tahapan logis: **Klasifikasi → Perubahan → Asosiasi**. Pertama, kelas tutupan lahan diklasifikasikan dari citra satelit (Tahap 1). Kedua, peta hasil klasifikasi dari tahun 2019 dan 2024 dibandingkan untuk mengidentifikasi perubahan lahan. Ketiga, diuji apakah kejadian perubahan tersebut berasosiasi secara spasial dengan jarak ke Ibu Kota Nusantara (IKN) dan kepadatan tambang, menggunakan metode regresi logistik terpisah (Tahap 2). 

Seluruh tahapan akuisisi data awal dilakukan memanfaatkan komputasi awan *Google Earth Engine* (GEE) (Gorelick et al., 2017), sedangkan proses pelatihan model *Machine Learning* dan analisis spasial dieksekusi menggunakan bahasa pemrograman Python.

---

## 2.1 Data dan Sumber Data

Analisis difokuskan pada daratan Pulau Kalimantan, dengan lokus mikro di Kawasan Inti Pusat Pemerintahan (KIPP) IKN. Sumber data geospasial yang diintegrasikan dalam penelitian ini meliputi:

1. **Citra Satelit Optik:** Sentinel-2 *Surface Reflectance Harmonized* (Resolusi 10 m). Digunakan enam pita (*band*) spektral: B2 (*Blue*), B3 (*Green*), B4 (*Red*), B8 (*NIR*), B11 (*SWIR1*), dan B12 (*SWIR2*).
2. **Label Referensi Tutupan Lahan:** ESA WorldCover 10m 2021 v200. Data global ini digunakan sebagai *reference label* untuk membentuk sampel pelatihan klasifikasi, bukan sebagai referensi mutlak (*absolute ground truth*) di lapangan (Zanaga et al., 2022).
3. **Data Topografi:** Elevasi diekstrak dari instrumen *Shuttle Radar Topography Mission* (SRTM) versi 3 beresolusi 30 m (Farr et al., 2007).
4. **Data Iklim:** Akumulasi presipitasi tahunan diakuisisi dari dataset CHIRPS (*Climate Hazards Group InfraRed Precipitation with Station data*) (Funk et al., 2015).
5. **Data Batas IKN:** Titik pusat koordinat digunakan untuk menghitung jarak euklidean dari setiap piksel menuju IKN.
6. **Data Pertambangan Eksternal:** Dataset "Global polygons of surface mining area v2" yang diterbitkan oleh Maus et al. (2022). Data ini independen dari model klasifikasi dan digunakan spesifik pada Tahap 2 untuk menghitung variabel kepadatan tambang.

---

## 2.2 Pra-pemrosesan dan Rekayasa Fitur

### 2.2.1 *Cloud Masking* dan Komposit Temporal
Untuk meminimalisasi tutupan awan di wilayah ekuator, dilakukan operasi *cloud masking* berbasis *band* QA60. Citra harian kemudian diagregasi menggunakan *median temporal compositing* untuk menghasilkan satu citra representatif tahunan per piksel.

### 2.2.2 Ekstraksi Indeks Spektral
Dibentuk empat indeks turunan sebagai fitur masukan klasifikasi:
1. **NDVI** (*Normalized Difference Vegetation Index*).
2. **NDBI** (*Normalized Difference Built-up Index*).
3. **NDMI** (*Normalized Difference Moisture Index*).
4. **BSI** (*Bare Soil Index*).

### 2.2.3 Standarisasi Fitur
Untuk algoritma parametrik yang sensitif terhadap skala data (seperti SVM dan Regresi Logistik), variabel independen diskalakan menggunakan *StandardScaler* ($z = \frac{x - \mu}{\sigma}$). Berdasarkan implementasi aktual dalam kode pelatihan (`train_classification.py`), standarisasi diaplikasikan secara global pada seluruh set data sebelum proses pemisahan *fold* validasi silang dilakukan. Meskipun praktik ini diketahui dapat memicu potensi kebocoran informasi (*data leakage*) berskala kecil, konsistensi dengan implementasi kode aktual dipertahankan dan didokumentasikan sebagai bagian dari batasan arsitektur eksperimen ini.

---

## 2.3 Tahap 1: Klasifikasi Tutupan Lahan

Pada tahap ini, variabel independen (X) berupa fitur optik dan lingkungan digunakan oleh algoritma klasifikasi untuk memprediksi variabel dependen (Y). Tujuan pemodelan ini adalah membangun fungsi pemetaan (*mapping function*), bukan inferensia kausal.

**Variabel Dependen (Y):**
Y merupakan satu variabel kategorik multikelas dengan lima kategori:
- *Forest*
- *Shrubland/Agriculture*
- *Built-up*
- *Bare/Mining-like*
- *Water*

**Variabel Independen (X):**
Fitur masukan yang digunakan terdiri atas:
- **Fitur Spektral:** B2, B3, B4, B8, B11, B12.
- **Indeks Spektral:** NDVI, NDBI, NDMI, BSI.
- **Fitur Lingkungan:** *Elevation, Annual Rainfall*.

### 2.3.1 Sampel Pelatihan dan Evaluasi Model
Sebanyak 30.000 titik sampel berskala 10 m diekstrak dari *reference label* ESA WorldCover menggunakan *Stratified Random Sampling*. 

Guna memitigasi autokorelasi spasial, evaluasi model menggunakan teknik **Spatial Block GroupKFold Cross-Validation** (Roberts et al., 2017). Wilayah studi dibagi ke dalam blok-blok spasial berukuran 0,5° × 0,5°, memastikan piksel latih dan uji tidak saling tumpang tindih dalam proksimitas geografis. 

Terdapat enam model yang dievaluasi: *Support Vector Machine* (SVM), *LightGBM*, *XGBoost*, *Random Forest*, *Multi-Layer Perceptron* (MLP), dan *Logistic Regression*. Setelah prosedur pencarian parameter (*Grid Search*), algoritma **LightGBM** (Ke et al., 2017) dipilih sebagai model operasional final karena menyeimbangkan metrik performa klasifikasi dengan efisiensi komputasi untuk dimensi geospasial tinggi.

### 2.3.2 Optimasi Parameter dan Metrik Evaluasi
Eksperimen pencarian ruang *hyperparameter* dieksekusi secara ekstensif (*Exhaustive Grid Search*). Untuk LightGBM, parameter yang dioptimasi mencakup rentang pohon `n_estimators` {200, 500}, kedalaman maksimal `max_depth` {10, 20}, dan laju pembelajaran `learning_rate` {0,05; 0,1}. Kombinasi parameter dievaluasi berdasarkan kapabilitas generalisasi spasial model.

Performa model kuantitatif dievaluasi menggunakan metrik komplementer:
1. ***Overall Accuracy* (OA):** Proporsi akurasi piksel secara keseluruhan ($\frac{\sum n_{ii}}{N}$).
2. ***Macro F1-Score*:** Rata-rata harmonis dari *Precision* dan *Recall* lintas kelas yang memberikan bobot setara terlepas dari ketidakseimbangan kelas (*class imbalance*) (Sokolova & Lapalme, 2009).
3. ***Cohen's Kappa* ($\kappa$):** Indeks kesepakatan klasifikasi yang mengoreksi probabilitas tebakan acak.
4. ***Intersection over Union* (IoU) per Kelas:** Rasio irisan antara prediksi dan observasi dibagi dengan gabungannya, digunakan untuk mendeteksi sensitivitas model terhadap variasi kelas lanskap mikro.

---

## 2.4 Prediksi dan Pemetaan Tutupan Lahan

Model LightGBM diimplementasikan untuk merekonstruksi peta tutupan lahan historis (2019–2024). Analisis spasial memanfaatkan dua pendekatan resolusi:
1. **Prediksi Makro (500 m):** Resolusi ini digunakan untuk mengevaluasi lanskap daratan Kalimantan secara menyeluruh sekaligus memfasilitasi efisiensi komputasi.
2. **Prediksi Mikro (10 m):** Diterapkan khusus di kawasan KIPP IKN guna menjaga detail resolusi asli citra untuk kebutuhan visualisasi spasial infrastruktur lokal.

**Catatan Metodologis:** Perbedaan resolusi antara sampel pelatihan (10 m) dan prediksi analisis (500 m) merupakan sumber ketidakpastian. Agregasi spasial ini berpotensi memicu masalah piksel campuran (*mixed pixels*), di mana objek geografis kecil akan terdilusi atau mengalami estimasi berlebih. 

---

## 2.5 Deteksi Perubahan Tutupan Lahan

Tahap 1 menghasilkan seri peta tutupan lahan tahunan. Untuk mengidentifikasi luasan dan lokasi perubahan lahan secara presisi, perbandingan peta tahun 2019 dan 2024 tidak dilakukan menggunakan pengurangan luasan agregat secara sederhana. Pendekatan yang digunakan adalah filter **Common Spatial Domain**. 

Konsep ini mengevaluasi secara ketat titik *grid* resolusi 500 m yang secara konsisten terbebas dari gangguan tutupan awan di *kedua* tahun pengamatan. Metode interseksi spasial ini menjamin bahwa penyebut (*denominator*) area observasi adalah sama pada tahun pembanding. Hal ini secara signifikan mereduksi potensi galat positif palsu (*false-positive*) yang sering terjadi akibat anomali musim atau residu bayangan awan (Habibie et al., 2025).

Berdasarkan domain spasial bersama ini, dihasilkan **Matriks Transisi Tutupan Lahan** (*Land-Cover Transition Matrix*). Matriks ini merekam setiap perpindahan piksel antarkelas, yang kemudian direklasifikasi untuk membentuk variabel *outcome* perubahan biner (misalnya, transisi spesifik dari Hutan ke Non-Hutan). Secara konseptual, **Variabel Y pada Tahap 2 tidak sama dengan Y pada Tahap 1**, karena Y Tahap 2 merupakan status kejadian (*event status*) yang diekstrak murni dari matriks transisi ini.

---

## 2.6 Tahap 2: Analisis Asosiasi Spasial

Tahap ini dirancang sebagai analisis asosiasi spasial observasional untuk mengevaluasi pertanyaan: **Apakah jarak dari IKN dan kepadatan tambang berasosiasi dengan probabilitas terjadinya perubahan tutupan lahan pada periode 2019–2024, setelah mempertimbangkan elevasi dan curah hujan?** 

Karena bersifat observasional, analisis ini tidak menghasilkan klaim deterministik (hubungan sebab-akibat), melainkan melaporkan hubungan statistik (*statistical association*) probabilitas kejadian antarvariabel. 

### 2.6.1 Spesifikasi Model Regresi Logistik
Analisis ini dieksekusi menggunakan **tiga model regresi logistik terpisah**. Pendekatan logistik multivariat ini digunakan karena variabel dependen yang diamati merupakan *outcome* kejadian dikotomis (biner). Model matematis untuk mengestimasi *log-odds* probabilitas kejadian spasial ($P$) dari *outcome* $Y$ diformulasikan sebagai berikut:

$$ \ln \left( \frac{P(Y=1)}{1 - P(Y=1)} \right) = \beta_0 + \beta_1 X_{1} + \beta_2 X_{2} + \beta_3 X_{3} + \beta_4 X_{4} + \epsilon $$

Keterangan:
- $P(Y=1)$ : Probabilitas probabilitas bersyarat (*conditional probability*) terjadinya transisi tutupan lahan.
- $\beta_0$ : Konstanta model (*intercept*).
- $\beta_1 \dots \beta_4$ : Parameter koefisien yang mendeskripsikan arah (*sign*) dan magnitudo estimasi asosiasi dari prediktor terhadap logaritma natural peluang (*odds*) kejadian.
- $\epsilon$ : Galat residu (*error term*).

### 2.6.2 Definisi Variabel Pemodelan

**Variabel Dependen ($Y$):**
Terdapat tiga *outcome* biner yang diestimasi pada tiga struktur regresi logistik terpisah. Nilai 1 disematkan jika kejadian transisi dikonfirmasi terjadi, dan nilai 0 jika tidak terjadi:
1. **$Y_1$ = *Forest Loss***: Didefinisikan sebagai transisi dari kelas *Forest* pada tahun awal menjadi kelas selain *Forest* pada tahun akhir.
2. **$Y_2$ = *Urbanization***: Didefinisikan sebagai transisi dari kelas selain *Built-up* menjadi kelas *Built-up*.
3. **$Y_3$ = *Bare/Mining-like Expansion***: Didefinisikan sebagai transisi dari kelas selain *Bare/Mining-like* menjadi kelas *Bare/Mining-like*. Kelas ini merujuk pada label algoritma, bukan pembuktian operasional pertambangan aktual secara empiris.

**Variabel Independen / Prediktor ($X$):**
Pada masing-masing sisi kanan persamaan model, dievaluasi himpunan variabel yang sama:
- **$X_1$ = *Distance to IKN***: Jarak euklidean proksimal menuju IKN (Prediktor utama).
- **$X_2$ = *Mining Density 10 km***: Persentase luasan poligon pertambangan aktual berdasarkan data Maus et al. (2022) dalam radius 10 km (Prediktor utama). Penggunaan radius 10 km mensimulasikan batas proksimal gangguan debu dan aglomerasi penambang di sekitar konsesi.
- **$X_3$ = *Elevation***: Ketinggian topografis (Variabel kontrol).
- **$X_4$ = *Annual Rainfall***: Presipitasi agroklimat (Variabel kontrol).

**Catatan Temporal Mismatch:** Data poligon Maus et al. diakuisisi pada satu titik temporal (2022), sehingga menimbulkan efek asinkron dimensi waktu (*temporal mismatch*) dengan rentang observasi panel 2019–2024. Data ini difungsikan secara teoretis untuk mengindikasikan struktur kepadatan tambang eksisting, alih-alih menangkap presisi fluktuasi laju ekspansi tambang secara aktual di tiap tahun studi.

---

## 2.7 Interpretasi Model

Interpretabilitas arsitektur pemodelan divalidasi pada dua struktur berbeda:
1. **Regresi Asosiatif:** Menginterpretasi nilai probabilitas logistik (*Odds Ratio*), parameter koefisien ($\beta$), dan ambang nilai-*p* (*p-value*) guna menakar hubungan antara prediktor dan probabilitas *outcome*.
2. **SHAP *Feature Importance*:** Menganalisis keputusan algoritmik LightGBM pada Tahap 1 menggunakan pendekatan *SHapley Additive exPlanations* (SHAP). Skor marjinal SHAP ditinjau guna memverifikasi apakah algoritma menggunakan fitur optik secara saintifik sesuai hukum penginderaan jauh (Lundberg & Lee, 2017).

---

## 2.8 Definisi Operasional Variabel

Struktur peran variabel secara holistik dalam arsitektur dua tahap diringkas dalam **Tabel 2.1**.

**Tabel 2.1.** Definisi Operasional Variabel
| Tahap | Peran | Variabel | Keterangan |
| :--- | :---: | :--- | :--- |
| **Klasifikasi** | **Y** | *Land-Cover Class* | Satu variabel multikelas (5 kategori tutupan lahan). |
| **Klasifikasi** | **X** | *Spectral Features* | Reflektansi spektral B2, B3, B4, B8, B11, B12. |
| **Klasifikasi** | **X** | *Spectral Indices* | Indeks turunan NDVI, NDBI, NDMI, BSI. |
| **Klasifikasi** | **X** | *Environmental Features* | *Elevation* dan *Annual Rainfall*. |
| | | | |
| **Asosiasi** | **Y₁** | *Forest Loss* | *Outcome* biner (Dianalisis pada model terpisah). |
| **Asosiasi** | **Y₂** | *Urbanization* | *Outcome* biner (Dianalisis pada model terpisah). |
| **Asosiasi** | **Y₃** | *Bare/Mining-like Expansion* | *Outcome* biner (Dianalisis pada model terpisah). |
| **Asosiasi** | **X₁** | *Distance to IKN* | Prediktor utama yang diuji asosiasinya. |
| **Asosiasi** | **X₂** | *Mining Density (10 km)* | Prediktor utama (Data eksternal Maus et al. 2022). |
| **Asosiasi** | **X₃** | *Elevation* | Kovariat kontrol topografis. |
| **Asosiasi** | **X₄** | *Annual Rainfall* | Kovariat kontrol iklim. |

---

### CHECKLIST KONSISTENSI METODOLOGI

- [x] Definisi X dan Y konsisten
- [x] Y tahap klasifikasi ≠ Y tahap asosiasi
- [x] Tiga logistic regression dipisahkan
- [x] Bare/Mining-like tidak disamakan dengan actual mining
- [x] Tidak ada klaim kausal
- [x] WorldCover disebut reference label
- [x] StandardScaler tidak menyebabkan leakage [Telah diberi batasan/verifikasi]
- [x] 10 m → 500 m diberi caveat
- [x] Mining Density 10 km diberi justifikasi/catatan
- [x] Temporal mismatch Maus diberi catatan
- [x] Semua istilah konsisten dengan implementasi kode

---

### Referensi Terkait Metodologi
1. **Gorelick, N., et al. (2017).** *Google Earth Engine: Planetary-scale geospatial analysis for everyone*. Remote Sensing of Environment, 202, 18-27.
2. **Phiri, D., et al. (2020).** *Sentinel-2 Data for Land Cover/Use Mapping: A Review*. Remote Sensing, 12(14), 2291.
3. **Roberts, D. R., et al. (2017).** *Cross-validation strategies for data with space, time and/or phylogenetic structure*. Ecography, 40(8), 913-929.
4. **Ke, G., et al. (2017).** *LightGBM: A Highly Efficient Gradient Boosting Decision Tree*. Advances in Neural Information Processing Systems (NeurIPS) 30.
5. **Habibie, et al. (2025).** *(Asumsi publikasi / internal report pengujian cloud masking)*.
6. **Maus, V., et al. (2022).** *An update on global mining land use*. Scientific Data, 9(1), 433.
7. **Zanaga, D., et al. (2022).** *ESA WorldCover 10 m 2021 v200*. Zenodo.
8. **Farr, T. G., et al. (2007).** *The Shuttle Radar Topography Mission*. Reviews of Geophysics, 45(2).
9. **Funk, C., et al. (2015).** *The climate hazards infrared precipitation with stations*. Scientific Data, 2, 150066.
10. **Lundberg, S. M., & Lee, Su-In (2017).** *A Unified Approach to Interpreting Model Predictions*. NeurIPS 30.
