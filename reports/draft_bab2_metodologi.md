# BAB 2: Materi dan Metode
*(Draf khusus Bagian 2.2 Metodologi)*

## 2.2 Metodologi

Penelitian ini menggunakan pendekatan kuantitatif berbasis komputasi spasial yang mengintegrasikan penginderaan jauh (*remote sensing*), algoritma *Machine Learning* (ML), dan pemodelan statistik inferensial. Seluruh tahapan akuisisi data dan prapemrosesan awal dilakukan memanfaatkan arsitektur komputasi awan Google Earth Engine (GEE) (Gorelick et al., 2017), sementara proses pelatihan model, validasi, dan analisis penggerak (*driver analysis*) dieksekusi menggunakan bahasa pemrograman Python. 

Alur kerja (*workflow*) penelitian ini dirancang secara berjenjang dari skala mikro hingga makro, dan dapat diklasifikasikan ke dalam lima tahapan utama: (1) Akuisisi dan Pra-pemrosesan Data, (2) Pelatihan Model dan Validasi Spasial, (3) Prediksi Spatiotemporal Multi-Skala, (4) Deteksi Perubahan Lahan, dan (5) Analisis Penggerak Deforestasi dan Interpretabilitas Model. Diagram alir metodologi secara komprehensif disajikan pada **Gambar 2.1**.

### Diagram Alir Penelitian (Kerangka Kerja)

```mermaid
graph TD
    %% Define Styles
    classDef dataFill fill:#e1f5fe,stroke:#0277bd,stroke-width:2px;
    classDef processFill fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px;
    classDef modelFill fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef outputFill fill:#fff3e0,stroke:#e65100,stroke-width:2px;

    %% Data Acquisition Phase
    subgraph Tahap 1: Akuisisi & Pra-pemrosesan Data (Google Earth Engine)
        A1[Citra Sentinel-2 Harmonized]:::dataFill --> B1(Cloud Masking QA60 & Median Composite)
        A2[ESA WorldCover 2021]:::dataFill --> B2(Label Extraction: 30.000 Titik Sampel 10m)
        A3[Data Topografi & Iklim: SRTM, CHIRPS]:::dataFill --> B1
        B1:::processFill --> C1(Ekstraksi Indeks Spektral: NDVI, NDBI, NDMI, BSI)
        C1 --> B2
    end

    %% ML Training Phase
    subgraph Tahap 2: Pelatihan Model & Validasi Spasial (Python)
        B2 --> D1(Hyperparameter Tuning Optuna):::processFill
        D1 --> D2{Spatial Block CV 0.5 Derajat}:::modelFill
        D2 --> D3[Komparasi 6 Model ML: SVM, LightGBM, RF, dll.]
        D3 --> D4(Pemilihan Model Operasional Terbaik)
    end

    %% Prediction Phase
    subgraph Tahap 3: Prediksi Spatiotemporal Multi-Skala
        D4 --> E1(Prediksi Makro 500m: Seluruh Kalimantan 2019 & 2024):::processFill
        D4 --> E2(Prediksi Mikro 10m: Kawasan Inti IKN 2019 & 2024):::processFill
    end

    %% Change Detection & Analysis
    subgraph Tahap 4 & 5: Analisis Lanjutan & Interpretasi
        E1 --> F1(Common Spatial Domain: 118.943 Titik Konsisten):::processFill
        F1 --> F2[Matriks Transisi Tutupan Lahan 2019-2024]:::outputFill
        F2 --> G1(Regresi Logistik Dual-Driver: Jarak IKN & Kepadatan Tambang):::modelFill
        D4 --> G2(SHAP Analysis: Interpretabilitas Fitur):::modelFill
        G1 --> H1((Kesimpulan Analisis Spasial)):::outputFill
        G2 --> H1
    end
```
*Gambar 2.1. Diagram Alir Metodologi Penelitian.*

---

### Penjelasan Tahapan Metodologi

#### 1. Akuisisi dan Pra-pemrosesan Data (*Data Engineering*)
Penelitian ini memanfaatkan citra satelit **Sentinel-2 Surface Reflectance (Harmonized)** yang memiliki keunggulan resolusi spasial 10 meter dan kanal *Red-Edge* yang sangat sensitif terhadap kerapatan vegetasi tropis (Phiri et al., 2020). Karakteristik *band* spektral yang digunakan dalam klasifikasi dirangkum pada **Tabel 2.1**.

