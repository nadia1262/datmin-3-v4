// ==============================================================================
// 03_export_kipp_dynamicworld.js
// Script GEE untuk mengekstrak Peta Tutupan Lahan 10m KIPP IKN (2019 vs 2024)
// Menggunakan dataset Google Dynamic World V1 (10m Resolution)
// ==============================================================================

// 1. Definisikan Bounding Box Kawasan Inti Pusat Pemerintahan (KIPP) IKN
// Area difokuskan pada Istana Negara dan Sumbu Kebangsaan
var kipp_ikn = ee.Geometry.Rectangle([116.63, -0.99, 116.78, -0.92]);

Map.centerObject(kipp_ikn, 12);
Map.addLayer(kipp_ikn, {color: 'red'}, 'Batas KIPP IKN', false);

// 2. Fungsi untuk mengambil komposit mode tahunan dari Dynamic World
// dan me-remap kelasnya agar cocok dengan 5 kelas proyek kita (0-4)
function getRemappedDynamicWorld(startDate, endDate) {
  var dw = ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1")
             .filterBounds(kipp_ikn)
             .filterDate(startDate, endDate)
             .select('label')
             .mode(); // Ambil kelas yang paling sering muncul sepanjang tahun
             
  // Dynamic World Asli:
  // 0: Water, 1: Trees, 2: Grass, 3: Flooded veg, 4: Crops, 5: Shrub & Scrub, 6: Built, 7: Bare, 8: Snow/Ice
  
  // Kelas Proyek Kita:
  // 0: Forest, 1: Shrub/Agri, 2: Built-up, 3: Bare/Mining, 4: Water
  
  var remapped = dw.remap(
    [1,  2, 4, 5,  6,  7,  0, 3, 8], // Dari DW
    [0,  1, 1, 1,  2,  3,  4, 4, 4]  // Ke Kelas Kita
  );
  
  return remapped.clip(kipp_ikn);
}

// 3. Proses untuk Tahun 2019 (Pra-Konstruksi)
var img_2019 = getRemappedDynamicWorld('2019-01-01', '2019-12-31');

// 4. Proses untuk Tahun 2024 (Fase Konstruksi Masif)
var img_2024 = getRemappedDynamicWorld('2024-01-01', '2024-12-31');

// 5. Visualisasi di GEE (Mengecek sebelum export)
var visParams = {
  min: 0,
  max: 4,
  palette: [
    '1F7A3D', // 0: Forest (Hijau Gelap)
    '6E9A2E', // 1: Shrubland (Hijau Terang)
    'C6371F', // 2: Built-up (Merah)
    'B87A1E', // 3: Bare (Cokelat)
    '1B5FA8'  // 4: Water (Biru)
  ]
};

Map.addLayer(img_2019, visParams, 'KIPP 10m - 2019');
Map.addLayer(img_2024, visParams, 'KIPP 10m - 2024');

// ==============================================================================
// 6. EXPORT TASK KE GOOGLE DRIVE
// Setelah script ini di-Run, buka tab "Tasks" di kanan atas GEE dan klik "Run".
// ==============================================================================

Export.image.toDrive({
  image: img_2019,
  description: 'Export_KIPP_2019',
  folder: 'DATMIN_Skripsi', // Folder di Google Drive Anda
  fileNamePrefix: 'ipp_k_10m_2019', // Nama file yang dicari oleh Streamlit
  region: kipp_ikn,
  scale: 10,
  crs: 'EPSG:4326',
  maxPixels: 1e10
});

Export.image.toDrive({
  image: img_2024,
  description: 'Export_KIPP_2024',
  folder: 'DATMIN_Skripsi',
  fileNamePrefix: 'ipp_k_10m_2024', // Nama file yang dicari oleh Streamlit
  region: kipp_ikn,
  scale: 10,
  crs: 'EPSG:4326',
  maxPixels: 1e10
});
