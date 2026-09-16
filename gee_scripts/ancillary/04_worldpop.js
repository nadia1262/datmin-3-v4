// =====================================================
// GEE Script 04: WorldPop Population (2021)
// Features: pop_total, pop_density
// =====================================================

var assetPath = 'users/YOUR_USERNAME/kalimantan_desa_final'; // ← CHANGE THIS
var desa = ee.FeatureCollection(assetPath);

// WorldPop 2020 (closest available year)
var pop = ee.ImageCollection('WorldPop/GP/100m/pop')
  .filter(ee.Filter.eq('country', 'IDN'))
  .filter(ee.Filter.eq('year', 2020))
  .first()
  .select('population');

// Sum = total population per village
var statSum = pop.reduceRegions({
  collection: desa,
  reducer: ee.Reducer.sum(),
  scale: 100,
  tileScale: 4
});

var output = statSum.map(function(f) {
  // Calculate area dynamically in GEE (meters^2 to km^2) to avoid missing property errors
  var area = f.area().divide(1e6);
  
  // If sum is missing (no pixels overlap), default to 0
  var total = ee.Algorithms.If(
    ee.Algorithms.IsEqual(f.get('sum'), null),
    0,
    f.get('sum')
  );
  total = ee.Number(total);
  
  var density = total.divide(area);
  
  return ee.Feature(null, {
    'kode_desa': f.get('kode_desa'),
    'pop_total': total,
    'pop_density': density
  });
});

Export.table.toDrive({
  collection: output,
  description: 'worldpop_kalimantan_2021',
  fileNamePrefix: 'worldpop_kalimantan_2021',
  fileFormat: 'CSV',
  selectors: ['kode_desa', 'pop_total', 'pop_density']
});

print('✅ WorldPop export ready.');
