# Latar Belakang dan Tujuan Penelitian

## Prediksi Skor Indeks Desa Membangun (IDM) Menggunakan Fitur Spasial Eksternal Berbasis Remote Sensing, Aksesibilitas, dan Konteks Wilayah dengan Pendekatan Multi-Algorithm Spatial Machine Learning di Kalimantan

---

## 1. LATAR BELAKANG

### 1.1 Urgensi Pengukuran Pembangunan Desa di Indonesia

Indonesia memiliki lebih dari 74.000 desa yang tersebar di seluruh kepulauan, menjadikannya salah satu negara dengan unit administrasi terkecil terbanyak di dunia. Sejak diberlakukannya Undang-Undang Nomor 6 Tahun 2014 tentang Desa, pemerintah mengalokasikan Dana Desa secara langsung ke setiap desa dengan total kumulatif yang telah mencapai ratusan triliun rupiah. Besarnya investasi ini memerlukan instrumen monitoring yang akurat, tepat waktu, dan mampu menangkap kondisi riil di lapangan.

Instrumen utama yang digunakan pemerintah untuk mengukur tingkat kemajuan dan kemandirian desa adalah **Indeks Desa Membangun (IDM)**, yang dikembangkan oleh Kementerian Desa, Pembangunan Daerah Tertinggal, dan Transmigrasi. IDM mengkombinasikan tiga dimensi — Ketahanan Sosial (IKS), Ketahanan Ekonomi (IKE), dan Ketahanan Lingkungan (IKL) — menjadi satu skor komposit pada rentang 0 hingga 1. Berdasarkan skor tersebut, setiap desa diklasifikasikan menjadi lima status: Sangat Tertinggal, Tertinggal, Berkembang, Maju, atau Mandiri.

Meskipun IDM telah menjadi acuan nasional, proses pengumpulan datanya masih bergantung pada **survei berbasis kuesioner** yang dilaporkan oleh aparatur desa. Mekanisme ini memiliki beberapa kelemahan fundamental: (1) subjektivitas pelaporan, di mana kualitas data sangat bergantung pada pemahaman dan kejujuran pelapor; (2) keterlambatan temporal, karena data survei memerlukan waktu berbulan-bulan untuk dikompilasi dan diverifikasi; serta (3) biaya operasional tinggi, terutama untuk menjangkau desa-desa terpencil di kawasan Indonesia bagian timur dan pedalaman pulau-pulau besar seperti Kalimantan. Keterbatasan ini membuka pertanyaan: **apakah kondisi pembangunan desa dapat diestimasi dari sinyal-sinyal spasial yang tersedia secara terbuka — tanpa harus menunggu hasil survei lapangan?**

### 1.2 Potensi Remote Sensing dan Data Geospasial Terbuka

Perkembangan teknologi penginderaan jauh (remote sensing) dan ketersediaan data geospasial terbuka telah membuka paradigma baru dalam pengukuran pembangunan. Citra satelit tidak lagi hanya merekam tampilan visual permukaan bumi, tetapi juga mengandung **sinyal-sinyal proxy** yang secara tidak langsung mencerminkan kondisi sosio-ekonomi suatu wilayah.

**Cahaya malam (Nighttime Lights/NTL)** dari sensor VIIRS, misalnya, telah digunakan secara luas dalam literatur sebagai proxy aktivitas ekonomi. Intensitas cahaya malam berkorelasi kuat dengan PDB, konsumsi listrik, dan tingkat urbanisasi. Di Kalimantan, variasi NTL sangat dramatis — dari area minerba dan kota-kota pesisir yang sangat terang, hingga pedalaman hutan primer yang nyaris tanpa cahaya — menciptakan sinyal yang kaya secara informasional.

