import os
from config_and_helpers import (
    h2, h3, h4, body, numbered_item, bullet_item, equation,
    add_academic_table, add_image_figure
)

def build_section_3(doc):
    h2(doc, "BAB III METODE PENELITIAN")
    
    h3(doc, "3.1 Desain Penelitian dan Alur Kerja Metodologis")
    body(
        doc,
        "Penelitian ini menerapkan kerangka kerja metodologis geospasial sekuensial yang merangkai tiga tahapan logis terintegrasi: "
        "Klasifikasi Tutupan Lahan (Tahap 1) → Deteksi Perubahan Spasiotemporal (Tahap 2) → Analisis Asosiasi Spasial Faktor Pendorong (Tahap 3). "
        "Secara konseptual, Tahap 1 mengekstraksi informasi tematik permukaan bumi dari citra satelit multispektral menggunakan algoritma machine learning "
        "yang tervalidasi secara spasial. Tahap 2 membandingkan hasil klasifikasi multi-tahun pada Common Spatial Domain tetap guna mengidentifikasi "
        "arah dan magnitudo transisi lahan secara objektif. Selanjutnya, Tahap 3 menguji keterkaitan spasial antara kejadian perubahan lahan "
        "tersebut dengan pusat pertumbuhan IKN dan klaster penambangan batubara menggunakan regresi logistik multivariat."
    )
    
    # Embed Gambar 3.1 Diagram Alir Penelitian
    img_flow = r"reports/_extracted_draft_images/image4.png"
    add_image_figure(
        doc, img_flow,
        caption="Gambar 3.1 Diagram Alir Metodologi Penelitian Tiga Tahap: Klasifikasi, Deteksi Perubahan, dan Regresi Logistik Spasial",
        source="Sumber: Desain Alur Metodologis Peneliti (2024)",
        width_cm=14.5
    )
    
    h3(doc, "3.2 Data dan Sumber Data")
    body(
        doc,
        "Pelaksanaan penelitian ini mengintegrasikan enam sumber data geospasial multi-sensor dan multi-resolusi yang diperoleh dari repositori "
        "ilmiah bereputasi global dan institusi pemerintah resmi. Rincian spesifikasi teknis dataset disajikan pada Tabel 3.1."
    )
    
    # Tabel Spesifikasi Data
    t_data_headers = ["Dataset / Variabel", "Sumber / Sensor", "Resolusi Spasial", "Resolusi Temporal / Tahun", "Peran dalam Analisis"]
    t_data_rows = [
        [
            "Citra Reflektansi Permukaan (Level-2A)",
            "Sentinel-2 MSI (Copernicus ESA)",
            "10 m & 20 m",
            "2019–2024 (Komposit Median Tahunan)",
            "Fitur masukan spektral utama (6 kanal optik & 4 indeks spektral) untuk Tahap 1."
        ],
        [
            "Peta Referensi Tutupan Lahan Global",
            "ESA WorldCover 2021 v200",
            "10 m",
            "Tahun Dasar 2021",
            "Label kebenaran lapangan (ground truth) untuk melatih dan menguji model machine learning."
        ],
        [
            "Model Elevasi Digital (DEM)",
            "SRTM v3.0 (NASA / USGS)",
            "30 m (1 arc-second)",
            "Statik (Tahun 2000)",
            "Kovariat biofisik topografi lingkungan pada pemodelan regresi logistik spasial Tahap 3."
        ],
        [
            "Presipitasi Curah Hujan Tahunan",
            "CHIRPS v2.0 (UCSB Climate Hazards Group)",
            "0,05° (~5,5 km)",
            "2019–2024 (Akumulasi Tahunan)",
            "Kovariat kontrol variabilitas iklim pada pemodelan regresi logistik spasial Tahap 3."
        ],
        [
            "Delineasi Batas Administrasi IKN & KIPP",
            "Otorita IKN & Kementerian ATR/BPN",
            "Vektor Poligon / Titik",
            "UU No. 3/2022 & UU No. 21/2023",
            "Penentuan koordinat sentroid KIPP (0,964°LS, 116,701°BT) untuk menghitung jarak Euklidian."
        ],
        [
            "Konsesi Tambang Permukaan Global",
            "Maus et al. (2022) & Minerba ESDM",
            "Vektor Poligon Poligon Tambang",
            "Update 2022 / Statik",
            "Penyusunan variabel densitas tambang (moving window radius 10 km) pada Tahap 3."
        ]
    ]
    t_data_widths = [3.2, 2.8, 2.2, 2.5, 4.3]
    add_academic_table(
        doc, t_data_headers, t_data_rows,
        caption="Tabel 3.1 Spesifikasi Dataset Geospasial Multi-Sumber yang Digunakan dalam Penelitian",
        source="Sumber: Kompilasi Metadata Sumber Data oleh Peneliti (2024)",
        col_widths=t_data_widths
    )
    
    h3(doc, "3.3 Pra-pemrosesan Citra dan Rekayasa Fitur")
    
    h4(doc, "3.3.1 Cloud Masking dan Komposit Temporal Median Tahunan")
    body(
        doc,
        "Wilayah ekuatorial Pulau Kalimantan memiliki tantangan tutupan awan konvektif tebal yang persisten sepanjang tahun. "
        "Untuk menghasilkan observasi permukaan bebas awan yang representatif, penelitian ini memanfaatkan platform Google Earth Engine (GEE). "
        "Seluruh citra Sentinel-2 Level-2A dalam rentang temporal 1 Januari hingga 31 Desember untuk setiap tahun pengamatan (2019–2024) "
        "disaring menggunakan algoritma penapisan awan berbasis pita Scene Classification Layer (SCL) dan bitmask QA60. "
        "Piksel yang teridentifikasi sebagai awan tebal, awan tipis (cirrus), dan bayangan awan diisolasi dan dieliminasi."
    )
    body(
        doc,
        "Koleksi citra berperiode jamak yang telah bersih selanjutnya direduksi menjadi satu citra komposit tahunan tunggal "
        "menggunakan statistik median temporal (temporal median reducer). Reduksi median terbukti sangat tangguh (robust) "
        "terhadap sisa artefak radiometrik dan pantulan ekstrem sesaat, menghasilkan estimasi nilai reflektansi permukaan dasar "
        "yang stabil dan konsisten antarwaktu."
    )
    
    h4(doc, "3.3.2 Ekstraksi Fitur Spektral Murni dan Penegasan Ruang Fitur Tahap 1")
    body(
        doc,
        "Dari komposit median tahunan yang dihasilkan, penelitian ini mengekstraksi sepuluh fitur spektral optik murni, yang terdiri dari:"
    )
    bullet_item(
        doc, "Enam Kanal Reflektansi Permukaan Dasar",
        "Pita B2 (Biru, 490 nm), B3 (Hijau, 560 nm), B4 (Merah, 665 nm), B8 (Inframerah Dekat/NIR, 842 nm), B11 (SWIR1, 1.610 nm), "
        "dan B12 (SWIR2, 2.190 nm). Kanal beresolusi 20 meter (B11 dan B12) diinterpolasi secara bilinear menjadi resolusi 10 meter."
    )
    bullet_item(
        doc, "Empat Indeks Spektral Biofisik Turunan",
        "NDVI untuk mengukur biomassa fotosintetik vegetasi, NDMI untuk mendeteksi kadar air tajuk dan kelembaban, "
        "NDBI untuk menonjolkan respons area terbangun, dan BSI untuk memisahkan tanah terbuka tanpa penutup."
    )
    body(
        doc,
        "PENTING: Sebagai bagian dari pemenuhan integritas metodologis hasil audit teknis, penelitian ini menegaskan bahwa pada Tahap 1 "
        "(Klasifikasi Tutupan Lahan), ruang fitur masukan dibatasi secara ketat hanya pada 10 fitur spektral optik murni di atas. "
        "Variabel lingkungan seperti elevasi topografi SRTM dan curah hujan tahunan CHIRPS TIDAK dimasukkan ke dalam model klasifikasi Tahap 1. "
        "Pemisahan ini dilakukan secara sengaja untuk mencegah kebocoran spasial (spatial data leakage) dan confounding effect, "
        "karena elevasi dan curah hujan memiliki autokorelasi spasial makro yang sangat kuat yang dapat mendistorsi batas keputusan spektral model. "
        "Kedua variabel lingkungan tersebut secara tepat dan proporsional dialokasikan sebagai kovariat kontrol pada model regresi logistik Tahap 3."
    )
    
    h4(doc, "3.3.3 Dokumentasi Empiris Multikolinearitas Matematis NDBI dan NDMI")
    body(
        doc,
        "Analisis korelasi Pearson terhadap himpunan data latih mengungkapkan adanya korelasi sempurna berbalik tanda antara NDBI dan NDMI "
        "(r = -1,000). Secara aljabar, fenomena ini dapat dibuktikan secara langsung dari persamaan matematis pembentuk kedua indeks: "
        "NDBI = (B11 - B8) / (B11 + B8) = - (B8 - B11) / (B8 + B11) = - NDMI. Keduanya merupakan transformasi linear satu sama lain "
        "dengan faktor pengali -1. Keberadaan pasangan variabel kolinear sempurna ini tidak mengganggu performa prediktif algoritma pohon keputusan "
        "(seperti LightGBM atau Random Forest) karena algoritma pohon memilih satu fitur pemisah terbaik pada setiap percabangan node (split node). "
        "Namun, dokumentasi empiris ini sangat penting bagi keterbukaan metodologis dan pencegahan kekeliruan interpretasi koefisien pada model parametrik."
    )
    
    h3(doc, "3.4 Tahap 1: Klasifikasi Tutupan Lahan Berbasis Machine Learning")
    
    h4(doc, "3.4.1 Skema Taksonomi Tutupan Lahan dan Variabel Target")
    body(
        doc,
        "Target klasifikasi tutupan lahan diformulasikan ke dalam lima kelas hierarkis yang mengagregasi 11 kelas asal ESA WorldCover 2021 v200:"
    )
    numbered_item(
        doc, "1.", "Hutan (Forest)",
        "Meliputi formasi hutan primer tropis dataran rendah, hutan rawa gambut, hutan pegunungan, serta hutan tanaman industri kanopi rapat (Tree cover)."
    )
    numbered_item(
        doc, "2.", "Semak Belukar dan Pertanian (Shrubland/Agriculture)",
        "Mengagregasi semak belukar, vegetasi herba alami, padang rumput (grassland), lahan pertanian tanaman semusim, dan kebun campuran."
    )
    numbered_item(
        doc, "3.", "Area Terbangun (Built-up)",
        "Mencakup struktur fisik permukiman perkotaan dan perdesaan, kompleks bangunan gedung, kawasan industri, dan jalan raya beraspal."
    )
    numbered_item(
        doc, "4.", "Lahan Terbuka / Menyerupai Tambang (Bare/Mining-like)",
        "Mencakup tanah terbuka tanpa vegetasi (bare ground), singkapan batuan dasar, lubang galian tambang terbuka, dan area timbunan limbah batuan steril."
    )
    numbered_item(
        doc, "5.", "Badan Air (Water)",
        "Mencakup entitas perairan permanen seperti badan sungai utama (Kapuas, Mahakam, Barito), danau alami/waduk, serta perairan pesisir pantai."
    )
    
    h4(doc, "3.4.2 Protokol Pengambilan Sampel dan Partisi Spatial Block Cross-Validation")
    body(
        doc,
        "Untuk melatih dan menguji model secara objektif, sebanyak 30.000 titik sampel acak berstrata (stratified random sampling) diekstraksi "
        "dari peta referensi ESA WorldCover 2021 di daratan Kalimantan. Titik sampel dipastikan berjarak minimal 50 meter dari batas antarkelas "
        "untuk menjamin karakteristik piksel murni (pure pixels). Proporsi alokasi sampel per kelas dirancang mencerminkan sebaran alami: "
        "Hutan (15.000 sampel), Semak/Pertanian (7.500 sampel), Area Terbangun (3.000 sampel), Lahan Terbuka/Tambang (2.500 sampel), dan Air (2.000 sampel)."
    )
    body(
        doc,
        "Evaluasi kinerja model menerapkan protokol Spatial Block GroupKFold 5-fold. Seluruh bentang daratan Kalimantan dipartisi ke dalam "
        "blok-blok grid spasial reguler berukuran 1° x 1° (~111 km x 111 km). Setiap blok spasial diberi ID pengelompokan unik, dan seluruh titik sampel "
        "di dalam satu blok dialokasikan ke fold yang sama. Pada setiap iterasi, empat fold (80% blok wilayah) digunakan untuk melatih model, "
        "dan satu fold tersisa (20% blok wilayah yang terisolasi secara spasial) digunakan murni sebagai data uji (out-of-fold validation). "
        "Pendekatan ini sepenuhnya memutus rantai autokorelasi spasial dan kebocoran data antarlipatan."
    )
    
    h4(doc, "3.4.3 Formulasi Matematis Metrik Evaluasi Kinerja")
    body(
        doc,
        "Kinerja model klasifikasi dievaluasi secara menyeluruh menggunakan enam metrik kuantitatif terstandarisasi yang dihitung dari matriks konfusi multi-kelas:"
    )
    body(
        doc,
        "1. Overall Accuracy (OA): Mengukur proporsi total piksel yang diprediksi secara tepat terhadap keseluruhan piksel observasi:"
    )
    equation(doc, "OA = (sum(i=1 to K) n_ii) / N", "6")
    body(doc, "dimana: n_ii adalah jumlah piksel kelas i yang diprediksi benar, N adalah total jumlah sampel observasi (N = 30.000), dan K = 5 kelas.")
    
    body(
        doc,
        "2. Koefisien Kappa Cohen (Kappa): Mengukur tingkat kesepakatan klasifikasi yang telah dikoreksi terhadap faktor kesepakatan peluang acak (chance agreement):"
    )
    equation(doc, "Kappa = (P_o - P_e) / (1 - P_e)", "7")
    body(doc, "dimana: P_o adalah akurasi observasi proporsional (P_o = OA), dan P_e adalah probabilitas kesepakatan yang diharapkan secara acak: P_e = sum(i=1 to K) (n_i+ * n_+i) / N^2.")
    
    body(
        doc,
        "3. F1-Score Makro (F1-Macro): Rata-rata tak berbobot dari nilai F1-Score per kelas, memberikan bobot evaluasi yang setara bagi kelas mayoritas maupun minoritas:"
    )
    equation(doc, "F1-Macro = (1 / K) * sum(i=1 to K) (2 * Precision_i * Recall_i) / (Precision_i + Recall_i)", "8")
    
    body(
        doc,
        "4. Producer's Accuracy (PA / Recall): Mengukur probabilitas suatu piksel di lapangan berhasil dipetakan secara benar oleh classifier (akurasi pembuat peta):"
    )
    equation(doc, "PA_i = n_ii / n_+i", "9")
    body(doc, "dimana: n_+i adalah jumlah piksel referensi kebenaran lapangan pada kelas i.")
    
    body(
        doc,
        "5. User's Accuracy (UA / Precision): Mengukur probabilitas suatu piksel pada peta hasil klasifikasi benar-benar merepresentasikan kelas tersebut di lapangan (keandalan pengguna):"
    )
    equation(doc, "UA_i = n_ii / n_i+", "10")
    body(doc, "dimana: n_i+ adalah jumlah piksel yang diprediksi ke dalam kelas i oleh model.")
    
    body(
        doc,
        "6. Intersection over Union (IoU / Jaccard Index): Mengukur derajat tumpang-tindih spasial antara himpunan prediksi dan himpunan ground truth:"
    )
    equation(doc, "IoU_i = n_ii / (n_i+ + n_+i - n_ii)", "11")
    
    h4(doc, "3.4.4 Strategi Seleksi Model Operasional dan Inferensi Multi-Skala")
    body(
        doc,
        "Berdasarkan komparasi performa dari pengujian silang spasial, model terbaik dipilih dengan mempertimbangkan trade-off antara akurasi "
        "dan efisiensi komputasi. Mengingat inferensi makro daratan Kalimantan mencakup luas 73 juta hektar (ratusan juta piksel), waktu komputasi "
        "dan skalabilitas memori menjadi parameter krusial. Model yang terpilih dioperasikan untuk melakukan prediksi tutupan lahan pada dua skala:"
    )
    bullet_item(
        doc, "Prediksi Skala Makro Pulau Kalimantan",
        "Diaplikasikan pada kisi-kisi grid spasial 500 meter berbasis Majority Voting Sub-Grid Aggregation yang mencakup 1.499.024 sel grid valid "
        "(~1,5 juta titik observasi) di seluruh daratan Pulau Kalimantan guna menangkap dinamika perubahan tutupan lahan regional secara komprehensif, "
        "sekaligus mengeliminasi bias under-sampling akibat tutupan awan khatulistiwa."
    )
    bullet_item(
        doc, "Prediksi Skala Mikro Kawasan Inti IKN",
        "Dikonstruksi pada resolusi spasial asli 10 meter Sentinel-2 di sekitar Kawasan Inti Pusat Pemerintahan (KIPP) IKN untuk mengamati "
        "detail fisik pembukaan infrastruktur, alur jalan tol, dan tapak gedung kementerian secara presisi tinggi."
    )
    
    h4(doc, "3.4.5 Formulasi Atribusi Fitur Berbasis Nilai SHAP")
    body(
        doc,
        "Interpretabilitas model pohon keputusan diuji menggunakan algoritma TreeSHAP (Lundberg et al., 2020). Nilai kontribusi marginal "
        "phi_j untuk fitur x_j dirumuskan berdasarkan rata-rata tertimbang selisih prediksi saat fitur dimasukkan vs dikeluarkan:"
    )
    equation(doc, "phi_j = sum(S subseteq F \\ {j}) [ |S|! * (|F| - |S| - 1)! / |F|! ] * [ f(S union {j}) - f(S) ]", "12")
    body(doc, "dimana: F adalah himpunan seluruh fitur masukan (|F| = 10), S adalah subset fitur tanpa fitur j, dan f(S) adalah prediksi model pada subset S.")
    
    h3(doc, "3.5 Tahap 2: Deteksi Perubahan Tutupan Lahan Berbasis Majority Voting Sub-Grid Aggregation (2019–2024)")
    
    h4(doc, "3.5.1 Keterbatasan Metode Sentroid Tunggal dan Bias Under-Sampling Akibat Awan Tropis")
    body(
        doc,
        "Pada desain awal penelitian konvensional, sampling spasiotemporal di wilayah seluas Pulau Kalimantan umumnya mengandalkan kisi-kisi "
        "sistematik titik sentroid tunggal (single-pixel centroid sampling pada grid 10 km). Namun demikian, hasil audit metodologis membuktikan "
        "bahwa pendekatan titik tunggal mengalami kelemahan fatal ketika dihadapkan pada karakteristik iklim tropis ekuatorial Kalimantan. "
        "Persistensi awan konvektif tebal, kabut asap, dan bayangan awan yang dinamis menyebabkan hilangnya data piksel secara masif (cloud dropout). "
        "Jika satu-satunya piksel sentroid di tengah sel grid mengalami masking awan pada salah satu tahun pengamatan, maka seluruh sel grid "
        "tersebut secara otomatis tereliminasi dari neraca analisis luas tutupan lahan (under-sampling bias)."
    )
    body(
        doc,
        "Bukti empiris menunjukkan bahwa pendekatan sentroid tunggal hanya mampu menyisakan sekitar 118.000 hingga 175.384 titik observasi valid "
        "di seluruh Kalimantan. Yang lebih krusial, sampling titik tunggal terbukti meremehkan laju perubahan bentang alam: estimasi kehilangan hutan "
        "hanya tercatat sebesar -10,3%. Kegagalan ini mengindikasikan bahwa fenomena pembukaan lahan berskala kecil hingga menengah di sekitar sentroid "
        "luput dari pengamatan, sehingga menuntut adanya transformasi metode agregasi spasial yang lebih tangguh dan representatif."
    )
    
    h4(doc, "3.5.2 Solusi Metodologis: Majority Voting Sub-Grid Aggregation 500 Meter")
    body(
        doc,
        "Untuk mengatasi bias under-sampling tersebut, penelitian ini merancang dan mengimplementasikan metodologi Majority Voting Sub-Grid Aggregation. "
        "Seluruh daratan Pulau Kalimantan dipartisi ke dalam unit sel grid reguler berukuran 500 meter x 500 meter (luas tapak 25 hektar per sel). "
        "Di dalam setiap sel grid 500 meter, diterapkan desain sub-grid sampling sistematik berinterval teratur 100 meter (CELL_SIZE = 500 m; SUBGRID_SCALE = 100 m). "
        "Desain kisi 5x5 ini menghasilkan 25 titik sampel observasi spasial per sel grid. Pada setiap titik sampel tersebut, diekstrak nilai piksel "
        "citra Sentinel-2 pada resolusi spasial aslinya (10 meter untuk kanal B2, B3, B4, B8, serta kanal Red-Edge dan SWIR yang diselaraskan)."
    )
    body(
        doc,
        "Rasionalitas metodologis di balik pemilihan 25 titik sampel sistematis (interval 100 meter) dibandingkan dengan pencacahan sensus seluruh piksel 10 meter "
        "(yang berjumlah 50 x 50 = 2.500 piksel per sel) didasarkan pada dua pertimbangan fundamental:"
    )
    bullet_item(
        doc, "Batasan Kapasitas Komputasi Awan (Cloud Memory Quota Constraint)",
        "Mencacah 2.500 piksel pada ~1,5 juta sel grid di seluruh Kalimantan membutuhkan ekstraksi 3,75 miliar titik data spektral. Beban komputasi masif ini "
        "melampaui alokasi kuota memori pengguna Google Earth Engine (GEE User Memory Limit Exceeded), memicu kegagalan sistemik. Sebaliknya, sub-grid 25 titik "
        "menghasilkan 37,5 juta titik observasi—volume data yang sangat optimal, stabil, dan dapat diproses secara andal dalam arsitektur komputasi terdistribusi GEE."
    )
    bullet_item(
        doc, "Efisiensi Geostatistika dan Mitigasi Redundansi Spasial (Tobler's First Law)",
        "Berdasarkan Hukum Pertama Geografi Tobler, piksel-piksel berdampingan pada jarak 10 meter memiliki autokorelasi spasial lokal yang sangat tinggi sehingga "
        "informasi spektralnya cenderung redundan. Kisi sub-grid sistematik berjarak 100 meter memberikan dispersi spasial yang merata di seluruh tapak sel 25 hektar, "
        "efektif menangkap variasi heterogenitas tutupan mikro tanpa bias pemusatan lokal."
    )
    body(
        doc,
        "Pendekatan ini bertindak sebagai filter spasial cerdas (robust spatial consensus filter). Suatu sel grid 500 meter tetap dipertahankan "
        "sebagai data valid selama memiliki sedikitnya satu titik sampel sub-grid bebas awan (M >= 1 dari 25 titik sampel). Kelas tutupan lahan representatif "
        "bagi sel grid 500 meter tersebut kemudian ditentukan secara objektif berdasarkan nilai modus (majority vote) dari seluruh titik sampel valid:"
    )
    equation(doc, "C_sel = argmax_(c in {0, 1, ..., K-1}) sum_(k=1)^(M) I(c_k = c)", "13")
    body(
        doc,
        "dimana: C_sel adalah kelas tutupan lahan mayoritas hasil konsensus pada sel 500 meter; c_k adalah prediksi kelas tutupan lahan pada titik sampel "
        "sub-grid ke-k (berbasis citra Sentinel-2 10 meter); M adalah jumlah titik sampel valid bebas awan di dalam sel (1 <= M <= 25); dan I(.) adalah fungsi indikator biner "
        "yang bernilai 1 jika kondisi terpenuhi dan 0 jika sebaliknya."
    )
    body(
        doc,
        "Penerapan Majority Voting terbukti merevolusi cakupan observasi spasial: jumlah sel grid valid melonjak drastis dari sebelumnya hanya "
        "~118 ribu titik menjadi 1.499.024 sel grid valid (~1,5 juta titik observasi) yang melingkupi seluruh bentang daratan Kalimantan. "
        "Lebih penting lagi, matriks transisi Majority Voting berhasil mengungkap laju kehilangan hutan riil yang lebih tajam (-13,3% dari dinamika "
        "transisi, dengan 79.777 sel hutan terkonversi), membuktikan keberhasilan metode ini dalam memulihkan data yang terdistorsi oleh tutupan awan."
    )
    
    # Embed Gambar 3.2 Skema Majority Voting
    img_mv = r"reports/ilustrasi_majority_voting.png"
    add_image_figure(
        doc, img_mv,
        caption="Gambar 3.2 Skema Metodologis Sub-Grid Aggregation dan Majority Voting 500 Meter (25 Titik Sampel Sistematis Spasi 100 Meter Berbasis Citra Sentinel-2 10 Meter per Sel Grid)",
        source="Sumber: Desain Metodologis Majority Voting Peneliti (2024)",
        width_cm=14.5
    )
    
    h4(doc, "3.5.3 Formulasi Aljabar Matriks Transisi Spasiotemporal 5x5")
    body(
        doc,
        "Dinamika perubahan tutupan lahan antarwaktu pada 1.499.024 sel grid Majority Voting dikuantifikasi melalui matriks transisi bujur sangkar "
        "T berdimensi K x K (5 x 5 kelas):"
    )
    equation(doc, "T = [T_ij]  untuk  i, j in {1, 2, ..., K}", "14")
    body(
        doc,
        "dimana elemen baris i merepresentasikan kelas tutupan lahan rona awal t_1 (2019), dan elemen kolom j merepresentasikan kelas tutupan lahan "
        "fase konstruksi t_2 (2024). Elemen diagonal utama (T_ii) mengindikasikan persistensi spasial (persistence), yakni jumlah sel lahan yang tidak "
        "berubah kelasnya. Elemen non-diagonal (T_ij untuk i != j) merepresentasikan alih fungsi spesifik dari kelas i ke kelas j."
    )
    body(
        doc,
        "Metrik-metrik neraca transisi dirumuskan sebagai berikut:"
    )
    bullet_item(doc, "Total Kehilangan Tutupan (Gross Loss)", "Loss_i = sum_(j != i) T_ij, merefleksikan seluruh sel kelas i yang beralih menjadi kelas lain.")
    bullet_item(doc, "Total Penambahan Tutupan (Gross Gain)", "Gain_j = sum_(i != j) T_ij, merefleksikan seluruh sel baru yang beralih menjadi kelas j.")
    bullet_item(doc, "Perubahan Luasan Neto (Net Change)", "Net Change_i = Gain_i - Loss_i = sum_(k) T_ki - sum_(k) T_ik.")
    
    h4(doc, "3.5.4 Dekomposisi Variabel Biner Kejadian Transisi Lahan")
    body(
        doc,
        "Untuk menghubungkan kejadian alih fungsi lahan dengan model analisis faktor pendorong, matriks transisi Majority Voting didekomposisi "
        "ke dalam tiga variabel respon biner (Y in {0, 1}):"
    )
    numbered_item(
        doc, "1.", "Deforestasi / Kehilangan Hutan (Forest Loss)",
        "Mengindikasikan peristiwa hilangnya kanopi hutan tahun 2019 menjadi kelas non-hutan pada tahun 2024:"
    )
    equation(doc, "Y_deforest = 1  jika  Class_2019 = Forest  DAN  Class_2024 != Forest;  0  jika  Class_2019 = Forest  DAN  Class_2024 = Forest", "15")
    
    numbered_item(
        doc, "2.", "Urbanisasi / Ekspansi Area Terbangun (Urbanization)",
        "Mengindikasikan konversi lahan bervegetasi atau terbuka menjadi infrastruktur dan area terbangun fisik:"
    )
    equation(doc, "Y_urban = 1  jika  Class_2019 != Built-up  DAN  Class_2024 = Built-up;  0  jika  Class_2019 != Built-up  DAN  Class_2024 != Built-up", "16")
    
    numbered_item(
        doc, "3.", "Ekspansi Lahan Terbuka / Tambang (Mining Expansion)",
        "Mengindikasikan pembukaan tanah terbuka menyerupai galian tambang dari kelas berpenutup lainnya:"
    )
    equation(doc, "Y_mining = 1  jika  Class_2019 != Bare/Mining  DAN  Class_2024 = Bare/Mining;  0  jika  Class_2019 != Bare/Mining  DAN  Class_2024 != Bare/Mining", "17")
    
    h4(doc, "3.5.5 Konstruksi Bridge Dataset: Penjembatanan Spasial Tahap 2 ke Tahap 3")
    body(
        doc,
        "Sebuah pertanyaan metodologis mendasar muncul dalam desain penelitian ini: Jika Tahap 2 menghasilkan 1.499.024 sel Majority Voting yang "
        "sangat akurat untuk neraca luasan, mengapa model Regresi Logistik dan analisis faktor pendorong (Tahap 3) tidak langsung dijalankan "
        "pada seluruh 1,5 juta sel tersebut? Jawabannya berakar pada dua prinsip inferensi statistika spasial yang sangat fundamental:"
    )
    numbered_item(
        doc, "1.", "Pelanggaran Asumsi Independensi Spasial (Hukum Pertama Tobler)",
        "Hukum Pertama Geografi Tobler menyatakan bahwa segala sesuatu berhubungan dengan yang lain, tetapi objek yang berdekatan lebih berhubungan "
        "daripada objek yang jauh. Sel-sel grid berukuran 500 meter yang saling berdampingan secara spasial memiliki tingkat autokorelasi spasial "
        "yang sangat tinggi. Menjalankan model regresi parametrik klasik pada 1,5 juta observasi yang tidak independen secara fatal melanggar "
        "asumsi dasar residual yang identik dan independen (i.i.d.)."
    )
    numbered_item(
        doc, "2.", "Pencegahan Bias Replikasi Semu (Pseudo-Replication)",
        "Memasukkan N = 1.499.024 unit observasi yang bertetangga rapat ke dalam fungsi optimasi Maximum Likelihood regresi logistik akan "
        "mengakibatkan replikasi semu (pseudo-replication). Ukuran sampel yang luar biasa masif secara artifisial akan mengempiskan standar error "
        "koefisien mendekati nol (SE -> 0) dan melambungkan nilai uji z-score, sehingga menghasilkan nilai p-value yang secara artifisial selalu "
        "signifikan (p < 0,0001) untuk variabel apa pun (overpowered model). Hal ini merusak keandalan inferensi ilmiah."
    )
    body(
        doc,
        "Sebagai solusinya, penelitian ini merancang jembatan spasial terstandarisasi (Bridge Dataset) melalui skrip 'bridge_majority_voting.py':"
    )
    bullet_item(
        doc, "Sumber Kebenaran Label (Source of Truth)",
        "Sebanyak 1.499.024 sel Majority Voting (Tahap 2) bertindak sebagai penyedia label kelas tutupan lahan 2019 dan 2024 yang paling sahih dan bebas awan."
    )
    bullet_item(
        doc, "Titik Jangkar Spasial (Spatial Anchors)",
        "Kisi-kisi sistematik berjarak ~10 km yang telah memiliki atribut jarak ke sentroid IKN, kepadatan tambang 10 km, elevasi SRTM, dan curah hujan CHIRPS digunakan sebagai jangkar independen."
    )
    bullet_item(
        doc, "Pencocokan Tetangga Terdekat (cKDTree Spatial Intersection)",
        "Algoritma k-d tree spasial (scipy.spatial.cKDTree) digunakan untuk memetakan label Majority Voting ke setiap titik jangkar dengan batas ambang jarak presisi (threshold < 0,02 derajat atau sekitar 2 km)."
    )
    body(
        doc,
        "Prosedur penjembatanan ini berhasil menghasilkan Bridge Dataset sebanyak 122.478 titik sampel spasial independen "
        "('change_points_2019_2024.csv'). Dataset jembatan ini secara sempurna memadukan keunggulan label konsensus Majority Voting "
        "dengan keterpisahan spasial antartitik (~10 km) yang menjamin independensi observasi untuk pemodelan ekonometrika Tahap 3."
    )
    
    h4(doc, "3.5.6 Validasi Konsistensi Temporal Trajektori dan Evaluasi Keyakinan Prediksi")
    body(
        doc,
        "Untuk menguji keabsahan perubahan tutupan lahan dan memisahkan alih fungsi antropogenik permanen dari artefak klasifikasi sesaat, "
        "lintasan perubahan piksel dilacak melintasi seluruh deret waktu tahunan (2019 hingga 2024) pada subsampel validasi temporal. "
        "Lintasan trajektori dikelompokkan ke dalam empat kategori konsistensi:"
    )
    bullet_item(doc, "Stabil (Stable)", "Piksel mempertahankan kelas tutupan lahan yang identik di seluruh enam tahun pengamatan.")
    bullet_item(doc, "Transisi Tetap (Persistent Transition)", "Piksel mengalami perubahan satu kali dan secara konsisten bertahan pada kelas barunya hingga 2024.")
    bullet_item(doc, "Transisi Sementara (Temporary Transition)", "Piksel berubah sesaat kemudian kembali ke kelas rona awal (misalnya siklus tebang-tanam).")
    bullet_item(doc, "Fluktuatif (Oscillating)", "Piksel berganti kelas bolak-balik lebih dari dua kali, mencerminkan tingginya ambiguitas spektral piksel campuran.")
    body(
        doc,
        "Tingkat keyakinan prediksi (prediction confidence) dievaluasi menggunakan nilai probabilitas softmax maksimum model LightGBM pada setiap piksel, "
        "memvalidasi bahwa piksel berstatus stabil memiliki nilai keyakinan yang signifikan lebih tinggi dibandingkan piksel yang berfluktuasi."
    )
    
    h3(doc, "3.6 Tahap 3: Analisis Asosiasi Spasial Faktor Pendorong (Regresi Logistik Multivariat)")
    
    h4(doc, "3.6.1 Spesifikasi Matematis Model Logit")
    body(
        doc,
        "Probabilitas terjadinya peristiwa transisi perubahan tutupan lahan pada unit piksel spasial i dimodelkan menggunakan fungsi logit multivariat:"
    )
    equation(doc, "ln( P_i / (1 - P_i) ) = beta_0 + beta_1 * X_1i + beta_2 * X_2i + beta_3 * X_3i + beta_4 * X_4i", "18")
    body(
        doc,
        "Persamaan probabilitas sigmoid yang bersesuaian diformulasikan sebagai:"
    )
    equation(doc, "P_i = 1 / (1 + exp(-(beta_0 + beta_1 * X_1i + beta_2 * X_2i + beta_3 * X_3i + beta_4 * X_4i)))", "19")
    body(
        doc,
        "Keterangan variabel:"
    )
    bullet_item(doc, "P_i", "Probabilitas bersyarat terjadinya peristiwa perubahan tutupan lahan (Deforestasi, Urbanisasi, atau Ekspansi Tambang) pada titik spasial i.")
    bullet_item(doc, "beta_0", "Konstanta intersep model.")
    bullet_item(doc, "X_1i (Distance to IKN)", "Jarak Euklidian spasial dari titik piksel i ke titik koordinat sentroid KIPP IKN (dalam kilometer).")
    bullet_item(doc, "X_2i (Mining Density 10km)", "Kepadatan poligon tambang permukaan terverifikasi dalam radius moving window 10 km di sekitar titik i (dalam satuan persentase luas atau km² per 100 km²).")
    bullet_item(doc, "X_3i (Elevation)", "Kovariat kontrol elevasi ketinggian tempat di atas permukaan laut yang diekstrak dari SRTM DEM (dalam satuan meter, distandarisasi z-score).")
    bullet_item(doc, "X_4i (Annual Rainfall)", "Kovariat kontrol akumulasi presipitasi curah hujan tahunan dari CHIRPS (dalam satuan mm/tahun, distandarisasi z-score).")
    bullet_item(doc, "beta_1, beta_2, beta_3, beta_4", "Koefisien regresi parsial untuk masing-masing prediktor penjelas.")
    
    h4(doc, "3.6.2 Interpretasi Parameter Statistik dan Odds Ratio")
    body(
        doc,
        "Pengaruh masing-masing variabel prediktor spasial terhadap kecenderungan perubahan tutupan lahan diinterpretasikan melalui nilai "
        "Rasio Odds (Odds Ratio / OR):"
    )
    equation(doc, "OR_k = exp(beta_k)", "20")
    body(
        doc,
        "Jika nilai OR > 1 dan signifikan secara statistik (p < 0,05), variabel prediktor tersebut berasosiasi positif dengan peningkatan risiko "
        "kejadian perubahan tutupan lahan. Sebaliknya, jika nilai OR < 1, variabel tersebut berasosiasi dengan penurunan peluang terjadinya konversi "
        "(faktor penahan/mitigasi). Signifikansi statistik dari masing-masing koefisien diuji menggunakan uji Wald z-statistic: z = beta_k / SE(beta_k). "
        "Kelayakan model secara keseluruhan dievaluasi menggunakan nilai Log-Likelihood dan McFadden's Pseudo-R²."
    )
    
    h4(doc, "3.6.3 Penegasan Batasan Inferensi: Asosiasi Spasial vs Hubungan Kausal")
    body(
        doc,
        "PENTING: Sebagai bagian integral dari kehati-hatian akademik yang digariskan dalam audit metodologi, penelitian ini menegaskan bahwa "
        "seluruh estimasi parameter regresi logistik yang dihasilkan MURNI mengukur korelasi atau asosiasi spasial (spatial association), "
        "dan SECARA TEGAS TIDAK BOLEH ditafsirkan sebagai bukti hubungan sebab-akibat kausal langsung (causal inference). "
        "Tanpa adanya kontrol variabel instrumental atau desain eksperimen quasi-kausal (seperti Difference-in-Differences spasial terbobot), "
        "koefisien regresi logistik semata-mata menunjukkan bagaimana probabilitas relatif suatu perubahan lahan terdistribusi secara empiris "
        "relatif terhadap jarak IKN dan konsentrasi klaster tambang."
    )