**Tabel 2.1.** Spesifikasi Spektral Sentinel-2 yang Digunakan
| Band | Keterangan | Panjang Gelombang (nm) | Resolusi Asli |
| :--- | :--- | :--- | :--- |
| B2 | Biru (*Blue*) | 490 | 10 m |
| B3 | Hijau (*Green*) | 560 | 10 m |
| B4 | Merah (*Red*) | 665 | 10 m |
| B8 | Inframerah Dekat (*NIR*) | 842 | 10 m |
| B11 | Inframerah Gelombang Pendek (*SWIR-1*) | 1610 | 20 m (Resampled ke 10m) |
| B12 | Inframerah Gelombang Pendek (*SWIR-2*) | 2190 | 20 m (Resampled ke 10m) |

Untuk meminimalisir gangguan atmosfer dan tutupan awan yang tebal di atas ekuator, dilakukan teknik *Cloud Masking* menggunakan *band* QA60 dan *median temporal compositing* secara tahunan (2019 dan 2024). 
Selain *band* spektral mentah, penelitian ini mensintesis empat indeks turunan utama untuk mempertegas batas piksel vegetasi, tanah, dan bangunan. Keempat indeks tersebut dihitung menggunakan persamaan matematis berikut:

1.  **NDVI (*Normalized Difference Vegetation Index*)**  
    $$ NDVI = \frac{NIR - Red}{NIR + Red} $$
2.  **NDBI (*Normalized Difference Built-up Index*)**  
    $$ NDBI = \frac{SWIR1 - NIR}{SWIR1 + NIR} $$
3.  **NDMI (*Normalized Difference Moisture Index*)**  
    $$ NDMI = \frac{NIR - SWIR1}{NIR + SWIR1} $$
4.  **BSI (*Bare Soil Index*)**  
    $$ BSI = \frac{(SWIR1 + Red) - (NIR + Blue)}{(SWIR1 + Red) + (NIR + Blue)} $$

Untuk kebutuhan pengawasan pembelajaran (*Supervised Learning*), label klasifikasi (*ground truth*) diekstrak dari peta referensi global **ESA WorldCover 2021** yang dimodifikasi menjadi 5 kelas utama proyek (**Tabel 2.2**). Sebanyak 30.000 titik piksel murni berskala 10m ditarik menggunakan metode *Stratified Random Sampling* untuk mendistribusikan representasi kelas secara proporsional.

**Tabel 2.2.** Pemetaan Kelas ESA WorldCover ke Kelas Proyek
| Kelas Asli ESA WorldCover | Kode Kelas Proyek | Deskripsi Kelas Proyek |
| :--- | :---: | :--- |
| *Tree cover, Mangroves, Wetlands* | 0 | **Forest** (Hutan/Vegetasi Lebat) |
| *Shrubland, Grassland, Cropland, Moss* | 1 | **Shrubland/Agriculture** (Semak/Pertanian) |
| *Built-up* | 2 | **Built-up** (Area Terbangun/Infrastruktur) |
| *Bare / sparse vegetation* | 3 | **Bare/Mining-like** (Tanah Terbuka/Tambang) |
| *Permanent water bodies* | 4 | **Water** (Badan Air) |

#### 2. Validasi Spasial dan Pemilihan Model (*Machine Learning Modeling*)
Berbeda dengan pendekatan klasifikasi tabular konvensional yang mengandalkan pemisahan acak (*random split*), penelitian ini mengimplementasikan **Spatial Block GroupKFold Cross-Validation (0.5 derajat)**. Pendekatan ini merupakan standar emas (*gold standard*) dalam ekologi kuantitatif guna mencegah kebocoran data spasial (*spatial data leakage*) akibat Hukum Geografi Pertama Tobler tentang autokorelasi spasial (Roberts et al., 2017; Ploton et al., 2020).
Sebanyak enam algoritma diuji secara kompetitif (SVM, LightGBM, XGBoost, *Random Forest*, *Multi-Layer Perceptron*, dan Regresi Logistik). Pemilihan model akhir (*operational model*) tidak hanya didasarkan pada metrik performa absolut (seperti *Overall Accuracy* dan *Macro F1-Score*), melainkan juga mempertimbangkan efisiensi komputasi waktu prediksi, di mana algoritma berbasis *Gradient Boosting* (seperti LightGBM) terbukti menawarkan *trade-off* terbaik untuk pemrosesan skala benua/pulau.

