# Slide 6 — Akurasi Per Kelas dan Fenomena Spectral Confusion

## Poin utama
Model (LightGBM) akurat tinggi buat kelas Water, tapi kesulitan bedain Forest vs Shrubland/Agriculture akibat spectral confusion pada lanskap vegetasi tropis.

## Isi

**IoU per kelas** (urut terbaik → terendah):

| Kelas | IoU | Proporsi Sampel (Grid 2019) |
|---|---|---|
| Water | 0,9037 | - |
| Forest | 0,7388 | - |
| Built-up | 0,7016 | - |
| Bare/Mining-like | 0,6405 | 0,40% |
| Shrubland/Agriculture | 0,6274 | 19,75% |

- Kelas IoU terendah **bukan** kelas dengan sampel tersedikit. Bare/Mining-like cuma 0,40% sampel tapi bukan yang terendah. Shrubland/Agriculture (19,75% sampel, jauh lebih besar) justru IoU-nya paling rendah → penyebabnya **spectral confusion**, bukan class imbalance.
- Confusion matrix (LightGBM, model utama): 1.395 piksel Forest salah diklasifikasi jadi Shrubland/Agriculture, 1.198 piksel sebaliknya — pasangan kesalahan terbesar dibanding pasangan kelas lain manapun.
- Root cause: ambang NDVI tumpang tindih antara hutan sekunder dan semak belukar, ciri khas lanskap vegetasi tropis heterogen (Lu & Weng, 2007; Gómez et al., 2016).

## Catatan kecil (footnote, font kecil)
> IoU (Intersection over Union) = TP / (TP + FP + FN) — proporsi overlap prediksi vs ground truth. Lebih ketat dari akurasi biasa karena menghukum juga piksel salah tebak (FP) dan piksel kelewat (FN). Skala 0–1, makin tinggi makin cocok.

## Visualisasi singkat
Gak perlu chart tambahan. Tabel di atas udah sorted (tertinggi→terendah) dan poinnya perbandingan 2 kolom (IoU vs Proporsi Sampel) — chart cuma nambah elemen tanpa nambah info. Highlight/bold baris Shrubland/Agriculture biar mata langsung fokus ke situ.

Visual utama slide: cuplikan confusion matrix `results/classification/confusion_matrices/cm_lgbm.png`, di-highlight sel Forest↔Shrubland/Agriculture.

---

# Slide 7 — Interpretasi Model: Feature Importance & SHAP

## Poin utama
NDVI dominan mutlak menentukan klasifikasi; indeks turunan SWIR (B11/B12/NDBI) berperan sekunder memisahkan area non-vegetasi.

## Isi

**Top 5 fitur (Rata-rata |SHAP|):**

| Fitur | Rata-rata \|SHAP\| |
|---|---|
| NDVI | 0,938 |
| B12 | 0,470 |
| B11 | 0,443 |
| B3 | 0,217 |
| NDBI | 0,178 |

- NDVI tinggi (SHAP beeswarm, warna merah) konsisten mendorong prediksi ke arah kelas Forest — pemisah utama vegetasi vs non-vegetasi.
- Pasangan B11–B12 (sensitif kelembapan tanah dan kandungan mineral) dominan memisahkan Built-up vs Bare/Mining-like.
- **Catatan teknis penting:** NDBI dan NDMI multikolinieritas sempurna (NDMI ≈ −NDBI). Skor SHAP NDMI kecil (0,046) bukan berarti gak penting — sinyalnya sama, tapi algoritma pohon random pilih salah satu representasi tiap simpul pemisah, jadi kontribusinya "terpecah". NDBI+NDMI harus dibaca sebagai satu indeks gabungan, bukan dibandingkan terpisah sebagai fitur independen.

## Visualisasi singkat
Gak perlu chart tambahan. Tabel di atas udah sorted (tertinggi→terendah), 5 angka doang, chart cuma nambah elemen tanpa nambah info.

Visual utama slide: `results/shap/lgbm/shap_summary.png` (beeswarm plot asli) — ini yang emang standar buat interpretasi SHAP, karena nunjukin distribusi tiap sample per fitur (bukan cuma rata-rata kayak tabel).
