# 📋 PANDUAN ONBOARDING ANGGOTA 3
# Peran: Penulis BAB III — Bagian Data & Google Earth Engine (GEE)

---

## 🎯 Tujuan Dokumen Ini
Tugasmu adalah menjelaskan DARI MANA data kita berasal dan BAGAIMANA cara mengolahnya di GEE. Kamu harus paham alur dari "piksel satelit mentah" hingga menjadi "file CSV siap training".

---

## 📚 STEP 1: Baca file-file ini dulu

1. **`gee_scripts/00_utils.js`** — Fungsi preprocessing utama (cloud masking, band scaling). Baca dan pahami tiap baris.
2. **`gee_scripts/01_sentinel2_composite.js`** — Cara membuat komposit tahunan
3. **`gee_scripts/07_stratified_sampling.js`** — Cara mengambil 30.000 sampel secara stratified
4. **`gee_scripts/09_prediction_grid.js`** — Cara membuat grid prediksi 300.000 titik
5. **`preprocessing/01_validate_samples.py`** — Jalankan untuk lihat statistik data training

---

## 🔍 STEP 2: Audit Mandiri — Uji Pemahaman Data Pipeline

1. **Dari mana label/ground truth kelas tutupan lahan kita berasal?** (Hint: bukan kita yang manual labeling)
2. **Apa itu "cloud masking" dan mengapa wajib dilakukan sebelum analisis?** (Hint: awan menutupi permukaan bumi di citra satelit)
3. **Mengapa kita menggunakan "median composite" dan bukan satu citra tunggal per tahun?**
4. **Berapa jumlah sampel training kita dan bagaimana proporsionalitasnya antar kelas?** (Buka `data/samples/training_samples_2021.csv` dan cek distribusi kolom `land_cover_class`)
5. **Apa itu "Spatial Block Cross-Validation" dan mengapa lebih baik dari random split untuk data spasial?** (Hint: masalah spatial autocorrelation)
6. **Mengapa kita mengekspor 300,000 titik per tahun untuk grid prediksi, bukan menggunakan sampling yang sama dengan training?**

---

## 🖥️ STEP 3: Eksplorasi Data Langsung

Buka terminal VSCode dan jalankan:
```bash
python preprocessing/01_validate_samples.py
```
Amati output-nya. Catat:
- Berapa jumlah titik per kelas?
- Apakah distribusinya seimbang atau tidak?
- Apa konsekuensi ketidakseimbangan ini terhadap model?

---

## ✅ STEP 4: Checklist sebelum mulai nulis

- [ ] Saya bisa menjelaskan alur: GEE Export → Training Samples → Data CSV
- [ ] Saya tahu apa itu cloud masking dan median composite
- [ ] Saya sudah menjalankan validate_samples.py dan melihat distribusi kelas
- [ ] Saya paham perbedaan `training_samples_2021.csv` vs `prediction_grid_2024.csv`

---

## 📝 Kerangka yang harus kamu tulis (setengah dari BAB III):

```
BAB III METODOLOGI
3.1 Desain Penelitian
    - Kerangka CRISP-DM (lihat: 00_justifikasi/crisp_dm_analysis.md)
    - Flowchart alur penelitian (kamu yang buat gambar/diagramnya!)

3.2 Data Penelitian
    3.2.1 Citra Sentinel-2 (sumber: ESA Copernicus via GEE)
          - Periode: 2018–2024 (7 tahun)
          - Band yang digunakan: B2, B3, B4, B8, B11, B12
          - Resolusi spasial: 10 meter
    3.2.2 Label Ground Truth: ESA WorldCover 2021
          - Definisi 5 kelas (Forest, Shrubland, Built-up, Bare, Water)
    3.2.3 Data Pendukung/Driver
          - Elevasi: SRTM (NASA, resolusi 30m)
          - Curah Hujan: CHIRPS (resolusi 5km, bulanan)
          - Jarak ke IKN: dihitung dari koordinat pusat IKN
          - Kepadatan Tambang: dihitung dalam radius 10km

3.3 Preprocessing di Google Earth Engine
    3.3.1 Cloud Masking (fungsi maskS2clouds di 00_utils.js)
    3.3.2 Median Annual Composite (mengapa median, bukan mean)
    3.3.3 Perhitungan Indeks Spektral (NDVI, NDBI, NDMI, BSI)

3.4 Pengambilan Sampel Training
    3.4.1 Stratified Sampling (30,000 titik, proporsional per kelas)
    3.4.2 Spatial Block Cross-Validation (8 blok spasial)
    3.4.3 Pemisahan Train-Test (70:30 berdasarkan blok)

3.5 Grid Prediksi (untuk pemetaan seluruh Kalimantan)
    - 300,000 titik per tahun (systematic sampling)
    - Parameter: scale=500m, tileScale=8, dropNulls=True
```
