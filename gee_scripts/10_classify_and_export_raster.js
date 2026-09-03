// ============================================================
// 10_classify_and_export_raster.js
// PETA RASTER PENUH — Klasifikasi Setiap Piksel Kalimantan
// ============================================================
// Tujuan: Menghasilkan peta tutupan lahan SOLID tanpa lubang (GeoTIFF)
// yang bisa dibuka di QGIS untuk gambar publikasi berkualitas tinggi.
//
// CARA PAKAI:
// 1. Copy-paste seluruh script ini ke GEE Code Editor (code.earthengine.google.com)
// 2. Klik Run
// 3. Di panel TASKS (kanan atas), klik RUN di setiap task export
// 4. Tunggu ~30-60 menit (proses di cloud GEE)
// 5. Download GeoTIFF dari Google Drive folder 'Kalimantan_LandCover_Maps'
// 6. Buka di QGIS, apply symbology warna 5 kelas
// ============================================================

// ============================================================
// BAGIAN 1: SETUP — Area & Fungsi Preprocessing
// ============================================================
var KALIMANTAN = ee.Geometry.Polygon(
  [[[108.5, 4.5], [108.5, -4.2], [119.5, -4.2], [119.5, 4.5]]], null, false);

var IKN_POINT = ee.Geometry.Point([116.847, -1.128]);

// Cloud masking (WAJIB — sama dengan skrip training)
function maskS2clouds(image) {
  var qa = image.select('QA60');
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
    .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
  return image.updateMask(mask).divide(10000);
}

// Buat composite tahunan (lebih fleksibel — coba semua bulan)
function getComposite(year) {
  return ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(KALIMANTAN)
    .filterDate(year + '-01-01', year + '-12-31')
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30)) // sedikit longgar untuk tutup gap
    .map(maskS2clouds)
    .select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12'])
    .median()
    .clip(KALIMANTAN);
}

// Hitung semua indeks spektral
function addIndices(img) {
  var ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI');
  var ndbi = img.normalizedDifference(['B11', 'B8']).rename('NDBI');
  var ndmi = img.normalizedDifference(['B8', 'B11']).rename('NDMI');
  var bsi = img.expression(
    '((SWIR1 + RED) - (NIR + BLUE)) / ((SWIR1 + RED) + (NIR + BLUE))',
    {'SWIR1': img.select('B11'), 'RED': img.select('B4'),
     'NIR': img.select('B8'),  'BLUE': img.select('B2')}
  ).rename('BSI');
  return img.addBands([ndvi, ndbi, ndmi, bsi]);
}

// Feature stack untuk klasifikasi (10 fitur — SAMA dengan Python model)
var FEATURE_BANDS = ['B2', 'B3', 'B4', 'B8', 'B11', 'B12', 'NDVI', 'NDBI', 'NDMI', 'BSI'];

// ============================================================
// BAGIAN 2: TRAINING DATA — ESA WorldCover 2021 sebagai Label
// ============================================================
// Reklasifikasi WorldCover ke 5 kelas kita (sama persis dengan training Python)
var worldcover = ee.ImageCollection("ESA/WorldCover/v200").first().clip(KALIMANTAN);

var remapped = worldcover.remap(
  [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100],  // kode asli ESA
  [ 0,  1,  1,  1,  2,  3,  3,  4,  0,  0,   1]   // ke kelas kita
).rename('land_cover_class').toByte();

// Ambil composite 2021 (tahun yang dipakai untuk training)
var composite2021 = getComposite('2021');
var features2021  = addIndices(composite2021);

// Stratified sample: 5000 titik per kelas = 25,000 total
var trainingData = features2021.addBands(remapped)
  .stratifiedSample({
    numPoints: 5000,
    classBand: 'land_cover_class',
    region: KALIMANTAN,
    scale: 100,
    seed: 42,
    dropNulls: true,
    tileScale: 8
  });

print('Training samples count:', trainingData.size());

