# Panduan Defense Sidang: Mengatasi Serangan "Skala & Mixed Pixels"

Dokumen ini disusun khusus sebagai **"senjata rahasia"** Anda untuk menghadapi penguji yang kritis terhadap perbedaan resolusi data *training* (10m) dan resolusi prediksi (500m) yang menyebabkan tingginya angka *Forest Gain*.

---

## 1. Memahami Akar Masalah Secara Mendetail (Mengapa Ini Terjadi?)

### A. Konsep Resolusi vs Grid Prediksi
*   **Saat Training (10 meter):** Model Anda dilatih menggunakan piksel asli Sentinel-2 (10x10 meter = 100 m²). Pada ukuran sekecil ini, sebuah piksel biasanya bersifat **Murni (Pure Pixel)**. Jika piksel itu jatuh di atas pohon, maka pantulannya 100% klorofil pohon. Model belajar mengenali "Hutan Murni" dengan sangat akurat.
*   **Saat Memprediksi (500 meter):** Demi menghemat komputasi untuk memetakan luasan 73 juta hektar (seluruh Kalimantan), Anda membuat titik grid setiap 500 meter. Satu area berukuran 500x500 meter sama dengan **2.500 kali lebih besar** dari piksel 10 meter. 

### B. Terjadinya Efek *Mixed Pixel* (Mixel)
Pada area seluas 500x500 meter di alam liar, sangat jarang ada tutupan lahan yang 100% seragam. Area tersebut mungkin berisi 40% hutan sekunder, 40% semak belukar, dan 20% jalan tanah. 
Namun, algoritma *Machine Learning* Anda menggunakan **Hard Classification** (memaksa model memilih 1 label mutlak untuk area tersebut). Akibatnya, nilai pantulan satelit menjadi "campur aduk" (*mixed spectral signature*).

### C. Kenapa *Forest Gain* Tiba-tiba Sangat Tinggi?
Di daerah tropis seperti Kalimantan, **Semak Belukar (*Shrubland*)** dan **Hutan Sekunder (*Forest*)** memiliki warna hijau (*NDVI*) dan kelembaban (*NDMI*) yang hampir identik dari kacamata satelit. Ketika model dihadapkan pada piksel campuran 500m yang dominan hijau, model sering keliru (*misclassification*) menganggap semak belukar yang baru tumbuh lebat sebagai "Hutan". Inilah yang menciptakan ilusi seolah-olah terjadi reforestasi masif (*Forest Gain* 10.187 titik), padahal secara biologis hutan tidak mungkin tumbuh secepat itu dalam 6 tahun.

---

## 2. Strategi Menjawab (Defense Script) Saat Sidang

Jika dosen bertanya: 
> *"Kenapa hasil Forest Gain kamu lebih tinggi dari Forest Loss? Apakah ini logis? Bukankah prediksi di 500 meter padahal training di 10 meter itu ngawur dan bias?"*

**Jangan panik dan jangan membantah.** Gunakan teknik *Acknowledge & Reframe* (Akui kelemahannya secara elegan, lalu ubah menjadi argumen akademis).

**Jawaban Anda (Hafalkan alur logika ini):**
> "Terima kasih atas pertanyaannya, Pak/Bu. Pertanyaan ini sangat tajam dan memang menyentuh limitasi utama dari penelitian *macro-scale* kami.
> 
> Pertama, kami **mengakui** bahwa tingginya angka *Forest Gain* kemungkinan besar bukanlah reforestasi fisik murni, melainkan artefak dari fenomena **Mixed Pixel (Mixel)**. Karena kami harus melakukan *upscaling* prediksi ke grid 500 meter demi kelayakan komputasi skala pulau, pantulan spektral dari semak belukar (shrubland) yang menghijau sering kali berbaur (*overlap*) dengan batas spektral hutan sekunder, sehingga algoritma men-generalisasinya sebagai kelas *Forest*.
> 
> Namun, pendekatan ini sangat lazim dalam kajian pemetaan tutupan lahan skala benua/pulau. Menurut literatur *remote sensing*, *Hard Classification* pada resolusi menengah pasti menghasilkan *mixed pixels*. 
> 
> Tujuan utama penelitian ini **bukanlah** menghitung presisi mutlak berapa meter persegi hutan yang hilang, melainkan **menemukan probabilitas spasial (Odds Ratio)**. Meskipun ada *noise* akibat *mixed pixels*, *noise* tersebut terdistribusi secara sistematis di seluruh tahun pengamatan. Sehingga, kesimpulan Regresi Logistik kami—bahwa jarak yang lebih dekat dengan IKN dan Tambang secara probabilitas berasosiasi dengan deforestasi—tetap kokoh dan valid secara statistik makro."

---

## 3. Rujukan Jurnal (Gunakan Ini di Laporan & PPT)

Untuk membuktikan bahwa Anda mengerti konsep ini, cantumkan 3 rujukan internasional ini di Laporan (Bab 4 Pembahasan) dan saat presentasi. Dosen akan kehabisan kata-kata jika Anda sudah mem- *backup* kelemahan Anda dengan literatur Q1.

### Rujukan 1: Tentang Masalah *Mixed Pixel* di Hutan Tropis
*   **Penulis:** Lu, D., & Weng, Q. (2007).
*   **Judul Paper:** *A survey of image classification methods and techniques for improving classification performance.*
*   **Jurnal:** International Journal of Remote Sensing.
*   **Kutipan Argumentatif:** "Lu & Weng (2007) menegaskan bahwa lanskap tropis yang heterogen selalu menghasilkan persentase *mixed pixels* yang tinggi, yang menjadi sumber utama penurunan akurasi pada *hard classification* tradisional."

### Rujukan 2: Tentang Kemiripan Spektral Hutan & Semak
*   **Penulis:** Gómez, C., White, J. C., & Wulder, M. A. (2016).
*   **Judul Paper:** *Optical remotely sensed time series data for land cover classification: A review.*
*   **Jurnal:** ISPRS Journal of Photogrammetry and Remote Sensing.
*   **Kutipan Argumentatif:** "Menurut Gómez et al. (2016), transisi vegetasi sekunder seperti semak belukar ke hutan memiliki ambang spektral (seperti NDVI) yang sangat bias (*overlapping*), sehingga algoritma klasifikasi rentan menghasilkan *false positive* pada deteksi perolehan hutan (*forest gain*)."

### Rujukan 3: Tentang Kesalahan Klasifikasi Akibat Penurunan Resolusi (*Scaling Effect*)
*   **Penulis:** Wu, J. (2004).
*   **Judul Paper:** *Effects of changing scale on landscape pattern analysis: scaling relations.*
*   **Jurnal:** Landscape ecology.
*   **Kutipan Argumentatif:** "Penurunan resolusi spasial (dalam studi ini dari 10m ke grid 500m) secara matematis mengubah proporsi agregasi tutupan lahan, sebagaimana dibuktikan oleh fenomena *Modifiable Areal Unit Problem (MAUP)* yang dibahas oleh Wu (2004)."

---

**Saran Eksekusi:** 
*Copy-paste* penjelasan di atas ke dalam draf **BAB 4 (Pembahasan / Keterbatasan Penelitian)** Anda. Kelemahan yang dijabarkan dengan kejujuran akademis tinggi seperti ini justru sering kali membuahkan **Nilai A**, karena menunjukkan level kematangan analisis mahasiswa!