**Fraksi area terbangun (built-up area)** dari Global Human Settlement Layer (GHSL) merekam perluasan permukiman fisik dari waktu ke waktu. **Indeks vegetasi (NDVI dan EVI)** dari MODIS menangkap tutupan lahan dan degradasi lingkungan. **Suhu permukaan daratan (LST)** mengindikasikan efek pulau panas perkotaan. **Data kehilangan hutan (forest loss)** dari Hansen/UMD merekam deforestasi kumulatif. Seluruh data ini tersedia secara gratis melalui platform Google Earth Engine (GEE).

Di sisi lain, **data aksesibilitas** — berupa waktu tempuh ke kota terdekat dan fasilitas kesehatan — telah dikompilasi secara global oleh Malaria Atlas Project (Oxford University) menggunakan friction surface yang memperhitungkan jaringan jalan, topografi, dan tutupan lahan. Data ini, bersama dengan informasi topografi dari SRTM, estimasi populasi dari WorldPop, dan infrastruktur jalan dari OpenStreetMap, membentuk gambaran multidimensional tentang **konteks spasial desa** yang tidak mungkin diperoleh dari kuesioner konvensional.

### 1.3 Kesenjangan Penelitian (Research Gap)

Studi-studi sebelumnya yang memanfaatkan machine learning untuk analisis IDM umumnya memiliki satu kelemahan fundamental: mereka menggunakan **komponen-komponen penyusun IDM itu sendiri sebagai fitur prediktor**. Misalnya, menggunakan jumlah fasilitas kesehatan (yang merupakan indikator IKS) untuk memprediksi skor IDM yang sudah mengandung variabel tersebut dalam perhitungannya. Pendekatan ini bersifat **tautologis** — model hanya merekonstruksi formula komposit yang sudah diketahui, tanpa menghasilkan pengetahuan baru tentang apa yang sebenarnya mendorong kemandirian desa.

Penelitian ini mengambil pendekatan yang secara fundamental berbeda. Seluruh fitur yang digunakan bersumber dari **sinyal spasial eksternal** — data yang bukan merupakan komponen penyusun IDM dan tidak diperoleh melalui survei yang sama. Pendekatan ini memiliki beberapa keunggulan metodologis:

1. **Bebas dari data leakage** — tidak ada overlap antara fitur prediktor dan variabel target.
2. **Reproducible** — seluruh sumber data bersifat open access dan dapat diakses oleh siapa pun melalui GEE, Geofabrik, dan portal data terbuka.
3. **Scalable** — metode yang sama dapat diaplikasikan ke seluruh Indonesia tanpa memerlukan survei tambahan.
4. **Interpretable secara kebijakan** — fitur-fitur spasial yang teridentifikasi sebagai prediktor kuat dapat langsung diterjemahkan menjadi rekomendasi intervensi pembangunan yang terukur.

### 1.4 Mengapa Kalimantan?

Kalimantan dipilih sebagai wilayah studi karena beberapa alasan substantif:

**Pertama, heterogenitas pembangunan yang ekstrem.** Kalimantan memiliki rentang variasi IDM yang sangat lebar. Di satu sisi terdapat pusat-pusat urban seperti Balikpapan, Samarinda, dan Banjarmasin dengan infrastruktur modern; di sisi lain terdapat ribuan desa di pedalaman Kalimantan Tengah, Kalimantan Barat, dan Kalimantan Utara yang masih berstatus Sangat Tertinggal dengan akses jalan yang nyaris tidak ada. Variasi yang besar ini merupakan kondisi ideal untuk supervised learning — model memiliki cukup variasi pada target variable untuk belajar pola yang bermakna.

**Kedua, sinyal remote sensing yang sangat kaya.** Kalimantan menghadirkan lanskap yang unik: kombinasi antara area pertambangan batubara dan migas yang sangat terang di citra malam, perkebunan kelapa sawit yang mendominasi dataran rendah, hutan hujan tropis primer yang masih tersisa di pegunungan Müller dan dataran tinggi, serta kawasan pesisir dengan dinamika pembangunan tersendiri. Diversitas tutupan lahan ini menciptakan variasi fitur remote sensing yang memungkinkan model menangkap pola yang tidak bisa ditangkap oleh satu atau dua variabel saja.

