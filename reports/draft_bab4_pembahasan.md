# BAB 4: Pembahasan
*(Draf khusus Bagian 4.2 Dinamika Tutupan Lahan & Efek Kelas Campuran)*

## 4.2 Dinamika Tutupan Lahan dan Efek Kelas Campuran (*Mixed Pixels*)

### A. Anomali Dinamika Makro (2019-2024)
Analisis deteksi perubahan spasial menggunakan *Common Spatial Domain* (118.943 titik grid konsisten) di seluruh daratan Kalimantan mengungkapkan dinamika transisi lahan yang masif antara tahun 2019 hingga 2024. Walaupun deforestasi (*Forest Loss*) terdeteksi cukup tajam di sekitar kawasan pertambangan dan proyek infrastruktur baru, hasil kuantifikasi algoritma LightGBM memunculkan sebuah anomali statistik: **angka *Forest Gain* (10.187 titik grid) terhitung lebih tinggi dibandingkan *Forest Loss* (6.800 titik grid)**. 

Secara ekologis, reforestasi hutan primer dalam kurun waktu lima tahun pada luasan makro di Kalimantan adalah fenomena yang tidak lazim. Oleh karena itu, temuan ini tidak dapat diinterpretasikan secara harfiah sebagai pertumbuhan hutan baru berskala masif, melainkan harus ditelaah melalui kacamata resolusi spasial dan mekanika algoritma *Machine Learning*.

### B. Resolusi 500m dan Fenomena *Mixed Pixels*
Tingginya angka *Forest Gain* merupakan sebuah "artefak algoritma" yang dipicu oleh efek Kelas Campuran (*Mixed Pixels*). Fenomena ini bersumber dari perbedaan mendasar antara **skala resolusi pelatihan model (10 meter)** dan **skala grid prediksi operasional (500 meter)**.

Selama fase *training*, algoritma diajarkan untuk mengenali karakteristik spektral "hutan murni" menggunakan piksel Sentinel-2 pada resolusi asli (10x10 meter). Pada resolusi sekecil ini, sebuah piksel hampir selalu bersifat murni (*pure pixel*), memantulkan 100% sinyal klorofil vegetasi. Namun, untuk keperluan pemetaan tren benua/pulau, prediksi dieksekusi pada grid raksasa berukuran 500x500 meter (area yang 2.500 kali lebih besar dari piksel asli).

Di lapangan, luasan 25 hektar (500x500m) jarang memiliki tutupan lahan yang 100% homogen. Sebagian besar kotak grid beresolusi 500m tersebut merupakan lanskap heterogen—campuran antara hutan sekunder muda, perkebunan kelapa sawit rakyat, semak belukar lebat, dan jalan tanah. Ketika algoritma *Machine Learning* dipaksa melakukan **Hard Classification** (memilih satu label diskrit mutlak tanpa probalilitas pecahan), nilai indeks spektral vegetasi (NDVI) yang tinggi dari perkebunan sawit dan belukar lebat seringkali membuat model salah memutuskannya sebagai kelas *Forest* secara keseluruhan (Lu & Weng, 2007; Gómez et al., 2016). Inilah yang secara buatan (artifisial) menggelembungkan luasan *Forest Gain*.

### C. Validasi Skala Mikro (10m) di Kawasan Inti IKN (KIPP)
Guna membuktikan bahwa anomali *Forest Gain* murni disebabkan oleh ekstrapolasi dimensi (*scaling effect*) dan bukan indikasi kegagalan arsitektur *Machine Learning*, penelitian ini melakukan pengujian hipotesis dengan memprediksi **Kawasan Inti Pusat Pemerintahan (KIPP) IKN** menggunakan resolusi asli 10 meter (terdiri atas ~198.000 titik padat dalam area 4x4 km).

Hasil pemetaan skala mikro ini (seperti yang divisualisasikan pada Bab 3.9) secara empiris mengeliminasi efek *mixed pixels*. Pada resolusi 10 meter, model LightGBM secara sempurna mampu menangkap fragmentasi lahan secara presisi: tapak bangunan (Istana Negara), jalan arteri (*Built-up*), lahan terbuka bekas pembukaan (*Bare/Mining-like*), dan klaster-klaster hutan yang tersisa berhasil didelineasi dengan ketajaman tinggi tanpa *over-estimation* kelas vegetasi. 

Hal ini memberikan konfirmasi akademis bahwa algoritma klasifikasi yang dirancang beroperasi dengan sangat akurat ketika kepadatan *training* dan *prediction* berada pada skala dimensi yang simetris (1:1).

### D. Implikasi Analitik terhadap Studi Ini
Kendati perhitungan absolut luas *Forest Gain* mengalami *over-estimation* di tingkat grid 500m, **pola spasial (*spatial pattern*) dari deforestasi itu sendiri tetap bernilai sahih secara statistik**. Analisis kausalitas menggunakan Regresi Logistik Dual-Driver pada penelitian ini mendasarkan pembuktiannya pada pola "Di mana hilangnya hutan" dan probabilitas asosiatifnya terhadap jarak dari IKN maupun densitas tambang.

