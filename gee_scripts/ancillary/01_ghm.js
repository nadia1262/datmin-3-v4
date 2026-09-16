// =====================================================
// GEE Script 01: Global Human Modification (gHM)
// Dataset: CSP gHM v1.0  
// Asset: "CSP/HM/GlobalHumanModification"
// Features: ghm_mean, ghm_max
// =====================================================
// INSTRUCTIONS:
// 1. Copy-paste this into GEE Code Editor (code.earthengine.google.com)
// 2. Change YOUR_ASSET_PATH below to your uploaded boundary asset ID
// 3. Click Run
// 4. In Tasks tab → Run the export task
// 5. Download CSV from Google Drive

// ---- CONFIG ----
var assetPath = 'users/YOUR_USERNAME/kalimantan_desa_final'; // ← CHANGE THIS
var desa = ee.FeatureCollection(assetPath);
print('Village count:', desa.size());

// ---- LOAD gHM ----
var ghm = ee.ImageCollection("CSP/HM/GlobalHumanModification")
  .first()
  .select('gHM');

// ---- ZONAL STATS ----
var stats = ghm.reduceRegions({
  collection: desa,
  reducer: ee.Reducer.mean().combine({
    reducer2: ee.Reducer.max(),
    sharedInputs: true
  }),
  scale: 1000,  // gHM native resolution
  tileScale: 4
});

// ---- SELECT ONLY NEEDED COLUMNS (drop .geo!) ----
var output = stats.map(function(f) {
  return ee.Feature(null, {
    'kode_desa': f.get('kode_desa'),
    'ghm_mean': f.get('mean'),
    'ghm_max': f.get('max')
  });
});

// ---- EXPORT ----
Export.table.toDrive({
  collection: output,
  description: 'ghm_kalimantan',
  fileNamePrefix: 'ghm_kalimantan',
  fileFormat: 'CSV',
  selectors: ['kode_desa', 'ghm_mean', 'ghm_max']
});

print('✅ Export task created. Go to Tasks tab → Run.');
