// =====================================================
// GEE Script 02: SRTM DEM (Elevation, Slope, Ruggedness)
// Dataset: USGS/SRTMGL1_003 (30m)
// Features: elevation_mean, slope_mean, ruggedness_mean
// =====================================================

var assetPath = 'users/YOUR_USERNAME/kalimantan_desa_final'; // ← CHANGE THIS
var desa = ee.FeatureCollection(assetPath);

// ---- LOAD & COMPUTE ----
var dem = ee.Image('USGS/SRTMGL1_003').select('elevation');
var slope = ee.Terrain.slope(dem).rename('slope');
// Terrain Ruggedness Index (TRI): stdDev of elevation in 3x3 kernel
var ruggedness = dem.reduceNeighborhood({
  reducer: ee.Reducer.stdDev(),
  kernel: ee.Kernel.square(3)
}).rename('ruggedness');

var stack = dem.addBands(slope).addBands(ruggedness);

// ---- ZONAL STATS ----
var stats = stack.reduceRegions({
  collection: desa,
  reducer: ee.Reducer.mean(),
  scale: 90,  // use 90m for speed (SRTM is 30m)
  tileScale: 4
});

var output = stats.map(function(f) {
  return ee.Feature(null, {
    'kode_desa': f.get('kode_desa'),
    'elevation_mean': f.get('elevation'),
    'slope_mean': f.get('slope'),
    'ruggedness_mean': f.get('ruggedness')
  });
});

Export.table.toDrive({
  collection: output,
  description: 'srtm_kalimantan',
  fileNamePrefix: 'srtm_kalimantan',
  fileFormat: 'CSV',
  selectors: ['kode_desa', 'elevation_mean', 'slope_mean', 'ruggedness_mean']
});

print('✅ SRTM export ready. Go to Tasks → Run.');
