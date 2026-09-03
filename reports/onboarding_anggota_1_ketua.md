# 📋 PANDUAN ONBOARDING ANGGOTA 1
# Peran: Ketua & Penulis BAB I (Pendahuluan)

---

## 🎯 Tujuan Dokumen Ini
Sebelum kamu mulai menulis apapun, kamu WAJIB memahami seluruh proyek dari sudut pandang *big picture*. Sebagai Ketua, kamu harus bisa menjelaskan proyek ini kepada siapapun dalam 2 menit.

---

## 📚 STEP 1: Baca file-file ini dulu (urutan penting!)

1. **`README.md`** — Gambaran umum proyek (baca dari atas ke bawah, 10 menit)
2. **`reports/urgensi_penelitian.md`** — Draf latar belakang (ini langsung bisa jadi bahan Bab I)
3. **`00_justifikasi/latar_belakang_tujuan.md`** — Konteks dan tujuan lebih detail
4. **`reports/audit_teknis_final.md`** — Audit menyeluruh dengan angka-angka final proyek

---

## 🔍 STEP 2: Audit Mandiri (Jawab 6 pertanyaan ini)

Jawab pertanyaan di bawah ini secara tertulis di kertas/notes. Kalau tidak bisa menjawab, berarti ada bagian yang perlu dibaca ulang.

1. **Apa objek penelitian kita?** (apa yang sedang kita "lihat" dan ukur?)
2. **Apa dua pemicu utama perubahan lahan yang kita teliti?** (Hint: ada 2 "driver")
3. **Mengapa kita menggunakan citra satelit Sentinel-2 dan bukan foto udara biasa?**
4. **Apa bedanya penelitian kita dengan sekadar "melihat Google Maps dari tahun ke tahun"?** (ini soal keunggulan ML)
5. **Apa yang membuat penelitian ini MENDESAK untuk dilakukan sekarang?** (bukan 5 tahun lalu, bukan 5 tahun lagi)
6. **Apa manfaat konkret hasil penelitian ini?** (untuk siapa? kebijakan apa?)

---

## 🖥️ STEP 3: Lihat Dashboard Streamlit

Jalankan: `streamlit run dashboard/app.py` di terminal VSCode.

Buka halaman **1_Land_Cover_Maps** dan amati peta prediksi tiap tahun. Bayangkan kamu sedang menjelaskan ini kepada dosen atau tamu yang tidak mengerti Machine Learning:
- Apa yang berubah dari 2018 ke 2024?
- Di mana perubahan paling mencolok?

---

## ✅ STEP 4: Checklist sebelum mulai nulis BAB I

- [ ] Saya bisa menjelaskan proyek ini dalam 2 menit tanpa melihat catatan
- [ ] Saya sudah membaca 4 file di Step 1
- [ ] Saya sudah menjawab 6 pertanyaan di Step 2
- [ ] Saya sudah melihat dashboard Streamlit

---

## 📝 Kerangka BAB I yang harus kamu tulis:

```
BAB I PENDAHULUAN
1.1 Latar Belakang (gunakan reports/urgensi_penelitian.md sebagai fondasi)
    - Paragraf 1: Kondisi hutan Kalimantan & urgensi ekologis
    - Paragraf 2: IKN sebagai mega-project dan potensi dampaknya
    - Paragraf 3: Pertambangan sebagai driver historis
    - Paragraf 4: Kebutuhan metode ML yang objektif & real-time
1.2 Rumusan Masalah (3 pertanyaan penelitian)
    - RQ1: Bagaimana akurasi model ML dalam mengklasifikasikan tutupan lahan?
    - RQ2: Bagaimana tren perubahan tutupan lahan 2018–2024?
    - RQ3: Seberapa besar pengaruh IKN dan pertambangan terhadap perubahan tersebut?
1.3 Tujuan Penelitian (jawaban dari RQ)
1.4 Manfaat Penelitian (Teoritis + Praktis)
1.5 Ruang Lingkup Penelitian (Kalimantan, 2018-2024, Sentinel-2, 5 kelas lahan)
```

**Angka konkret yang WAJIB masuk ke Latar Belakang:**
- 6 model diuji → LightGBM terbaik dengan OA 83.32%
- 9,624 titik observasi spasial matched 2018–2024
- 20.85% mengalami perubahan kelas (2,007 titik)
- 858 titik Forest hilang (deforestasi terdeteksi)
