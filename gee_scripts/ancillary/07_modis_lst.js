// =====================================================
// GEE Script 07: MODIS LST (2021)
// Dataset: MODIS/061/MOD11A2 (1km, 8-day)
// Features: lst_day_mean, lst_night_mean (°C)
// =====================================================

var assetPath = 'users/YOUR_USERNAME/kalimantan_desa_final'; // ← CHANGE THIS
var desa = ee.FeatureCollection(assetPath);

var modisLST = ee.ImageCollection('MODIS/061/MOD11A2')
  .filterDate('2021-01-01', '2021-12-31')
  .select(['LST_Day_1km', 'LST_Night_1km']);

// Scale (×0.02) and convert K → °C (−273.15)
var scaled = modisLST.map(function(img) {
  return img.multiply(0.02).subtract(273.15)
    .copyProperties(img, img.propertyNames());
});

var annual = scaled.mean().rename(['lst_day', 'lst_night']);

var stats = annual.reduceRegions({
  collection: desa,
  reducer: ee.Reducer.mean(),
  scale: 1000,
  tileScale: 4
});

var output = stats.map(function(f) {
  return ee.Feature(null, {
    'kode_desa': f.get('kode_desa'),
    'lst_day_mean': f.get('lst_day'),
    'lst_night_mean': f.get('lst_night')
  });
});

Export.table.toDrive({
  collection: output,
  description: 'modis_lst_kalimantan_2021',
  fileNamePrefix: 'modis_lst_kalimantan_2021',
  fileFormat: 'CSV',
  selectors: ['kode_desa', 'lst_day_mean', 'lst_night_mean']
});

print('✅ MODIS LST export ready.');
