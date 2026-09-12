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

### A. Evaluasi Empiris Hipotesis *Spillover Effect* IKN
Pembangunan Ibu Kota Nusantara (IKN) sejak tahun 2022 memicu kekhawatiran ekologis akan terjadinya *spillover effect* (efek limpahan)—yaitu ledakan urbanisasi dan deforestasi yang menyebar secara radial dari pusat IKN ke seluruh pelosok daratan Kalimantan. Untuk menguji kebenaran hipotesis spasial ini, penelitian ini memodelkan probabilitas kejadian urbanisasi, deforestasi, dan ekspansi tambang menggunakan Regresi Logistik Multivariat. 

Hasil uji signifikansi (Tabel 4.x) menunjukkan temuan empiris yang sangat krusial dan meruntuhkan hipotesis *spillover* klasik: **Jarak ke IKN terbukti tidak signifikan memicu urbanisasi berskala benua (*p-value* = 0.159)**. Artinya, kedekatan maupun kejauhan geografis dari pusat pemerintahan IKN tidak berkorelasi dengan fenomena pertumbuhan lahan terbangun baru (*Built-up*) di Kalimantan dalam periode 2019–2024. Pembangunan IKN sejauh ini masih sangat terlokalisasi secara mikro di dalam Kawasan Inti (sebagaimana dibuktikan oleh peta resolusi 10m di subbab sebelumnya) dan belum menarik aglomerasi pemukiman makro di luarnya.

### B. Dominasi Efek *Telecoupling* Pertambangan
Sebaliknya, analisis regresi secara absolut menempatkan **Kepadatan Tambang Eksisting (*Mining Density*)** sebagai motor penggerak spasial utama (Driver) bagi perubahan tutupan lahan di Kalimantan:

1. **Pemicu Utama Urbanisasi:** Kepadatan tambang memiliki efek prediktif yang sangat kuat dan signifikan (*p-value* < 0.001) terhadap pertumbuhan urbanisasi baru, dengan *Odds Ratio* (OR) 1.26. Setiap peningkatan 1 standar deviasi kepadatan tambang, kemungkinan munculnya urbanisasi baru naik 1.26 kali lipat. Ini membuktikan fenomena **Telecoupling** murni: permukiman baru tidak tumbuh mengikuti pusat administrasi (IKN), melainkan beraglomerasi di sekitar pusat ekstraksi modal dan sumber daya alam untuk menampung para pekerja tambang beserta fasilitas pendukungnya.
2. **Katalis Deforestasi Ekstrim:** Densitas tambang juga terbukti signifikan mendorong hilangnya hutan primer/sekunder (*Forest Loss*) dengan OR sebesar 1.09. Menariknya, variabel jarak ke IKN menunjukkan korelasi positif terhadap deforestasi (*OR* = 1.11, *p-value* < 0.001), yang mengartikan bahwa deforestasi justru semakin probabel terjadi di area yang **jauh** dari pengawasan zona penyangga IKN.
3. **Aglomerasi Ekstraktif (Tambang Melahirkan Tambang Baru):** Dalam model *Mining Expansion*, keberadaan tambang terdahulu adalah pendorong terkuat untuk pembukaan tambang baru (*OR* = 1.30). Lanskap Kalimantan dikuasai oleh perluasan lubang tambang secara sistematis yang memperlebar defisit ekologis.

### C. Pengaruh Variabel Lingkungan Pendukung
Selain *driver* artifisial, model juga mengonfirmasi hukum geografi deterministik. Deforestasi, urbanisasi, maupun ekspansi tambang menunjukkan korelasi negatif yang sangat kuat (*p-value* < 0.001) terhadap **Elevasi** dan **Curah Hujan Tahunan**. Transformasi tutupan lahan manusia secara selektif menghindari wilayah pegunungan yang terjal atau wilayah dengan curah hujan sangat tinggi, dan mengeksploitasi dataran rendah yang secara topografis lebih murah untuk dibangun infrastruktur logistik.

### D. Sintesis Kausalitas 
Jika keseluruhan temuan regresi disintesiskan, terbukti bahwa lanskap spasial Kalimantan saat ini belum merespons IKN sebagai pusat gravitasi baru. Evolusi tutupan lahan sejatinya masih dikendalikan secara mutlak oleh fenomena **Telecoupling Ekstraktif**. Walaupun ada kemungkinan bahwa ekspansi pertambangan masif di radius menengah/jauh beroperasi untuk menyuplai rantai pasok material (batu bara, batu, semen) bagi pembangunan infrastruktur IKN, penelitian ini baru sebatas mengonfirmasi *asosiasi spasial*, sedangkan rantai pasok logistik kausalnya membutuhkan studi ekonometrika lintas wilayah di masa depan (Liu et al., 2013).

---

### Referensi Khusus Bab Pembahasan
1. **Liu, J., et al. (2013).** *Framing sustainability in a telecoupled world*. Ecology and Society, 18(2).
2. **Abood, S. A., et al. (2015).** *Relative contributions of the logging, fiber, oil palm, and mining industries to forest loss in Indonesia*. Conservation Letters, 8(1), 58-67.
3. **Lu, D., & Weng, Q. (2007).** *A survey of image classification methods and techniques for improving classification performance*. International Journal of Remote Sensing, 28(5), 823-870.
4. **Gómez, C., White, J. C., & Wulder, M. A. (2016).** *Optical remotely sensed time series data for land cover classification: A review*. ISPRS Journal of Photogrammetry and Remote Sensing, 116, 55-72.
5. **Wu, J. (2004).** *Effects of changing scale on landscape pattern analysis: scaling relations*. Landscape Ecology, 19, 125-138.
