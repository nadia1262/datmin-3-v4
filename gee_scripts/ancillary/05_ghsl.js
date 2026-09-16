// =====================================================
// GEE Script 05: GHSL Built-Up Surface (2020)
// Features: builtup_fraction, builtup_area_km2
// =====================================================

var assetPath = 'users/YOUR_USERNAME/kalimantan_desa_final'; // ← CHANGE THIS
var desa = ee.FeatureCollection(assetPath);

// GHSL Built-Up Surface 2020 (100m)
var ghsl = ee.Image('JRC/GHSL/P2023A/GHS_BUILT_S/2020')
  .select('built_surface');

// Mean built-up m² per pixel → fraction of village that is built-up
var stats = ghsl.reduceRegions({
  collection: desa,
  reducer: ee.Reducer.mean().combine({
    reducer2: ee.Reducer.sum(),
    sharedInputs: true
  }),
  scale: 100,
  tileScale: 4
});

var output = stats.map(function(f) {
  // Calculate area dynamically in GEE (meters^2 to km^2) to avoid missing property errors
  var area = f.area().divide(1e6);
  
  // If sum is missing, default to 0
  var builtup_m2 = ee.Algorithms.If(
    ee.Algorithms.IsEqual(f.get('sum'), null),
    0,
    f.get('sum')
  );
  builtup_m2 = ee.Number(builtup_m2);
  
  // Convert m² to km² and compute fraction
  var builtup_km2 = builtup_m2.divide(1e6);
  var fraction = builtup_km2.divide(area);
  
  return ee.Feature(null, {
    'kode_desa': f.get('kode_desa'),
    'builtup_fraction': fraction,
    'builtup_area_km2': builtup_km2
  });
});

Export.table.toDrive({
  collection: output,
  description: 'ghsl_kalimantan_2020',
  fileNamePrefix: 'ghsl_kalimantan_2020',
  fileFormat: 'CSV',
  selectors: ['kode_desa', 'builtup_fraction', 'builtup_area_km2']
});

print('✅ GHSL export ready.');
