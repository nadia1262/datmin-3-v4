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


# HASIL DAN PEMBAHASAN
h2(doc, 'HASIL DAN PEMBAHASAN')

h4(doc, 'Kinerja Model Klasifikasi Machine Learning')
body(doc, 'Pengujian komparatif enam algoritma supervised machine learning menerapkan Spatial Block GroupKFold 5-fold. Hasil disajikan pada Tabel 2.')
tcap(doc, 'Tabel 2. Perbandingan Kinerja Model Klasifikasi')
mktable(doc, ['Model', 'N', 'Accuracy', 'F1 Macro', 'Kappa', 'Waktu (s)'], [
    ['SVM', '30.000', '0,8399', '0,8423', '0,7884', '759,9'],
    ['LightGBM', '30.000', '0,8332', '0,8347', '0,7795', '116,6'],
    ['XGBoost', '30.000', '0,8320', '0,8337', '0,7777', '189,3'],
    ['MLP', '10.000', '0,8285', '0,8328', '0,7742', '340,6'],
    ['Random Forest', '30.000', '0,8253', '0,8267', '0,7690', '449,5'],
    ['Logistic Reg.', '30.000', '0,7936', '0,7931', '0,7263', '14,6'],
])
body(doc, 'SVM mencatatkan performa tertinggi (OA 83,99%, Kappa 0,7884). LightGBM menempati posisi kedua dengan selisih akurasi 0,67 poin persentase, namun waktu pelatihannya 6,5 kali lebih cepat. LightGBM ditetapkan sebagai model operasional untuk inferensi jutaan titik grid pada enam titik temporal [28].')

tcap(doc, 'Tabel 3. Rincian Performa LightGBM per Kelas')
pc = lgbm['per_class']
t3r = []
for cls in ['Forest', 'Shrubland/Agriculture', 'Built-up', 'Bare/Mining-like', 'Water']:
    d = pc[cls]
    t3r.append([cls, f"{d['producers_accuracy']:.4f}", f"{d['users_accuracy']:.4f}", f"{d['iou']:.4f}"])
mktable(doc, ['Kelas', 'Prod. Acc.', 'User Acc.', 'IoU'], t3r)
body(doc, 'Water memiliki IoU terbaik (90,37%). Shrubland/Agriculture memiliki IoU terendah (62,74%), disebabkan tumpang tindih spektral dengan Forest pada lanskap vegetasi tropis heterogen [33]. Validasi Spatial Block CV menghasilkan Kappa 0,7601-0,7994 per-fold, setara evaluasi akhir (0,7795), menunjukkan model tidak bergantung pada autokorelasi spasial.')

h4(doc, 'Interpretasi Fitur Klasifikasi dengan SHAP')
tcap(doc, 'Tabel 4. Skor Rata-rata |SHAP| per Fitur (LightGBM)')
t4r = [[str(i+1), r['feature'], f"{r['mean_abs_shap']:.3f}"] for i, r in shap_df.iterrows()]
mktable(doc, ['Peringkat', 'Fitur', 'Mean |SHAP|'], t4r)
body(doc, 'NDVI mendominasi (skor 0,938), konsisten dengan ekspektasi fisik sebagai penentu utama klasifikasi Forest. B12 dan B11 (SWIR) menempati posisi kedua dan ketiga untuk pemisahan kelas Built-up dan Bare/Mining-like.')
body(doc, 'Catatan: NDBI berkontribusi 0,178 sedangkan NDMI hanya 0,046, padahal keduanya memiliki sinyal identik (r = -1,0). Algoritma pohon secara acak memilih salah satu representasi pada tiap simpul, sehingga kontribusi gabungan sinyal SWIR-NIR lebih besar dari yang tampak pada satu indeks saja.')
addimg(doc, os.path.join(SHAPDIR, 'shap_summary.png'), Cm(12))
fcap(doc, 'Gambar 1. SHAP Summary Plot (Beeswarm) Model LightGBM')

