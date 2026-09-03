# 📋 PANDUAN ONBOARDING ANGGOTA 5
# Peran: Penulis BAB IV — Hasil & Pembahasan (Core Results)

---

## 🎯 Tujuan Dokumen Ini
Tugasmu adalah mendeskripsikan dan menginterpretasikan TEMUAN NYATA dari proyek. Kamu harus bisa menjawab: "Apa yang kita temukan? Apa artinya?"

BAB IV adalah inti dari laporan. Kalau bagian ini lemah, semua kerja keras di pipeline sia-sia. Kamu WAJIB memahami angka-angka berikut sebelum menulis.

---

## 📚 STEP 1: Baca file-file ini

1. **`reports/audit_teknis_final.md`** — Ini adalah sumber utamamu. Baca Bab 1.1 s.d. 1.5 dengan sangat cermat.
2. **`results/change_maps/transition_matrix_2018_2024.csv`** — Buka di Excel, amati angka-angkanya
3. **`dashboard/data/temporal_composition.csv`** — Tren proporsi kelas per tahun
4. **`dashboard/data/driver_deforestation.csv`** — Hasil regresi logistik

---

## 🔍 STEP 2: Audit Mandiri — Uji Pemahaman Angka

Tanpa melihat catatan, isi tabel ini dari memori:

| Pertanyaan | Jawabanmu | Jawaban Benar |
|---|---|---|
| Overall Accuracy LGBM | ? | 83.32% |
| Kappa LGBM | ? | 0.7795 |
| Total titik observasi matched | ? | 9,624 |
| % titik yang berubah kelas | ? | 20.85% |
| Jumlah titik deforestasi (Forest Loss) | ? | 858 |
| Jumlah titik urbanisasi | ? | 159 |
| Jumlah titik ekspansi tambang | ? | 26 |
| Kelas dengan akurasi tertinggi | ? | Water (94.9%) |
| Kelas dengan akurasi terendah | ? | Shrubland (77.6%) |

Jika kurang dari 7 benar, baca ulang `audit_teknis_final.md` Bab 1.

---

## 🖥️ STEP 3: Eksplorasi Visual Mendalam

Buka dashboard Streamlit dan navigasi ke setiap halaman:

**Halaman 2_Change_Detection:**
- Amati grafik matriks transisi (warna merah = area berubah besar)
- Amati grafik temporal composition (tren 2018-2024)
- **Pertanyaan:** Di tahun berapa Built-up percentage paling tinggi? Mengapa?

**Halaman 4_Driver_Impact:**
- Amati tabel dan grafik signifikansi variabel
- **Pertanyaan:** Mana yang lebih berpengaruh terhadap deforestasi: IKN atau Tambang? (berdasarkan odds ratio)

---

## ✅ STEP 4: Checklist sebelum mulai nulis

- [ ] Saya hafal 9 angka kunci di tabel Step 2
- [ ] Saya sudah melihat semua gambar di `results/` dan tahu mana yang akan saya masukkan ke laporan
- [ ] Saya paham arti "Odds Ratio 1.108" untuk Mining Density (artinya: tiap 1 satuan peningkatan mining density, peluang deforestasi naik 10.8%)
- [ ] Saya bisa menjelaskan mengapa Built-up naik di 2023 dan mining naik di 2022-2023

---

## 📝 Kerangka yang harus kamu tulis (BAB IV Bagian 1-4):

```
BAB IV HASIL DAN PEMBAHASAN

4.1 Hasil Komparasi Model Klasifikasi
    - Tabel perbandingan 6 model (gunakan angka dari audit_teknis_final.md 1.1)
    - Justifikasi memilih LGBM (akurasi tertinggi, waktu tercepat)
    - Confusion matrix LGBM + interpretasi per kelas
    - Gambar: results/classification/confusion_matrices/cm_lgbm.png

4.2 Peta Tutupan Lahan Kalimantan 2018–2024
    - Deskripsikan tren dari tabel proporsi (audit_teknis_final.md 1.3)
    - Highlight: Built-up naik 2021-2023, Mining naik 2022-2023
    - Gambar: results/change_maps/temporal_trends.png

4.3 Deteksi Perubahan Tutupan Lahan 2018–2024
    - Matriks Transisi (angka dari audit_teknis_final.md 1.4)
    - Total 2,007 titik berubah (20.85%)
    - Pola dominan: Forest → Shrubland (791 titik) — degradasi hutan
    - Gambar: results/change_maps/transition_matrix_2018_2024.png

4.4 Analisis Deforestasi, Urbanisasi, dan Ekspansi Tambang
    4.4.1 Deforestasi: 858 titik, dari mana ke mana?
          (Forest → Shrubland 791, Forest → Built-up 56, dll)
    4.4.2 Urbanisasi: 159 titik
          (pola: Shrubland → Built-up 93 lebih besar dari Forest → Built-up 56)
          → urbanisasi lebih sering melalui degradasi bertahap
    4.4.3 Ekspansi Tambang: 26 titik (sampel kecil — ungkapkan sebagai limitasi)
```

**Gambar yang sudah siap dan WAJIB masuk:**
- `results/change_maps/transition_matrix_2018_2024.png`
- `results/change_maps/temporal_trends.png`
- `results/classification/confusion_matrices/cm_lgbm.png`