**Ketiga, tantangan aksesibilitas yang nyata.** Kalimantan memiliki jaringan jalan yang sangat terbatas di pedalaman. Banyak desa hanya bisa diakses melalui jalur sungai atau penerbangan perintis. Kondisi ini menjadikan fitur aksesibilitas (waktu tempuh ke kota, kepadatan jalan) sebagai prediktor yang secara teoritis sangat kuat — dan juga menjadikan metode monitoring berbasis remote sensing sangat relevan, karena justru desa-desa yang paling sulit dijangkau surveyor adalah desa yang paling membutuhkan monitoring.

**Keempat, dinamika pembangunan yang kontemporer.** Kalimantan mengalami transformasi ekonomi yang signifikan: ekspansi perkebunan sawit, industri pertambangan, dan wacana pembangunan Ibu Kota Nusantara (IKN). Dinamika ini menciptakan pola pembangunan yang tidak merata dan berubah cepat — kondisi yang hanya bisa dimonitor secara efektif melalui pendekatan spasial dan satelit.

Dengan sekitar **5.900 desa/kelurahan** yang tersebar di lima provinsi (Kalimantan Barat, Kalimantan Tengah, Kalimantan Selatan, Kalimantan Timur, dan Kalimantan Utara), Kalimantan menyediakan sample size yang memadai untuk perbandingan sistematik enam algoritma regresi dengan statistical power yang cukup.

### 1.5 Pendekatan Multi-Algorithm dan Interpretabilitas

Penelitian ini tidak hanya bertujuan menghasilkan prediksi akurat, tetapi juga memahami **mengapa** dan **di mana** model bekerja baik atau gagal. Untuk itu, digunakan pendekatan multi-algorithm yang membandingkan enam algoritma regresi dengan karakteristik yang berbeda — dari model linear sederhana (Linear Regression, Ridge) hingga ensemble nonlinear (Random Forest, Gradient Boosting, XGBoost) dan kernel-based (SVR). Perbandingan ini bukan sekadar benchmark performa, tetapi juga menjadi eksperimen untuk menguji apakah hubungan antara sinyal spasial dan kemandirian desa bersifat linear atau mengandung interaksi dan nonlinearitas yang hanya bisa ditangkap oleh model yang lebih kompleks.

Lebih dari itu, penggunaan **SHAP (SHapley Additive exPlanations)** analysis memungkinkan dekomposisi kontribusi setiap fitur terhadap prediksi, baik secara global maupun lokal per desa. Analisis ini menjawab pertanyaan kritis: **apa yang paling menentukan kemandirian desa di setiap zona Kalimantan?** Apakah NTL dan road density mendominasi di desa pesisir dekat industri ekstraktif? Apakah jarak ke kota dan kemiringan lereng mendominasi di desa pegunungan? Pemetaan fitur dominan per desa (Spatial SHAP Map) menjadi kontribusi visual dan analitis yang membedakan penelitian ini dari studi prediktif konvensional.

**Analisis residual spasial** melengkapi narasi dengan mengidentifikasi desa-desa yang *overperforming* (IDM aktual lebih tinggi dari prediksi — mengindikasikan faktor non-fisik seperti kualitas kepemimpinan atau modal sosial) dan desa-desa yang *underperforming* (IDM aktual lebih rendah dari yang seharusnya — mengindikasikan hambatan non-fisik seperti governance yang buruk atau konflik). Insight ini memiliki nilai kebijakan yang sangat tinggi karena mengarahkan perhatian pada desa-desa yang memerlukan intervensi berbeda dari pola umum.

---

## 2. TUJUAN PENELITIAN

### 2.1 Tujuan Umum