h4(doc, 'Deteksi Perubahan Spatiotemporal (2019-2024)')
body(doc, 'Dinamika tutupan lahan dievaluasi pada 118.943 titik Common Spatial Domain. Komposisi pada tahun awal dan akhir disajikan pada Tabel 5.')
tcap(doc, 'Tabel 5. Komposisi Tutupan Lahan pada Common Spatial Domain')
c19 = comp[comp['year']==2019].set_index('class_name')
c24 = comp[comp['year']==2024].set_index('class_name')
t5r = []
for cls in ['Forest', 'Shrubland/Agriculture', 'Built-up', 'Bare/Mining-like', 'Water']:
    p19 = c19.loc[cls, 'percentage']
    p24 = c24.loc[cls, 'percentage']
    d = p24 - p19
    s = '+' if d > 0 else ''
    t5r.append([cls, f'{p19:.2f}', f'{p24:.2f}', f'{s}{d:.2f}'])
mktable(doc, ['Kelas', '2019 (%)', '2024 (%)', 'Delta'], t5r)
body(doc, 'Forest mendominasi (72,69% di 2019, 75,54% di 2024). Fenomena net gain hutan (+2,85 pp) secara ekologis sulit dijelaskan dalam enam tahun dan mengindikasikan efek mixed-pixel pada resolusi agregasi 500 m. Area semak/pertanian yang ditumbuhi sebagian tajuk pohon cenderung teragregasi menjadi label Forest [34].')

tcap(doc, 'Tabel 6. Matriks Transisi 2019 ke 2024 (118.943 titik)')
cls5 = ['Forest', 'Shrubland/Agriculture', 'Built-up', 'Bare/Mining-like', 'Water']
t6h = ['Dari / Ke'] + [c[:10] for c in cls5]
t6r = []
for c in cls5:
    row = [c[:12]]
    for c2 in cls5:
        try:
            v = int(tmat.loc[c, c2])
            row.append(str(v))
        except:
            row.append('0')
    t6r.append(row)
mktable(doc, t6h, t6r)
body(doc, 'Forest secara dominan persisten (79.664 dari 86.464 titik, 92,1% tetap Forest). Transisi terbesar: Shrubland/Agriculture ke Forest (9.694 titik) dan Forest ke Shrubland/Agriculture (6.215 titik). Total Forest Gain (10.187) melampaui Forest Loss (6.800), konsisten dengan efek mixed-pixel.')

tcap(doc, 'Tabel 7. Konsistensi Temporal Perubahan')
t7r = [[r['category'], str(r['count']), f"{r['percentage']:.2f}%"] for _, r in cons.iterrows()]
mktable(doc, ['Kategori', 'Jumlah', 'Persen'], t7r)
body(doc, 'Hanya 67,99% titik stabil; 9,61% transisi persisten; 13,65% sementara; 8,74% fluktuatif. Proporsi fluktuatif yang besar memperkuat dugaan sebagian sinyal perubahan merupakan artefak klasifikasi akibat variasi komposisi sub-piksel dari tahun ke tahun.')

h4(doc, 'Pemetaan Skala Mikro KIPP IKN')
body(doc, 'Prediksi resolusi asli 10 m pada KIPP IKN memvalidasi perubahan berskala kecil. Detail perubahan seperti pembukaan jalan akses dan klaster bangunan baru lebih jelas terekam dibandingkan peta agregasi 500 m.')
addimg(doc, os.path.join(CLASSDIR, 'ikn_10m_map_2019.png'), Cm(13))
fcap(doc, 'Gambar 2. Peta Tutupan Lahan KIPP IKN Resolusi 10 m - 2019')
addimg(doc, os.path.join(CLASSDIR, 'ikn_10m_map_2024.png'), Cm(13))
fcap(doc, 'Gambar 3. Peta Tutupan Lahan KIPP IKN Resolusi 10 m - 2024')


h4(doc, 'Analisis Asosiasi Spasial: Regresi Logistik Multivariat')
body(doc, 'Regresi logistik multivariat diaplikasikan pada 118.943 titik Common Spatial Domain terhadap tiga variabel transisi lahan. Hasil disajikan pada Tabel 8.')
tcap(doc, 'Tabel 8. Hasil Regresi Logistik Multivariat - Tiga Model Transisi Lahan')

