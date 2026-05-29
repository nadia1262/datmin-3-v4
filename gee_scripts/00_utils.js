// ============================================================
// 00_utils.js — Master Utility Functions for Kalimantan LC Project
// ============================================================
// SEMUA script GEE HARUS menggunakan fungsi-fungsi ini (copy-paste)
// untuk menjamin KONSISTENSI preprocessing antara training dan prediction.
//
// PENTING: GEE Code Editor TIDAK mendukung import antar file.
// Jadi fungsi-fungsi ini harus di-copy ke setiap script yang membutuhkan.
// File ini adalah SINGLE SOURCE OF TRUTH.
// ============================================================

// --- Study Area ---
var KALIMANTAN = ee.Geometry.Polygon(
  [[[108.5, 4.5], [108.5, -4.2], [119.5, -4.2], [119.5, 4.5]]], null, false);

// --- IKN Center ---
var IKN_LON = 116.847;
var IKN_LAT = -1.128;
var IKN_POINT = ee.Geometry.Point([IKN_LON, IKN_LAT]);

// --- Constants ---
var CLOUD_THRESHOLD = 20;   // Max cloud cover % for scene filtering
var SCALE = 10;             // Sentinel-2 target resolution (meters)
var BLOCK_SIZE = 0.5;       // Spatial block size (degrees, ~55km)

// ============================================================
// CLOUD MASKING — QA60 bitmask + Surface Reflectance scaling
// ============================================================
// This function MUST be used in ALL scripts that process Sentinel-2.
// Without it, band values will be in DN (0-10000) instead of
// reflectance (0-1), causing model failure.
function maskS2clouds(image) {
  var qa = image.select('QA60');
  var cloudBitMask = 1 << 10;   // Bit 10: opaque clouds
  var cirrusBitMask = 1 << 11;  // Bit 11: cirrus clouds
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
    .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
  // Apply mask AND scale to reflectance [0, 1]
  return image.updateMask(mask).divide(10000);
}

// ============================================================
// ANNUAL MEDIAN COMPOSITE
// ============================================================
// Returns cloud-masked, scaled median composite for a given year.
function getComposite(year) {
  var start = year + '-01-01';
  var end = year + '-12-31';

  return ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(KALIMANTAN)
    .filterDate(start, end)
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', CLOUD_THRESHOLD))
    .map(maskS2clouds)
    .select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12'])
    .median()
    .clip(KALIMANTAN);
}

// ============================================================
// SPECTRAL INDICES
// ============================================================
// Adds NDVI, NDBI, NDMI, BSI bands to a Sentinel-2 composite.
// Input MUST be scaled reflectance (0-1).
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
// ESA WORLDCOVER 2021 LABELS (remapped to 5 project classes)
// ============================================================
// 0: Forest (Tree cover + Herbaceous wetland + Mangroves)
// 1: Shrubland/Agriculture (Shrubland + Grassland + Cropland)
// 2: Built-up
// 3: Bare/Mining-like
// 4: Water
function getLabels() {
  var wc = ee.ImageCollection('ESA/WorldCover/v200').first().clip(KALIMANTAN);
  // Remap ESA classes to project classes
  // ESA: 10=Tree, 20=Shrub, 30=Grass, 40=Crop, 50=Built, 60=Bare, 80=Water, 90=Wetland, 95=Mangrove
  // Also handle 70=Snow/Ice and 100=Moss/Lichen (rare in Kalimantan, map to nearest)
  return wc.remap(
    [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100],
    [ 0,  1,  1,  1,  2,  3,  3,  4,  0,  0,   1]
  ).rename('land_cover_class');
}

// ============================================================
// ANCILLARY LAYERS
// ============================================================
function getElevation() {
  return ee.Image('USGS/SRTMGL1_003').select('elevation').clip(KALIMANTAN);
}

function getRainfall(year) {
  return ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
    .filterDate(year + '-01-01', year + '-12-31')
    .sum()
    .rename('rainfall_annual')
    .clip(KALIMANTAN);
}

// ============================================================
// DISTANCE TO IKN — as ee.Image (NOT scalar!)
// ============================================================
// Uses approximate equirectangular distance formula.
// Accurate enough for relative distance ranking in Kalimantan (~0-1000km range).
function getIKNDistance() {
  var lonLat = ee.Image.pixelLonLat();
  var lon_rad = lonLat.select('longitude').subtract(IKN_LON).multiply(Math.PI / 180);
  var lat_rad = lonLat.select('latitude').subtract(IKN_LAT).multiply(Math.PI / 180);
  
  // Equirectangular approximation: d = R * sqrt((Δlon*cos(lat_mid))² + Δlat²)
  // At Kalimantan's latitude (~0°), cos(lat) ≈ 1, so simplified:
  var R = 6371; // Earth radius in km
  var dx = lon_rad.multiply(R); // Δlon in km (cos(~0°) ≈ 1)
  var dy = lat_rad.multiply(R); // Δlat in km
  
  return dx.pow(2).add(dy.pow(2)).sqrt()
    .rename('distance_to_ikn')
    .clip(KALIMANTAN);
}

