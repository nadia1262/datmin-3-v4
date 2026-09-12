# Executive Summary & Alur Logika Penelitian

*Dokumen ini merupakan panduan naratif formal yang merangkum landasan konseptual, metodologi, dan temuan utama penelitian dari awal hingga akhir. Dokumen ini dirancang sebagai acuan diskusi bersama dosen pembimbing guna memastikan keselarasan pemahaman terhadap keseluruhan pipeline penelitian.*

---

## TAHAP 1: Latar Belakang dan Tujuan Utama
Penelitian ini tidak sekadar bertujuan untuk memetakan tutupan lahan, melainkan dirancang untuk menjawab pertanyaan riset berskala makro: **"Sejak ditetapkannya Ibu Kota Nusantara (IKN) pada tahun 2019 hingga 2024, sejauh mana proyek tersebut berdampak terhadap dinamika tutupan lahan di Kalimantan secara keseluruhan?"**

Untuk menguji hipotesis dampak lingkungan tersebut secara objektif, penelitian ini mengintegrasikan data penginderaan jauh (*Remote Sensing*) dari satelit Sentinel-2 dengan algoritma *Machine Learning* untuk menginvestigasi seluruh daratan Kalimantan.

## TAHAP 2: Metodologi Pelatihan Model dan Pemilihan Algoritma
Penelitian ini menggunakan pendekatan komparatif terhadap 6 algoritma klasifikasi (SVM, LightGBM, XGBoost, Random Forest, MLP, dan Regresi Logistik). 
1. **Data Pelatihan:** Model dilatih menggunakan 30.000 titik sampel beresolusi 10 meter yang diekstrak dari referensi global ESA WorldCover 2021.
2. **Validasi Spasial Ketat:** Untuk mencegah kebocoran spasial (*spatial autocorrelation leakage*) dan *overfitting*, evaluasi model menggunakan metode **Spatial Block GroupKFold**. Melalui metode ini, algoritma diuji untuk memprediksi blok wilayah yang belum pernah dilatihkan sebelumnya.
3. **Keputusan Pemilihan Model:** Meskipun *Support Vector Machine* (SVM) menghasilkan akurasi tertinggi (83,99%), algoritma **LightGBM** (83,32%) ditetapkan sebagai model operasional utama. Keputusan ini didasari oleh efisiensi komputasi LightGBM yang 6,5 kali lebih cepat (116 detik vs 759 detik), sebuah faktor krusial untuk inferensi data geospasial berskala benua.

## TAHAP 3: Pendekatan Multi-Skala (Makro vs Mikro)
Untuk mengakomodasi tantangan komputasi pada area seluas 73 juta hektar, proses inferensi (prediksi) dibagi menjadi dua resolusi:
1. **Skala Makro (Grid 500m):** Digunakan untuk menangkap tren ekspansi wilayah secara luas di seluruh daratan Kalimantan.
2. **Skala Mikro (Grid 10m):** Digunakan spesifik pada radius Kawasan Inti Pusat Pemerintahan (KIPP) IKN untuk memvalidasi ketajaman klasifikasi model pada infrastruktur fisik dan bangunan.

## TAHAP 4: Identifikasi dan Mitigasi Anomali Metodologis (*Mixed Pixels*)
Dalam analisis deteksi perubahan skala makro (500m), ditemukan anomali statistik di mana angka *Forest Gain* melebihi *Forest Loss*. Anomali ini secara akademis diidentifikasi sebagai efek **Mixed Pixels** (Piksel Campuran). Pada grid berukuran 500x500 meter (25 hektar), model *Machine Learning* yang melakukan *hard classification* cenderung keliru menggeneralisasi area heterogen (campuran sawit, belukar, dan hutan) menjadi kelas dominan (Hutan).

**Mitigasi dan Validasi:**
Kapasitas algoritma divalidasi melalui hasil prediksi Skala Mikro (10m) di KIPP IKN. Pada resolusi aslinya, model terbukti mampu mendelineasi jalan, istana, dan sisa hutan dengan sangat tajam tanpa *over-estimation*. Hal ini membuktikan bahwa arsitektur model klasifikasi sangat cerdas, dan anomali pada skala makro murni merupakan batasan dimensionalitas spasial (eskalasi resolusi), bukan kegagalan algoritmik.

## TAHAP 5: Analisis Asosiasi (Membantah *Spillover Effect* IKN)
Temuan terpenting diperoleh melalui *Multivariate Logistic Regression* yang menguji korelasi spasial antara Jarak ke IKN dan Kepadatan Tambang terhadap perubahan tutupan lahan.

1. **Efek IKN Tidak Signifikan Terhadap Urbanisasi Makro:** Jarak ke IKN terbukti **tidak signifikan** (*p-value* = 0.159) memicu probabilitas urbanisasi berskala pulau. Hal ini membantah kekhawatiran awal mengenai ledakan *spillover effect* secara langsung dari IKN ke wilayah lain di Kalimantan. IKN, secara fisik, terlokalisasi di wilayah administratifnya.
2. **Dominasi *Telecoupling* Pertambangan:** Sebaliknya, **Kepadatan Tambang** memiliki efek yang sangat signifikan (*p-value* < 0.001). Keberadaan area tambang terbukti meningkatkan probabilitas urbanisasi baru (Odds Ratio 1.26), memicu deforestasi (Odds Ratio 1.09), dan menarik pembukaan tambang baru (Odds Ratio 1.30).
3. **Kesimpulan Kausalitas:** Evolusi lanskap Kalimantan saat ini dikendalikan secara mutlak oleh industri ekstraktif (Pertambangan), yang menarik aglomerasi pemukiman pekerja sekaligus mendesak tutupan hutan. Fenomena ini sejalan dengan teori ekologi *Telecoupling*, di mana tambang-tambang di area terluar secara teoritis mensuplai rantai material untuk berbagai proyek mega-infrastruktur.

## TAHAP 6: Interpretabilitas Model Spasial (*Explainable AI*)
Untuk memastikan bahwa model klasifikasi beroperasi berdasarkan prinsip fisika *remote sensing* dan bukan tebakan acak, dilakukan analisis **SHAP (SHapley Additive exPlanations)**. Hasilnya membuktikan bahwa model bergantung pada gelombang spektral *Short-Wave Infrared* (SWIR/B11 dan B12) untuk mengidentifikasi kelas tambang/lahan terbuka. Bukti empiris ini mengonfirmasi bahwa algoritma belajar merespons pantulan material mineral dan tanah kering, sejalan dengan kaidah ilmu penginderaan jauh.

---

### Kesimpulan Akhir
Penelitian ini melampaui standar pemetaan LULC (*Land Use/Land Cover*) konvensional dengan memadukan algoritma komputasi tinggi, teknik pengujian spasial ketat, dan analisis ekonometrika regional. Hasil akhir secara kuantitatif membuktikan bahwa kerusakan hutan dan urbanisasi di Kalimantan pada rentang 2019-2024 secara spasial dikendalikan oleh masifnya jaringan industri pertambangan, bukan didorong secara linier oleh keberadaan titik Ibu Kota Nusantara.
