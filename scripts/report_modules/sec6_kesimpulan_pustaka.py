from config_and_helpers import (
    h2, h3, h4, body, numbered_item, bullet_item, add_academic_table, format_run
)
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_section_6(doc):
    # BAB V
    h2(doc, "BAB V KESIMPULAN DAN SARAN")
    
    h3(doc, "5.1 Kesimpulan Komprehensif")
    body(
        doc,
        "Berdasarkan hasil analisis geospasial sekuensial tiga tahap (Klasifikasi → Deteksi Perubahan → Regresi Logistik Spasial) "
        "yang diaplikasikan pada citra satelit multispektral Sentinel-2 periode 2019–2024 di Pulau Kalimantan, penelitian ini menyimpulkan:"
    )
    numbered_item(
        doc, "1.", "Kinerja Model Klasifikasi Machine Learning",
        "Penerapan protokol Spatial Block GroupKFold 5-fold membuktikan bahwa model Support Vector Machine (SVM) dan Light Gradient Boosting Machine "
        "(LightGBM) mencapai tingkat akurasi generalisasi spasial tertinggi (masing-masing Overall Accuracy 84,00% dan 83,32%; Cohen's Kappa 0,7884 dan 0,7795). "
        "Namun, LightGBM terpilih sebagai model operasional terbaik karena mampu menuntaskan pelatihan dalam waktu 116,6 detik—yakni 6,5 kali lebih cepat "
        "daripada SVM (760,0 s) dan 3,9 kali lebih cepat daripada Random Forest (450,0 s), menjadikannya sangat scalable untuk mengolah bentang alam "
        "daratan 73 juta hektar secara multi-temporal."
    )
    numbered_item(
        doc, "2.", "Atribusi Fitur Berbasis Explainable AI (SHAP)",
        "Evaluasi atribusi nilai Shapley (SHAP) menegaskan bahwa indeks vegetasi NDVI merupakan fitur paling penting secara mutlak (mean |SHAP| = 0,9383), "
        "berperan sebagai pemisah fundamental antara formasi vegetasi hijau kanopi rapat dengan kelas non-vegetasi. Kanal inframerah gelombang pendek "
        "B12 (0,4702) dan B11 (0,4434) bertindak sebagai pembeda kritis berikutnya yang mengisolasi karakteristik lahan terbuka bekas galian tambang "
        "dan area terbangun dari tanah bervegetasi."
    )
    numbered_item(
        doc, "3.", "Dinamika Spasiotemporal Berbasis Majority Voting dan Dekonstruksi 'Net Forest Gain'",
        "Analisis deteksi perubahan pasca-klasifikasi berbasis Majority Voting Sub-Grid Aggregation 500 meter (1.499.024 sel grid valid) "
        "berhasil mengeliminasi bias under-sampling tutupan awan khatulistiwa dan mencatat persistensi kanopi hutan sebesar 93,27% (1.106.197 sel). "
        "Pendekatan ini berhasil membongkar kehilangan tutupan hutan riil (gross forest loss) yang tajam sebesar 79.777 sel (5,32% dari bentang daratan pulau, "
        "atau setara 6,73% dari hutan rona awal), ekspansi masif lahan terbuka tambang sebesar 8.075 sel (+43,36%), dan alih fungsi ke area terbangun "
        "sebesar 14.460 sel. Dekonstruksi ilmiah membuktikan bahwa penambahan hutan neto semu sebesar +29.971 sel (+2,00%) bukan merupakan ekspansi hutan primer, "
        "melainkan artefak spektral akibat efek piksel campuran (mixed pixels) dan variabilitas domain fenologis iklim (La Niña 2021 vs El Niño 2023). "
        "Secara total, sebanyak 215.861 sel (14,40%) mengalami transformasi bentang lahan sepanjang 2019–2024."
    )
    numbered_item(
        doc, "4.", "Delineasi Skala Mikro Kawasan Inti IKN (10 m)",
        "Berbeda dengan dinamika makro, klasifikasi skala mikro resolusi asli 10 meter di Kawasan Inti Pusat Pemerintahan (KIPP) IKN membuktikan "
        "terjadinya konversi tutupan lahan secara nyata dan terarah. Terpetakan pembukaan koridor linier infrastruktur transportasi (Jalan Tol Akses "
        "Seksi 3A/3B dan Sumbu Kebangsaan) serta klaster tapak konstruksi gedung pemerintahan (Istana Garuda dan Kompleks Kemenko) yang mengubah "
        "hutan tanaman industri menjadi lahan terbuka dan area terbangun."
    )
    numbered_item(
        doc, "5.", "Asosiasi Spasial Faktor Pendorong pada Bridge Dataset dan Kerangka Telecoupling",
        "Pemodelan regresi logistik multivariat pada Bridge Dataset (122.478 titik sampel spasial independen berjarak ~10 km via spatial intersection cKDTree) "
        "menegakkan asumsi independensi observasi bebas pseudo-replication dan membuktikan bekerjanya mekanisme spatial telecoupling secara sangat signifikan (p < 0,001): "
        "(a) Variabel jarak ke sentroid IKN berasosiasi positif terhadap deforestasi (OR = 1,114; p < 0,001), membuktikan pergeseran rembesan (spillover) "
        "tekanan pembukaan hutan ke koridor penyangga luar 10–50 km akibat penjagaan super ketat di zona inti KIPP; "
        "(b) Kepadatan tambang radius 10 km bertindak sebagai akselerator kuat alih fungsi lahan (OR = 1,093 pada deforestasi, OR = 1,268 pada urbanisasi, "
        "dan OR = 1,302 pada ekspansi tambang); serta (c) Kovariat biofisik elevasi tinggi (OR = 0,462) dan curah hujan tahunan (OR = 0,906) "
        "secara konsisten bertindak sebagai faktor mitigasi/penahan alami bentang alam."
    )
    
    h3(doc, "5.2 Implikasi Kebijakan dan Rekomendasi Tata Ruang")
    body(
        doc,
        "Temuan empiris penelitian ini menghasilkan rekomendasi strategis bagi instansi perencana dan penegak hukum lingkungan hidup:"
    )
    numbered_item(
        doc, "1.", "Pengawasan Khusus Koridor Penyangga IKN (Radius 10–50 km)",
        "Otorita IKN bersama Pemerintah Provinsi Kalimantan Timur dan Pemerintah Kabupaten Kutai Kartanegara/PPU disarankan segera membentuk "
        "Satuan Tugas Pengawasan Tata Ruang Terpadu di zona penyangga luar KIPP (khususnya wilayah Samboja, Muara Jawa, dan Sepaku luar). "
        "Regulasi zonasi penyangga hijau harus diperketat untuk membendung rembesan alih fungsi lahan liar dan spekulasi tanah komersial informal."
    )
    numbered_item(
        doc, "2.", "Moratorium dan Penertiban Tambang Batubara Ilegal di Sekitar Koridor IKN",
        "Kementerian ESDM dan Ditjen Gakkum KLHK perlu mengintensifkan inspeksi terhadap izin usaha pertambangan (IUP) dan lubang tambang ilegal "
        "di sekitar Daerah Aliran Sungai (DAS) Mahakam dan Samboja. Mengingat tingginya Odds Ratio kepadatan tambang terhadap degradasi lingkungan, "
        "kewajiban reklamasi lubang tambang (voids) dan revegetasi pascatambang harus ditegakkan secara mengikat dengan jaminan bank."
    )
    numbered_item(
        doc, "3.", "Pemanfaatan Platform Pemantauan Satelit Berkala",
        "Platform dashboard interaktif berbasis data Sentinel-2 dan machine learning yang dikembangkan dalam penelitian ini dapat diadopsi oleh "
        "Bappenas dan Otorita IKN sebagai sistem peringatan dini (early warning system) otomatis untuk mendeteksi anomali pembukaan kanopi hutan "
        "secara hampir seketika (near-real-time) setiap siklus 5 hari."
    )
    
    h3(doc, "5.3 Rekomendasi Riset Masa Depan")
    body(
        doc,
        "Untuk mengatasi keterbatasan teknis yang telah diidentifikasi, penelitian lanjutan disarankan untuk mengeksplorasi agenda berikut:"
    )
    bullet_item(
        doc, "Integrasi Citra Radar Sintetik (SAR Sentinel-1)",
        "Menggabungkan citra optik Sentinel-2 dengan polarisasi ganda (VV + VH) radar Sentinel-1 C-band. Sensor radar gelombang mikro mampu menembus "
        "lapisan awan tebal secara kontinu dan memberikan informasi kekasaran permukaan serta volume biomassa berkayu yang independen dari cuaca."
    )
    bullet_item(
        doc, "Penerapan Sensor Resolusi Sangat Tinggi (VHR)",
        "Menggunakan citra komersial resolusi tinggi (seperti PlanetScope 3 meter atau SPOT-7 1,5 meter) pada area-area bertransformasi cepat "
        "guna mengeliminasi efek piksel campuran dan memverifikasi batas fisik tapak proyek secara presisi."
    )
    bullet_item(
        doc, "Pengembangan Pemodelan Kausal Struktural (Spatial SEM)",
        "Menerapkan Structural Equation Modeling (SEM) geospasial atau analisis Difference-in-Differences (DiD) spasial berbobot untuk menguji "
        "hubungan kausalitas langsung antara intervensi kebijakan pemindahan ibu kota dengan degradasi lingkungan regional."
    )
    
    # DAFTAR PUSTAKA
    h2(doc, "DAFTAR PUSTAKA")
    
    references = [
        "Breiman, L. (2001). Random forests. Machine Learning, 45(1), 5–32. https://doi.org/10.1023/A:1010933404324",
        "Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 785–794. https://doi.org/10.1145/2939672.2939785",
        "Cortes, C., & Vapnik, V. (1995). Support-vector networks. Machine Learning, 20(3), 273–297. https://doi.org/10.1007/BF00994018",
        "Cracknell, A. P. (1998). Synergy in remote sensing—What's in a pixel? International Journal of Remote Sensing, 19(11), 2025–2047. https://doi.org/10.1080/014311698214848",
        "Di Gregorio, A., & Jansen, L. J. M. (2000). Land Cover Classification System (LCCS): Classification concepts and user manual. Food and Agriculture Organization of the United Nations (FAO), Rome.",
        "European Space Agency (ESA). (2021). ESA WorldCover 10 m 2021 v200. European Space Agency. https://doi.org/10.5281/zenodo.5571939",
        "Farr, T. G., Rosen, P. A., Caro, E., Crippen, R., Duren, R., Hensley, S., Kobrick, M., Paller, M., Rodriguez, E., Roth, L., Seal, D., Shaffer, S., Shimada, J., Umland, J., Werner, M., Oskin, M., Burbank, D., & Alsdorf, D. (2007). The Shuttle Radar Topography Mission. Reviews of Geophysics, 45(2), RG2004. https://doi.org/10.1029/2005RG000183",
        "Foody, G. M. (2002). Status of land cover classification accuracy assessment. Remote Sensing of Environment, 80(1), 185–201. https://doi.org/10.1016/S0034-4257(01)00295-4",
        "Funk, C., Peterson, P., Landsfeld, M., Pedreros, D., Verdin, J., Shukla, S., Husak, G., Rowland, J., Harrison, L., Hoell, A., & Michaelsen, J. (2015). The climate hazards infrared precipitation with stations—A new environmental record for monitoring extremes. Scientific Data, 2, 150066. https://doi.org/10.1038/sdata.2015.66",
        "Gao, B. C. (1996). NDWI—A normalized difference water index for remote sensing of vegetation liquid water from space. Remote Sensing of Environment, 58(3), 257–266. https://doi.org/10.1016/S0034-4257(96)00067-3",
        "Habibie, M. I., et al. (2025). Spatiotemporal dynamics of tropical land cover in Kalimantan using Sentinel-2 annual composites and Google Earth Engine. Remote Sensing of Environment, 310, 114201. https://doi.org/10.1016/j.rse.2024.114201",
        "Hansen, M. C., Potapov, P. V., Moore, R., Hancher, M., Turubanova, S. A., Tyukavina, A., Thau, D., Stehman, S. V., Goetz, S. J., Loveland, T. R., Kommareddy, A., Egorov, A., Chini, L., Justice, C. O., & Townshend, J. R. G. (2013). High-resolution global maps of 21st-century forest cover change. Science, 342(6160), 850–853. https://doi.org/10.1126/science.1244693",
        "Hastie, T., Tibshirani, R., & Friedman, J. (2009). The Elements of Statistical Learning: Data Mining, Inference, and Prediction (2nd ed.). Springer, New York.",
        "Hazanul, M., et al. (2022). Analisis dinamika tutupan lahan dan pemodelan spasial perkembangan kawasan IKN Nusantara berbasis citra multispektral. Jurnal Penginderaan Jauh dan Pengolahan Data Citra Digital, 19(2), 49–61.",
        "Hosmer, D. W., & Lemeshow, S. (2000). Applied Logistic Regression (2nd ed.). John Wiley & Sons, New York.",
        "Hussain, M., Chen, D., Cheng, A., Wei, H., & Stanley, D. (2013). Change detection from remotely sensed images: From pixel-based to object-based approaches. ISPRS Journal of Photogrammetry and Remote Sensing, 80, 91–106. https://doi.org/10.1016/j.isprsjprs.2013.03.006",
        "Jensen, J. R. (2015). Introductory Digital Image Processing: A Remote Sensing Perspective (4th ed.). Pearson Education, Glenview.",
        "Karra, K., Kontgis, C., Statman-Weil, Z., Mazzariello, J. C., Mathis, M., & Brumby, S. P. (2021). Global land use / land cover with Sentinel 2 and deep learning. IEEE International Geoscience and Remote Sensing Symposium (IGARSS), 4704–4707. https://doi.org/10.1109/IGARSS47720.2021.9553499",
        "Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T.-Y. (2017). LightGBM: A highly efficient gradient boosting decision tree. Advances in Neural Information Processing Systems (NeurIPS 2017), 30, 3146–3154.",
        "Lambin, E. F., Turner, B. L., Geist, H. J., Agbola, S. B., Angelsen, A., Bruce, J. W., Coomes, O. T., Dirzo, R., Fischer, G., Folke, C., George, P. S., Homewood, K., Imbernon, J., Leemans, R., Li, X., Moran, E. F., Mortimore, M., Ramakrishnan, P. S., Richards, J. F., ... Xu, J. (2001). The causes of land-use and land-cover change: Moving beyond the myths. Global Environmental Change, 11(4), 261–269. https://doi.org/10.1016/S0959-3780(01)00007-3",
        "Lambin, E. F., & Meyfroidt, P. (2011). Global land use change, economic globalization, and the looming land scarcity. Proceedings of the National Academy of Sciences, 108(9), 3465–3472. https://doi.org/10.1073/pnas.1100480108",
        "Lillesand, T., Kiefer, R. W., & Chipman, J. (2015). Remote Sensing and Image Interpretation (7th ed.). John Wiley & Sons, New York.",
        "Liu, J., Hull, V., Batistella, M., DeFries, R., Dietz, T., Fu, F., Hertel, T. W., Izaurralde, R. C., Lambin, E. F., Li, S., Martinelli, L. A., McConnell, W. J., Moran, E. F., Naylor, R., Ouyang, Z., Polenske, K. R., Reenberg, A., Rocha, G., Simmons, C. S., ... Zhu, C. (2013). Framing sustainability in a telecoupled world. Ecology and Society, 18(2), 26. https://doi.org/10.5751/ES-05873-180226",
        "Liu, J., Mooney, H., Hull, V., Davis, S. J., Gaskell, J., Hertel, T., Lubchenco, J., Seto, K. C., Gleason, P., Kremen, C., & Li, S. (2015). Systems integration for global sustainability. Science, 347(6225), 1258832. https://doi.org/10.1126/science.1258832",
        "Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. Advances in Neural Information Processing Systems (NeurIPS 2017), 30, 4765–4774.",
        "Lundberg, S. M., Erion, G., Chen, H., DeGrave, A., Prutkin, J. M., Nair, B., Katz, R., Himmelfarb, J., Bansal, N., & Lee, S.-I. (2020). From local explanations to global understanding with explainable AI for trees. Nature Machine Intelligence, 2(1), 56–67. https://doi.org/10.1038/s42256-019-0138-9",
        "Maus, V., Giljum, S., Gutschlhofer, J., da Silva, D. M., Probst, M., Gass, S. L. B., Luckeneder, S., Lieber, M., & McCallum, I. (2022). A global-scale dataset of surface mining areas. Scientific Data, 9(1), 743. https://doi.org/10.1038/s41597-022-01869-y",
        "Meyfroidt, P., Lambin, E. F., Erb, K.-H., & Hertel, T. W. (2014). Globalization of land use: Distant drivers of land change and geographic displacement of environmental impacts. Current Opinion in Environmental Sustainability, 5(5), 438–444. https://doi.org/10.1016/j.cosust.2013.04.003",
        "Phiri, D., Simwanda, M., Salekin, S., Nyirenda, V. R., Murayama, Y., & Ranagalage, M. (2020). Sentinel-2 data for land cover/use mapping: A review. Remote Sensing, 12(14), 2291. https://doi.org/10.3390/rs12142291",
        "Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., & Gulin, A. (2018). CatBoost: Unbiased boosting with categorical features. Advances in Neural Information Processing Systems (NeurIPS 2018), 31, 6638–6648.",
        "Rikimaru, A., Roy, P. S., & Miyatake, S. (2002). Tropical forest cover density mapping. Tropical Ecology, 43(1), 39–47.",
        "Roberts, D. R., Bahn, V., Ciuti, S., Boyce, M. S., Elith, J., Guillera-Arroita, G., Hauenstein, S., Lahoz-Monfort, J. J., Schröder, B., Thuiller, W., Warton, D. I., Wintle, B. A., Hartig, F., & Dormann, C. F. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. Ecography, 40(8), 913–929. https://doi.org/10.1111/ecog.02881",
        "Rouse, J. W., Haas, R. H., Schell, J. A., & Deering, D. W. (1974). Monitoring vegetation systems in the Great Plains with ERTS. Third Earth Resources Technology Satellite-1 Symposium, NASA SP-351, 309–317.",
        "Singh, A. (1989). Review article: Digital change detection techniques using remotely-sensed data. International Journal of Remote Sensing, 10(6), 989–1003. https://doi.org/10.1080/01431168908903939",
        "Sokolova, M., & Lapalme, G. (2009). A systematic analysis of performance measures for classification tasks. Information Processing & Management, 45(4), 427–437. https://doi.org/10.1016/j.ipm.2009.03.002",
        "Talukdar, S., Singha, P., Mahato, S., Shahfahad, Pal, S., Liou, Y.-A., & Rahman, A. (2020). Land-use land-cover classification by machine learning classifiers for satellite observations—A review. Remote Sensing, 12(7), 1135. https://doi.org/10.3390/rs12071135",
        "Tobler, W. R. (1970). A computer movie simulating urban growth in the Detroit region. Economic Geography, 46(sup1), 234–240. https://doi.org/10.2307/143141",
        "Valavi, R., Elith, J., Lahoz-Monfort, J. J., & Guillera-Arroita, G. (2019). blockCV: An R package for generating spatially or environmentally separated folds for k-fold cross-validation of species distribution models. Methods in Ecology and Evolution, 10(2), 225–232. https://doi.org/10.1111/2041-210X.13107",
        "Zha, Y., Gao, J., & Ni, S. (2003). Use of normalized difference built-up index in automatically mapping urban areas from TM imagery. International Journal of Remote Sensing, 24(3), 583–594. https://doi.org/10.1080/01431160304987",
        "Zhu, Z. (2017). Change detection using Landsat time series: A review of frequencies, preprocessing, algorithms, and applications. ISPRS Journal of Photogrammetry and Remote Sensing, 130, 370–384. https://doi.org/10.1016/j.isprsjprs.2017.06.013"
    ]
    
    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(0)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.05
        p_ref.paragraph_format.left_indent = Cm(0.75)
        p_ref.paragraph_format.first_line_indent = Cm(-0.75)
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p_ref.add_run(ref)
        format_run(r, size_pt=9.5, bold=False)
    
    # LAMPIRAN
    h2(doc, "LAMPIRAN LENGKAP")
    
    h3(doc, "Lampiran 1. Konfigurasi Hyperparameter Optimal Enam Algoritma Machine Learning")
    body(
        doc,
        "Konfigurasi hyperparameter optimal ditentukan melalui pengujian RandomizedSearchCV dan GridSearchCV "
        "yang diintegrasikan dengan Spatial Block GroupKFold 5-fold pada 30.000 titik sampel data latih:"
    )
    t_hyp_headers = ["Algoritma", "Hyperparameter Optimal", "Spesifikasi Nilai Terpilih", "Justifikasi Teknis"]
    t_hyp_data = [
        ["LightGBM", "n_estimators, max_depth, learning_rate, num_leaves", "500, -1 (unlimited), 0.01, 63", "Konvergensi halus dengan regularisasi leaf-wise."],
        ["XGBoost", "n_estimators, max_depth, learning_rate, subsample", "400, 8, 0.02, 0.8", "Mengendalikan varians pohon pada data spektral berdimensi 10."],
        ["Random Forest", "n_estimators, max_depth, max_features, min_samples_split", "300, 25, 'sqrt' (3 fitur), 5", "Mencegah korelasi antar pohon pada ensambel bagging."],
        ["CatBoost", "iterations, depth, learning_rate, l2_leaf_reg", "500, 7, 0.03, 3.0", "Mereduksi bias pergeseran target pada batas kelas vegetasi."],
        ["SVM (RBF)", "C (penalti), gamma (lebar kernel), scaler", "10.0, 'scale' (1/(n_features*Var), StandardScaler", "Margin optimal pada ruang proyeksi RBF non-linear."],
        ["Multinomial LogReg", "C (invers regularisasi L2), solver, max_iter", "1.0, 'lbfgs', 1000", "Solusi konvergen stabil sebagai garis dasar linier."]
    ]
    t_hyp_widths = [3.0, 4.5, 4.5, 4.5]
    add_academic_table(
        doc, t_hyp_headers, t_hyp_data,
        caption="Tabel L1.1 Ringkasan Konfigurasi Hyperparameter Optimal Hasil Penalaan Spatial Block CV",
        source="Sumber: Hasil Grid Search Hyperparameter Peneliti (2024)",
        col_widths=t_hyp_widths
    )
    
    h3(doc, "Lampiran 2. Matriks Dinamika Perubahan Antartahun Berturutan pada Subsampel Validasi Temporal")
    body(
        doc,
        "Dinamika perubahan tutupan lahan antartahun berturutan (consecutive year-to-year change) "
        "pada subsampel validasi temporal tahunan (118.943 titik observasi terintegrasi bebas awan 6 tahun berturutan) disajikan pada Tabel L2.1 "
        "guna memantau kecepatan dan volatilitas transisi antartahun:"
    )
    t_cons_headers = ["Periode Interval", "Total Titik", "Stabil / Persisten", "Kehilangan Hutan (Loss)", "Pertambahan Hutan (Gain)", "Urbanisasi Baru", "Ekspansi Tambang Baru"]
    t_cons_data = [
        ["2019 → 2020", "118.943", "109.845 (92,35%)", "6.718 titik", "7.487 titik", "810 titik", "310 titik"],
        ["2020 → 2021", "118.943", "108.924 (91,58%)", "6.068 titik", "7.831 titik", "964 titik", "351 titik"],
        ["2021 → 2022", "118.943", "107.540 (90,41%)", "4.708 titik", "8.569 titik", "914 titik", "624 titik"],
        ["2022 → 2023", "118.943", "106.812 (89,80%)", "8.017 titik", "5.018 titik", "1.815 titik", "657 titik"],
        ["2023 → 2024", "118.943", "107.930 (90,74%)", "6.497 titik", "6.490 titik", "987 titik", "326 titik"]
    ]
    t_cons_widths = [2.5, 2.3, 3.2, 2.8, 2.8, 2.5, 2.5]
    add_academic_table(
        doc, t_cons_headers, t_cons_data,
        caption="Tabel L2.1 Rekapitulasi Kejadian Perubahan Tutupan Lahan Antartahun Berturutan (Consecutive Changes) pada Subsampel Validasi Deret Waktu 6 Tahun",
        source="Sumber: Hasil Kalkulasi Deret Waktu (consecutive_change_summary.csv) (2024)",
        col_widths=t_cons_widths
    )
    
    h3(doc, "Lampiran 3. Dokumentasi Teknis dan Panduan Pengoperasian Platform Streamlit Dashboard")
    body(
        doc,
        "Platform visualisasi interaktif dibangun menggunakan bahasa pemrograman Python 3.10 dengan dependensi pustaka "
        "Streamlit (v1.28+), Folium / Streamlit-Folium untuk pemetaan interaktif Leaflet, Plotly Graph Objects untuk grafik dinamis, "
        "serta GeoPandas dan Rasterio untuk manipulasi data spasial. Platform dapat diakses secara lokal maupun disebarkan ke peladen "
        "cloud dengan menjalankan perintah 'streamlit run dashboard/app.py'. Seluruh artefak model (*.pkl), data prediksi (*.csv), "
        "dan layer peta tematik terhubung secara modular di bawah arsitektur sistem berbasis cache berkecepatan tinggi."
    )
