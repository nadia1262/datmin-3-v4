# scripts/generate_workspace_audit_md.py
import os
import sys
import datetime

workspace = r'd:\POLSTAT STIS\Tingkat 3\Semester 6\DATMIN\Kelompok_3_v4'
output_md = os.path.join(workspace, 'reports', 'AUDIT_STRUKTUR_WORKING_DIRECTORY.md')
exclude = {'.git', '__pycache__', '.venv', 'venv'}

def format_size(sz_bytes):
    if sz_bytes < 1024:
        return f"{sz_bytes} B"
    elif sz_bytes < 1024 * 1024:
        return f"{sz_bytes / 1024:.1f} KB"
    elif sz_bytes < 1024 * 1024 * 1024:
        return f"{sz_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{sz_bytes / (1024 * 1024 * 1024):.2f} GB"

def get_file_desc(filename, parent_dir):
    fn = filename.lower()
    p = parent_dir.lower()
    
    # Root
    if 'evaluasi kritis' in fn:
        return "Dokumen ulasan kritis (critical review) dari naskah laporan penelitian"
    if 'laporan_project_akhir' in fn and fn.endswith('.docx'):
        return "Naskah laporan akhir penelitian lengkap (Word Document, format STIS)"
    if 'slide_presentasi' in fn:
        return "File presentasi PowerPoint/dokumen paparan sidang kelompok 3"
    if 'requirements.txt' in fn:
        return "Daftar pustaka Python dependencies (Streamlit, PyTorch, LightGBM, dll)"
    if '.gitignore' in fn:
        return "Konfigurasi pengabaian file Git version control"
    if 'readme' in fn:
        return "Dokumentasi umum ringkasan proyek"

    # Configs
    if 'color_palette.py' in fn:
        return "Palet warna visualisasi tematik (kelas tutupan lahan, tema botani, dashboard)"
    if 'constants.py' in fn:
        return "Konstanta global sistem: jalur folder, skema 5 kelas, band Sentinel-2, resolusi"

    # Dashboard
    if fn == 'home.py':
        return "Halaman gerbang utama (Hero page & Overview Tiga Tahap) Streamlit dashboard"
    if fn == 'theme.py':
        return "Modul tema terpadu (Forest & Botanical Clean CSS, sidebar deep green, footer bukit)"
    if '1_land_cover_maps.py' in fn:
        return "Modul 01: Peta interaktif spasiotemporal tutupan lahan Kalimantan (2019-2024)"
    if '2_change_detection.py' in fn:
        return "Modul 02: Deteksi alih fungsi lahan, matriks transisi 1,5M sel & validasi mikro KIPP 10m"
    if '3_model_comparison.py' in fn:
        return "Modul 03: Komparasi benchmark kinerja 6 model Machine Learning (Spatial Block CV)"
    if '4_driver_impact.py' in fn:
        return "Modul 04: Analisis ekonometrika spasial regresi logistik (Jarak IKN vs Densitas Tambang)"
    if '5_spatiotemporal_heatmap.py' in fn:
        return "Modul 05: Visualisasi heksagonal 3D densitas spasial pergeseran tutupan lahan"
    if '7_shap_analysis.py' in fn:
        return "Modul 06/07: Interpretabilitas model AI (SHAP value atribusi fitur optik Sentinel-2)"
    if 'mossy_hills_transparent.png' in fn:
        return "Aset grafis bukit berlumut kanopi transparan (footer halaman & kaki sidebar)"
    if 'tropical_leaves_transparent.png' in fn:
        return "Aset grafis dedaunan tropis transparan resolusi tinggi"
    if 'hero_kalimantan.jpg' in fn:
        return "Foto citra kanopi hutan rimba Kalimantan untuk banner hero dashboard"
    if 'class_distribution.json' in fn:
        return "Cache terkomputasi distribusi statistik tutupan lahan per tahun (<15ms load)"

    # Scripts
    if 'build_full_report.py' in fn:
        return "Skrip kompilasi otomatis naskah laporan Word 30+ halaman format akademik STIS"
    if 'bridge_majority_voting.py' in fn:
        return "Skrip pembangun Bridge Dataset 10 km (menghubungkan Majority Voting ke Regresi)"
    if 'dual_driver_analysis.py' in fn:
        return "Skrip pemodelan regresi logistik spasial multivariat (Deforestasi, Urbanisasi, Tambang)"
    if 'audit_all_crucial_numbers.py' in fn:
        return "Skrip verifikasi dan audit aritmatika seluruh angka kuantitatif proyek"
    if 'generate_pure_majority_voting_slide_diagram.py' in fn:
        return "Skrip pembuat diagram arsitektur alur Majority Voting Sub-Grid 500m"
    if 'generate_slide8_visuals.py' in fn:
        return "Skrip pembuat infografis visualisasi deteksi makro 1,5 juta sel Kalimantan"
    if fn.startswith('sec') and 'report_modules' in p:
        return f"Modul pembangun bab naskah laporan ({filename})"

    # Results
    if 'cm_lgbm.png' in fn:
        return "Visualisasi matriks konfusi (Confusion Matrix) model LightGBM 5-Fold CV"
    if 'predictions_lgbm.csv' in fn:
        return "Tabel prediksi out-of-fold 30.000 titik sampel ground truth untuk evaluasi"
    if 'summary_lgbm.json' in fn:
        return "Ringkasan metrik evaluasi LightGBM (OA, F1-macro, Kappa, PA, UA, IoU per kelas)"
    if 'trained_models' in p:
        return "Model machine learning serialisasi biner (.joblib/.bin) siap pakai"
    if 'logistic_' in fn and fn.endswith('.csv'):
        return "Output estimasi parameter koefisien regresi logistik spasial multivariat"
    if 'shap_importance.csv' in fn:
        return "Tabel ranking nilai mutlak rerata SHAP per fitur spektral satelit"
    if 'transition_matrix' in fn:
        return "Data/grafik matriks transisi perubahan tutupan lahan 5x5 antartahun"
    if 'temporal_profile' in fn:
        return "Profil deret waktu temporal multi-tahun tutupan lahan Kalimantan"

    # Data
    if 'predictions' in p and fn.endswith('.csv'):
        return "Dataset prediksi tutupan lahan Kalimantan (output inferensi spasial)"
    if 'global_mining_areas' in p:
        return "Dataset poligon sebaran konsesi tambang batubara global Maus et al. (2020)"
    if 'idn_adm_bps' in p:
        return "Shapefile batas administrasi wilayah Republik Indonesia (BPS 2020)"

    # Default based on extension
    if fn.endswith('.py'):
        return "Skrip program Python"
    if fn.endswith('.csv'):
        return "Dataset tabel tabular koma (CSV)"
    if fn.endswith('.parquet'):
        return "Dataset kolom terkompresi Apache Parquet (ultra-fast IO)"
    if fn.endswith('.png') or fn.endswith('.jpg'):
        return "Aset grafis / visualisasi hasil analisis"
    if fn.endswith('.json'):
        return "File konfigurasi atau ringkasan data terstruktur JSON"
    if fn.endswith('.docx'):
        return "Dokumen naskah Microsoft Word"
    if fn.endswith('.pdf'):
        return "Dokumen rujukan / laporan format PDF"
    if fn.endswith('.shp') or fn.endswith('.shx') or fn.endswith('.dbf'):
        return "Format data geospasial vektor Shapefile (ESRI)"
    if fn.endswith('.js'):
        return "Skrip kode Google Earth Engine (JavaScript Code Editor)"
    return "File data / konfigurasi penunjang proyek"


