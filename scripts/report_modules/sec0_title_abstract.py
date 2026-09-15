from config_and_helpers import (
    add_title, add_subtitle, add_title_en, add_author_block,
    h2, h3, body, body_formatted, format_run
)
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

def build_section_0(doc):
    # Title Block (Paper-able Style)
    add_title(
        doc, 
        "TRANSFORMASI TUTUPAN LAHAN DAN SPATIAL TELECOUPLING PEMBANGUNAN IKN SERTA EKSPANSI PERTAMBANGAN DI KALIMANTAN: PENDEKATAN MACHINE LEARNING MULTI-SKALA"
    )
    add_subtitle(
        doc, 
        "Komparasi Spasial Rona Awal dan Puncak Konstruksi Menggunakan Citra Multispektral Sentinel-2"
    )
    add_title_en(
        doc, 
        "(Land-Cover Transformation and Spatial Telecoupling of Nusantara Capital City Development and Mining Expansion in Kalimantan: A Multi-Scale Machine Learning Approach)"
    )
    
    add_author_block(
        doc,
        authors="Kelompok 3: Nadia Paramita, dkk.",
        supervisor="Dosen Pengampu: Dr. Robert Kurniawan, S.Si., M.Si.",
        institution="Program Studi Komputasi Statistik, Politeknik Statistika STIS, Jakarta\nEmail Korespondensi: 222212798@stis.ac.id"
    )
    
    # ABSTRAK
    p_abs_h = doc.add_paragraph()
    p_abs_h.paragraph_format.space_before = Pt(8)
    p_abs_h.paragraph_format.space_after = Pt(3)
    p_abs_h.paragraph_format.keep_with_next = True
    r_abs_h = p_abs_h.add_run("ABSTRAK")
    format_run(r_abs_h, size_pt=11, bold=True)
    
    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.space_before = Pt(0)
    p_abs.paragraph_format.space_after = Pt(4)
    p_abs.paragraph_format.line_spacing = 1.05
    r_abs = p_abs.add_run(
        "Pulau Kalimantan merupakan bentang alam tropis strategis yang menghadapi tekanan ganda akibat mega-proyek pemindahan "
        "Ibu Kota Nusantara (IKN) dan ekspansi konsesi pertambangan batubara. Penelitian ini merancang kerangka kerja geospasial sekuensial "
        "tiga tahap (Klasifikasi → Deteksi Perubahan Berbasis Majority Voting → Asosiasi Spasial) menggunakan citra multispektral Sentinel-2 "
        "untuk membandingkan konfigurasi spasial rona awal pra-IKN (2019) dan puncak fase konstruksi fisik (2024). Tahap pertama menguji "
        "secara kompetitif enam algoritma supervised machine learning dengan protokol Spatial Block GroupKFold 5-fold pada 30.000 titik sampel "
        "murni berbasis 10 fitur spektral optik, di mana LightGBM terpilih sebagai model operasional terbaik (Overall Accuracy 83,32%, "
        "F1-Macro 0,8347, Kappa 0,7795, dan waktu pelatihan efisien 116,6 detik). Mengatasi kelemahan sampling titik tunggal yang rentan "
        "under-sampling akibat tutupan awan khatulistiwa, Tahap kedua menerapkan pendekatan agregasi spasial Majority Voting pada sel grid "
        "500 meter x 500 meter (didukung sub-grid sistematis 5x5 berisi 25 titik sampel berinterval 100 meter yang mengekstrak citra "
        "Sentinel-2 resolusi 10 meter) yang berhasil mencakup 1.499.024 sel grid valid (~1,5 juta titik) di seluruh daratan Kalimantan. "
        "Matriks transisi Majority Voting mengungkap dinamika perubahan masif pada 215.861 sel (14,40%), mencakup kehilangan hutan riil "
        "sebesar 79.777 sel (5,32%), ekspansi lahan terbuka tambang sebesar 8.075 sel (+43,4%), dan urbanisasi 14.460 sel. Untuk menghindari "
        "bias autokorelasi spasial ekstrem dan pseudo-replication pada inferensi ekonometrika, Tahap ketiga membangun Bridge Dataset "
        "sebanyak 122.478 titik sampel spasial independen (resolusi ~10 km via spatial intersection cKDTree) untuk memodelkan determinan pendorong "
        "menggunakan regresi logistik multivariat. Hasil pemodelan membuktikan bekerjanya mekanisme spatial telecoupling: deforestasi berasosiasi "
        "positif signifikan dengan jarak terhadap sentroid IKN (OR = 1,114; p < 0,001), di mana pengamanan ketat zona inti KIPP mendesak "
        "tekanan alih fungsi lahan ke koridor penyangga luar (10–50 km), sementara konsentrasi tambang (OR = 1,093; p < 0,001) memicu multiplikasi "
        "degradasi lahan di sekitarnya. Kovariat elevasi (OR = 0,462) dan curah hujan (OR = 0,906) bertindak sebagai faktor mitigasi alami. "
        "Temuan net forest gain makro didekonstruksi secara kritis sebagai efek piksel campuran dan pergeseran domain fenologis. Platform interaktif "
        "berbasis Streamlit diintegrasikan untuk mendukung tata kelola ruang presisi dan mitigasi risiko lingkungan terestrial."
    )
    format_run(r_abs, size_pt=10, bold=False)
    
    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(2)
    p_kw.paragraph_format.space_after = Pt(12)
    p_kw.paragraph_format.line_spacing = 1.05
    r_kwh = p_kw.add_run("Kata Kunci: ")
    format_run(r_kwh, size_pt=10, bold=True, italic=False)
    r_kwt = p_kw.add_run("Spatial Telecoupling, Majority Voting, Sentinel-2, LightGBM, Spatial Block Cross-Validation, Deteksi Perubahan, Ibu Kota Nusantara (IKN), Regresi Logistik Spasial.")
    format_run(r_kwt, size_pt=10, bold=False, italic=True)
    
    # ABSTRACT (English)
    p_abse_h = doc.add_paragraph()
    p_abse_h.paragraph_format.space_before = Pt(6)
    p_abse_h.paragraph_format.space_after = Pt(3)
    p_abse_h.paragraph_format.keep_with_next = True
    r_abse_h = p_abse_h.add_run("ABSTRACT")
    format_run(r_abse_h, size_pt=11, bold=True, italic=True)
    
    p_abse = doc.add_paragraph()
    p_abse.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abse.paragraph_format.space_before = Pt(0)
    p_abse.paragraph_format.space_after = Pt(4)
    p_abse.paragraph_format.line_spacing = 1.05
    r_abse = p_abse.add_run(
        "Kalimantan Island constitutes a critical tropical ecological landscape experiencing compound land-use pressures from the "
        "megaproject development of Indonesia’s new capital city (Nusantara / IKN) and the persistent expansion of coal mining concessions. "
        "This study establishes an integrated three-stage sequential geospatial framework (Classification → Majority Voting Change Detection "
        "→ Spatial Association) leveraging Sentinel-2 multispectral imagery to compare spatial configurations between baseline conditions (2019) "
        "and peak physical construction (2024). In Stage 1, six supervised machine learning algorithms were benchmarked using a 5-fold Spatial Block "
        "GroupKFold cross-validation protocol across 30,000 pure-pixel samples based on 10 optical spectral features, with LightGBM selected as "
        "the optimal operational classifier (Overall Accuracy 83.32%, F1-Macro 0.8347, Kappa 0.7795, and training time 116.6 s). Overcoming "
        "the under-sampling flaw of traditional single-pixel centroid sampling caused by equatorial cloud masking, Stage 2 deployed a 500 m "
        "sub-grid Majority Voting aggregation (a systematic 5x5 sub-grid of 25 sample points spaced 100 m apart extracting native 10 m Sentinel-2 pixels), "
        "successfully mapping 1,499,024 valid grid cells (~1.5 million points) across the island. The Majority Voting transition matrix revealed "
        "identifying 79,777 gross forest loss cells (5.32%), 8,075 newly expanded bare/mining cells (+43.4%), and 14,460 urbanization cells. "
        "To eliminate severe spatial autocorrelation and pseudo-replication in statistical modeling, Stage 3 constructed a spatially independent "
        "Bridge Dataset of 122,478 sample points (~10 km spacing via cKDTree spatial intersection) to evaluate multivariate spatial logistic regression. "
        "The empirical findings demonstrated pronounced spatial telecoupling: deforestation exhibited a statistically significant positive association "
        "with distance from the IKN centroid (OR = 1.114, p < 0.001), indicating that stringent surveillance within the core governmental precinct (KIPP) "
        "displaced land conversion pressures into outer 10–50 km buffer corridors, alongside intense local mining agglomeration (OR = 1.093, p < 0.001). "
        "Elevation (OR = 0.462) and annual rainfall (OR = 0.906) served as robust mitigating environmental covariates. The macro-scale net forest gain was "
        "critically deconstructed as an artifact of mixed-pixel heterogeneity and phenological domain shift. An interactive Streamlit monitoring platform "
        "was deployed to support precision spatial governance and sustainable terrestrial risk mitigation."
    )
    format_run(r_abse, size_pt=10, bold=False, italic=True)
    
    p_kwe = doc.add_paragraph()
    p_kwe.paragraph_format.space_before = Pt(2)
    p_kwe.paragraph_format.space_after = Pt(16)
    p_kwe.paragraph_format.line_spacing = 1.05
    r_kweh = p_kwe.add_run("Keywords: ")
    format_run(r_kweh, size_pt=10, bold=True, italic=True)
    r_kwet = p_kwe.add_run("Spatial Telecoupling, Majority Voting, Sentinel-2, LightGBM, Spatial Block Cross-Validation, Change Detection, Nusantara Capital City (IKN), Spatial Logistic Regression.")
    format_run(r_kwet, size_pt=10, bold=False, italic=True)