// ============================================================
// BAGIAN 3: TRAINING MODEL GEE (Random Forest)
// ============================================================
// Catatan: GEE tidak bisa menjalankan LightGBM (Python).
// Kita pakai RF bawaan GEE — akurasinya hampir sama.
var classifier = ee.Classifier.smileRandomForest({
  numberOfTrees: 200,
  seed: 42
}).train({
  features: trainingData,
  classProperty: 'land_cover_class',
  inputProperties: FEATURE_BANDS
});

// Cek akurasi training (OOB estimate)
var trainAccuracy = classifier.confusionMatrix();
print('Training Overall Accuracy:', trainAccuracy.accuracy());

// ============================================================
// BAGIAN 4: KLASIFIKASI SELURUH KALIMANTAN PER TAHUN
// ============================================================
// Daftar tahun yang ingin diekspor
var YEARS = ['2021', '2022', '2023', '2024'];

// Palette warna 5 kelas (untuk preview di Code Editor)
var VIS_PALETTE = {
  min: 0, max: 4,
  palette: [
    '1B7837',  // 0: Forest — hijau tua
    'A6D96A',  // 1: Shrubland/Agriculture — hijau muda
    'E31A1C',  // 2: Built-up — merah
    'C4A35A',  // 3: Bare/Mining-like — coklat
    '2166AC'   // 4: Water — biru
  ]
};

// Class names untuk legenda
var CLASS_NAMES = ['Forest', 'Shrubland/Agriculture', 'Built-up', 'Bare/Mining-like', 'Water'];

// Loop per tahun: klasifikasi + tampilkan + ekspor
YEARS.forEach(function(year) {
  // 1. Buat feature stack tahun tersebut
  var composite = getComposite(year);
  var featureStack = addIndices(composite).select(FEATURE_BANDS);

  // 2. Klasifikasi setiap piksel
  var classified = featureStack.classify(classifier).rename('land_cover');

  // 3. Tampilkan di peta preview Code Editor
  Map.addLayer(classified, VIS_PALETTE, 'Land Cover ' + year, false);

  // 4. Export GeoTIFF ke Google Drive
  Export.image.toDrive({
    image: classified,
    description: 'landcover_kalimantan_' + year,
    folder: 'Kalimantan_LandCover_Maps',
    fileNamePrefix: 'landcover_kalimantan_' + year,
    region: KALIMANTAN,
    scale: 250,          // 250m per piksel — balance antara detail & ukuran file
    crs: 'EPSG:4326',
    maxPixels: 1e10,
    fileFormat: 'GeoTIFF'
  });
});

// Tampilkan peta 2024 secara default
var composite2024  = getComposite('2024');
var featureStack24 = addIndices(composite2024).select(FEATURE_BANDS);
var classified2024 = featureStack24.classify(classifier);
Map.addLayer(classified2024, VIS_PALETTE, 'Land Cover 2024 (Default)', true);

// Center peta ke Kalimantan
Map.centerObject(KALIMANTAN, 6);

// ============================================================
// BAGIAN 5: INSTRUKSI BUKA DI QGIS
// ============================================================
// Setelah GeoTIFF terdownload, buka di QGIS:
// 1. Drag-drop file .tif ke QGIS
// 2. Klik kanan layer -> Properties -> Symbology
// 3. Render type: "Paletted/Unique values"
// 4. Klik "Classify" -> hapus kelas yang tidak perlu
// 5. Set warna manual:
//    Nilai 0 -> #1B7837 (Forest)
//    Nilai 1 -> #A6D96A (Shrubland/Agriculture)
//    Nilai 2 -> #E31A1C (Built-up)
//    Nilai 3 -> #C4A35A (Bare/Mining-like)
//    Nilai 4 -> #2166AC (Water)
// 6. Tambahkan: North Arrow, Scale Bar, Legend
// 7. Export: Project -> Import/Export -> Export Map to Image
//    Resolution: 300 DPI untuk publikasi

print('=== EXPORT TASKS READY ===');
print('Klik tab "Tasks" di kanan atas, lalu klik RUN untuk setiap task.');
print('Estimasi waktu: 30-90 menit per tahun (tergantung antrian GEE).');
