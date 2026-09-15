import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
from docx import Document
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

PROJECT = r'd:\POLSTAT STIS\Tingkat 3\Semester 6\DATMIN\Kelompok_3_v4'
TEMPLATE = os.path.join(PROJECT, 'reports', 'Template.docx')
OUTPUT = os.path.join(PROJECT, 'reports', 'Laporan_Project_Akhir_Datmin3_FINAL.docx')
CLASSDIR = os.path.join(PROJECT, 'results', 'classification')
CHANGEDIR = os.path.join(PROJECT, 'results', 'change_maps_v2')
DRIVERDIR = os.path.join(PROJECT, 'results', 'driver_analysis_v2')
SHAPDIR = os.path.join(PROJECT, 'results', 'shap', 'lgbm')

def _apply_style(p, style_id):
    """Apply style via XML to avoid latent style lookup issues."""
    pPr = p._element.get_or_add_pPr()
    pStyle = pPr.find(qn('w:pStyle'))
    if pStyle is None:
        pStyle = OxmlElement('w:pStyle')
        pPr.insert(0, pStyle)
    pStyle.set(qn('w:val'), style_id)

def body(doc, text, indent=0.75):
    p = doc.add_paragraph()
    _apply_style(p, 'BodyText')
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.space_after = Pt(6)
    if indent: pf.first_line_indent = Cm(indent)
    return p

def h2(doc, t):
    p = doc.add_paragraph()
    _apply_style(p, 'Heading2')
    r = p.add_run(t.upper()); r.font.name='Times New Roman'; r.font.size=Pt(12); r.bold=True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12); p.paragraph_format.space_after = Pt(6)

def h3(doc, t):
    p = doc.add_paragraph()
    _apply_style(p, 'Heading3')
    r = p.add_run(t); r.font.name='Times New Roman'; r.font.size=Pt(12); r.bold=True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(6)

def h4(doc, t):
    p = doc.add_paragraph()
    _apply_style(p, 'Heading4')
    r = p.add_run(t); r.font.name='Times New Roman'; r.font.size=Pt(11); r.bold=True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(6)

def tcap(doc, t):
    p = doc.add_paragraph()
    _apply_style(p, 'BodyText')
    r = p.add_run(t); r.font.name='Times New Roman'; r.font.size=Pt(11); r.bold=True
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(3)

def fcap(doc, t):
    p = doc.add_paragraph()
    _apply_style(p, 'BodyText')
    r = p.add_run(t); r.font.name='Times New Roman'; r.font.size=Pt(11); r.bold=True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(3); p.paragraph_format.space_after = Pt(6)

def note(doc, t):
    p = doc.add_paragraph()
    _apply_style(p, 'BodyText')
    r = p.add_run(t); r.font.name='Times New Roman'; r.font.size=Pt(9); r.italic=True

