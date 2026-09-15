from config_and_helpers import (
    h3, h4, body, numbered_item, bullet_item, add_academic_table
)

def build_section_5(doc):
    h3(doc, "4.B PEMBAHASAN MENDALAM DAN SINTESIS ILMIAH")
    
    h4(doc, "4.11 Interpretasi Kinerja Model Machine Learning dan Efisiensi Komputasi")
    body(
        doc,
        "Komparasi kinerja enam algoritma supervised machine learning pada pengujian Spatial Block Cross-Validation (Tabel 4.4) "
        "mengungkap dinamika trade-off mendasar antara akurasi pemodelan dan skalabilitas komputasi operasional. Secara teoritis, arsitektur "
        "Support Vector Machine (SVM) dengan kernel Radial Basis Function (RBF) mencatatkan akurasi tertinggi (OA 84,00%, Kappa 0,7884). "
        "Keunggulan marjinal SVM bersumber dari mekanismenya dalam memproyeksikan vektor fitur spektral ke dalam ruang Hilbert berdimensi tak hingga, "
        "yang memungkinkan pembentukan hyperplane pemisah non-linear global yang meminimalkan batas risiko struktural (structural risk minimization). "
        "Namun demikian, keunggulan akurasi sebesar 0,68% terhadap LightGBM harus ditebus dengan biaya komputasi yang sangat mahal: SVM membutuhkan "
        "waktu pelatihan 760 detik (hampir 13 menit) dan kompleksitas memori O(N²), yang menjadikannya tidak layak secara komputasional untuk "
        "mengklasifikasikan ratusan juta piksel citra satelit seluruh daratan Kalimantan."
    )
    body(
        doc,
        "Sebaliknya, Light Gradient Boosting Machine (LightGBM) membuktikan diri sebagai arsitektur paling seimbang dan optimal untuk sains data "
        "geospasial berskala besar. Dengan Overall Accuracy 83,32%, F1-Macro 0,8347, dan Kappa 0,7795, performa LightGBM hampir identik dengan SVM, "
        "namun diselesaikan dalam waktu hanya 116,6 detik—yakni 6,5 kali lebih cepat daripada SVM dan 3,9 kali lebih cepat daripada Random Forest. "
        "Efisiensi ekstrem LightGBM dimungkinkan oleh dua inovasi algoritmik utamanya (Ke et al., 2017): (1) Gradient-based One-Side Sampling (GOSS), "
        "yang mempertahankan instans data dengan gradien besar dan mengambil sampel acak instans dengan gradien kecil; serta (2) Exclusive Feature "
        "Bundling (EFB), yang menggabungkan fitur-fitur jarang (sparse features) yang eksklusif ke dalam bundel tunggal. Selain itu, strategi "
        "pertumbuhan pohon berbasis leaf-wise dengan pembatasan kedalaman (max_depth) memungkinkan LightGBM mencapai konvergensi loss function "
        "yang jauh lebih cepat dibandingkan pendekatan level-wise konvensional pada XGBoost atau Random Forest."
    )
    body(
        doc,
        "Poin refleksi metodologis yang sangat krusial adalah peran penentu dari protokol Spatial Block Cross-Validation. Pada studi-studi penginderaan "
        "jauh terdahulu yang menerapkan validasi silang acak biasa (random k-fold CV), akurasi model sering kali dilaporkan melambung sangat tinggi "
        "(mencapai >92–95%). Namun, sebagaimana dibuktikan oleh Roberts et al. (2017) dan Valavi et al. (2019), skor akurasi tersebut merupakan ilusi "
        "yang menyesatkan akibat kebocoran data spasial (spatial data leakage): piksel data latih dan data uji yang berdampingan secara geografis "
        "memiliki autokorelasi spasial tinggi, sehingga model hanya sekadar 'menghafal' lokasi terdekat. Dengan mempartisi data latih dan uji "
        "ke dalam blok grid spasial independen 1° x 1°, skor Overall Accuracy 83,32% pada penelitian ini merepresentasikan kapasitas generalisasi "
        "murni yang sebenarnya ketika model dihadapkan pada bentang alam baru yang belum pernah dipelajari sebelumnya."
    )
    
    h4(doc, "4.12 Dekonstruksi Hasil Majority Voting: Resolusi Masalah MAUP, Bias Under-Sampling, dan Fenomena Net Forest Gain Semu")
    body(
        doc,
        "Peralihan metodologis dari pendekatan sampling sentroid titik tunggal ke Majority Voting Sub-Grid Aggregation 500 meter "
        "merupakan inovasi sentral dalam penelitian ini yang secara fundamental mengubah akurasi neraca tutupan lahan Pulau Kalimantan. "
        "Pada pendekatan sentroid tunggal terdahulu (1 piksel per sel grid 10 km), persistensi tutupan awan konvektif khatulistiwa menyebabkan "
        "kehilangan data yang sangat masif (hanya menyisakan sekitar 118 ribu hingga 175 ribu titik valid). Yang lebih merugikan, metode titik tunggal "
        "mengalami bias under-sampling yang meremehkan laju deforestasi pulau: kehilangan hutan hanya tercatat sebesar -10,3%. "
        "Sebaliknya, dengan mengevaluasi konsensus 25 titik sampel (sub-grid sistematis 5x5 dengan interval 100 meter berbasis citra Sentinel-2 10 meter) "
        "pada setiap sel 500 meter, Majority Voting berhasil menyelamatkan 1.499.024 sel grid valid (~1,5 juta titik observasi) dan membongkar laju kehilangan hutan riil yang jauh lebih tajam "
        "(-13,3% dari dinamika transisi, dengan 79.777 sel hutan terkonversi secara permanen)."
    )
    body(
        doc,
        "Kendati demikian, matriks transisi Majority Voting (Tabel 4.7) juga mendokumentasikan adanya pertambahan tutupan hutan netto "
        "(net forest gain) sebesar +29.971 sel (+2,00% pada total sel grid pulau). Secara ekologis dan historis, terjadinya ekspansi neto hutan "
        "di bentang alam tropis Kalimantan dalam rentang 2019–2024 sangat tidak sejalan dengan intensitas pembangunan infrastruktur IKN dan eskalasi "
        "harga komoditas batubara yang mendorong pembukaan tambang secara agresif. Oleh karena itu, temuan net gain makro ini harus didekonstruksi "
        "secara kritis melalui tiga mekanisme biofisik dan keterbatasan penginderaan jauh satelit:"
    )
    numbered_item(
        doc, "1.", "Ketidaksesuaian Skala dan Efek Piksel Campuran (Mixed-Pixel Effect)",
        "Model LightGBM dilatih menggunakan data referensi kebenaran lapangan ESA WorldCover 2021 pada resolusi spasial murni 10 meter. "
        "Namun, agregasi makro pulau beroperasi pada unit sel 500 meter x 500 meter (luas tapak 25 hektar per sel). Pada lanskap tropis Kalimantan, "
        "area seluas 25 hektar sangat jarang berupa kanopi hutan homogen, melainkan mosaik campuran (heterogeneous mosaic) yang memadukan sisa "
        "hutan sekunder terfragmentasi, belukar tebangan, semak liar, kebun kelapa sawit rakyat, dan jalan rintis. Respon reflektansi yang terekam "
        "merupakan percampuran spektral linear (linear spectral mixture). Pada sel-sel transisional, dominasi relatif tajuk hijau semak belukar tua "
        "sering kali melampaui ambang batas klasifikasi sehingga sel tersebut secara keliru diklasifikasikan sebagai Forest."
    )
    numbered_item(
        doc, "2.", "Pergeseran Domain Spektral Akibat Variabilitas Iklim dan Fenologi Musiman",
        "Pergeseran domain (domain shift) terjadi akibat anomali iklim ekstrem regional. Tahun 2021 (tahun dasar pelatihan label) dipengaruhi fenomena "
        "La Niña basah dengan curah hujan tinggi yang memaksimalkan kehijauan tajuk vegetasi. Sebaliknya, paruh kedua tahun 2023 dilanda El Niño kuat "
        "yang memicu kekeringan tajam dan defoliasi daun semak, yang kemudian disusul oleh pemulihan vegetasi luar biasa cepat (green flush) "
        "pada musim hujan awal tahun 2024. Fluktuasi musiman indeks vegetasi (NDVI) pada lanskap semak belukar ini menggeser ribuan sel melintasi "
        "ambang keputusan model, memicu reklasifikasi Shrubland menjadi Forest sebesar 104.412 sel (menyumbang 95,14% dari total forest gain semu)."
    )
    numbered_item(
        doc, "3.", "Ambiguitas Batas Spektral Kanopi Terbuka",
        "Formasi vegetasi semak belukar tua (old secondary shrub) yang sedang mengalami suksesi alami dan perkebunan monokultur kelapa sawit berkanopi rapat "
        "memiliki profil reflektansi NIR (B8) dan SWIR (B11, B12) yang berhimpitan erat dengan kanopi hutan sekunder terdegradasi. Pada resolusi 500 meter, "
        "sedikit peningkatan kadar air kanopi atau kelembaban tanah dapat membalikkan label klasifikasi. Bukti empiris keyakinan prediksi (Tabel 4.9) "
        "memperlihatkan bahwa sel-sel transisional ini memiliki probabilitas softmax terendah (0,6986), menegaskan bahwa gain yang terdeteksi bukan "
        "ekspansi hutan primer baru, melainkan artefak ketidakpastian spektral."
    )
    body(
        doc,
        "Kontras yang sangat tajam terlihat ketika membandingkan hasil makro dengan klasifikasi resolusi asli 10 meter di Kawasan Inti IKN "
        "(Gambar 4.6 vs Gambar 4.7). Pada skala mikro murni di mana efek piksel campuran tereliminasi, pembukaan hutan akibat koridor jalan tol "
        "dan tapak gedung pemerintahan terdeteksi secara tegas dan nyata tanpa adanya artefak pemulihan semu. Tabel 4.11 merangkum sintesis komparatif "
        "antar tingkatan resolusi tersebut."
    )
    
    # Tabel 4.11 Perbandingan Karakteristik Multi-Skala
    t411_headers = ["Dimensi Karakteristik", "Tahap Pelatihan Model", "Prediksi Skala Makro Pulau", "Prediksi Skala Mikro IKN"]
    t411_data = [
        ["Resolusi Spasial", "10 meter (Sentinel-2 asli)", "500 meter (Majority Voting 25 Titik @100m)", "10 meter (Sentinel-2 asli)"],
        ["Cakupan Wilayah", "Titik Sampel Terdistribusi Se-Kalimantan", "Seluruh Daratan Pulau Kalimantan (~54 juta ha)", "Kawasan Inti IKN / KIPP (~6.671 ha)"],
        ["Jumlah Unit Observasi", "30.000 titik sampel murni", "1.499.024 sel grid valid (~1,5 juta)", "~667.100 piksel citra asli"],
        ["Karakteristik Piksel", "Piksel Murni (Pure Pixels, buffer 50 m)", "Konsensus Spasial (25 Titik Sub-Grid @100m)", "Piksel Murni & Detil Mikro"],
        ["Tujuan Analisis", "Pembelajaran batas keputusan spektral optimal", "Kuantifikasi neraca regional bebas bias awan", "Delineasi fisik tapak proyek & jalan tol"],
        ["Fenomena yang Teramati", "Pemisahan kelas spektral tajam (OA 83,3%)", "Deforestasi riil 79.777 sel; gain semu 109.748", "Deforestasi nyata terpetakan tegas di lapangan"]
    ]
    t411_widths = [3.5, 3.8, 4.5, 4.0]
    add_academic_table(
        doc, t411_headers, t411_data,
        caption="Tabel 4.11 Perbandingan Komparatif Karakteristik Multi-Skala: Tahap Pelatihan (10 m), Skala Makro Majority Voting (500 m), dan Skala Mikro IKN (10 m)",
        source="Sumber: Sintesis Metodologis Multi-Skala oleh Peneliti (2024)",
        col_widths=t411_widths
    )
    
    h4(doc, "4.13 Interaksi Spasial Pembangunan IKN dan Penambangan: Perspektif Kerangka Telecoupling")
    body(
        doc,
        "Pemodelan regresi logistik multivariat pada Bridge Dataset (N = 122.478 titik sampel spasial independen) menghasilkan temuan empiris "
        "yang membuktikan secara kuat bekerjanya kerangka teoretis Spatial Telecoupling (Liu et al., 2013, 2015). Penggunaan Bridge Dataset "
        "yang diturunkan dari label Majority Voting melalui spatial nearest-neighbor cKDTree (~10 km) terbukti krusial: pendekatan ini menghindarkan "
        "penelitian dari bias replikasi semu (pseudo-replication) dan pelanggaran autokorelasi spasial Hukum Tobler, yang akan terjadi apabila model "
        "dipaksakan berjalan langsung pada 1,5 juta sel bertetangga."
    )
    body(
        doc,
        "Hasil estimasi koefisien jarak ke sentroid IKN (distance_to_ikn) pada model Deforestasi menghasilkan nilai positif dan sangat signifikan "
        "(beta = +0,1083; z = 7,79; p < 0,001) dengan Odds Ratio sebesar 1,1144. Secara substantif, temuan ini membuktikan bahwa setiap pertambahan "
        "satu satuan jarak menjauh dari episentrum IKN, peluang terjadinya peristiwa kehilangan hutan justru meningkat sebesar 11,4%."
    )
    body(
        doc,
        "Temuan ini sekilas tampak berlawanan dengan asumsi intuitif bahwa pembangunan IKN akan menyebabkan deforestasi terpusat di titik episentrumnya. "
        "Namun, kerangka telecoupling memberikan eksplanasi ilmiah yang sangat koheren: Kawasan Inti Pusat Pemerintahan (KIPP) IKN merupakan sending/receiving "
        "system yang mendapat perlindungan dan pengawasan hukum luar biasa ketat dari pemerintah pusat, Otorita IKN, kepolisian, dan satgas kehutanan. "
        "Penebangan liar, perambahan lahan skala besar, dan pembukaan tambang ilegal di dalam zona inti KIPP langsung ditindak tegas. "
        "Akibatnya, tekanan alih fungsi lahan mengalami fenomena pergeseran rembesan (spillover / leakage effect): aktivitas konversi hutan terdorong "
        "ke luar zona inti menuju koridor penyangga berjarak 10 hingga 50 km (seperti kawasan Samboja, Muara Jawa, dan Loa Janan di Kutai Kartanegara) "
        "yang minim pengawasan ketat namun mengalami lonjakan permintaan permukiman baru, material pasir/batu, dan kebun penyuplai logistik pangan."
    )
    body(
        doc,
        "Sebaliknya, pada model Ekspansi Tambang, variabel distance_to_ikn berkoefisien negatif dan sangat signifikan (beta = -0,2431; p < 0,001; OR = 0,7842). "
        "Artinya, peluang kemunculan lahan terbuka tambang baru justru berkurang sebesar 21,6% untuk setiap satuan jarak menjauhi IKN—dengan kata lain, "
        "aktivitas pertambangan terkonsentrasi lebih padat pada jarak yang lebih dekat ke koridor IKN dan Samarinda. Hal ini mencerminkan realitas tata ruang "
        "historis Provinsi Kalimantan Timur, di mana konsesi tambang batubara memang telah mengepung perimeter timur dan utara IKN jauh sebelum mega-proyek ini diumumkan."
    )
    body(
        doc,
        "Pengaruh Kepadatan Tambang (mining_density_10km) memperlihatkan efek multiplikatif yang konsisten dan sangat merusak melintasi seluruh model "
        "(OR = 1,093 pada Deforestasi; OR = 1,268 pada Urbanisasi; dan OR = 1,261 pada Ekspansi Tambang). Tingginya kepadatan lubang tambang eksisting "
        "mempercepat deforestasi melalui pembukaan jalan angkut (hauling road), pembangunan dermaga tongkang batubara (jetty) di sepanjang Sungai Mahakam, "
        "serta menarik pertumbuhan kantong-kantong permukiman pekerja tambang informal (urbanisasi). Kepadatan tambang terbukti bertindak sebagai episentrum "
        "aglomerasi yang terus merekrut lahan bervegetasi alami di sekitarnya."
    )
    body(
        doc,
        "Di sisi lain, kovariat biofisik topografi (elevasi) dan iklim (curah hujan) terbukti secara konsisten bertindak sebagai faktor penahan/mitigasi "
        "alami yang sangat tangguh (p < 0,001). Elevasi tinggi memangkas risiko deforestasi hingga lebih dari separuh (OR = 0,462), mencerminkan bahwa "
        "kawasan pegunungan Muller-Schwaner dan dataran tinggi Heart of Borneo secara fisik terlindungi dari akses alat berat ekskavator tambang dan truk logging. "
        "Demikian pula, tingginya presipitasi hujan tahunan (OR = 0,906) menekan risiko pembakaran hutan dan mempersulit mobilitas pembukaan lahan terbuka."
    )
    
    h4(doc, "4.14 Evaluasi Kritis Keterbatasan Metodologis Penelitian")
    body(
        doc,
        "Untuk memelihara integritas objektivitas ilmiah, penelitian ini secara transparan mendokumentasikan lima keterbatasan metodologis pokok:"
    )
    numbered_item(
        doc, "1.", "Ketidaksesuaian Resolusi Spasial (Resolution Mismatch)",
        "Terdapat diskoneksi skala antara data kebenaran lapangan referensi ESA WorldCover (10 meter) dengan kisi-kisi analisis makro Majority Voting "
        "(500 meter). Walaupun agregasi 500 meter diperlukan demi kelayakan komputasi pemrosesan deret waktu 73 juta hektar dan menyelamatkan observasi berawan, "
        "resolusi ini tetap membawa efek piksel campuran (mixed pixels) yang menyulitkan pemisahan murni antara semak belukar lebat dan kanopi hutan sekunder terfragmentasi."
    )
    numbered_item(
        doc, "2.", "Sifat Hubungan Asosiasi Spasial vs Inferensi Kausal Langsung",
        "Sebagaimana ditekankan dalam audit metodologi, model regresi logistik yang diestimasi murni mengukur korelasi spasial empiris. "
        "Penelitian ini tidak menggunakan desain eksperimen semu (quasi-experimental) atau variabel instrumental, sehingga koefisien positif "
        "distance_to_ikn tidak boleh ditafsirkan bahwa keberadaan IKN secara langsung 'menyebabkan' deforestasi di pedalaman, melainkan bahwa "
        "laju deforestasi secara spasial memang terdistribusi lebih padat di luar zona penyangga inti KIPP."
    )
    numbered_item(
        doc, "3.", "Ketidakseimbangan Kelas Ekstrem pada Peristiwa Langka (Rare Events Imbalance)",
        "Peristiwa pembukaan tambang baru (Mining Expansion) merupakan kejadian langka (rare event) yang teramati pada 740 kejadian dari 121.878 titik "
        "observasi non-tambang pada Bridge Dataset (proporsi ~0,61%). Walaupun model logistik berhasil mengestimasi parameter yang signifikan, "
        "ketidakseimbangan kelas ekstrem ini menghasilkan selang kepercayaan (confidence interval) yang relatif lebih lebar dibandingkan model deforestasi."
    )
    numbered_item(
        doc, "4.", "Ketergantungan pada Label Referensi Tunggal Tahun 2021",
        "Pelatihan model machine learning mengandalkan label ground truth ESA WorldCover tahun 2021 sebagai jangkar kalibrasi tunggal. "
        "Model kemudian diproyeksikan ke belakang ke tahun 2019 dan ke depan hingga 2024 dengan asumsi kestabilan invarian spektral. "
        "Variasi fenologis antar tahun (seperti kekeringan El Niño 2023) berpotensi mendistorsi prediksi pada tahun-tahun di luar 2021."
    )
    numbered_item(
        doc, "5.", "Multikolinearitas Matematis Sempurna NDBI dan NDMI",
        "Korelasi Pearson r = -1,000 antara NDBI dan NDMI membuktikan adanya redundansi informasi spektral penuh. Kendati algoritma pohon LightGBM "
        "kebal terhadap multikolinearitas dalam hal akurasi prediksi, keberadaan kedua fitur ini membagi nilai atribusi kepentingan fitur (feature importance split) "
        "di antara keduanya, yang harus dipahami secara hati-hati dalam interpretasi pemodelan."
    )