def fmtor(df, var):
    r = df[df['variable']==var].iloc[0]
    o = r['odds_ratio']
    pv = r['p_value']
    if pv < 0.001: ps = 'p<0,001'
    else: ps = f'p={pv:.3f}'
    st = '***' if pv<0.001 else ('**' if pv<0.01 else ('*' if pv<0.05 else 'ns'))
    return f'{o:.3f} ({ps}) {st}'

t8r = []
for v in ['distance_to_ikn', 'mining_density_10km', 'elevation', 'rainfall_annual']:
    vl = {'distance_to_ikn': 'Jarak ke IKN', 'mining_density_10km': 'Kep. Tambang 10km',
          'elevation': 'Elevasi', 'rainfall_annual': 'Curah Hujan'}[v]
    t8r.append([vl, fmtor(ld, v), fmtor(lu, v), fmtor(lm, v)])
mktable(doc, ['Variabel', 'Deforestasi OR', 'Urbanisasi OR', 'Eks. Tambang OR'], t8r)
note(doc, 'Keterangan: *** p<0,001; ** p<0,01; * p<0,05; ns = tidak signifikan.')

body(doc, 'Variabel mining_density_10km menunjukkan konsistensi tertinggi: kepadatan pertambangan dalam radius 10 km berasosiasi positif dan signifikan pada ketiga model, mengindikasikan efek cascading dari aktivitas tambang [7].')
body(doc, 'Pada model Deforestasi, koefisien jarak ke IKN bertanda positif dan signifikan (OR = 1,108; p < 0,001). Semakin jauh suatu titik dari pusat IKN, semakin tinggi peluang deforestasi. Pola ini selaras dengan konsep telecoupling [5]: kawasan inti IKN dilindungi oleh zonasi hijau perkotaan, sehingga tekanan deforestasi bergeser ke zona penyangga luar yang menyediakan kayu, material galian, dan pangan bagi proyek pembangunan.')
body(doc, 'Pola berlawanan muncul pada model Ekspansi Tambang: semakin dekat dengan IKN, semakin tinggi peluang ekspansi tambang (OR = 0,784; p < 0,001), mengindikasikan permintaan material konstruksi di sekitar IKN. Pada model Urbanisasi, jarak ke IKN tidak signifikan (p = 0,159).')
body(doc, 'Elevasi dan curah hujan konsisten berasosiasi negatif dan signifikan pada ketiga model (OR elevasi: 0,46-0,77; OR curah hujan: 0,73-0,91). Lahan rendah dan kering secara praktis lebih mudah dikonversi untuk permukiman, jalur akses, maupun aktivitas tambang.')

addimg(doc, os.path.join(DRIVERDIR, 'driver_effects.png'), Cm(14))
fcap(doc, 'Gambar 4. Efek Marginal Jarak IKN dan Kepadatan Tambang terhadap Deforestasi')

h4(doc, 'Keterbatasan Penelitian')
body(doc, 'Pertama, perbedaan resolusi (resolution mismatch) antara skala pelatihan (10 m) dan prediksi makro (500 m) menimbulkan domain shift yang teramati pada fenomena net forest gain akibat mixed-pixel [34].')
body(doc, 'Kedua, multikolinearitas sempurna NDMI-NDBI (r = -1,0) tidak memengaruhi akurasi tree-based, namun menyebabkan kepentingan SHAP terpecah antara dua indeks identik.')
body(doc, 'Ketiga, ukuran sampel besar (N = 118.943) menyebabkan standard error regresi sangat kecil, sehingga hampir semua variabel signifikan meskipun efek absolutnya tipis. Pseudo R-squared relatif kecil, menunjukkan faktor di luar model masih dominan.')
body(doc, 'Keempat, label ESA WorldCover 2021 sebagai ground truth tunggal mengandalkan asumsi temporal transferability karakteristik spektral selama enam tahun pengamatan.')

