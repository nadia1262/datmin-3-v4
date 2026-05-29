// ============================================================
// 09_prediction_grid.js (REFACTORED)
// ============================================================
// Generates systematic prediction grids for each year (2018-2024).
// Uses the SAME preprocessing as 07_stratified_sampling.js:
// - Cloud masking (QA60 bitmask + divide(10000))
// - Spectral index calculation
// - Ancillary features (elevation, rainfall, IKN distance, mining density)
//
// CRITICAL: Cloud masking and scaling MUST match training data exactly.
//           Functions below are copied from 00_utils.js.
// ============================================================

// --- Study Area ---
var KALIMANTAN = ee.Geometry.Polygon(
  [[[108.5, 4.5], [108.5, -4.2], [119.5, -4.2], [119.5, 4.5]]], null, false);

// --- IKN Center ---
var IKN_LON = 116.847;
var IKN_LAT = -1.128;

// --- Constants ---
var CLOUD_THRESHOLD = 20;
var PREDICTION_SCALE = 500; // meters — trade-off: 10m=impossible, 500m=feasible

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

// FIXED: Distance to IKN as ee.Image (not scalar)
// Uses equirectangular approximation — accurate enough at equatorial latitudes
function getIKNDistance() {
  var lonLat = ee.Image.pixelLonLat();
  var R = 6371; // Earth radius km
  var lon_rad = lonLat.select('longitude').subtract(IKN_LON).multiply(Math.PI / 180);
  var lat_rad = lonLat.select('latitude').subtract(IKN_LAT).multiply(Math.PI / 180);
  var dx = lon_rad.multiply(R);
  var dy = lat_rad.multiply(R);
  return dx.pow(2).add(dy.pow(2)).sqrt()
    .rename('distance_to_ikn')
    .clip(KALIMANTAN);
}

// Mining density proxy from WorldCover Bare class
function getMiningDensity10km() {
  var worldcover = ee.ImageCollection('ESA/WorldCover/v200').first().clip(KALIMANTAN);
  var bare_proxy = worldcover.eq(60);
  var kernel = ee.Kernel.square({radius: 10000, units: 'meters'});
  return bare_proxy.reduceNeighborhood({
    reducer: ee.Reducer.mean(),
    kernel: kernel,
    optimization: 'boxcar'
  }).multiply(100).rename('mining_density_10km').clip(KALIMANTAN);
}

// ============================================================
// EXPORT FUNCTION PER YEAR
// ============================================================
function exportYearGrid(year) {
  var s2 = getComposite(year);
  var s2_idx = addIndices(s2);

  // Static layers
  var elevation = ee.Image('USGS/SRTMGL1_003').select('elevation').clip(KALIMANTAN);
  var ikn_dist = getIKNDistance();
  var mining_density = getMiningDensity10km();

  // Year-specific layers
  var rainfall = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
    .filterDate(year + '-01-01', year + '-12-31')
    .sum().rename('rainfall_annual').clip(KALIMANTAN);

  // Stack all features
  var stack = s2_idx.addBands([elevation, rainfall, ikn_dist, mining_density]);

  // Systematic sampling for prediction grid
  var grid = stack.sample({
    region: KALIMANTAN,
    scale: PREDICTION_SCALE,
    geometries: true,
    dropNulls: true,
    seed: 42,            // Deterministic sampling
    numPixels: 300000,   // Reduced slightly to save memory
    tileScale: 8         // CRITICAL FIX: prevents 'User memory limit exceeded'
  });

  Export.table.toDrive({
    collection: grid,
    description: 'prediction_grid_' + year,
    folder: 'Kalimantan_LandCover_Grids',
    fileFormat: 'CSV'
  });

  print('Grid ' + year + ' sample count:', grid.size());
}

// ============================================================
// EXPORT ALL YEARS
// ============================================================
// Priority order: 2021 (in-sample validation), 2024 (endline), 2018 (baseline), then rest
// In GEE Code Editor, each call creates a separate task in the Tasks tab.
// Run them manually — they will export in parallel.

// HIGH PRIORITY
exportYearGrid(2021);
exportYearGrid(2024);
exportYearGrid(2018);

// MEDIUM PRIORITY (run after high priority completes to stay within quota)
exportYearGrid(2019);
exportYearGrid(2020);
exportYearGrid(2022);
exportYearGrid(2023);
