// =====================================================
// GEE Script 08: CHIRPS Rainfall (2021)
// Dataset: UCSB-CHG/CHIRPS/DAILY
// Features: annual_rain_mm, rain_cv
// =====================================================

var assetPath = 'users/YOUR_USERNAME/kalimantan_desa_final'; // ← CHANGE THIS
var desa = ee.FeatureCollection(assetPath);

// Sum daily precipitation to get annual total
var chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
  .filterDate('2021-01-01', '2021-12-31')
  .select('precipitation');

var annualRain = chirps.sum().rename('annual_rain');

// Monthly sums for CV calculation
var months = ee.List.sequence(1, 12);
var monthlySums = ee.ImageCollection(months.map(function(m) {
  return chirps
    .filter(ee.Filter.calendarRange(m, m, 'month'))
    .sum()
    .set('month', m);
}));

var monthlyMean = monthlySums.mean().rename('monthly_mean');
var monthlyStd = monthlySums.reduce(ee.Reducer.stdDev()).rename('monthly_std');
var rainCV = monthlyStd.divide(monthlyMean).rename('rain_cv');

var stack = annualRain.addBands(rainCV);

var stats = stack.reduceRegions({
  collection: desa,
  reducer: ee.Reducer.mean(),
  scale: 5000,  // CHIRPS ~5km
  tileScale: 4
});

var output = stats.map(function(f) {
  return ee.Feature(null, {
    'kode_desa': f.get('kode_desa'),
    'annual_rain_mm': f.get('annual_rain'),
    'rain_cv': f.get('rain_cv')
  });
});

Export.table.toDrive({
  collection: output,
  description: 'chirps_kalimantan_2021',
  fileNamePrefix: 'chirps_kalimantan_2021',
  fileFormat: 'CSV',
  selectors: ['kode_desa', 'annual_rain_mm', 'rain_cv']
});

print('✅ CHIRPS export ready.');
