// ============================================================
// 12_majority_voting_grid.js (v3 — SPLIT BY PROVINCE)
// ============================================================
// TUJUAN: Menggantikan Systematic Point Sampling (centroid-only)
// dengan Sub-grid 5x5 (25 titik per sel 500m) agar bisa dilakukan
// Majority Voting yang jauh lebih representatif.
//
// v3 FIXES:
// - SPLIT per provinsi agar tidak crash "Computed value is too large"
// - HAPUS mining_density_10km (reduceNeighborhood 10km = penyebab crash)
//   → dual_driver_analysis.py sudah pakai mining_density_maus.csv
// - TETAP sertakan elevation, rainfall, distance_to_ikn (ringan, untuk Tahap 3)
// - geometries: false (koordinat via pixelLonLat band)
// ============================================================

// --- Study Area (Kalimantan Bounding Box for clipping composites) ---
var KALIMANTAN = ee.Geometry.Polygon(
  [[[108.5, 4.5], [108.5, -4.2], [119.5, -4.2], [119.5, 4.5]]], null, false);

// --- Provinsi di Kalimantan yang TERSEDIA di FAO/GAUL/2015/level1 ---
// CATATAN: Kalimantan Utara TIDAK ada di FAO GAUL karena baru dibentuk 2012.
// Kaltara ditangani terpisah menggunakan Bounding Box manual (lihat bagian bawah).
var PROVINCES = [
  'Kalimantan Barat',
  'Kalimantan Tengah',
  'Kalimantan Selatan',
  'Kalimantan Timur'
];

// Bounding Box manual untuk Kalimantan Utara
// (approx: lon 114.5-118.5, lat 1.0-4.3)
var KALTARA_BBOX = ee.Geometry.Rectangle([114.5, 1.0, 118.5, 4.3]);

var INDO_PROV = ee.FeatureCollection("FAO/GAUL/2015/level1")
  .filter(ee.Filter.eq('ADM0_NAME', 'Indonesia'));

// --- Constants ---
var CLOUD_THRESHOLD = 20;
var CELL_SIZE = 500;        // Ukuran sel grid (meters)
var SUBGRID_SCALE = 100;    // Resolusi sub-grid (meters) -> 500/100 = 5x5 = 25 titik per sel

// ============================================================
// FUNCTIONS (dari 00_utils.js — KEEP IN SYNC)
// ============================================================

function maskS2clouds(image) {
  var qa = image.select('QA60');
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
    .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
  return image.updateMask(mask).divide(10000);
}

function getComposite(year) {
  return ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(KALIMANTAN)
    .filterDate(year + '-01-01', year + '-12-31')
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', CLOUD_THRESHOLD))
    .map(maskS2clouds)
    .select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12'])
    .median()
    .clip(KALIMANTAN);
}

function addIndices(s2) {
  var ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI');
  var ndbi = s2.normalizedDifference(['B11', 'B8']).rename('NDBI');
  var ndmi = s2.normalizedDifference(['B8', 'B11']).rename('NDMI');
  var bsi = s2.expression(
    '((SWIR1 + RED) - (NIR + BLUE)) / ((SWIR1 + RED) + (NIR + BLUE))', {
      'SWIR1': s2.select('B11'),
      'RED':   s2.select('B4'),
      'NIR':   s2.select('B8'),
      'BLUE':  s2.select('B2')
    }).rename('BSI');
  return s2.addBands([ndvi, ndbi, ndmi, bsi]);
}

// ============================================================
// CELL ID GENERATOR
// ============================================================
function getCellId() {
  var lonLat = ee.Image.pixelLonLat();
  var cellSizeDeg = CELL_SIZE / 111320;
  var cell_col = lonLat.select('longitude').divide(cellSizeDeg).floor();
  var cell_row = lonLat.select('latitude').divide(cellSizeDeg).floor().add(20000);
  return cell_col.multiply(100000).add(cell_row)
    .rename('cell_id')
    .toLong();
}

// ============================================================
// EXPORT FUNCTION PER PROVINCE & YEAR
// ============================================================
function exportProvinceSubgrid(year, provName) {
  var provGeom = INDO_PROV.filter(ee.Filter.eq('ADM1_NAME', provName)).geometry();
  exportWithRegion(year, provGeom, provName.replace(/ /g, '_'));
}

// Export menggunakan Bounding Box (untuk Kaltara)
function exportBBoxSubgrid(year, bbox, label) {
  exportWithRegion(year, bbox, label);
}

// Core export logic (dipakai oleh kedua fungsi di atas)
function exportWithRegion(year, region, label) {

  var s2 = getComposite(year);
  var s2_idx = addIndices(s2);

  // --- Fitur untuk LightGBM classifier (10 spektral) ---
  // --- Plus ancillary drivers untuk dual_driver_analysis.py (Tahap 3) ---
  // CATATAN: mining_density_10km SENGAJA TIDAK diikutkan karena:
  //   1. reduceNeighborhood(10km kernel) menyebabkan GEE crash
  //   2. dual_driver_analysis.py sudah pakai sumber tersendiri (mining_density_maus.csv)
  var cell_id = getCellId();
  var lonLat = ee.Image.pixelLonLat();

  // Layer ringan (TIDAK menyebabkan crash)
  var elevation = ee.Image('USGS/SRTMGL1_003').select('elevation').clip(KALIMANTAN);
  var rainfall = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
    .filterDate(year + '-01-01', year + '-12-31')
    .sum().rename('rainfall_annual').clip(KALIMANTAN);
  var ikn_dist = (function() {
    var ll = ee.Image.pixelLonLat();
    var R = 6371;
    var dx = ll.select('longitude').subtract(116.847).multiply(Math.PI / 180).multiply(R);
    var dy = ll.select('latitude').subtract(-1.128).multiply(Math.PI / 180).multiply(R);
    return dx.pow(2).add(dy.pow(2)).sqrt().rename('distance_to_ikn').clip(KALIMANTAN);
  })();

  var stack = s2_idx.addBands([cell_id, lonLat, elevation, rainfall, ikn_dist]);

  var grid = stack.sample({
    region: region,             // Bisa berupa provGeom atau KALTARA_BBOX
    scale: SUBGRID_SCALE,       // 100m = 5x5 sub-grid per 500m cell
    geometries: false,          // Koordinat sudah ada di lonLat bands
    dropNulls: true,
    seed: 42,
    numPixels: 1000000,         // 1M titik per provinsi (sangat aman)
    tileScale: 16               // Prevent memory limit exceeded
  });

  var taskName = 'mv_' + year + '_' + label;

  Export.table.toDrive({
    collection: grid,
    description: taskName,
    folder: 'Kalimantan_MajorityVoting',
    fileFormat: 'CSV'
  });

  print('Task created: ' + taskName);
}

// ============================================================
// EXPORT: 2019 & 2024 x 5 PROVINSI = 10 TASKS
// ============================================================
PROVINCES.forEach(function(prov) {
  exportProvinceSubgrid(2019, prov);
  exportProvinceSubgrid(2024, prov);
});

// Kalimantan Utara — menggunakan Bounding Box karena tidak ada di FAO GAUL 2015
exportBBoxSubgrid(2019, KALTARA_BBOX, 'Kalimantan_Utara');
exportBBoxSubgrid(2024, KALTARA_BBOX, 'Kalimantan_Utara');

print('');
print('========================================');
print('TOTAL: 10 TASKS (4 provinsi GAUL + Kaltara BBox)');
print('Per provinsi: ~1M titik, ~100MB CSV');
print('Jalankan SEMUA task di tab Tasks');
print('========================================');