# KESIMPULAN
h2(doc, 'KESIMPULAN')
body(doc, 'Penelitian ini menunjukkan bahwa citra Sentinel-2 dan pendekatan machine learning dapat memetakan serta menganalisis transformasi tutupan lahan di Pulau Kalimantan selama periode 2019-2024. Dari enam algoritma yang dievaluasi, LightGBM dipilih sebagai model operasional (OA 83,32%, F1-Macro 83,47%, Kappa 0,7795) karena menawarkan trade-off terbaik antara akurasi dan efisiensi komputasi.')
body(doc, 'Analisis SHAP mengonfirmasi NDVI sebagai fitur paling dominan (mean |SHAP| = 0,938), diikuti band SWIR (B12, B11). Temuan ini konsisten dengan prinsip fisika optik vegetasi tropis dan memvalidasi bahwa keputusan algoritmik model sejalan dengan hukum penginderaan jauh.')
body(doc, 'Deteksi perubahan pada 118.943 titik Common Spatial Domain berhasil mengidentifikasi berbagai transisi antarkelas. Metode Majority Voting pada resolusi 500 m meningkatkan cakupan menjadi 1.499.024 sel (12 kali lipat). Namun, fenomena net forest gain mengindikasikan efek mixed-pixel pada resolusi agregasi yang perlu diinterpretasikan hati-hati.')
body(doc, 'Regresi logistik menunjukkan kepadatan pertambangan dalam radius 10 km berasosiasi positif dan signifikan dengan ketiga transisi lahan. Jarak terhadap IKN menunjukkan pola telecoupling: deforestasi lebih tinggi di wilayah jauh dari IKN (OR = 1,108), sementara ekspansi tambang meningkat di sekitar IKN (OR = 0,784). Pola ini menunjukkan dampak pembangunan IKN bersifat spasial tidak langsung dan memerlukan pemantauan berkelanjutan.')