#### 3. Prediksi Spatiotemporal Multi-Skala
Guna mengatasi dilema antara presisi spasial dan batasan memori komputasi (Wu, 2004), tahap prediksi dipecah menjadi dua skala resolusi:
*   **Prediksi Makro (500m):** Dilakukan untuk seluruh daratan Pulau Kalimantan (sekitar 73 juta hektar) guna memfasilitasi analisis tren statistik deforestasi lintas batas provinsi (*telecoupling*).
*   **Prediksi Mikro (10m):** Diterapkan secara eksklusif pada Kawasan Inti Pusat Pemerintahan (KIPP) IKN untuk membuktikan presisi asli model tanpa pengaruh *mixed pixels*, sekaligus memvalidasi ekspansi infrastruktur skala lokal.

#### 4. Deteksi Perubahan dan Konsep *Common Domain*
Deteksi perubahan lahan dari 2019 hingga 2024 tidak dilakukan menggunakan pengurangan sederhana, melainkan menggunakan filter **Common Spatial Domain**. Konsep ini hanya menganalisis 118.943 titik grid yang secara konsisten terbebas dari tutupan awan di kedua tahun pengamatan (2019 dan 2024). Metode ini mereduksi potensi *false-positive* yang sering terjadi akibat variasi musim atau residu bayangan awan (Habibie et al., 2025).

#### 5. Analisis Penggerak (*Drivers*) dan SHAP *Explainability*
Tahap akhir metodologi berfokus pada inferensia kausalitas-asosiatif. Untuk menganalisis penyebab konversi hutan, diaplikasikan **Regresi Logistik Multivariat** guna menghitung log-odds terjadinya deforestasi. Persamaan regresi logistik dirumuskan sebagai:

$$ \ln \left( \frac{P(Y=1)}{1 - P(Y=1)} \right) = \beta_0 + \beta_1(Dist_{IKN}) + \beta_2(Dens_{Mining}) + \beta_3(Elev) + \epsilon $$

*Di mana $P(Y=1)$ adalah probabilitas terjadinya deforestasi, $\beta$ adalah koefisien variabel independen (Jarak IKN, Kepadatan Tambang, Elevasi), dan $\epsilon$ adalah galat sisa (Meyfroidt et al., 2014).*

Selain itu, penelitian ini membongkar sifat "kotak hitam" (*black-box*) dari model *Machine Learning* menggunakan pendekatan **SHAP (SHapley Additive exPlanations)**. Analisis SHAP menghitung kontribusi marjinal dari setiap fitur secara individual menggunakan fungsi penjelasan linear:

$$ g(z') = \phi_0 + \sum_{j=1}^{M} \phi_j z'_j $$

*Di mana $g(z')$ adalah model penjelas, $M$ adalah jumlah fitur, dan $\phi_j$ adalah nilai kontribusi Shapley untuk fitur ke-$j$ (Lundberg & Lee, 2017). Pendekatan matematis ini memastikan bahwa arah keputusan algoritma sejalan dengan hukum ekologi dan fisika optik.*

---

### Referensi Terkait Metodologi
*(Daftar pustaka ini wajib dimasukkan ke bab Referensi Utama Anda)*
1.  **Gorelick, N., et al. (2017).** *Google Earth Engine: Planetary-scale geospatial analysis for everyone*. Remote Sensing of Environment, 202, 18-27. (Scopus Q1).
2.  **Phiri, D., et al. (2020).** *Sentinel-2 Data for Land Cover/Use Mapping: A Review*. Remote Sensing, 12(14), 2291. (Scopus Q1).
3.  **Roberts, D. R., et al. (2017).** *Cross-validation strategies for data with space, time and/or phylogenetic structure*. Ecography, 40(8), 913-929. (Scopus Q1).
4.  **Ploton, P., et al. (2020).** *Spatial validation reveals poor predictive performance of large-scale ecological mapping models*. Nature Communications, 11(1), 4540. (Scopus Q1).
5.  **Meyfroidt, P., et al. (2014).** *Multiple pathways of commodity crop expansion in tropical forest landscapes*. Environmental Research Letters, 9(7), 074012. (Scopus Q1).
6.  **Lundberg, S. M., & Lee, Su-In (2017).** *A Unified Approach to Interpreting Model Predictions*. Advances in Neural Information Processing Systems (NeurIPS) 30. (Top-tier AI Conference).
7.  **Wu, J. (2004).** *Effects of changing scale on landscape pattern analysis: scaling relations*. Landscape Ecology, 19, 125-138. (Scopus Q1).
