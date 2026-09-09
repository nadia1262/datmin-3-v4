# Panduan Storyline untuk Tim (Satu Frekuensi)

*Gunakan draf ini saat rapat/kumpul dengan anggota kelompok agar semuanya paham alur cerita proyek kita dari awal sampai akhir, tanpa harus pusing dengan bahasa coding.*

---

## BABAK 1: Misi Kita (Tujuan Awal)
"Gais, inti dari proyek kita ini adalah pengen jawab satu pertanyaan besar: **Sejak IKN diumumkan (2019) sampai sekarang (2024), apakah hutan di Kalimantan itu hancur gara-gara IKN?** 
Nah, untuk jawab ini, kita nggak pakai data BPS biasa, tapi kita *download* citra satelit Sentinel-2 dan kita suruh *Machine Learning* (AI) buat nebak mana hutan, mana tambang, mana kota."

## BABAK 2: Cara Kerja (Biar Kelihatan Keren)
"Cara kerjanya gini:
1. Kita ajarin AI kita pakai peta dari Eropa (ESA WorldCover 2021). Kita kasih dia 30.000 titik sampel dengan resolusi sangat tajam (**10 meter**).
2. Kita nggak cuma nyoba satu algoritma, tapi 6 algoritma sekaligus biar dosen lihat kita niat! Biar dosen nggak bilang model kita 'cuma menghafal', kita ujinya pakai metode *Spatial Block CV* (diuji di daerah yang belum pernah dia lihat). 
   Ini hasil perbandingan akurasi piksel 10 meter kita:

   | Peringkat | Algoritma *Machine Learning* | Akurasi | Waktu Pelatihan |
   | :---: | :--- | :---: | :---: |
   | 1 | **SVM (Support Vector Machine)** | 83,99% | 759,9 detik (Sangat Lambat) |
   | 2 | **LightGBM (Terpilih)** | 83,32% | 116,6 detik (Sangat Cepat) |
   | 3 | **XGBoost** | 83,20% | 189,3 detik |
   | 4 | **MLP (Neural Network)** | 82,85% | 340,6 detik |
   | 5 | **Random Forest** | 82,53% | 449,5 detik |
   | 6 | **Regresi Logistik** | 79,36% | 14,6 detik |

   *(Catatan buat tim: Walaupun SVM juara 1 beda tipis 0,6%, kita pilih **LightGBM** sebagai model operasional utama karena dia **6,5x lebih cepat**. Untuk ngerjain data spasial raksasa skala pulau, kecepatan itu segalanya!)*

3. Setelah pinter, kita suruh model LightGBM ini nebak **seluruh pulau Kalimantan** untuk tahun 2019 dan 2024. Tapi masalahnya, Kalimantan itu gedenya 73 juta hektar! Kalau kita nebak per 10 meter, laptop kita bisa meledak (butuh miliaran titik). Jadi, kita kompromi: kita tebaknya per **500 meter** (jadi cuma 155 ribu titik).

## BABAK 3: Plot Twist (Masalah yang Muncul)
"Nah, pas hasil tebakannya keluar, ada hasil yang aneh banget. Angka **Forest Gain (Hutan Nambah) kita malah lebih tinggi dari Forest Loss (Hutan Hilang)**. 
Dosen pasti bakal nanya: *'Kok bisa? Masa dalam 5 tahun Kalimantan tiba-tiba jadi rimbun lagi?'*
Ini jawabannya: **Efek Mixed Pixels**. Karena kita tadi nebaknya per kotak 500 meter (25 hektar), satu kotak itu isinya campur aduk (ada kebun sawit, belukar, dan dikit hutan). Karena AI kita dipaksa milih 1 tebakan mutlak, dia milih 'Hutan' karena spektral hijaunya dominan. Jadi, hutan yang nambah itu sebenarnya halusinasi algoritma gara-gara resolusi 500m."

## BABAK 4: Senjata Rahasia (Cara Kita Bertahan)
"Terus kalau ditanya dosen, *'Berarti model kalian gagal dong?'* 
Kita jawab: **TIDAK!** Kita punya buktinya. 
Kita bikin **Peta Mikro 10 meter khusus di KIPP (Kawasan Istana Negara IKN)**. Di skala 10 meter aslinya ini, tebakan model kita **sempurna**. Bangunan, jalan tanah, dan sisa hutan terpetakan dengan sangat tajam tanpa *error*. Jadi, model kita itu aslinya sangat cerdas, 'error' tadi murni cuma efek nge-*zoom-out* ke 500 meter aja buat ngakalin keterbatasan laptop."

## BABAK 5: Kesimpulan Pamungkas (Korelasi vs Kausalitas)
"Terus gimana kesimpulan akhir paper kita? Kesimpulannya sangat objektif berdasarkan data regresi logistik:
- Hutan di radius dekat IKN itu nggak banyak yang hancur. Pemerintah sukses menjaga *buffer zone*.
- TAPI, hutan yang hancur karena **Tambang** meledak di mana-mana!
- **Kesimpulannya:** Secara spasial, ancaman terbesar bagi hutan Kalimantan bukanlah pembangunan fisik IKN itu sendiri, melainkan industri ekstraktif (pertambangan). Walaupun secara teori mungkin ada efek *Telecoupling* (tambang-tambang tersebut menyuplai material untuk IKN), kita harus jujur ke dosen bahwa data satelit kita hanya mengukur **korelasi spasial**, bukan melacak rantai pasok material. Jadi kesimpulan utamanya adalah: IKN aman secara lokal, tapi Kalimantan secara keseluruhan masih terus digerogoti oleh perluasan tambang."

---
**Pesan Penutup untuk Tim:** 
*"Jadi gais, kalau nanti ditanya pas presentasi, ingat ya: Kita ini jujur kalau ada kelemahan di 500m (mixed pixels), tapi kita buktikan kecerdasan model kita di 10m (Peta KIPP IKN). Dan temuan kita harus disampaikan secara objektif: IKN secara fisik aman, tapi ancaman sesungguhnya di Kalimantan adalah industri ekstraktif (tambang) yang tersebar luas, di mana secara teori mungkin menyuplai material pembangunan mega-proyek."*
