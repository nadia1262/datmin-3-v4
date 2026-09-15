# Flowchart & Narasi Alur Penelitian

Dokumen ini memuat audit komprehensif dari seluruh *pipeline* penelitian Anda dari hulu (Google Earth Engine) hingga hilir (Dashboard Web). Gunakan dokumen ini sebagai acuan utama untuk menyusun narasi Bab Metodologi (Bab 2) dan lampiran teknis presentasi.

---

## 1. Diagram Metodologi (Figure 1)

Berikut adalah diagram alir penelitian yang dirancang dengan gaya visual *scientific workflow* (publikasi jurnal internasional):

```mermaid
graph TD
    classDef panel fill:#f0f2f5,stroke:#b0bec5,stroke-width:1.5px,stroke-dasharray: 5 5,color:#333;
    classDef process fill:#fff9e6,stroke:#e0d4b3,stroke-width:1.5px,color:#2c3e50,rx:5px,ry:5px,font-family:sans-serif,font-size:13px;
    classDef highlight fill:#e3f2fd,stroke:#1e88e5,stroke-width:1.5px,color:#0d47a1,font-weight:bold,rx:5px,ry:5px;

    subgraph S1 ["<b>1. AKUISISI DATA & PRA-PEMROSESAN</b>"]
        direction TB
        D1["Sentinel-2 & ESA WorldCover 2021 (Reference Label)"]:::process
        D2["Cloud Masking & Temporal Composite"]:::process
        D1 --> D2
    end

    subgraph S2 ["<b>2. TAHAP 1: KLASIFIKASI TUTUPAN LAHAN</b>"]
        direction TB
        X_ML["<b>X = Spectral & Environmental Features</b><br/>Spectral Bands (B2, B3, B4, B8, B11, B12)<br/>NDVI, NDBI, NDMI, BSI<br/>Elevation, Annual Rainfall"]:::highlight
        ML["<b>LightGBM</b><br/>(Spatial Block GroupKFold)"]:::process
        Y_ML["<b>Y = Land-Cover Class (5 categories)</b><br/>Forest, Shrubland/Agriculture, Built-up,<br/>Bare/Mining-like, Water"]:::highlight
        
        X_ML --> ML --> Y_ML
    end

    subgraph S3 ["<b>3. PETA TUTUPAN LAHAN (2019–2024)</b>"]
        direction TB
        Maps["Kalimantan (500 m) & IKN (10 m)"]:::process
    end

    subgraph S4 ["<b>4. DETEKSI PERUBAHAN</b>"]
        direction TB
        CSD["Majority Voting Grid 500m<br/>1.499.024 sel (2019 vs 2024)"]:::process
        Y_Logit["<b>Y = Binary Change Outcomes</b><br/>Y₁ = Forest Loss<br/>Y₂ = Urbanization<br/>Y₃ = Bare/Mining-like Expansion"]:::highlight
        CSD --> Y_Logit
    end

    subgraph S5 ["<b>5. VARIABEL INDEPENDEN TAHAP 2 (X)</b>"]
        direction TB
        Maus["Maus et al. (2022)<br/>↓<br/>Mining Polygons<br/>↓<br/>Spatial Processing<br/>↓<br/>Mining Density (10 km)"]:::process
        X_Logit["<b>X = Predictors</b><br/>X₁ = Distance to IKN (Utama)<br/>X₂ = Mining Density 10 km (Utama)<br/>X₃ = Elevation (Kontrol)<br/>X₄ = Annual Rainfall (Kontrol)"]:::highlight
        Maus -.-> X_Logit
    end

    subgraph S6 ["<b>6. TAHAP 2: ANALISIS ASOSIASI</b>"]
        direction TB
        Logit["<b>3 Model Logistic Regression Terpisah</b><br/>Model 1 → Y₁<br/>Model 2 → Y₂<br/>Model 3 → Y₃"]:::process
        Out_Logit["<b>Output:</b><br/>β | Odds Ratio | p-value"]:::process
        Logit --> Out_Logit
    end

    subgraph S7 ["<b>7. INTERPRETASI & OUTPUT</b>"]
        direction TB
        SHAP["SHAP Feature Importance"]:::process
        Dash["Interactive Web Dashboard"]:::process
    end

    %% --- CONNECTIONS ---
    D2 --> X_ML
    Y_ML --> Maps
    Maps --> CSD
    
    Y_Logit --> Logit
    X_Logit --> Logit
    
    ML -.-> SHAP
    Out_Logit --> Dash
    SHAP --> Dash

    class S1,S2,S3,S4,S5,S6,S7 panel;
```

