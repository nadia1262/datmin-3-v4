import os
from config_and_helpers import (
    h2, h3, h4, body, numbered_item, bullet_item, equation,
    add_academic_table, add_image_figure
)

def build_section_2(doc):
    h2(doc, "BAB II TINJAUAN PUSTAKA DAN LANDASAN TEORI")
    
    h3(doc, "2.1 Landasan Teori")
    
    h4(doc, "2.1.1 Tutupan Lahan dan Konseptualisasi Perubahan Tutupan Lahan")
    body(
        doc,
        "Tutupan lahan (land cover) didefinisikan oleh Food and Agriculture Organization (FAO) melalui Land Cover Classification System (LCCS) "
        "sebagai kenampakan biofisik aktual yang menutupi permukaan terestrial bumi, mencakup vegetasi alami, badan air, tanah terbuka, "
        "batuan dasar, serta struktur infrastruktur terbangun buatan manusia (Di Gregorio & Jansen, 2000). Konsep tutupan lahan harus dibedakan "
        "secara tegas dari penggunaan lahan (land use), yang lebih mengacu pada fungsi sosio-ekonomi atau pengaturan tata kelola lahan oleh manusia "
        "(seperti kawasan konservasi, hutan produksi, pemukiman transmigrasi, atau konsesi pertambangan)."
    )
    body(
        doc,
        "Tutupan lahan bersifat dinamis dan berevolusi secara spasiotemporal akibat interaksi kompleks antara proses biofisik alami (seperti "
        "suksesi ekologis, variasi iklim musiman, dan erosi) serta intervensi antropogenik (seperti ekspansi pertanian, penebangan hutan, "
        "dan urbanisasi). Dalam perspektif lanskap ekologi, perubahan tutupan lahan tidak sekadar merepresentasikan perubahan luasan fisik, "
        "tetapi juga memicu konsekuensi mendalam terhadap fragmentasi habitat, penurunan kapasitas retensi air DAS, pelepasan cadangan karbon "
        "ke atmosfer, serta perubahan albedo dan fluks energi permukaan bumi (Lambin & Meyfroidt, 2011). Oleh karena itu, kuantifikasi transisi "
        "tutupan lahan antarkelas dari waktu ke waktu menjadi fondasi analitis esensial dalam tata kelola lingkungan terestrial."
    )
    
    h4(doc, "2.1.2 Deforestasi dan Faktor Pendorong Perubahan Tutupan Lahan")
    body(
        doc,
        "Deforestasi secara ilmiah dikonseptualisasikan sebagai konversi permanen atau jangka panjang dari area hutan berkanopi padat menjadi "
        "kelas tutupan lahan non-hutan, seperti lahan pertanian tanaman semusim, perkebunan kelapa sawit, area terbangun, atau lubang tambang terbuka "
        "(Hansen et al., 2013). Dalam kerangka teoretis yang dirumuskan oleh Lambin et al. (2001), faktor pendorong perubahan lahan (land-change drivers) "
        "diklasifikasikan secara hierarkis ke dalam dua dimensi utama: penyebab langsung (proximate causes) dan faktor pendorong mendasar (underlying drivers)."
    )
    body(
        doc,
        "Penyebab langsung mencakup aksi-aksi antropogenik terdekat pada tingkat lokal yang secara visual mengubah permukaan tanah, seperti "
        "penebangan pohon komersial, pembukaan jalan akses logistik, pengupasan tanah pucuk untuk operasi pertambangan, dan pembangunan gedung. "
        "Sebaliknya, faktor pendorong mendasar beroperasi pada skala makro regional atau global, mencakup dinamika demografi (migrasi penduduk), "
        "kebijakan makroekonomi (dorongan ekspor komoditas batubara), tata kelola institusional (pemberian izin konsesi), serta keputusan geopolitik "
        "strategis seperti pemindahan ibu kota negara (Meyfroidt et al., 2014)."
    )
    body(
        doc,
        "Dalam konteks Pulau Kalimantan kontemporer, pembangunan IKN dan ekspansi tambang batubara berinteraksi secara spasial. Pembangunan IKN "
        "menciptakan episentrum pembangunan baru yang menarik migrasi tenaga kerja dan memicu permintaan material bangunan. Di sisi lain, "
        "keberadaan konsesi tambang batubara yang masif di Provinsi Kalimantan Timur bertindak sebagai pendorong deforestasi langsung melalui "
        "penggalian lubang tambang dan pembentukan timbunan limbah batuan. Membedah kontribusi kedua pendorong spasial ini membutuhkan kerangka "
        "analisis asosiasi multivariat yang mampu mengontrol faktor biofisik alami lingkungan."
    )
    
    h4(doc, "2.1.3 Prinsip Penginderaan Jauh Optik untuk Pemantauan Biofisik")
    body(
        doc,
        "Penginderaan jauh optik (optical remote sensing) memanfaatkan perekaman radiasi gelombang elektromagnetik matahari yang dipantulkan kembali "
        "oleh objek-objek di permukaan bumi (Lillesand, Kiefer, & Chipman, 2015). Sensor satelit mengukur tingkat radiansi spektral yang kemudian "
        "dikonversi menjadi nilai reflektansi permukaan (surface reflectance). Setiap tipe tutupan lahan memiliki pola kurva pantulan spektral "
        "(spectral signature) yang unik melintasi panjang gelombang yang berbeda."
    )
    body(
        doc,
        "Daun vegetasi berhijau kanopi lebat menyerap radiasi cahaya tampak (khususnya kanal biru dan merah) secara kuat untuk proses fotosintesis "
        "melalui pigmen klorofil, namun memantulkan radiasi inframerah dekat (near-infrared / NIR) secara intensif akibat hamburan internal "
        "pada struktur sel mesofil daun (Rouse et al., 1974). Sebaliknya, tanah terbuka dan area terbangun buatan manusia memperlihatkan peningkatan "
        "reflektansi linier yang lebih stabil melintasi spektrum tampak hingga inframerah gelombang pendek (shortwave infrared / SWIR), "
        "sementara badan air menyerap radiasi inframerah hampir secara sempurna sehingga tampak sangat gelap pada kanal NIR dan SWIR. "
        "Perbedaan karakteristik respons spektral inilah yang memungkinkan diskriminasi kelas tutupan lahan secara digital."
    )
    
    h4(doc, "2.1.4 Karakteristik Misi Sentinel-2 Multi-Spectral Instrument (MSI)")
    body(
        doc,
        "Misi Sentinel-2 merupakan bagian dari konstelasi Copernicus yang dioperasikan oleh European Space Agency (ESA), terdiri dari dua satelit "
        "identik (Sentinel-2A diluncurkan 2015 dan Sentinel-2B diluncurkan 2017) yang berbagi bidang orbit sinkron matahari pada ketinggian 786 km "
        "(Phiri et al., 2020). Konstelasi ini dilengkapi instrumen Multi-Spectral Instrument (MSI) dengan sudut sapuan (swath width) 290 km "
        "dan periode kunjungan ulang (revisit time) mencapai 5 hari pada khatulistiwa, memberikan keunggulan kritis untuk memantau kawasan tropis basah "
        "Kalimantan yang sering tertutup awan konvektif."
    )
    body(
        doc,
        "Sensor MSI Sentinel-2 merekam data pada 13 kanal spektral dengan tiga tingkatan resolusi spasial: (1) pita tampak B2 (Biru, 490 nm), "
        "B3 (Hijau, 560 nm), B4 (Merah, 665 nm), dan B8 (NIR, 842 nm) beresolusi 10 meter; (2) kanal red-edge B5 (705 nm), B6 (740 nm), B7 (783 nm), "
        "B8a (865 nm), serta kanal SWIR B11 (1.610 nm) dan B12 (2.190 nm) beresolusi 20 meter; dan (3) kanal koreksi atmosferik B1, B9, B10 beresolusi 60 meter. "
        "Koleksi Level-2A Harmonized yang digunakan dalam penelitian ini telah melalui koreksi atmosfer Bottom-of-Atmosphere (BOA) tersertifikasi "
        "menggunakan algoritma Sen2Cor, sehingga nilai reflektansi dapat langsung dibandingkan antarwaktu secara andal."
    )
    
    h4(doc, "2.1.5 Formulasi dan Signifikansi Fisik Indeks Spektral")
    body(
        doc,
        "Untuk memaksimalkan daya pisah (separability) antar kelas tutupan lahan dan mereduksi pengaruh variasi sudut iluminasi matahari "
        "serta efek topografi, citra satelit ditransformasikan ke dalam indeks spektral aljabar (Jensen, 2015). Penelitian ini mengekstraksi "
        "empat indeks spektral utama:"
    )
    body(
        doc,
        "1. Normalized Difference Vegetation Index (NDVI): Merupakan rasio ternormalisasi antara kanal inframerah dekat (NIR) dan merah (Red) "
        "yang mengukur biomassa fotosintetik hijau, kerapatan tajuk, dan kesehatan kanopi (Rouse et al., 1974):"
    )
    equation(doc, "NDVI = (B8 - B4) / (B8 + B4)", "1")
    body(
        doc,
        "2. Normalized Difference Moisture Index (NDMI): Memanfaatkan perbandingan antara kanal NIR dan SWIR1 untuk mengestimasi kadar air "
        "dalam jaringan kanopi vegetasi dan kelembaban permukaan tanah (Gao, 1996):"
    )
    equation(doc, "NDMI = (B8 - B11) / (B8 + B11)", "2")
    body(
        doc,
        "3. Normalized Difference Built-up Index (NDBI): Dirancang untuk menonjolkan fitur buatan manusia, beton, atap bangunan, dan jalan aspal "
        "dengan memanfaatkan tingginya reflektansi area terbangun pada kanal SWIR1 dibandingkan NIR (Zha et al., 2003):"
    )
    equation(doc, "NDBI = (B11 - B8) / (B11 + B8)", "3")
    body(
        doc,
        "4. Bare Soil Index (BSI): Mengombinasikan kanal SWIR1, Red, NIR, dan Blue untuk memisahkan tanah terbuka tanpa vegetasi dan batuan "
        "dari lingkungan sekitarnya (Rikimaru et al., 2002):"
    )
    equation(doc, "BSI = ((B11 + B4) - (B8 + B2)) / ((B11 + B4) + (B8 + B2))", "4")
    body(
        doc,
        "Secara matematis, terdapat hubungan komplementer terbalik yang sangat kaku antara NDBI dan NDMI karena keduanya dibentuk dari kanal "
        "B8 dan B11 dengan orientasi pembilang yang berlawanan tanda: NDBI = -NDMI. Konsekuensi matematis ini akan dianalisis secara mendalam "
        "dalam bab pembahasan terkait multikolinearitas."
    )
    
    h4(doc, "2.1.6 Klasifikasi Tutupan Lahan Berbasis Supervised Machine Learning")
    body(
        doc,
        "Klasifikasi tutupan lahan berbasis supervised machine learning memetakan matriks fitur spektral X berdimensi-p ke dalam himpunan diskrit "
        "label kelas tutupan lahan y in {1, 2, ..., K} berdasarkan aturan keputusan yang dipelajari dari data latih berlabel ground truth (Hastie et al., 2009). "
        "Dibandingkan dengan classifier parametrik tradisional, algoritma modern machine learning memiliki keunggulan fleksibilitas non-parametrik, "
        "mampu memodelkan interaksi multi-fitur non-linear, dan tidak terikat asumsi normalitas multivariat."
    )
    body(
        doc,
        "Dalam penelitian ini, enam arsitektur machine learning diuji secara kompetitif:"
    )
    bullet_item(
        doc, "Random Forest (RF)",
        "Metode ensambel bagging yang membangun kumpulan pohon keputusan (decision trees) independen dengan teknik bootstrap aggregating "
        "dan seleksi fitur acak pada setiap split node untuk mereduksi varians prediksi (Breiman, 2001)."
    )
    bullet_item(
        doc, "Extreme Gradient Boosting (XGBoost)",
        "Algoritma gradient tree boosting yang membangun pohon keputusan secara sekuensial dengan mengoptimalkan fungsi loss melalui ekspansi Taylor "
        "orde kedua serta menerapkan regularisasi L1/L2 untuk mencegah overfitting (Chen & Guestrin, 2016)."
    )
    bullet_item(
        doc, "Light Gradient Boosting Machine (LightGBM)",
        "Kerangka kerja gradient boosting berbasis pohon yang sangat efisien, menerapkan teknik Gradient-based One-Side Sampling (GOSS) dan "
        "Exclusive Feature Bundling (EFB) dengan strategi pertumbuhan pohon leaf-wise, menghasilkan kecepatan pelatihan hingga orde kali lebih cepat "
        "tanpa mengorbankan akurasi (Ke et al., 2017)."
    )
    bullet_item(
        doc, "CatBoost",
        "Algoritma gradient boosting yang dirancang khusus untuk menangani fitur kategorikal secara optimal dan mengatasi bias target shift "
        "melalui teknik ordered boosting (Prokhorenkova et al., 2018)."
    )
    bullet_item(
        doc, "Support Vector Machine (SVM)",
        "Algoritma pembelajaran berbasis margin maksimal yang memproyeksikan fitur masukan ke ruang berdimensi lebih tinggi menggunakan "
        "fungsi Radial Basis Function (RBF) kernel untuk mencari hyperplane pemisah optimal (Cortes & Vapnik, 1995)."
    )
    bullet_item(
        doc, "Multinomial Logistic Regression",
        "Model parametrik berbasis fungsi softmax sebagai garis dasar (baseline) pembanding linier standar (Hosmer & Lemeshow, 2000)."
    )
    
    h4(doc, "2.1.7 Autokorelasi Spasial dan Protokol Spatial Block Cross-Validation")
    body(
        doc,
        "Data geospasial memiliki karakteristik inheren berupa ketergantungan spasial, sebagaimana dirumuskan dalam Hukum Pertama Geografi Tobler (1970): "
        "'everything is related to everything else, but near things are more related than distant things.' Nilai piksel yang berdekatan secara geografis "
        "cenderung memiliki respons spektral, karakteristik vegetasi, dan kondisi lingkungan yang hampir identik."
    )
    body(
        doc,
        "Konsekuensi langsung dari autokorelasi spasial ini adalah kerentanan terhadap kebocoran data spasial (spatial data leakage) apabila evaluasi "
        "kinerja model dilakukan menggunakan metode partisi acak konvensional (random k-fold cross-validation) (Roberts et al., 2017; Valavi et al., 2019). "
        "Pada partisi acak, piksel-piksel pada lipatan latih (training fold) dan lipatan uji (testing fold) sering kali berasal dari lokasi geografis yang "
        "bertetangga dekat, sehingga model machine learning dapat sekadar 'menghafal' korelasi lokal daripada mempelajari pola spektral yang dapat digeneralisasi. "
        "Hal ini menghasilkan ilusi performa yang sangat overoptimistik."
    )
    body(
        doc,
        "Untuk mengatasi bias fundamental tersebut, penelitian ini menerapkan protokol Spatial Block Cross-Validation (GroupKFold 5-fold). "
        "Wilayah geografis Kalimantan dipartisi ke dalam blok-blok grid spasial reguler berukuran 1° x 1°. Seluruh sampel observasi dalam satu blok spasial "
        "ditetapkan ke dalam fold yang sama, memastikan bahwa evaluasi performa model dilakukan terhadap blok wilayah yang sama sekali belum pernah "
        "dilihat oleh model selama fase pelatihan. Pendekatan ini menjamin keabsahan dan keandalan estimasi akurasi generalisasi model di lapangan."
    )
    
    h4(doc, "2.1.8 Deteksi Perubahan Tutupan Lahan Spatiotemporal")
    body(
        doc,
        "Deteksi perubahan (change detection) adalah proses identifikasi perbedaan kondisi suatu objek atau fenomena biofisik permukaan bumi "
        "melalui pengamatan citra pada waktu yang berbeda (Singh, 1989; Hussain et al., 2013). Metode yang diterapkan dalam penelitian ini adalah "
        "komparasi pasca-klasifikasi (Post-Classification Comparison / PCC). Pada pendekatan PCC, citra satelit dari masing-masing tahun diklasifikasikan "
        "secara independen terlebih dahulu, dan peta tutupan lahan yang dihasilkan kemudian ditumpangsusunkan (overlay) untuk membangun matriks transisi "
        "dari-ke (from-to transition matrix) (Zhu, 2017)."
    )
    body(
        doc,
        "Keunggulan utama teknik PCC adalah kemampuannya dalam memetakan secara eksplisit lintasan transisi kualitatif antar kelas tutupan lahan "
        "(misalnya: konversi spesifik dari Forest ke Built-up versus dari Shrubland ke Built-up). Namun demikian, kelemahan inheren dari metode PCC "
        "adalah adanya propagasi kesalahan (multiplicative error propagation), di mana akurasi peta perubahan setara dengan perkalian dari akurasi "
        "masing-masing peta klasifikasi tahunan. Oleh karena itu, pengujian konsistensi temporal multi-tahunan sangat diperlukan guna memvalidasi "
        "apakah perubahan yang terdeteksi bersifat permanen atau sekadar fluktuasi sesaat."
    )
    
    h4(doc, "2.1.9 Pemodelan Determinan Spasial Berbasis Regresi Logistik dan Kerangka Telecoupling")
    body(
        doc,
        "Untuk menganalisis determinan spasial di balik kejadian perubahan tutupan lahan, regresi logistik multivariat (multivariate logistic regression) "
        "merupakan instrumen statistik standar dalam sains perubahan lahan (land change science) (Meyfroidt et al., 2014). Model logistik menghubungkan "
        "peluang bersyarat terjadinya suatu peristiwa perubahan biner (misalnya deforestasi: Y = 1, persistensi hutan: Y = 0) dengan serangkaian "
        "variabel penjelas spasial melalui fungsi penghubung logit:"
    )
    equation(doc, "logit(P) = ln(P / (1 - P)) = β0 + β1*X1 + β2*X2 + ... + βk*Xk", "5")
    body(
        doc,
        "Parameter koefisien regresi beta_k ditransformasikan ke dalam bentuk Rasio Odds (Odds Ratio / OR = exp(beta_k)), yang merefleksikan perubahan "
        "faktor pengali pada peluang odds terjadinya konversi lahan untuk setiap kenaikan satu satuan variabel prediktor X_k, ceteris paribus (Hosmer & Lemeshow, 2000)."
    )
    body(
        doc,
        "Analisis asosiasi spasial ini diperkaya dengan kerangka teoretis Telecoupling yang diperkenalkan oleh Liu et al. (2013, 2015). Kerangka telecoupling "
        "menjelaskan bagaimana interaksi sosio-ekologis antara sistem manusia dan alam dapat mentransmisikan dampak lintas batas geografis yang jauh "
        "(distant socio-economic and ecological interactions). Dalam kerangka ini, kawasan IKN dapat dipandang sebagai sending system (pusat kebijakan dan arus modal), "
        "kawasan pedalaman konsesi tambang dan hutan produksi sebagai receiving system (area penyedia energi dan komoditas), dan zona koridor jalan logistik "
        "serta wilayah penyangga (buffer) sebagai spillover systems (area penerima dampak rembesan konversi lahan)."
    )
    
    h4(doc, "2.1.10 Pergeseran Domain dan Efek Piksel Campuran (Mixed Pixels)")
    body(
        doc,
        "Tantangan metodologis krusial dalam pemodelan penginderaan jauh multi-skala bersumber dari fenomena ketidaksesuaian resolusi (resolution mismatch) "
        "dan pergeseran domain (domain shift) (Habibie et al., 2025). Pada resolusi 10 meter Sentinel-2 asli, sebagian besar unit piksel dapat diasumsikan "
        "sebagai piksel murni (pure pixels) yang didominasi oleh satu kelas penutup homogen. Namun, ketika model yang dilatih pada skala 10 meter murni "
        "diaplikasikan untuk memprediksi data makro pulau yang diagregasi ke grid resolusi 500 meter, timbul fenomena piksel campuran (mixed pixels) "
        "(Cracknell, 1998; Foody, 2002)."
    )
    body(
        doc,
        "Satu piksel grid 500 x 500 meter mencakup area daratan seluas 25 hektar, yang di bentang alam tropis Kalimantan umumnya merupakan mosaik rumit "
        "yang memadukan fragmen kanopi hutan, semak sekunder, ladang berpindah, dan alur jalan tanah. Respons spektral yang terekam adalah rata-rata linear "
        "dari berbagai konstituen tersebut. Jika classifier pohon keputusan memiliki batas pemisah (decision boundary) yang tajam, sedikit pergeseran "
        "respons kehijauan (misalnya akibat musim basah ekstrem vs kemarau El Niño) dapat menggeser klasifikasi ribuan piksel campuran dari Shrubland "
        "ke Forest atau sebaliknya, memicu anomali net forest gain semu. Pemahaman biofisik ini sangat vital untuk mencegah interpretasi yang keliru."
    )
    
    h4(doc, "2.1.11 Explainable Machine Learning dengan Nilai SHAP")
    body(
        doc,
        "Meskipun model machine learning ensambel (seperti LightGBM) memberikan performa akurasi superior, model ini sering dikritik karena sifatnya "
        "yang tertutup menyerupai kotak hitam (black-box model). Untuk membedah kontribusi masing-masing fitur masukan terhadap keputusan prediksi, "
        "penelitian ini menerapkan pendekatan Explainable Artificial Intelligence (XAI) berbasis SHAP (Shapley Additive Explanations) (Lundberg & Lee, 2017)."
    )
    body(
        doc,
        "Berdasar pada teori permainan kooperatif (cooperative game theory) yang dirumuskan oleh Lloyd Shapley (1953), nilai SHAP mengkuantifikasi "
        "kontribusi marginal rata-rata dari suatu fitur di seluruh kemungkinan subset kombinasi fitur lainnya. Nilai SHAP menjamin tiga sifat matematis "
        "fundamental: keakuratan lokal (local accuracy), ketiadaan fitur (missingness), dan konsistensi (consistency). Dengan SHAP, peneliti tidak hanya "
        "mengetahui fitur mana yang paling penting secara global (global importance), tetapi juga arah dan besaran pengaruh nilai fitur spesifik "
        "terhadap probabilitas tiap kelas lahan secara individual."
    )
    
    h3(doc, "2.2 Penelitian Terdahulu")
    body(
        doc,
        "Kajian dinamika tutupan lahan, deforestasi, dan pemodelan geospasial telah berkembang pesat dalam satu dekade terakhir. "
        "Untuk memposisikan kontribusi orisinalitas (novelty gap) penelitian ini, disajikan sintesis komparatif dari tujuh literatur acuan utama "
        "pada Tabel 2.1."
    )
    
    # Tabel 2.1 Penelitian Terdahulu
    t21_headers = ["Peneliti & Tahun", "Wilayah & Skala", "Data & Sumber Citra", "Metodologi & Model", "Temuan Kunci", "Keterkaitan / Gap dengan Penelitian Ini"]
    t21_data = [
        [
            "Habibie et al. (2025)",
            "Kalimantan (Makro Pulau)",
            "Sentinel-2 MSI 10m, GEE Komposit Tahunan",
            "Random Forest, GEE Cloud, Confusion Matrix",
            "Mendokumentasikan fluktuasi tutupan lahan makro dan tantangan piksel campuran pada skala pulau.",
            "Rujukan utama alur klasifikasi GEE, namun belum mengintegrasikan Spatial Block CV dan regresi logistik pendorong."
        ],
        [
            "Hazanul et al. (2022)",
            "Kawasan IKN, Kalimantan Timur",
            "Landsat-8 OLI, Sentinel-2 (2014–2021)",
            "Supervised SVM & Random Forest, Cellular Automata",
            "Mendeteksi tren ekspansi area terbangun dan degradasi hutan sekunder di sekitar KIPP IKN.",
            "Memberikan landasan spasial zonasi IKN, namun cakupan temporal belum mencakup puncak konstruksi fisik 2024."
        ],
        [
            "Lambin et al. (2001); Meyfroidt et al. (2014)",
            "Global Tropis (Kajian Teoretis)",
            "Meta-analisis global tutupan lahan",
            "Kerangka analitis Proximate vs Underlying Drivers, Land Use Transition",
            "Menegaskan bahwa deforestasi tropis didorong interaksi infrastruktur, pasar komoditas, dan kebijakan institusional.",
            "Menjadi fondasi teoretis dalam pemilihan prediktor pendorong (jarak IKN, tambang, elevasi, curah hujan)."
        ],
        [
            "Liu et al. (2013, 2015)",
            "Global Terestrial (Kerangka Konseptual)",
            "Studi integrasi sosio-ekologis global",
            "Telecoupling Framework (Sending, Receiving, Spillover)",
            "Menjelaskan bagaimana interaksi manusia-alam mentransmisikan dampak melintasi batas geografis yang jauh.",
            "Menjadi kerangka analisis dalam menjelaskan mengapa dampak deforestasi IKN merembes ke zona penyangga luar."
        ],
        [
            "Phiri et al. (2020)",
            "Kawasan Tropis Dunia",
            "Sentinel-2 MSI Level-2A",
            "Tinjauan komparatif kanal spektral & algoritma machine learning",
            "Menunjukkan superioritas kanal red-edge dan SWIR Sentinel-2 dalam memetakan vegetasi dan area terbuka.",
            "Menjadi acuan dalam pemilihan 10 fitur spektral murni (B2, B3, B4, B8, B11, B12, NDVI, NDMI, NDBI, BSI)."
        ],
        [
            "Roberts et al. (2017); Valavi et al. (2019)",
            "Kajian Metodologi Geospasial",
            "Data observasi bumi multi-sensor",
            "Spatial Block Cross-Validation vs Random CV",
            "Membuktikan bahwa Random CV melebih-lebihkan akurasi model hingga 20–30% akibat kebocoran autokorelasi spasial.",
            "Menjadi justifikasi metodologis penerapan Spatial Block GroupKFold 5-fold pada evaluasi enam algoritma."
        ],
        [
            "Maus et al. (2022)",
            "Global / Indonesia",
            "Citra resolusi tinggi & poligon tambang terbuka",
            "Delineasi poligon tambang permukaan global (v2)",
            "Menyediakan dataset poligon tambang permukaan terverifikasi mencakup area konsesi batubara Kalimantan.",
            "Sumber data eksternal utama untuk merekonstruksi variabel pendorong kepadatan tambang 10 km."
        ]
    ]
    t21_widths = [2.5, 2.0, 2.2, 2.5, 3.5, 3.8]
    add_academic_table(
        doc, t21_headers, t21_data,
        caption="Tabel 2.1 Sintesis Komparatif Penelitian Terdahulu dan Posisi Orisinalitas Penelitian",
        source="Sumber: Hasil Sintesis Peneliti dari Literatur Rujukan (2024)",
        col_widths=t21_widths
    )
    
    h3(doc, "2.3 Kerangka Pikir Penelitian")
    body(
        doc,
        "Kerangka pikir penelitian ini dibangun berdasarkan alur input-proses-output yang mengintegrasikan sains penginderaan jauh "
        "multispektral, geospasial data mining, dan pemodelan statistik spasial multivariat. Pada dimensi input, komposit tahunan Sentinel-2 "
        "diolah bersama label referensi ESA WorldCover 2021, data konsesi pertambangan MAUS, titik sentroid IKN, topografi SRTM, dan presipitasi CHIRPS. "
        "Pada dimensi proses, tiga tahapan sekuensial dieksekusi: (1) Pelatihan dan validasi silang spasial enam algoritma machine learning dengan "
        "penjelasan interpretabilitas SHAP; (2) Deteksi perubahan pasca-klasifikasi berbasis Majority Voting Sub-Grid Aggregation 500 meter "
        "(1.499.024 sel grid bebas bias awan); dan (3) Pemodelan regresi logistik spasial multivariat pada Bridge Dataset (122.478 titik sampel independen) "
        "untuk menguji asosiasi spasial jarak IKN dan konsentrasi tambang dalam kerangka spatial telecoupling bebas pseudo-replication. "
        "Pada dimensi output, dihasilkan pemahaman kuantitatif dinamika tutupan lahan, dekonstruksi fenomena mixed-pixels, dan platform dashboard interaktif."
    )
    
    # Embed Gambar 2.1 Kerangka Pikir
    img_kp = r"reports/_extracted_draft_images/image5.jpg"
    add_image_figure(
        doc, img_kp,
        caption="Gambar 2.1 Diagram Kerangka Pikir Konseptual Penelitian Spatiotemporal Kalimantan (2019–2024)",
        source="Sumber: Desain Konseptual Peneliti (2024)",
        width_cm=14.0
    )
