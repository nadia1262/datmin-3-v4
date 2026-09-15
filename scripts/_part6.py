
h4(doc, 'Analisis Asosiasi Spasial: Regresi Logistik Multivariat')
body(doc, 'Regresi logistik multivariat diaplikasikan pada 118.943 titik Common Spatial Domain terhadap tiga variabel transisi lahan. Hasil disajikan pada Tabel 8.')
tcap(doc, 'Tabel 8. Hasil Regresi Logistik Multivariat - Tiga Model Transisi Lahan')

def fmtor(df, var):
    r = df[df['variable']==var].iloc[0]
    o = r['odds_ratio']
    pv = r['p_value']
    if pv < 0.001: ps = 'p<0,001'
    else: ps = f'p={pv:.3f}'
    st = '***' if pv<0.001 else ('**' if pv<0.01 else ('*' if pv<0.05 else 'ns'))
    return f'{o:.3f} ({ps}) {st}'

t8r = []
for v in ['distance_to_ikn', 'mining_density_10km', 'elevation', 'rainfall_annual']:
    vl = {'distance_to_ikn': 'Jarak ke IKN', 'mining_density_10km': 'Kep. Tambang 10km',
          'elevation': 'Elevasi', 'rainfall_annual': 'Curah Hujan'}[v]
    t8r.append([vl, fmtor(ld, v), fmtor(lu, v), fmtor(lm, v)])
mktable(doc, ['Variabel', 'Deforestasi OR', 'Urbanisasi OR', 'Eks. Tambang OR'], t8r)
note(doc, 'Keterangan: *** p<0,001; ** p<0,01; * p<0,05; ns = tidak signifikan.')

body(doc, 'Variabel mining_density_10km menunjukkan konsistensi tertinggi: kepadatan pertambangan dalam radius 10 km berasosiasi positif dan signifikan pada ketiga model, mengindikasikan efek cascading dari aktivitas tambang [7].')
body(doc, 'Pada model Deforestasi, koefisien jarak ke IKN bertanda positif dan signifikan (OR = 1,108; p < 0,001). Semakin jauh suatu titik dari pusat IKN, semakin tinggi peluang deforestasi. Pola ini selaras dengan konsep telecoupling [5]: kawasan inti IKN dilindungi oleh zonasi hijau perkotaan, sehingga tekanan deforestasi bergeser ke zona penyangga luar yang menyediakan kayu, material galian, dan pangan bagi proyek pembangunan.')
body(doc, 'Pola berlawanan muncul pada model Ekspansi Tambang: semakin dekat dengan IKN, semakin tinggi peluang ekspansi tambang (OR = 0,784; p < 0,001), mengindikasikan permintaan material konstruksi di sekitar IKN. Pada model Urbanisasi, jarak ke IKN tidak signifikan (p = 0,159).')
body(doc, 'Elevasi dan curah hujan konsisten berasosiasi negatif dan signifikan pada ketiga model (OR elevasi: 0,46-0,77; OR curah hujan: 0,73-0,91). Lahan rendah dan kering secara praktis lebih mudah dikonversi untuk permukiman, jalur akses, maupun aktivitas tambang.')

addimg(doc, os.path.join(DRIVERDIR, 'driver_effects.png'), Cm(14))
fcap(doc, 'Gambar 4. Efek Marginal Jarak IKN dan Kepadatan Tambang terhadap Deforestasi')

h4(doc, 'Keterbatasan Penelitian')
body(doc, 'Pertama, perbedaan resolusi (resolution mismatch) antara skala pelatihan (10 m) dan prediksi makro (500 m) menimbulkan domain shift yang teramati pada fenomena net forest gain akibat mixed-pixel [34].')
body(doc, 'Kedua, multikolinearitas sempurna NDMI-NDBI (r = -1,0) tidak memengaruhi akurasi tree-based, namun menyebabkan kepentingan SHAP terpecah antara dua indeks identik.')
body(doc, 'Ketiga, ukuran sampel besar (N = 118.943) menyebabkan standard error regresi sangat kecil, sehingga hampir semua variabel signifikan meskipun efek absolutnya tipis. Pseudo R-squared relatif kecil, menunjukkan faktor di luar model masih dominan.')
body(doc, 'Keempat, label ESA WorldCover 2021 sebagai ground truth tunggal mengandalkan asumsi temporal transferability karakteristik spektral selama enam tahun pengamatan.')