def mktable(doc, headers, rows):
    t = doc.add_table(rows=len(rows)+1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(headers):
        c = t.rows[0].cells[j]; c.text = ''
        r = c.paragraphs[0].add_run(h); r.font.name='Times New Roman'; r.font.size=Pt(10); r.bold=True
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = t.rows[i+1].cells[j]; c.text = ''
            r = c.paragraphs[0].add_run(str(val)); r.font.name='Times New Roman'; r.font.size=Pt(10)
            c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

def addimg(doc, path, w=Cm(13)):
    if os.path.exists(path):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(path, width=w)

def centered(doc, text, sz=11, bold=False, italic=False):
    p = doc.add_paragraph()
    _apply_style(p, 'BodyText')
    r = p.add_run(text); r.font.name='Times New Roman'; r.font.size=Pt(sz); r.bold=bold; r.italic=italic
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

def mkref(doc, t):
    p = doc.add_paragraph()
    _apply_style(p, 'BodyText')
    r = p.add_run(t); r.font.name='Times New Roman'; r.font.size=Pt(11)
    pf = p.paragraph_format; pf.space_before=Pt(0); pf.space_after=Pt(3)
    pf.left_indent=Cm(0.75); pf.first_line_indent=Cm(-0.75)

# ---- LOAD DATA ----
print('Loading data...')
with open(os.path.join(CLASSDIR, 'summary_lgbm.json')) as f: lgbm = json.load(f)
comp = pd.read_csv(os.path.join(CHANGEDIR, 'common_domain_composition.csv'))
cons = pd.read_csv(os.path.join(CHANGEDIR, 'temporal_consistency_summary.csv'))
tmat = pd.read_csv(os.path.join(CHANGEDIR, 'transition_matrix_2019_2024.csv'), index_col=0)
shap_df = pd.read_csv(os.path.join(SHAPDIR, 'shap_importance.csv'))
ld = pd.read_csv(os.path.join(DRIVERDIR, 'logistic_forest_loss_2019_2024.csv'))
lu = pd.read_csv(os.path.join(DRIVERDIR, 'logistic_urbanization_2019_2024.csv'))
lm = pd.read_csv(os.path.join(DRIVERDIR, 'logistic_mining_expansion_2019_2024.csv'))
print('Data loaded.')

doc = Document(TEMPLATE)
for p in doc.paragraphs[:]: p._element.getparent().remove(p._element)
for t in doc.tables[:]: t._element.getparent().remove(t._element)

# TITLE
centered(doc, 'Analisis Spatiotemporal Transformasi Tutupan Lahan di Pulau Kalimantan (2019-2024): Integrasi Machine Learning, Majority Voting, dan Regresi Logistik untuk Mengidentifikasi Pola Perubahan Terkait Pembangunan IKN dan Ekspansi Pertambangan', sz=14, bold=True)
centered(doc, '(Spatiotemporal Analysis of Land Cover Transformation in Kalimantan Island (2019-2024): Integration of Machine Learning, Majority Voting, and Logistic Regression to Identify Change Patterns Related to IKN Development and Mining Expansion)', sz=12, italic=True)
centered(doc, 'Kelompok 3 - Komputasi Statistik', sz=11)
centered(doc, 'Dosen Pengampu: Robert Kurniawan', sz=11)

# ABSTRAK
h2(doc, 'ABSTRAK')
body(doc, 'Penelitian ini menganalisis transformasi tutupan lahan di Pulau Kalimantan selama periode 2019-2024 menggunakan citra Sentinel-2 dan algoritma machine learning. Enam algoritma dievaluasi melalui Spatial Block GroupKFold Cross-Validation; LightGBM dipilih sebagai model operasional (Overall Accuracy 83,32%%, F1-Macro 83,47%%, Kappa 0,7795). Deteksi perubahan dilakukan pada domain spasial bersama (118.943 titik grid 500 m) dan diperkuat dengan metode Majority Voting pada resolusi 500 m (1.499.024 sel). Analisis regresi logistik multivariat terhadap tiga transisi lahan menunjukkan bahwa kepadatan pertambangan dalam radius 10 km berasosiasi positif dan signifikan pada ketiga model. Jarak terhadap IKN menunjukkan pola telecoupling: deforestasi justru meningkat di wilayah yang lebih jauh dari pusat IKN (OR = 1,108; p < 0,001). Analisis SHAP mengonfirmasi NDVI sebagai fitur paling dominan dalam klasifikasi (mean |SHAP| = 0,938).', indent=0)
p = doc.add_paragraph()
_apply_style(p, 'BodyText')
r = p.add_run('Kata kunci: '); r.font.name='Times New Roman'; r.font.size=Pt(10); r.bold=True
r = p.add_run('tutupan lahan, machine learning, LightGBM, deforestasi, IKN, SHAP'); r.font.name='Times New Roman'; r.font.size=Pt(10)

h3(doc, 'ABSTRACT')
body(doc, 'This study analyzes land cover transformation in Kalimantan Island during 2019-2024 using Sentinel-2 imagery and machine learning. Six algorithms were evaluated through Spatial Block GroupKFold Cross-Validation; LightGBM was selected as the operational model (OA 83.32%%, F1-Macro 83.47%%, Kappa 0.7795). Change detection was performed on a common spatial domain (118,943 grid points at 500 m) and enhanced by Majority Voting at 500 m resolution (1,499,024 cells). Multivariate logistic regression showed mining density within 10 km was consistently positively associated with all three land transitions. Distance to IKN exhibited a telecoupling pattern: deforestation increased farther from IKN (OR = 1.108, p < 0.001). SHAP confirmed NDVI as the most dominant feature (mean |SHAP| = 0.938).', indent=0)
p = doc.add_paragraph()
_apply_style(p, 'BodyText')
r = p.add_run('Keywords: '); r.font.name='Times New Roman'; r.font.size=Pt(10); r.bold=True
r = p.add_run('land cover, machine learning, LightGBM, deforestation, IKN, SHAP'); r.font.name='Times New Roman'; r.font.size=Pt(10)

# PENDAHULUAN
h2(doc, 'PENDAHULUAN')
body(doc, 'Kalimantan merupakan salah satu pulau terbesar di Indonesia yang menyimpan kawasan hutan tropis, lahan gambut, jaringan sungai, serta sumber daya mineral dalam jumlah besar. Sebagian besar wilayahnya masih berupa hutan lahan kering primer dan sekunder yang memiliki nilai ekologis tinggi sebagai penyimpan karbon, habitat biodiversitas, dan pengatur siklus hidrologi regional [1]. Namun, dalam beberapa dekade terakhir, Kalimantan mengalami tekanan perubahan tutupan lahan yang intensif akibat konversi hutan untuk perkebunan, pertambangan, dan pembangunan infrastruktur [2].')
body(doc, 'Salah satu perubahan signifikan terjadi setelah pemerintah menetapkan lokasi Ibu Kota Nusantara (IKN) pada 2019 di Kalimantan Timur, yang diperkuat melalui Undang-Undang Nomor 3 Tahun 2022 tentang Ibu Kota Negara [3]. Pembangunan kawasan pemerintahan baru merupakan proyek infrastruktur skala besar yang dapat memicu konversi lahan secara langsung melalui pembukaan kawasan inti, maupun secara tidak langsung melalui peningkatan aksesibilitas dan permintaan material konstruksi di wilayah penyangga [4]. Pengaruh pembangunan berskala besar terhadap wilayah di luar lokasi proyek dikenal dalam literatur sebagai telecoupling [5].')
body(doc, 'Selain pembangunan IKN, aktivitas pertambangan turut menjadi bagian penting dari dinamika pemanfaatan lahan di Kalimantan. Kegiatan pertambangan tergolong proximate driver yang dapat menyebabkan hilangnya tutupan hutan secara langsung melalui pembukaan lahan untuk area galian, serta secara tidak langsung melalui pembangunan jalan akses dan permukiman pekerja di sekitar konsesi [6], [7].')
body(doc, 'Luasnya wilayah Kalimantan menjadikan survei lapangan konvensional kurang memadai untuk memantau perubahan tutupan lahan secara menyeluruh. Penginderaan jauh menyediakan alternatif pemantauan yang mampu merekam kondisi permukaan bumi secara berulang pada cakupan wilayah luas [8]. Citra Sentinel-2 dipilih sebagai sumber data utama karena memiliki resolusi spasial tinggi (10 m), kanal red-edge yang sensitif terhadap kerapatan vegetasi tropis, serta waktu kunjungan ulang yang singkat [9]. Informasi spektral diolah menggunakan algoritma machine learning untuk menghasilkan peta tutupan lahan [10], [11].')
body(doc, 'Peta tutupan lahan pada setiap tahun pengamatan dibandingkan melalui post-classification comparison untuk mengidentifikasi lokasi dan arah perubahan [12]. Penelitian ini menggunakan regresi logistik multivariat guna mengukur keterkaitan statistik antara faktor antropogenik (jarak ke IKN dan kepadatan pertambangan) dengan probabilitas perubahan tutupan lahan, setelah mengontrol faktor topografi dan iklim [13].')

h4(doc, 'Rumusan Masalah')
body(doc, '1. Bagaimana pola perubahan luas dan distribusi kelas tutupan lahan di Pulau Kalimantan selama periode 2019-2024 berdasarkan hasil klasifikasi citra Sentinel-2?')
body(doc, '2. Bagaimana pola spasial perubahan tutupan lahan bervariasi antara skala makro (seluruh Kalimantan) dan skala mikro (KIPP IKN)?')
body(doc, '3. Sejauh mana jarak terhadap pusat IKN dan kepadatan aktivitas pertambangan berkontribusi terhadap probabilitas perubahan tutupan lahan, setelah memperhitungkan variabel elevasi dan curah hujan?')
body(doc, '4. Bagaimana kinerja algoritma machine learning dalam mengklasifikasikan tutupan lahan, dan fitur prediktor mana yang paling berkontribusi?')

h4(doc, 'Tujuan Penelitian')
body(doc, '1. Mengidentifikasi dan mengklasifikasikan tutupan lahan Pulau Kalimantan menggunakan citra Sentinel-2 dan algoritma machine learning pada periode 2019-2024.')
body(doc, '2. Menganalisis perubahan tutupan lahan secara temporal pada skala makro (seluruh Kalimantan, 500 m) dan skala mikro (KIPP IKN, 10 m).')
body(doc, '3. Mengukur asosiasi antara jarak terhadap pusat IKN dan kepadatan pertambangan terhadap probabilitas perubahan tutupan lahan melalui regresi logistik multivariat.')
body(doc, '4. Mengevaluasi kinerja enam algoritma machine learning dan menginterpretasikan kontribusi fitur prediktor menggunakan SHAP.')

h4(doc, 'Ruang Lingkup dan Batasan')
body(doc, '1. Wilayah penelitian mencakup seluruh daratan Pulau Kalimantan untuk analisis skala makro, dengan fokus mikro pada KIPP IKN.')
body(doc, '2. Periode pengamatan 2019-2024; tahun 2018 hanya digunakan sebagai referensi awal.')
body(doc, '3. Kelas tutupan lahan: 5 kelas reklasifikasi ESA WorldCover 2021 (Forest, Shrubland/Agriculture, Built-up, Bare/Mining-like, Water) [14].')
body(doc, '4. Fitur input klasifikasi (Tahap 1): 10 fitur spektral optik (B2, B3, B4, B8, B11, B12, NDVI, NDBI, NDMI, BSI). Variabel elevasi dan curah hujan TIDAK digunakan dalam klasifikasi, melainkan hanya sebagai kovariat kontrol pada Tahap 3.')
body(doc, '5. Seluruh hasil regresi logistik melaporkan asosiasi statistik, bukan hubungan kausalitas.')

# METODE
h2(doc, 'METODE')
body(doc, 'Secara konseptual, penelitian ini merangkai tiga tahapan analisis geospasial sekuensial: Klasifikasi, Perubahan, dan Asosiasi. Pertama, tutupan lahan diklasifikasikan dari citra satelit (Tahap 1). Kedua, peta hasil klasifikasi dibandingkan melalui dua pendekatan: Common Spatial Domain pada grid 10 km dan Majority Voting pada resolusi 500 m (Tahap 2). Ketiga, diuji asosiasi spasial dengan jarak ke IKN dan kepadatan tambang menggunakan regresi logistik (Tahap 3). Akuisisi data dilakukan melalui Google Earth Engine, pelatihan model dan analisis statistik menggunakan Python.')

h4(doc, 'Data dan Sumber Data')
body(doc, 'Analisis difokuskan pada daratan Pulau Kalimantan, dengan lokus mikro di KIPP IKN. Sumber data geospasial disajikan pada Tabel 1.')
tcap(doc, 'Tabel 1. Sumber Data Penelitian')
mktable(doc, ['No', 'Data', 'Sumber', 'Resolusi', 'Keterangan'], [
    ['1', 'Citra Sentinel-2 SR', 'Google Earth Engine', '10 m', '6 band spektral'],
    ['2', 'Label Referensi', 'ESA WorldCover 2021', '10 m', '5 kelas [14]'],
    ['3', 'Elevasi', 'SRTM v3', '30 m', 'Kovariat Tahap 3 [15]'],
    ['4', 'Curah Hujan', 'CHIRPS', '~5 km', 'Kovariat Tahap 3 [16]'],
    ['5', 'Poligon Tambang', 'Maus et al. (2022)', 'Vektor', 'Prediktor Tahap 3 [17]'],
    ['6', 'Sentroid IKN', 'UU No. 3/2022', 'Titik', 'Jarak euklidean'],
])

h4(doc, 'Pra-pemrosesan dan Rekayasa Fitur')
body(doc, 'Pra-pemrosesan citra Sentinel-2 diawali dengan cloud masking menggunakan QA60 untuk mengeliminasi observasi terkontaminasi awan tebal. Deret waktu yang telah dibersihkan diagregasi menggunakan median temporal compositing untuk menghasilkan satu citra representatif tahunan per piksel [18].')
body(doc, 'Dari komposit median tahunan, diekstraksi enam pita spektral optik (B2, B3, B4, B8, B11, B12) dan empat indeks spektral turunan:')
body(doc, 'NDVI = (B8 - B4) / (B8 + B4) [19]', indent=1.5)
body(doc, 'NDBI = (B11 - B8) / (B11 + B8) [20]', indent=1.5)
body(doc, 'NDMI = (B8 - B11) / (B8 + B11) [21]', indent=1.5)
body(doc, 'BSI = ((B11 + B4) - (B8 + B2)) / ((B11 + B4) + (B8 + B2)) [22]', indent=1.5)
body(doc, 'NDBI dan NDMI memiliki korelasi negatif sempurna (r = -1,000) karena merupakan negasi satu sama lain. Kedua indeks tetap dipertahankan untuk menguji ketahanan model tree-based terhadap redundansi. Total fitur klasifikasi (Tahap 1): 10 fitur spektral optik. Variabel elevasi dan curah hujan TIDAK digunakan sebagai fitur klasifikasi, melainkan hanya sebagai kovariat kontrol pada Tahap 3.')

h4(doc, 'Tahap 1: Klasifikasi Tutupan Lahan')
body(doc, 'Label referensi dari ESA WorldCover 2021 direklasifikasi menjadi 5 kelas: Forest, Shrubland/Agriculture, Built-up, Bare/Mining-like, dan Water. Sebanyak 30.000 titik sampel berskala 10 m diekstrak menggunakan stratified random sampling dengan oversampling kelas minoritas [14].')
body(doc, 'Validasi: Spatial Block GroupKFold CV dengan blok 0,5 x 0,5 derajat (~55 km x 55 km), K = 5 fold [23], [24]. Enam algoritma dievaluasi: Logistic Regression, Random Forest [25], SVM [26], XGBoost [27], LightGBM [28], MLP. Optimasi hyperparameter melalui Grid Search dengan 3-fold GroupKFold. Metrik: Overall Accuracy, Macro F1, Kappa [29], [30], IoU.')
body(doc, 'Prediksi spasial pada dua skala: (a) Makro 500 m untuk seluruh Kalimantan, (b) Mikro 10 m khusus KIPP IKN. Interpretasi fitur menggunakan SHAP TreeExplainer [31].')

h4(doc, 'Tahap 2: Deteksi Perubahan Tutupan Lahan')
body(doc, 'Deteksi perubahan menggunakan Common Spatial Domain: 118.943 titik grid 500 m yang konsisten bebas awan di seluruh tahun pengamatan [32]. Matriks transisi C berdimensi 5x5 dihasilkan. Tiga variabel dependen biner diturunkan: Forest Loss (Y1), Urbanization (Y2), Mining Expansion (Y3).')

h4(doc, 'Agregasi Majority Voting')
body(doc, 'Untuk mengatasi kelemahan metode Centroid (apabila piksel centroid tertutup awan, seluruh blok gugur), penelitian ini mengadopsi Majority Voting pada resolusi 500 m. Setiap sel grid 500 m x 500 m didekomposisi menjadi sub-grid 5x5 (25 sub-piksel). Kelas ditentukan melalui majority vote. Selama minimal satu sub-piksel valid, sel tetap dipertahankan.')
body(doc, 'Metode ini menghasilkan 1.499.024 sel grid valid (12 kali lipat dari metode Centroid). Implementasi: (a) ekstraksi sub-grid di GEE per provinsi, (b) agregasi majority voting menggunakan pandas.')

h4(doc, 'Tahap 3: Analisis Asosiasi Spasial (Regresi Logistik)')
body(doc, 'Probabilitas transisi lahan dimodelkan melalui fungsi logit:')
centered(doc, 'ln(P/(1-P)) = B0 + B1*X1 + B2*X2 + B3*X3 + B4*X4', italic=True)
body(doc, 'di mana P = probabilitas transisi; X1 = jarak ke IKN; X2 = kepadatan tambang 10 km [17]; X3 = elevasi [15]; X4 = curah hujan [16]. Seluruh variabel di-StandardScaler. Interpretasi menggunakan Odds Ratio (OR = exp(B)). Seluruh kerangka pemodelan merupakan analisis asosiasi spasial, bukan inferensi kausal.', indent=0)
