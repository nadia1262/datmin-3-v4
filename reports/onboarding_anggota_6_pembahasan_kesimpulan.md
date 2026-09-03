# 📋 PANDUAN ONBOARDING ANGGOTA 6
# Peran: Penulis BAB IV (Pembahasan Lanjut: Driver & SHAP) + BAB V + Abstrak

---

## 🎯 Tujuan Dokumen Ini
Kamu memegang bagian TERPENTING secara intelektual: interpretasi hasil statistik, sintesis temuan, dan penarikan kesimpulan. Ini bagian yang paling ditanya dosen saat sidang.

---

## 📚 STEP 1: Baca file-file ini (WAJIB semua)

1. **`reports/audit_teknis_final.md`** — Baca Bab 1.5 (Driver Analysis) dan Bab IV (Narasi Sidang) dengan sangat cermat
2. **`dashboard/data/driver_deforestation.csv`** — Data regresi lengkap dengan P-Value dan Odds Ratio
3. **`dashboard/data/driver_urbanization.csv`** dan **`driver_mining.csv`**
4. **`results/shap/lgbm/shap_importance.csv`** — Ranking fitur berdasarkan SHAP
5. **`00_justifikasi/reviewer_defense.md`** — Persiapan argumen untuk menghadapi pertanyaan dosen/reviewer

---

## 🔍 STEP 2: Audit Mandiri — Uji Pemahaman Statistik

Ini adalah bagian paling kritis. Jawab pertanyaan berikut tanpa melihat catatan:

1. **Apa arti Odds Ratio 0.877 untuk variabel "jarak ke IKN" pada model deforestasi?**
   (Petunjuk: koefisiennya negatif, ORnya < 1, artinya jika jarak ke IKN...)

2. **Apa arti Odds Ratio 1.108 untuk "kepadatan tambang"?**
   (Petunjuk: ORnya > 1, artinya setiap kenaikan 1 unit mining density...)

3. **Mengapa P-Value "jarak ke IKN" = 0.272 untuk model urbanisasi, sedangkan untuk deforestasi = 0.0015?**
   (Ini adalah TEMUAN PALING MENARIK — apa implikasinya?)

4. **Apa arti Pseudo R² = 0.0056 yang sangat rendah?** (Apakah ini berarti model kita buruk?)

5. **Apa itu SHAP value?** Jika NDVI memiliki SHAP value negatif (-0.5) untuk satu piksel, apa artinya?

6. **Dalam konteks penelitian kita, apa perbedaan antara "deforestasi karena IKN" dengan "deforestasi karena tambang"?** (secara spasial, di mana pola masing-masing?)

---

## 🖥️ STEP 3: Eksplorasi Output Statistik Langsung

Jalankan ini di terminal untuk melihat angka aslinya:

```bash
python -c "
import pandas as pd
for lbl, f in [('DEFORESTASI','driver_deforestation'), ('URBANISASI','driver_urbanization'), ('TAMBANG','driver_mining')]:
    df = pd.read_csv(f'dashboard/data/{f}.csv')
    print(f'\n=== {lbl} ===')
    print(df[['variable','coefficient','p_value','odds_ratio','significant']].to_string(index=False))
"
```

Buka juga `results/shap/lgbm/shap_summary.png` untuk memahami urutan kepentingan fitur.

---

## ✅ STEP 4: Checklist sebelum mulai nulis

- [ ] Saya bisa menjelaskan arti Odds Ratio < 1 vs > 1 dengan contoh konkret
- [ ] Saya paham mengapa IKN tidak signifikan untuk urbanisasi dan bisa membuat narasi logis
- [ ] Saya tahu 3 fitur paling penting menurut SHAP dan mengapa itu masuk akal secara ilmiah
- [ ] Saya bisa merumuskan 3 kesimpulan yang menjawab 3 rumusan masalah

---

## 📝 Kerangka yang harus kamu tulis:

```
BAB IV (Lanjutan)

4.5 Analisis Faktor Pendorong (Dual-Driver): IKN vs Pertambangan
    4.5.1 Pendorong Deforestasi
          - Tabel koefisien, P-Value, Odds Ratio
          - distance_to_ikn: negatif signifikan → semakin dekat IKN, semakin tinggi risiko
          - mining_density: positif signifikan → tambang makin padat, hutan makin terancam
          - Gambar: results/driver_analysis/driver_effects.png

    4.5.2 Pendorong Urbanisasi
          - IKN TIDAK SIGNIFIKAN (p=0.272) — analisis dan narasi mengapa
          - mining_density signifikan (p=0.033)
          - Interpretasi: urbanisasi terdorong oleh aktivitas tambang, bukan langsung oleh IKN

    4.5.3 Pendorong Ekspansi Tambang
          - distance_to_ikn POSITIF signifikan → tambang cenderung JAUH dari IKN
          - mining_density signifikan → clustering spatial tambang
          - Interpretasi: pola segregasi spasial (IKN di tengah, tambang di pinggir)

4.6 SHAP Feature Importance
    - Interpretasi global: fitur apa yang paling menentukan klasifikasi?
    - Interpretasi kelas: fitur apa yang paling penting untuk deteksi hutan? tambang?
    - Gambar: results/shap/lgbm/shap_summary.png

4.7 Sintesis dan Diskusi
    - Pola dominan: deforestasi ke semak (degradasi bertahap) > deforestasi ke bangunan
    - Urbanisasi bertahap: hutan → semak → kota (multi-step conversion)
    - Keterbatasan: ukuran sampel 2018, pseudo R² rendah, cakupan grid
    - Perbandingan dengan penelitian terdahulu

---

BAB V PENUTUP

5.1 Kesimpulan
    1. [Jawab RQ1: Performa model] LightGBM mencapai akurasi 83.32%...
    2. [Jawab RQ2: Tren perubahan] Terdeteksi 2,007 titik (20.85%) berubah...
    3. [Jawab RQ3: Driver] IKN signifikan terhadap deforestasi (p<0.01)...

5.2 Keterbatasan Penelitian
    - Grid 2018 lebih kecil (13K vs 155K titik)
    - Pseudo R² rendah: variabel driver lain tidak tercover (jarak ke jalan, populasi)
    - Skala citra 500m: perubahan kecil < 500m tidak terdeteksi

5.3 Saran
    - Gunakan Planet Labs (resolusi 3m) untuk analisis skala lebih detail
    - Tambahkan variabel driver: jarak ke jalan, density populasi
    - Ulangi analisis setelah 2026 ketika IKN sudah lebih matang

---

ABSTRAK (Bahasa Indonesia + Inggris, masing-masing 200-250 kata, format IMRaD)
```

**Narasi kunci untuk Bab 4.5 (anti-salah tafsir):**
> "Temuan bahwa IKN tidak berpengaruh signifikan terhadap urbanisasi BUKAN berarti IKN tidak berdampak, melainkan bahwa efek spill-over IKN belum sepenuhnya terwujud dalam rentang 2018–2024 mengingat konstruksi besar-besaran baru dimulai 2022."
