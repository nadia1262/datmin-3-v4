// =====================================================
// GEE Script 09: Hansen Global Forest Change
// Dataset: UMD/hansen/global_forest_change_2023_v1_11
// Features: cover_2000, loss_cumulative, loss_recent (2017-2021)
// ⚠️ HEAVY — use tileScale: 8 or 16
// =====================================================

var assetPath = 'users/YOUR_USERNAME/kalimantan_desa_final'; // ← CHANGE THIS
var desa = ee.FeatureCollection(assetPath);

var hansen = ee.Image('UMD/hansen/global_forest_change_2023_v1_11');

// Tree cover 2000 (%)
var cover2000 = hansen.select('treecover2000').rename('cover_2000');

// Loss year (1-23 = 2001-2023)
var lossYear = hansen.select('lossyear');

// Cumulative loss up to 2021 (year 1-21)
var lossCum = lossYear.gt(0).and(lossYear.lte(21)).rename('loss_cum');

// Recent loss 2017-2021 (year 17-21)
var lossRecent = lossYear.gte(17).and(lossYear.lte(21)).rename('loss_recent');

var stack = cover2000.addBands(lossCum).addBands(lossRecent);

// ⚠️ tileScale: 8 because Hansen is 30m resolution → very heavy
var stats = stack.reduceRegions({
  collection: desa,
  reducer: ee.Reducer.mean(),
  scale: 30,
  tileScale: 8  // increase to 16 if timeout
});

var output = stats.map(function(f) {
  return ee.Feature(null, {
    'kode_desa': f.get('kode_desa'),
    'cover_2000_pct': f.get('cover_2000'),
    'loss_cum_frac': f.get('loss_cum'),
    'loss_recent_frac': f.get('loss_recent')
  });
});

Export.table.toDrive({
  collection: output,
  description: 'hansen_kalimantan',
  fileNamePrefix: 'hansen_kalimantan',
  fileFormat: 'CSV',
  selectors: ['kode_desa', 'cover_2000_pct', 'loss_cum_frac', 'loss_recent_frac']
});

print('✅ Hansen export ready. ⚠️ This may take 30-60 minutes!');