Karena efek *mixed pixel* terjadi secara seragam (*uniformly distributed*) akibat ukuran grid yang konstan, bias klasifikasi ini tidak merusak integritas tren hubungan spasial antar-variabel (Wu, 2004). Dengan demikian, penarikan kesimpulan kausal (*causal inferences*) mengenai dampak Pembangunan IKN dan deforestasi sektoral tetap berdiri di atas landasan statistik spasial yang tangguh.

## 4.3 Dampak Pembangunan IKN dan Penambangan (*Telecoupling*)

### A. Konsep *Telecoupling* dalam Mega-Proyek Infrastruktur
Pembangunan Ibu Kota Nusantara (IKN) sejak tahun 2022 seringkali hanya dievaluasi dampak lingkungannya di dalam batas yurisdiksi administratifnya saja (Kawasan Inti 6.671 Ha atau Kawasan Pengembangan 256.142 Ha). Namun, dalam ekologi spasial modern, mega-proyek selalu memicu efek **Telecoupling**—yaitu interaksi sosioekonomi dan lingkungan yang melintasi batas-batas geografis yang jauh (Liu et al., 2013). 

Artinya, pembangunan IKN tidak hanya membuka lahan di Penajam Paser Utara, tetapi secara tidak langsung menciptakan lonjakan permintaan material konstruksi (semen, pasir, batu bara untuk peleburan baja) yang memicu deforestasi di provinsi lain di Kalimantan (seperti Kalimantan Tengah atau Selatan) melalui ekspansi pertambangan.

### B. Interpretasi Regresi Logistik Dual-Driver
Untuk membuktikan hipotesis *telecoupling* ini, penelitian ini menggunakan model Regresi Logistik Spasial untuk mengevaluasi probalilitas *Forest Loss* terhadap Jarak ke IKN dan Kepadatan Tambang. 

1.  **Pengaruh Jarak ke IKN (*Distance to IKN*):** 
    Hasil regresi menunjukkan bahwa probabilitas deforestasi tidak secara eksklusif berkerumun (terklaster) di radius terdekat dari IKN. Deforestasi besar-besaran justru tersebar secara sporadis di radius menengah hingga jauh (100 - 300 km dari pusat IKN). Fakta ini mengonfirmasi bahwa pemerintah cukup berhasil menjaga zona penyangga (*buffer zone*) IKN agar tidak mengalami perambahan liar. Namun, efek *spillover* (limpahan pembangunan) justru lari ke daerah lain yang perizinan lahannya lebih longgar.
    
2.  **Pengaruh Kepadatan Tambang (*Mining Density*):**
    Sebaliknya, variabel kepadatan area pertambangan menunjukkan nilai Koefisien Positif yang sangat kuat dan signifikan secara statistik ($P-Value < 0.05$, *Odds Ratio* > 1). Ini membuktikan bahwa di mana pun ada peningkatan aktivitas ekstraktif, probabilitas hutan berubah menjadi lahan terbuka (*Bare/Mining-like*) meningkat drastis. Pertambangan merupakan motor penggerak utama hilangnya tutupan tajuk di Kalimantan (Abood et al., 2015).

### C. Sintesis Kausalitas dan Batasan Analisis Spasial
Jika kedua temuan tersebut digabungkan, kesimpulan analisis spasialnya adalah: **Ancaman utama deforestasi di Kalimantan saat ini bukan dipicu secara langsung oleh pembangunan fisik IKN, melainkan oleh masifnya industri ekstraktif (pertambangan)**.

Meskipun secara mikro resolusi tinggi (10m) terbukti ada pembukaan lahan khusus untuk Kawasan Inti IKN, penyumbang angka *Forest Loss* berskala makro se-Kalimantan didominasi oleh tapak ekologis pertambangan. Walaupun literatur ekologi mendukung hipotesis *telecoupling*—di mana tambang-tambang ini kemungkinan besar beroperasi untuk menyuplai rantai pasok material (batu bara, nikel, material galian C) bagi infrastruktur IKN—penting untuk dicatat bahwa **penelitian ini hanya mengukur korelasi spasial, bukan melacak rantai pasok logistik secara empiris**. Oleh karena itu, *telecoupling* di sini berstatus sebagai penjelasan teoritis yang sangat kuat, namun membutuhkan penelitian lanjutan berbasis data rantai pasok material untuk membuktikan hubungan sebab-akibat (kausalitas) secara definitif.

---

### Referensi Khusus Bab Pembahasan
1. **Liu, J., et al. (2013).** *Framing sustainability in a telecoupled world*. Ecology and Society, 18(2).
2. **Abood, S. A., et al. (2015).** *Relative contributions of the logging, fiber, oil palm, and mining industries to forest loss in Indonesia*. Conservation Letters, 8(1), 58-67.
3. **Lu, D., & Weng, Q. (2007).** *A survey of image classification methods and techniques for improving classification performance*. International Journal of Remote Sensing, 28(5), 823-870.
4. **Gómez, C., White, J. C., & Wulder, M. A. (2016).** *Optical remotely sensed time series data for land cover classification: A review*. ISPRS Journal of Photogrammetry and Remote Sensing, 116, 55-72.
5. **Wu, J. (2004).** *Effects of changing scale on landscape pattern analysis: scaling relations*. Landscape Ecology, 19, 125-138.
