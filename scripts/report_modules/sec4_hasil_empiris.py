import os
from config_and_helpers import (
    h2, h3, h4, body, numbered_item, bullet_item,
    add_academic_table, add_image_figure
)
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_section_4(doc):
    h2(doc, "BAB IV HASIL DAN PEMBAHASAN")
    
    h3(doc, "4.A HASIL PENGUJIAN DAN ANALISIS EMPIRIS")
    
    h4(doc, "4.1 Eksplorasi Data: Karakteristik Sampel, Sebaran Tutupan Lahan, dan Korelasi Fitur Spektral")
    body(
        doc,
        "Evaluasi sebaran spasial kelas tutupan lahan makro daratan Pulau Kalimantan dianalisis menggunakan agregasi spasial Majority Voting 500 meter "
        "(sub-grid sistematis 5x5 berisi 25 titik sampel berjarak teratur 100 meter berbasis citra Sentinel-2 10 meter) yang mencakup "
        "1.499.024 sel grid valid bebas awan. Tabel 4.1 menyajikan perbandingan komparatif komposisi dan proporsi kelas tutupan lahan antara "
        "tahun dasar rona awal (2019) dan tahun akhir pengamatan aktual (2024)."
    )
    
    # Tabel 4.1 Komparasi Proporsi Kelas Lahan Majority Voting
    t41_headers = ["ID", "Kategori Tutupan Lahan", "Jumlah Sel 2019", "Proporsi 2019 (%)", "Jumlah Sel 2024", "Proporsi 2024 (%)", "Perubahan Neto (Sel)", "Arah Perubahan"]
    t41_data = [
        ["0", "Hutan (Forest)", "1.185.974", "79,12%", "1.215.945", "81,12%", "+29.971", "Net Gain Semu (+2,00%)"],
        ["1", "Semak / Pertanian (Shrub/Agri)", "264.273", "17,63%", "228.783", "15,26%", "-35.490", "Konversi / Pengurangan (-2,37%)"],
        ["2", "Badan Air (Water)", "22.159", "1,48%", "23.454", "1,56%", "+1.295", "Fluktuasi Hidrologis (+0,09%)"],
        ["3", "Area Terbangun (Built-up)", "19.490", "1,30%", "20.623", "1,38%", "+1.133", "Ekspansi Terkonsentrasi (+0,08%)"],
        ["4", "Lahan Terbuka / Tambang (Bare)", "7.128", "0,48%", "10.219", "0,68%", "+3.091", "Ekspansi Masif (+43,36%)"],
        ["-", "Total Sel Grid Majority Voting", "1.499.024", "100,00%", "1.499.024", "100,00%", "0", "Cakupan Bebas Bias Awan"]
    ]
    t41_widths = [1.0, 4.0, 2.3, 2.3, 2.3, 2.3, 2.5, 2.8]
    add_academic_table(
        doc, t41_headers, t41_data,
        caption="Tabel 4.1 Komparasi Komposisi dan Proporsi Tutupan Lahan Pulau Kalimantan Berbasis Agregasi Spasial Majority Voting 500 Meter (2019 vs 2024)",
        source="Sumber: Hasil Olahan Majority Voting Model LightGBM pada Citra Sentinel-2 (1.499.024 Sel Grid) (2024)",
        col_widths=t41_widths
    )
    
    body(
        doc,
        "Untuk memahami struktur multivariat fitur masukan, pengujian korelasi Pearson diaplikasikan pada 30.000 sampel data latih "
        "lintas sepuluh fitur spektral optik (Tabel 4.2). Hasil kalkulasi menunjukkan bahwa kanal tampak (B2, B3, B4) memperlihatkan korelasi "
        "positif yang sangat kuat (r > 0,930), mencerminkan redundansi spektral alami cahaya tampak. Kanal inframerah gelombang pendek "
        "(B11 dan B12) juga saling berkolerasi tinggi (r = 0,928). Di sisi lain, indeks vegetasi NDVI memperlihatkan korelasi positif kuat "
        "dengan kanal inframerah dekat B8 (r = 0,709) dan korelasi negatif tajam dengan kanal merah B4 (r = -0,449) dan BSI (r = -0,545), "
        "menegaskan sensitivitas NDVI terhadap kanopi hijau."
    )
    body(
        doc,
        "Temuan metodologis terpenting dari matriks korelasi ini adalah konfirmasi empiris korelasi sempurna berbalik tanda antara NDBI dan NDMI "
        "(r = -1,000). Nilai korelasi -1,000 ini secara eksak memvalidasi derivasi aljabar bahwa kedua indeks tersebut merupakan cerminan polar "
        "dari kombinasi kanal B8 (NIR) dan B11 (SWIR1)."
    )
    
    # Tabel 4.2 Matriks Korelasi Pearson
    t42_headers = ["Fitur", "B2", "B3", "B4", "B8", "B11", "B12", "NDVI", "NDBI", "NDMI", "BSI"]
    t42_data = [
        ["B2", "1.000", "0.974", "0.932", "0.189", "0.602", "0.746", "-0.423", "0.410", "-0.410", "0.449"],
        ["B3", "0.974", "1.000", "0.960", "0.271", "0.652", "0.760", "-0.384", "0.377", "-0.377", "0.464"],
        ["B4", "0.932", "0.960", "1.000", "0.173", "0.671", "0.803", "-0.449", "0.469", "-0.469", "0.612"],
        ["B8", "0.189", "0.271", "0.173", "1.000", "0.621", "0.365", "0.709", "-0.186", "0.186", "-0.289"],
        ["B11", "0.602", "0.652", "0.671", "0.621", "1.000", "0.928", "0.168", "0.555", "-0.555", "0.484"],
        ["B12", "0.746", "0.760", "0.803", "0.365", "0.928", "1.000", "-0.126", "0.674", "-0.674", "0.639"],
        ["NDVI", "-0.423", "-0.384", "-0.449", "0.709", "0.168", "-0.126", "1.000", "-0.350", "0.350", "-0.545"],
        ["NDBI", "0.410", "0.377", "0.469", "-0.186", "0.555", "0.674", "-0.350", "1.000", "-1.000", "0.795"],
        ["NDMI", "-0.410", "-0.377", "-0.469", "0.186", "-0.555", "-0.674", "0.350", "-1.000", "1.000", "-0.795"],
        ["BSI", "0.449", "0.464", "0.612", "-0.289", "0.484", "0.639", "-0.545", "0.795", "-0.795", "1.000"]
    ]
    t42_widths = [1.6, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.5, 1.5, 1.5, 1.5]
    add_academic_table(
        doc, t42_headers, t42_data,
        caption="Tabel 4.2 Matriks Korelasi Pearson Antarvariabel Prediktor Spektral pada Himpunan Data Latih (N = 30.000)",
        source="Sumber: Hasil Kalkulasi Peneliti pada Data Sampel Latih 2021 (2024)",
        col_widths=t42_widths
    )
    
    h4(doc, "4.2 Analisis Distribusi Nilai Spektral dan Sebaran Outlier Biofisik")
    body(
        doc,
        "Pemeriksaan sebaran statistik deskriptif dilakukan terhadap 30.000 sampel latih tahun 2021 guna mendeteksi keberadaan anomali "
        "atau pencilan (outlier) biofisik berdasarkan metode Interquartile Range (IQR = Q3 - Q1). Batas bawah didefinisikan sebagai Q1 - 1,5*IQR "
        "dan batas atas sebagai Q3 + 1,5*IQR. Rincian hasil perhitungan dipaparkan pada Tabel 4.3."
    )
    
    # Tabel 4.3 Sebaran Outlier
    t43_headers = ["Fitur", "Rata-rata", "Median", "Standar Deviasi", "Kuartil Bawah (Q1)", "Kuartil Atas (Q3)", "Jumlah Outlier", "Persentase Outlier (%)"]
    t43_data = [
        ["B2", "0,0668", "0,0438", "0,0635", "0,0297", "0,0810", "2.117", "7,06%"],
        ["B3", "0,0888", "0,0690", "0,0644", "0,0507", "0,1040", "2.128", "7,09%"],
        ["B4", "0,0793", "0,0490", "0,0765", "0,0286", "0,1058", "1.666", "5,55%"],
        ["B8", "0,2501", "0,2672", "0,1182", "0,1882", "0,3316", "95", "0,32%"],
        ["B11", "0,1885", "0,1876", "0,1038", "0,1325", "0,2462", "712", "2,37%"],
        ["B12", "0,1186", "0,0909", "0,0925", "0,0569", "0,1662", "976", "3,25%"],
        ["NDVI", "0,4567", "0,5842", "0,4110", "0,1549", "0,8220", "10", "0,03%"],
        ["NDBI", "-0,1583", "-0,1868", "0,2196", "-0,3284", "0,0090", "100", "0,33%"],
        ["NDMI", "0,1583", "0,1868", "0,2196", "-0,0090", "0,3284", "100", "0,33%"],
        ["BSI", "-0,1138", "-0,1244", "0,1913", "-0,2831", "0,0444", "2", "0,01%"]
    ]
    t43_widths = [1.8, 2.0, 2.0, 2.3, 2.5, 2.5, 2.2, 2.5]
    add_academic_table(
        doc, t43_headers, t43_data,
        caption="Tabel 4.3 Distribusi Statistik Deskriptif dan Sebaran Outlier Fitur Masukan Spektral (N = 30.000)",
        source="Sumber: Hasil Kalkulasi Statistik Peneliti (2024)",
        col_widths=t43_widths
    )
    
    body(
        doc,
        "Berdasarkan hasil kalkulasi, kanal tampak B2 dan B3 memegang rasio anomali tertinggi, masing-masing menyentuh 7,06% dan 7,09% "
        "dari total observasi. Kesenjangan antara nilai rata-rata (mean) dan median pada B2 (0,0668 vs 0,0438) dan B4 (0,0793 vs 0,0490) "
        "mengindikasikan skewness positif (kemencengan ke kanan). Nilai-nilai ekstrem tinggi pada kanal optik ini tidak dikategorikan sebagai "
        "kesalahan sensor, melainkan mencerminkan respons pantulan spektral yang sangat kuat dari atap seng/aluminium bangunan perkotaan "
        "serta singkapan batuan pasir/kuarsa putih pada dasar lubang tambang batubara aktif. Keberadaan nilai ekstrem yang sahih secara biofisik ini "
        "semakin memperkuat keputusan penggunaan algoritma berbasis pohon keputusan (tree-based models) yang kebal terhadap pengaruh skewness data."
    )
    
    h4(doc, "4.3 Evaluasi Komparatif Kinerja Enam Model Machine Learning")
    body(
        doc,
        "Pengujian komparatif dijalankan terhadap enam arsitektur supervised machine learning menerapkan protokol Spatial Block GroupKFold 5-fold "
        "pada 30.000 titik data latih. Rangkuman metrik evaluasi kinerja dan efisiensi waktu komputasi pelatihan disajikan pada Tabel 4.4."
    )
    
    # Tabel 4.4 Komparasi Kinerja Model
    t44_headers = ["Peringkat", "Arsitektur Algoritma", "Overall Accuracy (%)", "F1-Macro", "Cohen's Kappa", "Waktu Pelatihan (s)", "Karakteristik Operasional"]
    t44_data = [
        ["1", "Support Vector Machine (SVM RBF)", "84,00%", "0,8423", "0,7884", "760,0 s", "Akurasi tertinggi, namun waktu komputasi sangat lambat."],
        ["2", "Light Gradient Boosting (LightGBM)", "83,32%", "0,8347", "0,7795", "116,6 s", "Optimal: Akurasi hampir setara SVM, 6,5x lebih cepat."],
        ["3", "Extreme Gradient Boosting (XGBoost)", "83,20%", "0,8337", "0,7777", "189,0 s", "Akurasi sangat solid, waktu pelatihan moderat."],
        ["4", "Multi-Layer Perceptron (MLP Neural Net)", "82,90%", "0,8328", "0,7740", "340,0 s", "Performa baik, sensitif terhadap skala fitur."],
        ["5", "Random Forest (RF Ensambel)", "82,53%", "0,8267", "0,7690", "450,0 s", "Sangat stabil, namun ukuran model disk besar (>290 MB)."],
        ["6", "Multinomial Logistic Regression", "79,36%", "0,7931", "0,7263", "14,6 s", "Sangat cepat, namun gagal memodelkan relasi non-linear."]
    ]
    t44_widths = [1.5, 3.8, 2.5, 2.0, 2.0, 2.3, 4.5]
    add_academic_table(
        doc, t44_headers, t44_data,
        caption="Tabel 4.4 Perbandingan Kinerja Enam Algoritma Klasifikasi Machine Learning Berdasarkan Protokol Spatial Block Cross-Validation",
        source="Sumber: Hasil Uji Validasi Silang Spasial 5-Fold Peneliti (2024)",
        col_widths=t44_widths
    )
    
    body(
        doc,
        "Berdasarkan rekapan hasil uji, model SVM mencatatkan skor akurasi paling unggul secara keseluruhan dengan Overall Accuracy 84,00%, "
        "F1-Macro 0,8423, dan Kappa 0,7884. Keunggulan SVM didorong oleh kemampuannya memproyeksikan fitur ke ruang dimensi tinggi via kernel RBF "
        "untuk menemukan batas pemisah margin maksimal. Namun demikian, SVM memerlukan waktu komputasi pelatihan hingga 760 detik dan kompleksitas "
        "inferensi O(N_support_vectors * d), yang menjadikannya sangat mahal untuk memproses ratusan juta piksel Pulau Kalimantan."
    )
    body(
        doc,
        "LightGBM menempati posisi kedua dengan perbedaan akurasi yang sangat marjinal (OA 83,32%, F1-Macro 0,8347, Kappa 0,7795), "
        "namun menuntaskan proses pelatihan hanya dalam waktu 116,6 detik—yakni 6,5 kali lebih cepat daripada SVM dan hampir 4 kali lebih cepat "
        "daripada Random Forest. Dengan mempertimbangkan kebutuhan pemrosesan makro 73 juta hektar secara multi-temporal, LightGBM secara definitif "
        "ditetapkan sebagai model operasional final dalam penelitian ini."
    )
    
    h4(doc, "4.4 Evaluasi Rinci Kinerja Model Operasional LightGBM per Kategori Lahan")
    body(
        doc,
        "Pengujian tingkat keandalan model operasional LightGBM dievaluasi lebih lanjut pada tingkat kelas tutupan lahan spesifik "
        "menggunakan data out-of-fold testing set. Rincian Producer's Accuracy, User's Accuracy, F1-Score, dan IoU disajikan pada Tabel 4.5."
    )
    
    # Tabel 4.5 Rincian Per Kategori Lahan LightGBM
    t45_headers = ["Kelas Tutupan Lahan", "Producer's Accuracy (PA / Recall)", "User's Accuracy (UA / Precision)", "F1-Score", "Intersection over Union (IoU)", "Evaluasi Keandalan"]
    t45_data = [
        ["Badan Air (Water)", "0,9490 (94,9%)", "0,9496 (95,0%)", "0,9493", "0,9037", "Sangat Istimewa: Daya serap NIR sempurna."],
        ["Hutan (Forest)", "0,8412 (84,1%)", "0,8585 (85,9%)", "0,8498", "0,7388", "Tinggi: Kanopi padat terpetakan sangat konsisten."],
        ["Area Terbangun (Built-up)", "0,8346 (83,5%)", "0,8143 (81,4%)", "0,8243", "0,7016", "Baik: NDBI berhasil memisahkan struktur fisik."],
        ["Lahan Terbuka / Tambang (Bare)", "0,7832 (78,3%)", "0,7771 (77,7%)", "0,7801", "0,6405", "Cukup: Terjadi sedikit konfusi dengan tanah pertanian kering."],
        ["Semak / Pertanian (Shrub/Agri)", "0,7755 (77,6%)", "0,7658 (76,6%)", "0,7706", "0,6274", "Terendah: Transisi gradasi spektral dengan kanopi hutan."]
    ]
    t45_widths = [3.5, 2.7, 2.7, 2.0, 2.5, 4.5]
    add_academic_table(
        doc, t45_headers, t45_data,
        caption="Tabel 4.5 Rincian Metrik Evaluasi Klasifikasi per Kategori Tutupan Lahan pada Model Operasional LightGBM",
        source="Sumber: Ringkasan Evaluasi Model LightGBM (summary_lgbm.json) (2024)",
        col_widths=t45_widths
    )
    
    # Gambar Matriks Konfusi LightGBM
    img_cm = r"results/classification/confusion_matrices/cm_lgbm.png"
    add_image_figure(
        doc, img_cm,
        caption="Gambar 4.1 Visualisasi Matriks Konfusi (Confusion Matrix) Model Operasional LightGBM pada Pengujian Spatial Block 5-Fold",
        source="Sumber: Hasil Visualisasi Matriks Konfusi Peneliti (2024)",
        width_cm=13.5
    )
    
    body(
        doc,
        "Analisis matriks konfusi (Gambar 4.1) memperlihatkan bahwa kelas Water merupakan kelas dengan performa terbaik (PA 94,9%, UA 95,0%, IoU 0,9037) "
        "karena karakteristik penyerapan radiasi inframerah yang sangat kontras terhadap objek daratan. Kelas Forest mencatatkan IoU 0,7388 dengan UA 85,85%, "
        "menunjukkan keandalan tinggi dalam mendeteksi tutupan vegetasi berkayu. Sebaliknya, tantangan klasifikasi terbesar muncul pada pemisahan "
        "antara Shrubland/Agriculture (IoU 0,6274) dan Forest, di mana vegetasi semak belukar yang lebat dan perkebunan kelapa sawit muda sering kali "
        "memiliki nilai reflektansi kanopi yang bertumpang tindih dengan hutan sekunder regenerasi."
    )
    
    h4(doc, "4.5 Atribusi Fitur dan Analisis Explainable AI (SHAP)")
    body(
        doc,
        "Untuk memahami mekanisme keputusan internal model LightGBM, dilakukan evaluasi kontribusi prediktor menggunakan nilai rata-rata absolut SHAP "
        "(mean |SHAP value|) serta metrik split importance berbasis frekuensi percabangan pohon. Hasil peringkat disajikan pada Tabel 4.6."
    )
    
    # Tabel 4.6 Feature Importance & SHAP
    t46_headers = ["Peringkat", "Fitur Prediktor", "Mean |SHAP Value|", "Split Count Importance", "Domain Spektral", "Signifikansi Interpretasi Biofisik"]
    t46_data = [
        ["1", "NDVI", "0,9383", "3.245", "Indeks Vegetasi (NIR & Red)", "Prediktor paling dominan: Pemisah utama vegetasi hijau dari non-vegetasi."],
        ["2", "B12", "0,4702", "4.120", "SWIR2 (2.190 nm)", "Sensitif terhadap struktur tanah terbuka, batuan tambang, dan kelembaban."],
        ["3", "B11", "0,4434", "3.890", "SWIR1 (1.610 nm)", "Membedakan kadar air kanopi dan memisahkan area terbangun dari tanah."],
        ["4", "B3", "0,2174", "2.950", "Green (560 nm)", "Puncak reflektansi vegetasi pada spektrum tampak."],
        ["5", "NDBI", "0,1779", "2.410", "Indeks Terbangun (SWIR1 & NIR)", "Penentu utama diskriminasi struktur fisik terbangun dan jalan."],
        ["6", "B2", "0,1659", "2.180", "Blue (490 nm)", "Sensitif terhadap partikel atmosfer dan penetrasi perairan dangkal."],
        ["7", "BSI", "0,1586", "2.050", "Indeks Tanah Terbuka", "Membantu delineasi lahan terbuka tambang terhadap tanah pertanian."],
        ["8", "B4", "0,1541", "1.920", "Red (665 nm)", "Kanal penyerapan klorofil vegetasi aktif."],
        ["9", "B8", "0,1403", "1.740", "NIR (842 nm)", "Reflektansi struktur mesofil daun."],
        ["10", "NDMI", "0,0463", "890", "Indeks Kelembaban", "Kolinear dengan NDBI; memberikan kontribusi marginal residu."]
    ]
    t46_widths = [1.2, 1.8, 2.5, 2.5, 3.2, 5.0]
    add_academic_table(
        doc, t46_headers, t46_data,
        caption="Tabel 4.6 Peringkat Kepentingan Fitur Spektral Berdasarkan Nilai Rata-rata Absolut SHAP dan Split Importance Model LightGBM",
        source="Sumber: Hasil Ekstraksi TreeSHAP Peneliti (shap_importance.csv) (2024)",
        col_widths=t46_widths
    )
    
    # Gambar SHAP Summary
    img_shap = r"results/shap/lgbm/shap_summary.png"
    add_image_figure(
        doc, img_shap,
        caption="Gambar 4.2 Visualisasi Distribusi dan Arah Pengaruh Fitur Spektral Berbasis SHAP Summary Plot Model LightGBM",
        source="Sumber: Hasil Analisis SHAP Peneliti (2024)",
        width_cm=14.0
    )
    
    body(
        doc,
        "Dominasi luar biasa NDVI (mean |SHAP| = 0,9383—hampir dua kali lipat fitur kedua) menegaskan bahwa diferensiasi kanopi vegetasi "
        "terhadap kelas non-vegetasi merupakan sumbu keputusan utama model. Kanal gelombang pendek B12 (0,4702) dan B11 (0,4434) menempati posisi "
        "krusial berikutnya. Plot ringkasan SHAP (Gambar 4.2) memperlihatkan bahwa nilai B12 yang tinggi secara konsisten mendorong prediksi ke arah "
        "kelas Bare/Mining-like dan Built-up, sementara nilai NDVI yang tinggi secara tegas mengunci prediksi pada kelas Forest."
    )
    
    h4(doc, "4.6 Hasil Deteksi Perubahan Spatiotemporal Kalimantan (2019–2024)")
    body(
        doc,
        "Dinamika perubahan tutupan lahan Pulau Kalimantan dievaluasi secara menyeluruh menggunakan agregasi spasial Majority Voting 500 meter "
        "yang mencakup 1.499.024 sel grid valid. Matriks transisi spasiotemporal 5 x 5 disajikan pada Tabel 4.7, merangkum secara presisi "
        "trajektori alih fungsi antarkelas antara kondisi rona awal pra-IKN (2019) dan puncak fase konstruksi fisik (2024)."
    )
    
    # Tabel 4.7 Matriks Transisi Majority Voting 2019-2024
    t47_headers = ["Kelas Tutupan 2019", "Bare/Mining (2024)", "Built-up (2024)", "Forest (2024)", "Shrubland (2024)", "Water (2024)", "Total 2019", "Persistensi (%)"]
    t47_data = [
        ["Bare / Mining-like", "2.144", "818", "1.342", "1.768", "1.056", "7.128", "30,08%"],
        ["Built-up", "766", "6.163", "3.456", "8.640", "465", "19.490", "31,62%"],
        ["Forest", "3.797", "6.853", "1.106.197", "68.678", "449", "1.185.974", "93,27%"],
        ["Shrubland / Agri", "2.470", "6.616", "104.412", "148.975", "1.800", "264.273", "56,37%"],
        ["Water", "1.042", "173", "538", "722", "19.684", "22.159", "88,83%"],
        ["Total 2024", "10.219", "20.623", "1.215.945", "228.783", "23.454", "1.499.024", "85,60%"],
        ["Gross Gain (Sel)", "+8.075", "+14.460", "+109.748", "+79.808", "+3.770", "-", "-"]
    ]
    t47_widths = [3.2, 2.0, 2.0, 2.0, 2.0, 2.0, 2.2, 2.2]
    add_academic_table(
        doc, t47_headers, t47_data,
        caption="Tabel 4.7 Matriks Transisi Spasiotemporal Tutupan Lahan Kalimantan Periode 2019–2024 Berbasis Majority Voting 500 Meter (N = 1.499.024 Sel Grid)",
        source="Sumber: Hasil Analisis Post-Classification Comparison Majority Voting (majority_voting_kalimantan.csv) (2024)",
        col_widths=t47_widths
    )
    
    # Gambar Tren Temporal & Heatmap Matriks Transisi
    img_trend = r"results/change_maps_v2/temporal_trends_v2.png"
    add_image_figure(
        doc, img_trend,
        caption="Gambar 4.3 Tren Temporal Komposisi Tutupan Lahan Pulau Kalimantan Berdasarkan Deret Waktu Tahunan (2019–2024)",
        source="Sumber: Hasil Olahan Analisis Tren Temporal Peneliti (2024)",
        width_cm=14.5
    )
    
    img_tm_heat = r"results/change_maps_v2/transition_matrix_2019_2024.png"
    add_image_figure(
        doc, img_tm_heat,
        caption="Gambar 4.4 Heatmap Matriks Transisi Tutupan Lahan Kalimantan (2019–2024) Menunjukkan Jalur Konversi Dominan",
        source="Sumber: Hasil Visualisasi Matriks Transisi Peneliti (2024)",
        width_cm=12.5
    )
    
    body(
        doc,
        "Berdasarkan matriks transisi Majority Voting (Tabel 4.7), total lanskap yang mengalami alih fungsi kelas mencapai 215.861 sel (14,40%), "
        "sementara 1.283.163 sel (85,60%) berada dalam status persistensi stabil. Sebanyak 1.106.197 dari 1.185.974 sel Forest tahun 2019 berhasil "
        "mempertahankan kanopinya hingga 2024 (tingkat persistensi 93,27%). Namun demikian, terjadi kehilangan tutupan hutan riil (gross forest loss) "
        "yang sangat masif sebesar 79.777 sel (5,32% dari total daratan pulau, atau 6,73% dari luasan hutan rona awal), yang mayoritas terkonversi "
        "menjadi Shrubland/Agriculture (68.678 sel), Area Terbangun (6.853 sel), dan Lahan Terbuka/Tambang (3.797 sel)."
    )
    body(
        doc,
        "Di sisi lain, teramati penambahan tutupan hutan semu (gross forest gain) sebesar 109.748 sel, yang sebagian besar berasal dari reklasifikasi "
        "Shrubland/Agriculture menjadi Forest (104.412 sel). Dinamika ini menghasilkan net forest change sebesar +29.971 sel (+2,00%), yang secara "
        "mendalam didekonstruksi pada Bagian 4.B sebagai konsekuensi pergeseran domain fenologis iklim dan efek piksel campuran. Selain itu, temuan "
        "kritis lainnya adalah eskalasi agresif Lahan Terbuka/Tambang (Bare/Mining-like) yang mencatat penambahan 8.075 sel baru (melonjak +43,36% "
        "dari 7.128 menjadi 10.219 sel) serta urbanisasi fisik yang mengonversi 14.460 sel non-terbangun menjadi area infrastruktur terbangun."
    )
    
    h4(doc, "4.7 Analisis Trajektori dan Konsistensi Temporal Dinamika Lahan")
    body(
        doc,
        "Untuk membedakan antara konversi lahan riil yang permanen dengan fluktuasi spektral sesaat, seluruh lintasan piksel antar tahun "
        "diklasifikasikan ke dalam empat tipe konsistensi temporal (Tabel 4.8). Selain itu, tingkat keyakinan prediksi model dievaluasi "
        "melintasi masing-masing kategori stabilitas (Tabel 4.9)."
    )
    
    # Tabel 4.8 Konsistensi Temporal Trajektori
    t48_headers = ["Kategori Trajektori", "Definisi Karakteristik Perubahan", "Jumlah Titik Grid", "Proporsi (%)", "Status Validitas Ekologis"]
    t48_data = [
        ["Stabil (Stable)", "Piksel mempertahankan kelas yang sama persis di seluruh 6 tahun.", "80.876", "67,99%", "Sangat Sahih: Lanskap tidak terganggu."],
        ["Transisi Tetap (Persistent)", "Piksel mengalami transisi satu kali dan bertahan hingga 2024.", "11.435", "9,61%", "Sahih: Konversi lahan antropogenik permanen."],
        ["Transisi Sementara (Temporary)", "Piksel berubah sesaat kemudian kembali ke kelas rona awal.", "16.239", "13,65%", "Dinamis: Siklus tebang-tanam atau variasi musiman."],
        ["Fluktuatif (Oscillating)", "Piksel berganti kelas bolak-balik lebih dari dua kali.", "10.393", "8,74%", "Artefak / Noise: Didominasi efek piksel campuran."],
        ["Total Common Domain", "Seluruh pengamatan terintegrasi", "118.943", "100,00%", "-"]
    ]
    t48_widths = [3.0, 4.5, 2.3, 2.0, 4.0]
    add_academic_table(
        doc, t48_headers, t48_data,
        caption="Tabel 4.8 Evaluasi Konsistensi Temporal Trajektori Perubahan Tutupan Lahan Kalimantan (2019–2024)",
        source="Sumber: Hasil Analisis Temporal Trajectory (temporal_consistency_summary.csv) (2024)",
        col_widths=t48_widths
    )
    
    # Tabel 4.9 Keyakinan Prediksi
    t49_headers = ["Kategori Stabilitas Piksel", "Rata-rata Probabilitas Maksimum", "Rata-rata Probabilitas Minimum", "Standar Deviasi Probabilitas", "Jumlah Titik (N)"]
    t49_data = [
        ["Stabil (Stable)", "0,9081 (90,8%)", "0,7913", "0,0719", "80.876"],
        ["Transisi Tetap (Persistent)", "0,7653 (76,5%)", "0,5721", "0,1317", "11.435"],
        ["Transisi Sementara (Temporary)", "0,7541 (75,4%)", "0,5580", "0,1338", "16.239"],
        ["Fluktuatif (Oscillating)", "0,6986 (69,9%)", "0,5273", "0,1300", "10.393"]
    ]
    t49_widths = [3.5, 3.2, 3.0, 3.0, 2.5]
    add_academic_table(
        doc, t49_headers, t49_data,
        caption="Tabel 4.9 Evaluasi Nilai Keyakinan (Confidence) Prediksi Model Berdasarkan Status Stabilitas Trajektori Lahan",
        source="Sumber: Hasil Evaluasi Keyakinan Prediksi (confidence_evaluation.csv) (2024)",
        col_widths=t49_widths
    )
    
    # Gambar Distribusi Keyakinan
    img_conf = r"results/change_maps_v2/confidence_distribution.png"
    add_image_figure(
        doc, img_conf,
        caption="Gambar 4.5 Distribusi Tingkat Keyakinan Prediksi Model LightGBM Menunjukkan Penurunan Keyakinan Signifikan pada Piksel Fluktuatif",
        source="Sumber: Hasil Visualisasi Keyakinan Peneliti (2024)",
        width_cm=13.5
    )
    
    body(
        doc,
        "Hasil evaluasi keyakinan (Tabel 4.9 dan Gambar 4.5) membuktikan secara empiris bahwa piksel berstatus stabil memiliki tingkat keyakinan "
        "yang sangat tinggi (rata-rata softmax probability = 0,9081 dengan standar deviasi sempit 0,0719). Sebaliknya, piksel yang mengalami "
        "transisi fluktuatif mencatatkan rata-rata probabilitas terendah (0,6986 dengan standar deviasi melebar 0,1300). Penurunan keyakinan ini "
        "mengonfirmasi bahwa transisi fluktuatif sebagian besar berada di sekitar batas ambang keputusan (decision boundary) antara kanopi vegetasi "
        "dan semak pada piksel campuran 500 meter."
    )
    
    h4(doc, "4.8 Pemetaan Spasial Skala Mikro Kawasan Inti IKN (10 m) vs Skala Makro (500 m)")
    body(
        doc,
        "Untuk melengkapi pemahaman spasial, klasifikasi resolusi tinggi 10 meter Sentinel-2 asli diaplikasikan secara spesifik pada Kawasan Inti "
        "Pusat Pemerintahan (KIPP) IKN seluas ~6.671 hektar. Perbandingan visual antara kondisi rona awal 2019 (sebelum proyek diumumkan) "
        "dan kondisi konstruksi fisik 2024 disajikan pada Gambar 4.6 dan Gambar 4.7."
    )
    
    # Gambar Peta Mikro IKN 2019 & 2024
    img_ikn_2019 = r"results/classification/ikn_10m_map_2019.png"
    add_image_figure(
        doc, img_ikn_2019,
        caption="Gambar 4.6 Peta Klasifikasi Tutupan Lahan Skala Mikro Resolusi 10 Meter Kawasan IKN Tahun 2019 (Kondisi Rona Awal / Baseline)",
        source="Sumber: Hasil Klasifikasi Model LightGBM 10m Peneliti (2024)",
        width_cm=14.0
    )
    
    img_ikn_2024 = r"results/classification/ikn_10m_map_2024.png"
    add_image_figure(
        doc, img_ikn_2024,
        caption="Gambar 4.7 Peta Klasifikasi Tutupan Lahan Skala Mikro Resolusi 10 Meter Kawasan IKN Tahun 2024 (Fase Konstruksi Fisik Aktif)",
        source="Sumber: Hasil Klasifikasi Model LightGBM 10m Peneliti (2024)",
        width_cm=14.0
    )
    
    body(
        doc,
        "Komparasi peta skala mikro (Gambar 4.6 vs Gambar 4.7) memperlihatkan transformasi spasial yang sangat tajam di pusat KIPP IKN. "
        "Pada tahun 2019, kawasan tersebut didominasi secara homogen oleh kanopi hutan tanaman industri (Eucalyptus pellita) dan semak belukar. "
        "Pada tahun 2024, terdeteksi pembukaan lahan masif membentuk pola koridor linier dan klaster poligonal area terbuka (Bare/Mining-like) "
        "serta area terbangun (Built-up). Pola linier merefleksikan pembukaan koridor Jalan Tol Akses IKN Seksi 3A/3B dan Jalan Sumbu Kebangsaan Barat/Timur, "
        "sementara pola klaster poligonal merepresentasikan tapak konstruksi Istana Garuda, Kantor Presiden, dan kompleks gedung kementerian koordinator. "
        "Delineasi skala mikro 10 meter ini berhasil menangkap detail fisik yang terlewatkan pada agregasi makro 500 meter."
    )
    
    h4(doc, "4.9 Hasil Pemodelan Regresi Logistik Spasial Multivariat Faktor Pendorong")
    body(
        doc,
        "Untuk menjawab pertanyaan penelitian terkait asosiasi spasial pembangunan IKN dan ekspansi pertambangan terhadap dinamika tutupan lahan, "
        "model regresi logistik multivariat diestimasi pada Bridge Dataset (N = 122.478 titik sampel spasial independen). Penggunaan Bridge Dataset "
        "berjarak ~10 km ini secara ketat menegakkan asumsi independensi observasi (Hukum Tobler) dan mengeliminasi risiko pseudo-replication "
        "yang dapat terjadi jika pemodelan dipaksakan pada 1,5 juta sel bertetangga. Hasil estimasi parameter statistik, standard error, z-statistic, "
        "p-value, dan Odds Ratio (OR) untuk tiga model transisi biner dirangkum pada Tabel 4.10."
    )
    
    # Tabel 4.10 Regresi Logistik Multivariat Bridge Dataset
    t410_headers = ["Variabel Prediktor", "Koefisien (β)", "Standard Error (SE)", "z-statistic", "p-value", "Odds Ratio (OR)", "Signifikansi & Arah Asosiasi"]
    t410_data = [
        ["MODEL 1: DEFORESTASI (FOREST LOSS) - Basis: 96.783 Titik Hutan 2019, Kejadian = 6.711", "", "", "", "", "", ""],
        ["Konstanta (Intersep)", "-2,9974", "0,0163", "-183,57", "<0,001", "0,0499", "Signifikan negatif"],
        ["Jarak ke IKN (distance_to_ikn)", "+0,1083", "0,0139", "+7,79", "<0,001", "1,1144", "Signifikan positif: OR = 1,114 (+11,4% per unit jarak)"],
        ["Kepadatan Tambang (mining_density_10km)", "+0,0891", "0,0088", "+10,15", "<0,001", "1,0932", "Signifikan positif: OR = 1,093 (+9,3% per unit densitas)"],
        ["Elevasi Topografi (elevation)", "-0,7723", "0,0305", "-25,32", "<0,001", "0,4620", "Signifikan mitigasi: OR = 0,462 (-53,8% per SD)"],
        ["Curah Hujan Tahunan (rainfall_annual)", "-0,0982", "0,0154", "-6,36", "<0,001", "0,9065", "Signifikan mitigasi: OR = 0,906 (-9,4% per SD)"],
        ["MODEL 2: URBANISASI (BUILT-UP EXPANSION) - Basis: 120.902 Titik Non-Terbangun, Kejadian = 1.282", "", "", "", "", "", ""],
        ["Konstanta (Intersep)", "-4,9018", "0,0376", "-130,29", "<0,001", "0,0074", "Signifikan negatif"],
        ["Jarak ke IKN (distance_to_ikn)", "-0,0477", "0,0339", "-1,41", "0,159", "0,9535", "Tidak signifikan secara statistik (p = 0,159)"],
        ["Kepadatan Tambang (mining_density_10km)", "+0,2378", "0,0106", "+22,53", "<0,001", "1,2685", "Signifikan positif: OR = 1,268 (+26,8% per unit densitas)"],
        ["Elevasi Topografi (elevation)", "-0,4713", "0,0609", "-7,75", "<0,001", "0,6242", "Signifikan mitigasi: OR = 0,624 (-37,6% per SD)"],
        ["Curah Hujan Tahunan (rainfall_annual)", "-0,2602", "0,0382", "-6,82", "<0,001", "0,7709", "Signifikan mitigasi: OR = 0,771 (-22,9% per SD)"],
        ["MODEL 3: EKSPANSI TAMBANG (BARE/MINING-LIKE) - Basis: 121.878 Titik Non-Tambang, Kejadian = 740", "", "", "", "", "", ""],
        ["Konstanta (Intersep)", "-5,9418", "0,0614", "-96,78", "<0,001", "0,0026", "Signifikan negatif"],
        ["Jarak ke IKN (distance_to_ikn)", "-0,2617", "0,0566", "-4,63", "<0,001", "0,7698", "Signifikan negatif: OR = 0,770 (-23,0% per unit jarak)"],
        ["Kepadatan Tambang (mining_density_10km)", "+0,2637", "0,0137", "+19,18", "<0,001", "1,3017", "Signifikan positif: OR = 1,302 (+30,2% per unit densitas)"],
        ["Elevasi Topografi (elevation)", "-0,2511", "0,0784", "-3,20", "0,001", "0,7779", "Signifikan mitigasi: OR = 0,778 (-22,2% per SD)"],
        ["Curah Hujan Tahunan (rainfall_annual)", "-0,3198", "0,0621", "-5,15", "<0,001", "0,7263", "Signifikan mitigasi: OR = 0,726 (-27,4% per SD)"]
    ]
    t410_widths = [3.8, 1.8, 1.8, 1.6, 1.4, 1.6, 4.5]
    add_academic_table(
        doc, t410_headers, t410_data,
        caption="Tabel 4.10 Hasil Estimasi Parameter Model Regresi Logistik Spasial Multivariat pada Bridge Dataset (N = 122.478 Titik Sampel Independen)",
        source="Sumber: Hasil Estimasi Ekonometrika Spasial Peneliti (logistic_*_2019_2024.csv) (2024)",
        col_widths=t410_widths
    )
    
    # Gambar Driver Effects Plot
    img_driver = r"results/driver_analysis_v2/driver_effects.png"
    add_image_figure(
        doc, img_driver,
        caption="Gambar 4.8 Plot Estimasi Odds Ratio dan Selang Kepercayaan 95% Faktor Pendorong Perubahan Tutupan Lahan",
        source="Sumber: Hasil Analisis Regresi Logistik Spasial Peneliti (2024)",
        width_cm=14.5
    )
    
    body(
        doc,
        "Temuan empiris dari pemodelan regresi logistik multivariat (Tabel 4.10 dan Gambar 4.8) mengungkap beberapa pola spasial krusial:"
    )
    numbered_item(
        doc, "1.", "Asosiasi Positif Jarak ke IKN terhadap Deforestasi (OR = 1,114; p < 0,001)",
        "Semakin jauh jarak suatu titik dari sentroid IKN, probabilitas terjadinya deforestasi justru meningkat sebesar 11,4% per satuan jarak standar. "
        "Hal ini membuktikan secara empiris bekerjanya kerangka telecoupling: zona inti IKN (KIPP) dijaga dan diawasi secara sangat ketat oleh pemerintah "
        "sehingga deforestasi terdorong ke koridor luar dan zona penyangga (spillover zones) yang minim pengawasan."
    )
    numbered_item(
        doc, "2.", "Pengaruh Kuat Kepadatan Tambang terhadap Seluruh Jalur Transisi",
        "Kepadatan tambang radius 10 km berasosiasi positif dan sangat signifikan (p < 0,001) terhadap ketiga model transisi: "
        "meningkatkan risiko deforestasi sebesar 9,3% (OR = 1,093), memicu urbanisasi sebesar 26,8% (OR = 1,268), dan melipatgandakan "
        "ekspansi tambang baru sebesar 26,1% (OR = 1,261)."
    )
    numbered_item(
        doc, "3.", "Peran Konsisten Mitigasi Kovariat Biofisik Lingkungan",
        "Elevasi topografi dan curah hujan tahunan secara konsisten berkoefisien negatif dan sangat signifikan (p < 0,001) di seluruh model. "
        "Elevasi tinggi mereduksi peluang deforestasi hingga 53,8% (OR = 0,462), mencerminkan bahwa medan terjal dan perbukitan pedalaman "
        "bertindak sebagai benteng pertahanan alami terhadap perambahan lahan."
    )
    
    h4(doc, "4.10 Arsitektur Platform Dashboard Interaktif Berbasis Streamlit")
    body(
        doc,
        "Sebagai bagian dari diseminasi hasil penelitian dan sarana komunikasi kebijakan, dibangun platform visualisasi interaktif geospasial "
        "memanfaatkan framework Streamlit. Sistem ini dirancang dengan antarmuka modern yang membagi fungsionalitas analitis ke dalam enam halaman modul utama:"
    )
    bullet_item(doc, "1. Land Cover Maps", "Menyajikan visualisasi peta tematik tutupan lahan Pulau Kalimantan dan mikro IKN lintas tahun pengamatan 2019–2024 dengan kontrol layer interaktif.")
    bullet_item(doc, "2. Change Detection", "Melacak dinamika matriks transisi antarkelas spasial, memetakan titik-titik deforestasi, urbanisasi, dan ekspansi tambang secara rinci.")
    bullet_item(doc, "3. Model Comparison", "Mengadu metrik komparatif (OA, F1-Score, Kappa, Waktu) keenam algoritma machine learning hasil evaluasi Spatial Block CV.")
    bullet_item(doc, "4. Driver Impact", "Mengeksplorasi hubungan spasial faktor pendorong (jarak IKN, kepadatan tambang, elevasi, curah hujan) dengan kurva respons probabilitas logistik.")
    bullet_item(doc, "5. Spatiotemporal Heatmap", "Menampilkan kepadatan titik-titik perubahan lahan secara spasial dan kewilayahan melintasi lima provinsi di Kalimantan.")
    bullet_item(doc, "6. SHAP Analysis", "Membedah atribusi nilai Shapley lokal dan global pada model LightGBM untuk transparansi ilmiah penuh.")
