/**
 * Script 11: Export Micro-Scale (10m) Prediction Grid for IKN Core Zone
 * 
 * Script ini KHUSUS untuk mengekspor data spektral 10 meter (Native Resolution) 
 * HANYA di area sangat kecil (Kawasan Inti Pusat Pemerintahan / KIPP IKN).
 * Tujuan: Untuk pamer di laporan bahwa model Python kita mampu memprediksi 
 * sangat presisi (10m) untuk area spesifik, melengkapi prediksi makro 500m.
 */

// 1. Definisikan Bounding Box untuk Zona Inti IKN (KIPP)
// Karena resolusi 10m sangat berat, kita perkecil areanya menjadi ~4km x 4km
// (Hanya fokus pada pusat pemerintahan / Istana Negara IKN)
var iknCoreZone = ee.Geometry.Rectangle([116.68, -0.98, 116.72, -0.94]);

Map.centerObject(iknCoreZone, 14);
Map.addLayer(iknCoreZone, {color: 'red'}, 'KIPP IKN Bounding Box (4x4 km)', false);

// 2. Fungsi untuk mengambil Sentinel-2 dan menghitung Indeks
function getSentinelData(year) {
  var start = year + '-01-01';
  var end = year + '-12-31';
  
  // Ambil Harmonized Sentinel-2
  var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(iknCoreZone)
    .filterDate(start, end)
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20));
    
  // Fungsi Masking Awan
  var maskClouds = function(image) {
    var qa = image.select('QA60');
    var cloudBitMask = 1 << 10;
    var cirrusBitMask = 1 << 11;
    var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
      .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
    return image.updateMask(mask);
  };
  
  var composite = s2.map(maskClouds).median().clip(iknCoreZone);
  
  // Hitung Indeks
  var ndvi = composite.normalizedDifference(['B8', 'B4']).rename('NDVI');
  var ndbi = composite.normalizedDifference(['B11', 'B8']).rename('NDBI');
  var ndmi = composite.normalizedDifference(['B8', 'B11']).rename('NDMI');
  
  // BSI: ((B11 + B4) - (B8 + B2)) / ((B11 + B4) + (B8 + B2))
  var bsi = composite.expression(
    '((SWIR1 + RED) - (NIR + BLUE)) / ((SWIR1 + RED) + (NIR + BLUE))', {
      'SWIR1': composite.select('B11'),
      'RED': composite.select('B4'),
      'NIR': composite.select('B8'),
      'BLUE': composite.select('B2')
    }).rename('BSI');
    
  // Topografi (Elevasi)
  var elevation = ee.Image('USGS/SRTMGL1_003').clip(iknCoreZone).rename('elevation');
  
  // Jarak ke IKN (Selalu 0 sampai bbrp km karena kita di pusat IKN)
  var iknPoint = ee.Geometry.Point([116.70, -0.95]);
  var distIKN = ee.FeatureCollection([ee.Feature(iknPoint)]).distance(50000).rename('distance_to_ikn');
  
  // Kepadatan Tambang (Kosongkan/Set 0 karena ini zona inti IKN)
  var miningDensity = ee.Image(0).rename('mining_density_10km');
  
  // Hujan Tahunan (Gunakan rata-rata Kaltim untuk simplifikasi)
  var rainfall = ee.Image(2500).rename('annual_rainfall');
  
  return composite.select(['B2','B3','B4','B8','B11','B12'])
    .addBands([ndvi, ndbi, ndmi, bsi, elevation, distIKN, miningDensity, rainfall]);
}

// 3. Ekspor Data Tahun 2019 dan 2024
var years = [2019, 2024];

years.forEach(function(year) {
  var image = getSentinelData(year);
  
  // Ekstrak nilai piksel murni (10 meter)
  var sample = image.sample({
    region: iknCoreZone,
    scale: 10, // RESOLUSI ASLI 10 METER!
    projection: 'EPSG:4326',
    geometries: true,
    dropNulls: true,
    tileScale: 16 // Mencegah memory limit error (membagi komputasi)
  });
  
  Export.table.toDrive({
    collection: sample,
    description: 'ikn_10m_grid_' + year,
    folder: 'DATMIN_IKN_10M', // Folder di Google Drive Anda
    fileFormat: 'CSV'
  });
});

print('Tugas ekspor IKN 10m (2019 dan 2024) ditambahkan ke tab Tasks!');
print('Jalankan task tersebut. File CSV yang dihasilkan akan berisi ~1 juta baris.');