# DAFTAR PUSTAKA
h2(doc, 'DAFTAR PUSTAKA')
refs = [
    '[1] A. Di Gregorio and L. J. M. Jansen, Land Cover Classification System (LCCS): Classification Concepts and User Manual, 2nd ed. Rome, Italy: FAO, 2005.',
    '[2] E. F. Lambin et al., "The causes of land-use and land-cover change: Moving beyond the myths," Global Environmental Change, vol. 11, no. 4, pp. 261-269, 2001.',
    '[3] Republik Indonesia, Undang-Undang Nomor 3 Tahun 2022 tentang Ibu Kota Negara. Lembaran Negara RI Tahun 2022.',
    '[4] W. F. Laurance et al., "A global strategy for road building," Nature, vol. 513, pp. 229-232, 2014.',
    '[5] P. Meyfroidt, E. F. Lambin, K.-H. Erb, and T. W. Hertel, "Globalization of land use: Distant drivers of land change and geographic displacement of land use," Current Opinion in Environmental Sustainability, vol. 5, no. 5, pp. 438-444, 2014.',
    '[6] E. F. Lambin and P. Meyfroidt, "Land use transitions: Socio-ecological feedback versus socio-economic change," Land Use Policy, vol. 27, no. 2, pp. 108-118, 2010.',
    '[7] H. Werner et al., "Patterns of infringement, risk, and impact driven by coal mining permits in Indonesia," Ambio, 2023.',
    '[8] Z. Zhu, S. Qiu, and S. Ye, "Remote sensing of land change: A multifaceted perspective," Remote Sensing of Environment, vol. 282, Art. no. 113266, 2022.',
    '[9] D. Phiri et al., "Sentinel-2 data for land cover/use mapping: A review," Remote Sensing, vol. 12, no. 14, Art. no. 2291, 2020.',
    '[10] S. Talukdar et al., "Land-use land-cover classification by machine learning classifiers for satellite observations - A review," Remote Sensing, vol. 12, no. 7, Art. no. 1135, 2020.',
    '[11] K. Karra et al., "Global land use/land cover mapping using Sentinel-2 data," 2021 IEEE IGARSS, pp. 4704-4707, 2021.',
    '[12] M. Hussain et al., "Change detection from remotely sensed images: From pixel-based to object-based approaches," ISPRS J. Photogrammetry and Remote Sensing, vol. 80, pp. 91-106, 2013.',
    '[13] Z. Zhu, C. E. Woodcock, M. Olofsson et al., "Transitioning from change detection to monitoring with remote sensing," Remote Sensing of Environment, 2019.',
    '[14] D. Zanaga et al., ESA WorldCover 10 m 2021 v200. Zenodo, 2022, doi: 10.5281/zenodo.7254220.',
    '[15] T. G. Farr et al., "The Shuttle Radar Topography Mission," Reviews of Geophysics, vol. 45, no. 2, 2007.',
    '[16] C. Funk et al., "The climate hazards infrared precipitation with stations - a new environmental record for monitoring extremes," Scientific Data, vol. 2, Art. no. 150066, 2015.',
    '[17] V. Maus et al., "An update on global mining land use," Scientific Data, vol. 9, Art. no. 433, 2022.',
    '[18] N. Gorelick et al., "Google Earth Engine: Planetary-scale geospatial analysis for everyone," Remote Sensing of Environment, vol. 202, pp. 18-27, 2017.',
    '[19] J. W. Rouse et al., "Monitoring vegetation systems in the Great Plains with ERTS," in Third ERTS Symposium, NASA SP-351, pp. 309-317, 1974.',
    '[20] Y. Zha, J. Gao, and S. Ni, "Use of normalized difference built-up index in automatically mapping urban areas from TM imagery," International J. Remote Sensing, vol. 24, no. 3, pp. 583-594, 2003.',
    '[21] B.-C. Gao, "NDWI - A normalized difference water index for remote sensing of vegetation liquid water from space," Remote Sensing of Environment, vol. 58, no. 3, pp. 257-266, 1996.',
    '[22] A. Rikimaru, P. S. Roy, and S. Miyatake, "Tropical forest cover density mapping," Tropical Ecology, vol. 43, no. 1, pp. 39-47, 2002.',
    '[23] D. R. Roberts et al., "Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure," Ecography, vol. 40, no. 8, pp. 913-929, 2017.',
    '[24] P. Ploton et al., "Spatial validation reveals poor predictive performance of large-scale ecological mapping models," Nature Communications, vol. 11, Art. no. 4540, 2020.',
    '[25] L. Breiman, "Random forests," Machine Learning, vol. 45, no. 1, pp. 5-32, 2001.',
    '[26] C. Cortes and V. Vapnik, "Support-vector networks," Machine Learning, vol. 20, no. 3, pp. 273-297, 1995.',
    '[27] T. Chen and C. Guestrin, "XGBoost: A scalable tree boosting system," Proc. 22nd ACM SIGKDD, pp. 785-794, 2016.',
    '[28] G. Ke et al., "LightGBM: A highly efficient gradient boosting decision tree," Advances in Neural Information Processing Systems, vol. 30, 2017.',
    '[29] M. Sokolova and G. Lapalme, "A systematic analysis of performance measures for classification tasks," Information Processing and Management, vol. 45, no. 4, pp. 427-437, 2009.',
    '[30] J. Cohen, "A coefficient of agreement for nominal scales," Educational and Psychological Measurement, vol. 20, no. 1, pp. 37-46, 1960.',
    '[31] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions," Advances in Neural Information Processing Systems, vol. 30, 2017.',
    '[32] Z. Zhu et al., "Remote sensing of land change: A multifaceted perspective," Remote Sensing of Environment, vol. 282, 2022.',
    '[33] D. Lu and Q. Weng, "A survey of image classification methods and techniques for improving classification performance," International J. Remote Sensing, vol. 28, no. 5, pp. 823-870, 2007.',
    '[34] D. Tuia, C. Persello, and L. Bruzzone, "Domain adaptation for the classification of remote sensing data," IEEE Geoscience and Remote Sensing Magazine, vol. 4, no. 2, pp. 41-57, 2016.',
    '[35] F. Pedregosa et al., "Scikit-learn: Machine learning in Python," Journal of Machine Learning Research, vol. 12, pp. 2825-2830, 2011.',
]
for r_text in refs:
    mkref(doc, r_text)

# SAVE
print(f'Saving to {OUTPUT}...')
doc.save(OUTPUT)
print(f'[SUCCESS] Report saved!')
print(f'File size: {os.path.getsize(OUTPUT):,} bytes')

