// ============================================================
// 07_stratified_sampling.js (REFACTORED)
// ============================================================
// Generates stratified training samples for 2021 using:
// - Sentinel-2 SR Harmonized (cloud-masked, scaled to reflectance)
// - ESA WorldCover v200 (remapped to 5 project classes)
// - SRTM elevation + CHIRPS rainfall
// - Spatial block IDs for GroupKFold CV
// - Deterministic point IDs for cross-year matching
//
// CRITICAL: All functions below are copied from 00_utils.js.
//           ANY change to preprocessing MUST be made in 00_utils.js first,
//           then propagated to this file AND 09_prediction_grid.js.
// ============================================================

// --- Study Area ---
var KALIMANTAN = ee.Geometry.Polygon(
  [[[108.5, 4.5], [108.5, -4.2], [119.5, -4.2], [119.5, 4.5]]], null, false);

// --- Constants ---
var CLOUD_THRESHOLD = 20;
var SCALE = 10;
var BLOCK_SIZE = 0.5;

// ============================================================
// FUNCTIONS (from 00_utils.js — KEEP IN SYNC)
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

function getLabels() {
  var wc = ee.ImageCollection('ESA/WorldCover/v200').first().clip(KALIMANTAN);
  return wc.remap(
    [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100],
    [ 0,  1,  1,  1,  2,  3,  3,  4,  0,  0,   1]
  ).rename('land_cover_class');
}

function getBlockId() {
  var lonLat = ee.Image.pixelLonLat();
  var lon_block = lonLat.select('longitude').divide(BLOCK_SIZE).floor();
  var lat_block = lonLat.select('latitude').divide(BLOCK_SIZE).floor().add(90);
  return lon_block.multiply(1000).add(lat_block)
    .rename('spatial_block_id')
    .toInt();
}

// ============================================================
// BUILD TRAINING STACK
// ============================================================
var s2_2021 = getComposite(2021);
var s2_idx = addIndices(s2_2021);

var elevation = ee.Image('USGS/SRTMGL1_003').select('elevation').clip(KALIMANTAN);
var rainfall = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
  .filterDate('2021-01-01', '2021-12-31').sum().rename('rainfall_annual').clip(KALIMANTAN);

var labels = getLabels();
var block_id = getBlockId();

var full_stack = s2_idx.addBands([elevation, rainfall, block_id, labels]);

// ============================================================
// VALIDATION: Check band value ranges
// ============================================================
print('Band value check (should be reflectance 0-0.5, not DN 0-10000):');
print('B2 range:', s2_2021.select('B2').reduceRegion({
  reducer: ee.Reducer.percentile([1, 50, 99]),
  geometry: KALIMANTAN,
  scale: 1000,
  maxPixels: 1e8
}));

// ============================================================
// STRATIFIED SAMPLING
// ============================================================
var sample = full_stack.stratifiedSample({
  numPoints: 0,
  classBand: 'land_cover_class',
  region: KALIMANTAN,
  scale: SCALE,
  seed: 42,
  classValues: [0, 1, 2, 3, 4],
  classPoints: [10000, 8000, 5000, 3000, 4000], // Total: 30,000
  geometries: true,
  dropNulls: true
});

// Add validation: print class counts
print('Sample size:', sample.size());
print('Class distribution:', sample.aggregate_histogram('land_cover_class'));

// ============================================================
// EXPORT TO DRIVE
// ============================================================
Export.table.toDrive({
  collection: sample,
  description: 'training_samples_2021',
  folder: 'Kalimantan_LandCover',
  fileFormat: 'CSV'
});
