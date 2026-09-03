# Flowchart Alur Penelitian

Berikut adalah visualisasi alur penelitian Anda berdasarkan kode Mermaid yang diberikan:

```mermaid
graph TD
    %% Rumusan Masalah & Tujuan
    RM["<b>Rumusan Masalah</b><br/>Bagaimana performa komparatif algoritma ML (Spatial Block CV)<br/>dalam klasifikasi tutupan lahan (2018-2024)<br/>serta dampaknya akibat dual-driver IKN & Tambang?"]
    T["<b>Tujuan Penelitian</b><br/>1. Komparasi 6 Model ML<br/>2. Change Detection<br/>3. Analisis Dual-Driver<br/>4. Interpretabilitas SHAP<br/>5. Dashboard Deployment"]
    RM --> T
    
    %% Sumber Data
    subgraph "Sumber Data"
        S2["Sentinel-2 SR<br/>(Fitur Optik)"]
        ESA["ESA WorldCover 2021<br/>(Label Klasifikasi)"]
        Env["Data Lingkungan & Spasial<br/>(SRTM, CHIRPS, Distance to IKN)"]
    end
    T --> S2
    T --> ESA
    T --> Env

    %% Variabel
    subgraph "Variabel Penelitian"
        V_Inp["<b>Variabel Independen (Fitur Input)</b><br/>6 Bands Sentinel-2<br/>4 Indeks (NDVI, NDBI, NDMI, BSI)<br/>Topografi, Iklim, & Jarak Spasial"]
        V_Out["<b>Variabel Dependen (Target)</b><br/>7 Kelas Tutupan Lahan<br/>(Hutan, Semak, Tani, Terbangun, Terbuka, Air, Lahan Basah)"]
    end
    S2 --> V_Inp
    Env --> V_Inp
    ESA --> V_Out

    %% Metode (CRISP-DM Pipeline)
    subgraph "Metode (CRISP-DM) & Data Pipeline"
        P1["Data Preparation<br/>(GEE Export, Cloud Masking,<br/>Median Composite, Sampling)"]
        P2["Modeling<br/>(RF, XGB, LGBM, LR, SVM, MLP)<br/>& Hyperparameter Tuning"]
        P3["Evaluasi Model<br/>Spatial Block Cross Validation<br/>(OA ≥80%, F1 Macro ≥0.75, Kappa ≥0.75)"]
        P4["Change Detection & Hotspot Analysis<br/>(PCC 2018, 2020, 2022, 2024<br/>& KDE Spatial Analysis)"]
        P5["SHAP Analysis<br/>(Interpretabilitas Fitur)"]
        
        P1 --> P2 --> P3
        P3 --> P4
        P3 --> P5
    end
    V_Inp --> P1
    V_Out --> P1

    %% Hasil / Output
    subgraph "Hasil & Deployment"
        H1["Peta Tutupan Lahan & Matriks Transisi"]
        H2["Hotspot Ekspansi IKN & Pertambangan"]
        H3["Grafik Kontribusi Fitur (SHAP)"]
        DB{"<b>Dashboard Web GIS Interaktif</b><br/>(Streamlit: Map Viewer, Temporal Slider, Statistics Panel)"}
    end
    P4 --> H1
    P4 --> H2
    P5 --> H3
    H1 --> DB
    H2 --> DB
    H3 --> DB
    
    style RM fill:#fff3e0,stroke:#f57c00
    style T fill:#e3f2fd,stroke:#1e88e5
    style P3 fill:#fce4ec,stroke:#e91e63
    style DB fill:#e8f5e9,stroke:#43a047,stroke-width:2px
```

> **Tips:** Anda dapat mengambil screenshot (*screen capture*) dari diagram di atas untuk disisipkan ke dalam laporan proposal atau presentasi PowerPoint Anda.