Membangun model prediksi skor Indeks Desa Membangun (IDM) berbasis fitur spasial eksternal yang bersumber dari remote sensing, data aksesibilitas, dan konteks wilayah menggunakan pendekatan multi-algorithm spatial machine learning, serta menganalisis faktor-faktor spasial yang paling menentukan tingkat kemandirian desa di Kalimantan.

### 2.2 Tujuan Khusus

1. **Mengevaluasi dan membandingkan performa enam algoritma regresi** — Linear Regression, Ridge Regression, Random Forest, Gradient Boosting, XGBoost, dan Support Vector Regression (SVR) — dalam memprediksi skor IDM desa-desa di Kalimantan berdasarkan metrik R², RMSE, MAE, dan MAPE, dengan menggunakan spatial cross-validation untuk menghindari spatial leakage.

2. **Mengidentifikasi fitur spasial eksternal yang paling dominan** dalam menjelaskan variasi skor IDM melalui SHAP (SHapley Additive exPlanations) analysis, dan menganalisis apakah kontribusi relatif fitur-fitur tersebut berbeda secara spasial antar zona geografis di Kalimantan (pesisir vs pedalaman, dataran rendah vs pegunungan, urban fringe vs rural terpencil).

3. **Memetakan pola residual spasial** (selisih antara IDM aktual dan prediksi) untuk mengidentifikasi desa-desa yang *overperforming* dan *underperforming* relatif terhadap kondisi spasialnya, serta mengeksplorasi fenomena pembangunan yang dapat menjelaskan pola tersebut.

4. **Membangun visualisasi spasial interaktif** berupa peta choropleth IDM aktual, IDM prediksi, residual, dan fitur dominan per desa sebagai instrumen komunikasi hasil analisis yang dapat diakses oleh pengambil kebijakan.

---

## 3. MANFAAT PENELITIAN

### 3.1 Manfaat Akademis

- Memberikan kontribusi metodologis berupa framework prediksi indeks pembangunan desa yang bebas dari tautologi dan data leakage, menggunakan fitur spasial eksternal yang sepenuhnya independent dari komponen penyusun IDM.
- Menyediakan bukti empiris tentang hubungan nonlinear antara sinyal remote sensing, aksesibilitas, dan kemandirian desa — sesuatu yang tidak dapat ditangkap oleh analisis regresi konvensional.
- Memperkenalkan penggunaan Spatial SHAP Analysis untuk memvisualisasikan heterogenitas faktor-faktor penentu pembangunan desa secara spasial, sebuah pendekatan yang masih jarang digunakan dalam konteks pembangunan pedesaan di Indonesia.

### 3.2 Manfaat Praktis

- Menyediakan metode estimasi IDM yang lebih cepat dan lebih murah untuk desa-desa yang belum tersurvei atau terlambat melaporkan data, khususnya di wilayah terpencil Kalimantan.
- Mengidentifikasi desa-desa *underperforming* yang memerlukan perhatian khusus dari pemerintah — yaitu desa-desa yang kondisi spasialnya seharusnya mendukung pembangunan, tetapi skor IDM-nya tetap rendah, mengindikasikan adanya hambatan non-fisik yang perlu diinvestigasi lebih lanjut.
- Memberikan rekomendasi berbasis data tentang prioritas intervensi pembangunan berdasarkan fitur spasial yang paling berpengaruh di setiap zona, sehingga alokasi sumber daya dapat lebih tepat sasaran.

### 3.3 Manfaat Metodologis

- Seluruh pipeline penelitian — dari pengumpulan data hingga modeling — menggunakan tools open-source dan data open access (Google Earth Engine, Python, QGIS, OpenStreetMap), sehingga sepenuhnya reproducible oleh peneliti lain.
- Framework yang dihasilkan bersifat scalable dan dapat diadaptasi ke provinsi atau pulau lain di Indonesia, maupun ke negara berkembang lain yang memiliki indeks pembangunan desa serupa.
