# 🗡️ REVIEWER ATTACK — 20 Pertanyaan Paling Berbahaya

---

## METODOLOGI & DATA

### Q1: "Kenapa NDBI dan NDMI kalian masukkan dua-duanya? Bukannya itu variabel yang sama?"
**Kenapa berbahaya:** NDBI = -NDMI secara matematis. Korelasi = -1.0. Memasukkan keduanya menunjukkan kurangnya pemahaman tentang fitur yang digunakan.
**Kemampuan jawab saat ini:** ❌ LEMAH — tidak pernah dibahas di dokumentasi
**Bukti:** `corr(NDBI, NDMI) = -1.000`
**Yang harus disiapkan:** Akui kesalahan, tunjukkan bahwa SHAP membuktikan NDMI tidak berkontribusi (0.046), dan tree-based models otomatis mengabaikan redundansi. Idealnya, jalankan ablation study.

### Q2: "Training data kalian resolusi 10m tapi prediksi di resolusi 500m. Apakah modelnya valid?"
**Kenapa berbahaya:** Domain shift jelas — pixel 500m adalah agregasi dari 2,500 pixel 10m. Distribusi berbeda.
**Kemampuan jawab saat ini:** ⚠️ SEDANG — disebutkan tapi tidak dianalisis
**Bukti:** GEE script 07 (scale=10) vs 09 (PREDICTION_SCALE=500)
**Yang harus disiapkan:** Tunjukkan temporal drift analysis yang menunjukkan distribusi fitur relatif stabil. Argumen: median composite pada 500m tetap mempertahankan sinyal spektral dominan.

### Q3: "Grid 2018 kalian cuma 13 ribu titik, yang lain 155 ribu. Kenapa begitu? Bagaimana ini mempengaruhi hasil?"
**Kenapa berbahaya:** Ini kelemahan fundamental yang mempengaruhi seluruh change detection.
**Kemampuan jawab saat ini:** ⚠️ SEBAGIAN — disebutkan sebagai catatan tapi tidak dianalisis dampaknya
**Bukti:** `prediction_grid_2018.csv`: 13,632 rows vs 2019: 175,384
**Yang harus disiapkan:** Jelaskan bahwa Sentinel-2B baru beroperasi penuh 2018 → cakupan cloud-free lebih terbatas. Tambahkan analisis alternatif 2019→2024.

### Q4: "Scaler StandardScaler kalian fit sebelum cross-validation. Apakah ada data leakage?"
**Kenapa berbahaya:** Ini pertanyaan teknis standar. Scaler fit pada test data = leakage.
**Kemampuan jawab saat ini:** ❌ LEMAH — code memang leaky
**Bukti:** `train_classification.py` line 112: `X = scaler.fit_transform(X)` sebelum CV loop
**Yang harus disiapkan:** Akui, jelaskan bahwa efeknya minimal (<1% pada LogReg/SVM/MLP), dan model utama (LGBM, RF, XGB) tidak menggunakan scaler sama sekali.

---

## MODEL & EVALUASI

### Q5: "Kenapa LightGBM terpilih dan bukan SVM yang F1-macro-nya lebih tinggi (0.8371 vs 0.8347)?"
**Kenapa berbahaya:** SVM sebenarnya punya F1-macro tertinggi (0.8371)! Audit teknis bilang LGBM terbaik tapi itu untuk OA, bukan F1.
**Kemampuan jawab saat ini:** ⚠️ SEDANG — klaim perlu diperhalus
**Bukti:** summary_svm.json: f1_macro=0.8371 > lgbm: 0.8347
**Yang harus disiapkan:** Justifikasi: LGBM terbaik secara OA (0.8332) dan efisiensi (116s vs 14,343s). SVM disubsample ke 10K, jadi komparisonnya tidak 100% fair. F1-macro perbedaannya <0.003.

### Q6: "SVM dilatih pada 10.000 sampel tapi model finalnya pada 30.000. Ini valid?"
**Kenapa berbahaya:** CV metrics dihitung pada subset 10K tapi model deployed dilatih pada 30K. Metrics tidak merepresentasikan model final.
**Kemampuan jawab saat ini:** ❌ LEMAH — inkonsistensi nyata
**Bukti:** `train_classification.py` line 115-120 (subsample) vs 181 (full data)
**Yang harus disiapkan:** Akui sebagai trade-off komputasi. Argumen: final model pada data lebih banyak → umumnya lebih baik, jadi CV metrics bisa dianggap lower bound.