def main():
    print("Menganalisis struktur direktori secara mendalam...")
    
    total_files = 0
    total_size = 0
    dir_data = []

    for root, dirs, files in os.walk(workspace):
        dirs[:] = [d for d in sorted(dirs) if d not in exclude]
        rel_root = os.path.relpath(root, workspace)
        
        file_list = []
        d_size = 0
        for f in sorted(files):
            fp = os.path.join(root, f)
            try:
                sz = os.path.getsize(fp)
                d_size += sz
                desc = get_file_desc(f, rel_root)
                file_list.append((f, sz, desc))
            except:
                pass
                
        total_files += len(files)
        total_size += d_size
        dir_data.append((rel_root, dirs, file_list, d_size))

    print(f"Total direktori: {len(dir_data)}, Total file: {total_files}, Total ukuran: {format_size(total_size)}")
    
    # Write Markdown
    md = []
    md.append("# AUDIT LENGKAP STRUKTUR WORKING DIRECTORY")
    md.append("**Proyek Data Mining: Pemodelan Transformasi Tutupan Lahan Kalimantan (2019–2024)**  ")
    md.append(f"*Path Workspace:* `{workspace}`  ")
    md.append(f"*Waktu Audit:* `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`  ")
    md.append(f"*Total Direktori:* **{len(dir_data)} folder** | *Total File:* **{total_files} file** | *Total Kapasitas:* **{format_size(total_size)}**  ")
    md.append("\n---\n")

    md.append("## 🧭 1. EXECUTIVE SUMMARY & ARSITEKTUR WORKSPACE")
    md.append("Struktur proyek dirancang berbasis alur kerja data mining geospasial sekuensial tiga tahap:")
    md.append("1. **`configs/`**: Fondasi konfigurasi global, kamus warna tematik, band satelit Sentinel-2, dan path sistem.")
    md.append("2. **`gee_scripts/`**: Skrip ekstraksi dan reduksi citra satelit multispektral skala masif via Google Earth Engine.")
    md.append("3. **`data/`**: Data masukan mentah, shapefile batas BPS, konsesi tambang global (Maus et al.), serta hasil inferensi spasial ribuan megabyte.")
    md.append("4. **`scripts/` & `scripts/report_modules/`**: Mesin analitis Python (pelatihan 6 model ML, SHAP, Majority Voting 500m, Bridge Dataset 10km, regresi logistik spasial, dan generator otomatis naskah laporan Word).")
    md.append("5. **`results/`**: Gudang output empiris tervalidasi (bobot model `.joblib`, matriks konfusi, heatmap matriks transisi 2019-2024, tabel regresi logistik, SHAP beeswarm).")
    md.append("6. **`dashboard/`**: Antarmuka interaktif eksekutif berbasis Streamlit dengan arsitektur multi-halaman berdesain *Forest & Botanical Clean*.")
    md.append("7. **`reports/`**: Publikasi luaran resmi (naskah laporan skripsi/proyek akhir `.docx`, bahan tayang presentasi `.pptx`, infografis arsitektur, dan ringkasan audit).")
    md.append("8. **`reference/`**: Landasan teoretis jurnal terindeks Scopus/Sinta, panduan teknis, dan dokumen ilmiah rujukan.")
    md.append("9. **`_ARCHIVE/`**: Ruang isolasi historis yang menyimpan eksperimen draf lama (baseline 2018 v1, eksplorasi indeks desa IDM/IKE) agar workspace utama tetap bersih.")
    md.append("\n---\n")

    # High-level Directory Map Table
    md.append("## 📊 2. PETA DISTRIBUSI PENYIMPANAN WORKSPACE")
    md.append("| No | Folder Utama | Peran & Fungsi Utama | Jumlah File | Total Kapasitas |")
    md.append("| :-: | :--- | :--- | :-: | :-: |")
    
    # Sort top-level dirs
    top_dirs = [d for d in dir_data if d[0] == '.' or os.sep not in d[0]]
    for idx, (rel, subdirs, flist, dsz) in enumerate(sorted(top_dirs, key=lambda x: x[0])):
        name = "ROOT WORKSPACE" if rel == '.' else f"`{rel}/`"
        if rel == '.':
            role = "File eksekutif utama (Naskah Laporan FINAL, Slide Presentasi, Review, Requirements)"
        elif rel == 'dashboard':
            role = "Web App interaktif Streamlit (Home + 6 Halaman Modul + Tema Botani)"
        elif rel == 'scripts':
            role = "Pipeline kode analitis (ML, Majority Voting, Bridge, Regresi, Report Builder)"
        elif rel == 'results':
            role = "Output hasil empiris (Model biner, Confusion Matrix, Matriks Transisi, SHAP)"
        elif rel == 'data':
            role = "Dataset tabular prediksi spasial, citra satelit, batas BPS, konsesi tambang"
        elif rel == 'reports':
            role = "Arsip laporan Word final, slide paparan, infografis diagram rancangan"
        elif rel == 'configs':
            role = "Konfigurasi konstanta global dan palet warna akademik STIS"
        elif rel == 'gee_scripts':
            role = "Skrip cloud computing Google Earth Engine (JavaScript & Python API)"
        elif rel == 'reference':
            role = "Dokumen PDF jurnal ilmiah dan literatur ekonometrika spasial"
        elif rel == '_ARCHIVE':
            role = "Arsip draf lama dan eksperimen terdahulu (IDM, IKE, v1 2018)"
        else:
            role = "Direktori pendukung workspace"
            
        # calculate recursive size for top-level dir
        rec_size = sum(x[3] for x in dir_data if x[0] == rel or x[0].startswith(rel + os.sep))
        rec_files = sum(len(x[2]) for x in dir_data if x[0] == rel or x[0].startswith(rel + os.sep))
        md.append(f"| {idx+1} | **{name}** | {role} | {rec_files} file | {format_size(rec_size)} |")
        
    md.append("\n---\n")

    # Detailed Audit per Directory
    md.append("## 🔍 3. INVENTARISASI RINCI SELURUH DIREKTORI & FILE")
    
    for rel, subdirs, flist, dsz in sorted(dir_data, key=lambda x: x[0]):
        display_name = "ROOT WORKSPACE (d:\\POLSTAT STIS\\Tingkat 3\\Semester 6\\DATMIN\\Kelompok_3_v4)" if rel == '.' else f"📁 {rel}/"
        md.append(f"### {display_name}")
        md.append(f"*Sub-direktori:* `{len(subdirs)}` | *Jumlah File:* `{len(flist)}` | *Kapasitas Folder:* `{format_size(dsz)}`\n")
        
        if len(flist) == 0:
            md.append("*(Tidak ada file langsung di folder ini — hanya berisi sub-direktori)*\n")
            continue
            
        md.append("| Nama File | Ukuran | Deskripsi & Fungsi dalam Proyek |")
        md.append("| :--- | :---: | :--- |")
        for fn, sz, desc in flist:
            md.append(f"| `{fn}` | {format_size(sz)} | {desc} |")
        md.append("")

    md.append("\n---\n")
    md.append("## 🛡️ 4. CATATAN PEMELIHARAAN & KEAMANAN SISTEM")
    md.append("1. **Integritas Naskah**: Dokumen laporan komprehensif berada di `reports/Laporan_Project_Akhir_Datmin3_FINAL.docx` yang dikompilasi secara deterministik via `scripts/build_full_report.py`.")
    md.append("2. **Konsistensi Majority Voting**: Seluruh visualisasi dashboard dan naskah merujuk pada basis populasi yang sama: **1.499.024 sel grid konsensus**.")
    md.append("3. **Isolasi Folder Archive**: Seluruh file di dalam `_ARCHIVE/` tidak dipanggil oleh pipeline aktif saat ini, sehingga aman untuk tidak diikutsertakan dalam bahan presentasi.")

    with open(output_md, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))

    print(f"Berhasil membuat dokumen audit lengkap: {output_md}")

if __name__ == '__main__':
    main()
