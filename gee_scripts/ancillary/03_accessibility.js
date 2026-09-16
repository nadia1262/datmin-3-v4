// =====================================================
// GEE Script 03: Oxford MAP Accessibility
// Features: time_to_city_mean
// NOTE: healthcare asset (2019) is corrupted on GEE.
//       Using only city accessibility.
//       If you need a 2nd feature, uncomment the walking block.
// =====================================================

var assetPath = 'users/YOUR_USERNAME/kalimantan_desa_final'; // ← CHANGE THIS
var desa = ee.FeatureCollection(assetPath);

// Travel time to nearest city (>50k pop) — 2015
var city = ee.Image('Oxford/MAP/accessibility_to_cities_2015_v1_0')
  .select('accessibility').rename('time_city');

// OPTION: Walking-only travel time (alternative since healthcare is broken)
// Uncomment the next 2 lines if you want a 2nd accessibility metric
// var walking = ee.Image('Oxford/MAP/accessibility_to_cities_2015_v1_0')
//   .select('accessibility_walking_only').rename('time_city_walking');

var stats = city.reduceRegions({
  collection: desa,
  reducer: ee.Reducer.mean(),
  scale: 1000,
  tileScale: 4
});

var output = stats.map(function(f) {
  return ee.Feature(null, {
    'kode_desa': f.get('kode_desa'),
    'time_city_mean': f.get('mean')
  });
});

Export.table.toDrive({
  collection: output,
  description: 'accessibility_kalimantan',
  fileNamePrefix: 'accessibility_kalimantan',
  fileFormat: 'CSV',
  selectors: ['kode_desa', 'time_city_mean']
});

print('✅ Accessibility export ready.');

