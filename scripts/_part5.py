
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