// ============================================================
// IKN BUFFER ZONES
// ============================================================
// 0: core (<10km), 1: 10-25km, 2: 25-50km, 3: 50-100km, 4: >100km
function getIKNBufferZone() {
  var dist = getIKNDistance();
  return ee.Image(4)
    .where(dist.lte(100), 3)
    .where(dist.lte(50), 2)
    .where(dist.lte(25), 1)
    .where(dist.lte(10), 0)
    .rename('ikn_buffer_zone')
    .toInt()
    .clip(KALIMANTAN);
}

// ============================================================
// SPATIAL BLOCK ID (for GroupKFold CV)
// ============================================================
// Creates a unique integer ID per 0.5° × 0.5° grid cell.
function getBlockId() {
  var lonLat = ee.Image.pixelLonLat();
  var lon_block = lonLat.select('longitude').divide(BLOCK_SIZE).floor();
  var lat_block = lonLat.select('latitude').divide(BLOCK_SIZE).floor().add(90); // offset negative lat
  return lon_block.multiply(1000).add(lat_block)
    .rename('spatial_block_id')
    .toInt();
}

// ============================================================
// POINT ID (deterministic, based on grid position)
// ============================================================
// Generates a unique ID for each pixel based on its lon/lat.
// This ensures the SAME point gets the SAME ID across all years.
// Format: floor(lon*10000) * 100000 + floor((lat+90)*10000)
function getPointId() {
  var lonLat = ee.Image.pixelLonLat();
  var lon_int = lonLat.select('longitude').multiply(10000).floor();
  var lat_int = lonLat.select('latitude').add(90).multiply(10000).floor();
  return lon_int.multiply(100000000).add(lat_int)
    .rename('point_id')
    .toLong();
}

// ============================================================
// MINING PROXIMITY (using WorldCover Bare class as proxy)
// ============================================================
function getMiningProxy() {
  var worldcover = ee.ImageCollection('ESA/WorldCover/v200').first().clip(KALIMANTAN);
  var bare_proxy = worldcover.eq(60); // Binary: 1 if Bare/sparse

  // Distance to nearest bare pixel (km)
  var distToMining = bare_proxy.fastDistanceTransform().sqrt()
    .multiply(ee.Image.pixelArea().sqrt())
    .divide(1000)
    .rename('distance_to_mining')
    .clip(KALIMANTAN);

  // Mining density in 10km buffer (% of area)
  var kernel_10km = ee.Kernel.square({radius: 10000, units: 'meters'});
  var density_10km = bare_proxy.reduceNeighborhood({
    reducer: ee.Reducer.mean(),
    kernel: kernel_10km,
    optimization: 'boxcar'
  }).multiply(100).rename('mining_density_10km').clip(KALIMANTAN);

  return {distance: distToMining, density: density_10km};
}

// ============================================================
// FULL FEATURE STACK (for training or prediction)
// ============================================================
// mode: 'training' (includes labels + block_id)
//        'prediction' (includes drivers, no labels)
function getFeatureStack(year, mode) {
  var s2 = getComposite(year);
  var s2_idx = addIndices(s2);
  var elevation = getElevation();
  var rainfall = getRainfall(year);
  var point_id = getPointId();

  var stack = s2_idx.addBands([elevation, rainfall, point_id]);

  if (mode === 'training') {
    var labels = getLabels();
    var block_id = getBlockId();
    stack = stack.addBands([block_id, labels]);
  }

  if (mode === 'prediction') {
    var ikn_dist = getIKNDistance();
    var mining = getMiningProxy();
    stack = stack.addBands([ikn_dist, mining.density]);
  }

  return stack;
}

// ============================================================
// USAGE EXAMPLES
// ============================================================
// --- Training (copy to 07_stratified_sampling.js): ---
// var stack = getFeatureStack(2021, 'training');
// var sample = stack.stratifiedSample({...});
//
// --- Prediction (copy to 09_prediction_grid.js): ---
// var stack = getFeatureStack(2018, 'prediction');
// var grid = stack.sample({...});

// ============================================================
// QUICK VISUAL CHECK (run in Code Editor)
// ============================================================
var s2_2021 = getComposite(2021);
print('2021 Composite band stats (should be ~0.0-0.3):', s2_2021.reduceRegion({
  reducer: ee.Reducer.minMax(),
  geometry: IKN_POINT.buffer(10000),
  scale: 100
}));

Map.centerObject(KALIMANTAN, 5);
Map.addLayer(s2_2021, {bands: ['B4', 'B3', 'B2'], min: 0, max: 0.3}, 'S2 2021 RGB');
Map.addLayer(getIKNDistance(), {min: 0, max: 500, palette: ['red', 'yellow', 'green']}, 'Dist to IKN (km)');