# KESIMPULAN
h2(doc, 'KESIMPULAN')
body(doc, 'Penelitian ini menunjukkan bahwa citra Sentinel-2 dan pendekatan machine learning dapat memetakan serta menganalisis transformasi tutupan lahan di Pulau Kalimantan selama periode 2019-2024. Dari enam algoritma yang dievaluasi, LightGBM dipilih sebagai model operasional (OA 83,32%, F1-Macro 83,47%, Kappa 0,7795) karena menawarkan trade-off terbaik antara akurasi dan efisiensi komputasi.')
body(doc, 'Analisis SHAP mengonfirmasi NDVI sebagai fitur paling dominan (mean |SHAP| = 0,938), diikuti band SWIR (B12, B11). Temuan ini konsisten dengan prinsip fisika optik vegetasi tropis dan memvalidasi bahwa keputusan algoritmik model sejalan dengan hukum penginderaan jauh.')
body(doc, 'Deteksi perubahan pada 118.943 titik Common Spatial Domain berhasil mengidentifikasi berbagai transisi antarkelas. Metode Majority Voting pada resolusi 500 m meningkatkan cakupan menjadi 1.499.024 sel (12 kali lipat). Namun, fenomena net forest gain mengindikasikan efek mixed-pixel pada resolusi agregasi yang perlu diinterpretasikan hati-hati.')
body(doc, 'Regresi logistik menunjukkan kepadatan pertambangan dalam radius 10 km berasosiasi positif dan signifikan dengan ketiga transisi lahan. Jarak terhadap IKN menunjukkan pola telecoupling: deforestasi lebih tinggi di wilayah jauh dari IKN (OR = 1,108), sementara ekspansi tambang meningkat di sekitar IKN (OR = 0,784). Pola ini menunjukkan dampak pembangunan IKN bersifat spasial tidak langsung dan memerlukan pemantauan berkelanjutan.')