### Q7: "Kappa 0.78 itu termasuk kategori apa? Apakah cukup?"
**Kenapa berbahaya:** 0.78 masuk "substantial agreement" (0.61-0.80), bukan "almost perfect" (>0.81).
**Kemampuan jawab saat ini:** ✅ BAIK — ada di audit teknis
**Yang harus disiapkan:** Kontekstualisasi: untuk 5 kelas di area heterogen seluas Kalimantan, kappa 0.78 sangat kompetitif. Literatur sejenis umumnya 0.70-0.85.

### Q8: "Kalian pakai Spatial Block CV, tapi apakah 0.5° itu cukup untuk menghindari spatial autocorrelation?"
**Kenapa berbahaya:** Jika block size terlalu kecil, titik yang berdekatan bisa masuk ke fold berbeda → spatial leakage.
**Kemampuan jawab saat ini:** ⚠️ SEDANG — 0.5° = ~55 km, cukup besar untuk Sentinel-2
**Yang harus disiapkan:** Argumentasi: 0.5° = ~55 km at equator, jauh melampaui typical spatial autocorrelation range untuk data Sentinel-2 10m. Referensi: Ploton et al. (2020) merekomendasikan block size ≥2× autocorrelation range.

---

## CHANGE DETECTION & TEMPORAL

### Q9: "Dari matriks transisi, forest gain (889) lebih banyak dari forest loss (858). Jadi sebenarnya hutan bertambah?"
**Kenapa berbahaya:** Ini kontradiksi dengan narratif deforestasi.
**Kemampuan jawab saat ini:** ❌ LEMAH — tidak pernah dibahas
**Yang harus disiapkan:** Analisis: forest gain mungkin dari shrubland yang terprediksi forest di 2024 — bisa karena resolusi 500m membuat boundary ambigous, atau vegetasi recovery alami. Perlu cross-check dengan spectral values.

### Q10: "Kalian mengklaim deforestasi, tapi model prediksi sama dipakai untuk 2018 dan 2024. Apakah 'perubahan' itu nyata atau cuma model noise?"
**Kenapa berbahaya:** Ini pertanyaan fundamental. Model dilatih pada 2021, lalu diterapkan ke tahun lain. "Perubahan" bisa jadi variasi prediksi model, bukan perubahan tutupan lahan nyata.
**Kemampuan jawab saat ini:** ⚠️ SEDANG — temporal drift check ada tapi tidak mendalam
**Yang harus disiapkan:** Tunjukkan temporal consistency check. Argumen: model merespons sinyal spektral riil — jika NDVI berubah, prediksi berubah. Ini bukan noise random tapi refleksi dari perubahan fisik surface.

### Q11: "Kenapa tidak menggunakan ESA WorldCover 2018 dan 2024 untuk validasi temporal?"
**Kenapa berbahaya:** WorldCover v100 (2020) dan v200 (2021) tersedia. Kalau ada ground truth multi-tahun, harusnya dipakai.
**Kemampuan jawab saat ini:** ⚠️ SEDANG
**Yang harus disiapkan:** WorldCover hanya tersedia untuk 2020 dan 2021 (bukan 2018 atau 2024). Tidak ada ground truth temporal yang tersedia secara gratis untuk semua 7 tahun. Ini justifikasi menggunakan temporal transfer.

---

## DRIVER ANALYSIS & STATISTIK

### Q12: "Pseudo R² cuma 0.005. Model driver kalian sebenarnya tidak menjelaskan apa-apa kan?"
**Kenapa berbahaya:** Secara literal benar — 99.5% variasi tidak dijelaskan.
**Kemampuan jawab saat ini:** ✅ BAIK — ada defense di reviewer_defense.md
**Yang harus disiapkan:** (1) Pseudo R² bukan R² OLS, interpretasinya berbeda. (2) Pada data piksel-level (ribuan observasi), variasi individu sangat tinggi. (3) Yang penting: signifikansi dan arah koefisien, bukan magnitude R². (4) Referensi literatur sejenis.

