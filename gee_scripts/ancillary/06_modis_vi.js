// =====================================================
// GEE Script 06: MODIS Vegetation Index (2021)
// Dataset: MODIS/061/MOD13A2 (1km, 16-day)
// Features: ndvi_mean, evi_mean
// =====================================================

var assetPath = 'users/YOUR_USERNAME/kalimantan_desa_final'; // ← CHANGE THIS
var desa = ee.FeatureCollection(assetPath);

// Full year 2021 (1yr before IDM 2022)
var modisVI = ee.ImageCollection('MODIS/061/MOD13A2')
  .filterDate('2021-01-01', '2021-12-31')
  .select(['NDVI', 'EVI']);

// Apply scale factor: *0.0001
var scaled = modisVI.map(function(img) {
  return img.multiply(0.0001)
    .copyProperties(img, img.propertyNames());
});

// Annual mean composite
var annual = scaled.mean().rename(['ndvi_mean', 'evi_mean']);

var stats = annual.reduceRegions({
  collection: desa,
  reducer: ee.Reducer.mean(),
  scale: 1000,
  tileScale: 4
});

var output = stats.map(function(f) {
  return ee.Feature(null, {
    'kode_desa': f.get('kode_desa'),
    'ndvi_mean': f.get('ndvi_mean'),
    'evi_mean': f.get('evi_mean')
  });
});

Export.table.toDrive({
  collection: output,
  description: 'modis_vi_kalimantan_2021',
  fileNamePrefix: 'modis_vi_kalimantan_2021',
  fileFormat: 'CSV',
  selectors: ['kode_desa', 'ndvi_mean', 'evi_mean']
});

print('✅ MODIS VI export ready.');