# DAFTAR PUSTAKA
h2(doc, 'DAFTAR PUSTAKA')
refs = [
    '[1] A. Di Gregorio and L. J. M. Jansen, Land Cover Classification System (LCCS): Classification Concepts and User Manual, 2nd ed. Rome, Italy: FAO, 2005.',
    '[2] E. F. Lambin et al., "The causes of land-use and land-cover change: Moving beyond the myths," Global Environmental Change, vol. 11, no. 4, pp. 261-269, 2001.',
    '[3] Republik Indonesia, Undang-Undang Nomor 3 Tahun 2022 tentang Ibu Kota Negara. Lembaran Negara RI Tahun 2022.',
    '[4] W. F. Laurance et al., "A global strategy for road building," Nature, vol. 513, pp. 229-232, 2014.',
    '[5] P. Meyfroidt, E. F. Lambin, K.-H. Erb, and T. W. Hertel, "Globalization of land use: Distant drivers of land change and geographic displacement of land use," Current Opinion in Environmental Sustainability, vol. 5, no. 5, pp. 438-444, 2014.',
    '[6] E. F. Lambin and P. Meyfroidt, "Land use transitions: Socio-ecological feedback versus socio-economic change," Land Use Policy, vol. 27, no. 2, pp. 108-118, 2010.',
    '[7] H. Werner et al., "Patterns of infringement, risk, and impact driven by coal mining permits in Indonesia," Ambio, 2023.',
    '[8] Z. Zhu, S. Qiu, and S. Ye, "Remote sensing of land change: A multifaceted perspective," Remote Sensing of Environment, vol. 282, Art. no. 113266, 2022.',
    '[9] D. Phiri et al., "Sentinel-2 data for land cover/use mapping: A review," Remote Sensing, vol. 12, no. 14, Art. no. 2291, 2020.',
    '[10] S. Talukdar et al., "Land-use land-cover classification by machine learning classifiers for satellite observations - A review," Remote Sensing, vol. 12, no. 7, Art. no. 1135, 2020.',
    '[11] K. Karra et al., "Global land use/land cover mapping using Sentinel-2 data," 2021 IEEE IGARSS, pp. 4704-4707, 2021.',
    '[12] M. Hussain et al., "Change detection from remotely sensed images: From pixel-based to object-based approaches," ISPRS J. Photogrammetry and Remote Sensing, vol. 80, pp. 91-106, 2013.',
    '[13] Z. Zhu, C. E. Woodcock, M. Olofsson et al., "Transitioning from change detection to monitoring with remote sensing," Remote Sensing of Environment, 2019.',
    '[14] D. Zanaga et al., ESA WorldCover 10 m 2021 v200. Zenodo, 2022, doi: 10.5281/zenodo.7254220.',
    '[15] T. G. Farr et al., "The Shuttle Radar Topography Mission," Reviews of Geophysics, vol. 45, no. 2, 2007.',
    '[16] C. Funk et al., "The climate hazards infrared precipitation with stations - a new environmental record for monitoring extremes," Scientific Data, vol. 2, Art. no. 150066, 2015.',
    '[17] V. Maus et al., "An update on global mining land use," Scientific Data, vol. 9, Art. no. 433, 2022.',
    '[18] N. Gorelick et al., "Google Earth Engine: Planetary-scale geospatial analysis for everyone," Remote Sensing of Environment, vol. 202, pp. 18-27, 2017.',
    '[19] J. W. Rouse et al., "Monitoring vegetation systems in the Great Plains with ERTS," in Third ERTS Symposium, NASA SP-351, pp. 309-317, 1974.',
    '[20] Y. Zha, J. Gao, and S. Ni, "Use of normalized difference built-up index in automatically mapping urban areas from TM imagery," International J. Remote Sensing, vol. 24, no. 3, pp. 583-594, 2003.',
    '[21] B.-C. Gao, "NDWI - A normalized difference water index for remote sensing of vegetation liquid water from space," Remote Sensing of Environment, vol. 58, no. 3, pp. 257-266, 1996.',
    '[22] A. Rikimaru, P. S. Roy, and S. Miyatake, "Tropical forest cover density mapping," Tropical Ecology, vol. 43, no. 1, pp. 39-47, 2002.',
    '[23] D. R. Roberts et al., "Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure," Ecography, vol. 40, no. 8, pp. 913-929, 2017.',
    '[24] P. Ploton et al., "Spatial validation reveals poor predictive performance of large-scale ecological mapping models," Nature Communications, vol. 11, Art. no. 4540, 2020.',
    '[25] L. Breiman, "Random forests," Machine Learning, vol. 45, no. 1, pp. 5-32, 2001.',
    '[26] C. Cortes and V. Vapnik, "Support-vector networks," Machine Learning, vol. 20, no. 3, pp. 273-297, 1995.',
    '[27] T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," Proc. 22nd ACM SIGKDD, pp. 785-794, 2016.',
    '[28] G. Ke et al., "LightGBM: A highly efficient gradient boosting decision tree," Advances in Neural Information Processing Systems, vol. 30, 2017.',
    '[29] M. Sokolova and G. Lapalme, "A systematic analysis of performance measures for classification tasks," Information Processing and Management, vol. 45, no. 4, pp. 427-437, 2009.',
    '[30] J. Cohen, "A coefficient of agreement for nominal scales," Educational and Psychological Measurement, vol. 20, no. 1, pp. 37-46, 1960.',
    '[31] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," Advances in Neural Information Processing Systems, vol. 30, 2017.',
    '[32] Z. Zhu et al., "Remote sensing of land change: A multifaceted perspective," Remote Sensing of Environment, vol. 282, 2022.',
    '[33] D. Lu and Q. Weng, "A survey of image classification methods and techniques for improving classification performance," International J. Remote Sensing, vol. 28, no. 5, pp. 823-870, 2007.',
    '[34] D. Tuia, C. Persello, and L. Bruzzone, "Domain adaptation for the classification of remote sensing data," IEEE Geoscience and Remote Sensing Magazine, vol. 4, no. 2, pp. 41-57, 2016.',
    '[35] F. Pedregosa et al., "Scikit-learn: Machine learning in Python," Journal of Machine Learning Research, vol. 12, pp. 2825-2830, 2011.',
]
for r_text in refs:
    mkref(doc, r_text)

# SAVE
print(f'Saving to {OUTPUT}...')
doc.save(OUTPUT)
print(f'[SUCCESS] Report saved!')
print(f'File size: {os.path.getsize(OUTPUT):,} bytes')