### Q13: "Mining density kalian dihitung dari WorldCover 2021. Tapi kalian analisis perubahan 2018-2024. Apakah itu valid?"
**Kenapa berbahaya:** Driver variable seharusnya bervariasi temporal untuk klaim kausal.
**Kemampuan jawab saat ini:** ❌ LEMAH — tidak dibahas di dokumentasi
**Yang harus disiapkan:** Akui ini sebagai proxy statis. Argumen: mining areas generally persist — area yang sudah tambang di 2021 kemungkinan besar sudah tambang sebelumnya. Tapi ini tetap keterbatasan.

### Q14: "26 kasus mining expansion cukup untuk regresi logistik? Bukankah itu terlalu sedikit?"
**Kenapa berbahaya:** Statistikawan mana pun akan menolak ini. Rule of thumb: minimal 10 events per variable.
**Kemampuan jawab saat ini:** ❌ LEMAH
**Yang harus disiapkan:** Akui kekurangan sampel. Present sebagai "exploratory finding" bukan "conclusive evidence". Gunakan exact test atau Fisher's test sebagai alternatif.

### Q15: "Apakah ini kausalitas atau korelasi? Bisa nggak kalian bilang IKN 'menyebabkan' deforestasi?"
**Kenapa berbahaya:** Cross-sectional logistic regression TIDAK BISA membuktikan kausalitas.
**Kemampuan jawab saat ini:** ⚠️ SEDANG — audit menggunakan kata "signifikan" dan "mendukung hipotesis"
**Yang harus disiapkan:** Hati-hati dengan bahasa. Gunakan: "berasosiasi dengan", "berkorelasi spasial", "konsisten dengan hipotesis". JANGAN gunakan: "menyebabkan", "memicu".

---

## SHAP & INTERPRETABILITY

### Q16: "NDVI kontribusi SHAP-nya 0.94, runner-up cuma 0.47. Kenapa sangat dominan?"
**Kenapa berbahaya:** Jika NDVI sangat dominan, mengapa butuh 9 fitur lain?
**Kemampuan jawab saat ini:** ✅ BAIK
**Yang harus disiapkan:** NDVI adalah indeks vegetasi paling fundamental. Ia membedakan vegetated vs non-vegetated. Tapi 9 fitur lain dibutuhkan untuk membedakan ANTAR kelas non-vegetated (Built-up vs Bare vs Water) dan gradasi vegetasi (Forest vs Shrubland).

### Q17: "NDMI SHAP-nya 0.046 — praktis tidak berguna. Kenapa tetap dimasukkan?"
**Kenapa berbahaya:** Terkait Q1 — NDMI redundan dengan NDBI.
**Kemampuan jawab saat ini:** ❌ LEMAH
**Yang harus disiapkan:** Akui bahwa NDMI memang redundan karena -NDBI. Ini keterbatasan desain fitur yang harus diakui.

---

## DASHBOARD & PRESENTASI

### Q18: "Dashboard Change Detection menampilkan angka yang berbeda dari hasil analisis. Mana yang benar?"
**Kenapa berbahaya:** Dashboard menampilkan DUMMY DATA (14.2%, +2.5%, +1.8%) yang sepenuhnya fiktif.
**Kemampuan jawab saat ini:** 🔴 FATAL — ini harus diperbaiki sebelum demo
**Yang harus disiapkan:** FIX DASHBOARD SEKARANG.

### Q19: "Kenapa dashboard bilang XGBoost terbaik, tapi analisis kalian pilih LightGBM?"
**Kenapa berbahaya:** Inkonsistensi antar deliverable.
**Kemampuan jawab saat ini:** 🔴 FATAL — ada di dashboard page 3
**Yang harus disiapkan:** Fix info box di page 3.

### Q20: "5 kelas tutupan lahan — kenapa tidak 7 seperti ESA WorldCover aslinya? Apa justifikasinya?"
**Kenapa berbahaya:** Menggabungkan kelas (misal Wetland → Forest, Grassland → Shrubland) bisa menyembunyikan perubahan penting.
**Kemampuan jawab saat ini:** ⚠️ SEDANG
**Yang harus disiapkan:** (1) Di Kalimantan, beberapa kelas ESA sangat jarang (Snow/Ice, Moss/Lichen = <0.1%). (2) Penggabungan berdasarkan kesamaan spektral dan ekologis. (3) 5 kelas memberikan keseimbangan antara detail dan robustness klasifikasi.