---

## 2. Narasi Alur (*The Storyline*)

Penelitian ini dibagi menjadi beberapa tahapan komputasi utama yang saling berkesinambungan:

### Tahap 1 & 2: Akuisisi Data & Pra-pemrosesan
Proses dimulai di *cloud* GEE untuk menghindari *download* citra bergiga-giga. Kita menggunakan citra **Sentinel-2** (komposit median tahunan 2019-2024) untuk mendapatkan fitur spektral (B2, B3, B4, NIR, SWIR, NDVI, dll). Sebagai *Reference Label*, kita memakai **ESA WorldCover 2021** yang disederhanakan menjadi **5 Kelas Utama**: *Forest, Shrubland/Agriculture, Built-up, Bare/Mining-like, Water*. Selain itu, dihitung pula elevasi, curah hujan, dan jarak ke IKN.

### Tahap 3 & 4: Data Pelatihan & Klasifikasi Terawasi
Dataset 30.000 titik (10 m) diekstrak dan dilatih menggunakan 6 algoritma. Untuk mencegah *spatial autocorrelation leakage*, digunakan metode **Spatial Block GroupKFold**. Seluruh kandidat dioptimasi menggunakan Grid Search, kemudian dievaluasi validasi spasialnya. Hasilnya, **LightGBM** dipilih sebagai model operasional utama.

### Tahap 5: Prediksi Spasial
LightGBM yang sudah terlatih digunakan untuk melakukan prediksi. Proses ini dicabangkan menjadi dua:
- **Makro (Kalimantan):** Prediksi grid 500 m untuk tahun 2019-2024.
- **Mikro (IKN):** Prediksi detail di resolusi asli 10 m khusus radius IKN.

### Tahap 6: Analisis Perubahan Tutupan Lahan
Menggunakan peta prediksi makro, setiap sel grid 500 m didekomposisi menjadi sub-grid 5×5 (25 sub-piksel) dan kelas tutupan lahan ditentukan via **Majority Voting**. Metode ini menghasilkan **1.499.024 sel valid** — 12× lebih banyak dari metode Centroid lama. Melalui perbandingan dua titik waktu (2019 vs 2024), dihasilkan matriks transisi yang mengkuantifikasi parameter utama: *Forest Loss, Urbanization*, dan *Mining Expansion*. Untuk Tahap 3 (Regresi), label Majority Voting di-*downsample* ke grid sistematis 10 km (**122.478 titik**) via *Spatial Intersection* guna menjaga asumsi independensi statistik.

### Tahap 7: Data Tambang Eksternal (Independen)
Secara **terpisah** dari *pipeline* klasifikasi optik, dataset independen poligon tambang aktual dari **Maus et al. (2022)** diproses secara spasial untuk menghasilkan variabel kepadatan tambang (*Mining Density 10 km*).

### Tahap 8: Analisis Asosiasi
Digunakan **Multivariate Logistic Regression** untuk menginvestigasi asosiasi antara variabel lingkungan (jarak IKN, kepadatan tambang, dll) terhadap hasil perubahan tutupan lahan. Output yang dianalisis berupa *Odds Ratio* dan *p-value*.

### Tahap 9: Interpretasi & Output
Seluruh hasil dirangkum melalui interpretasi *SHAP Feature Importance*, Peta Perubahan, dan Matriks Transisi, yang semuanya diintegrasikan ke dalam sebuah **Visualisasi / Dashboard Web Interaktif**.
