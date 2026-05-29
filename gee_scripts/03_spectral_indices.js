// 03_spectral_indices.js
// Computes NDVI, NDBI, NDMI, BSI from Sentinel-2 composite

function addSpectralIndices(image) {
  // NDVI = (NIR - Red) / (NIR + Red)
  var ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI');
  
  // NDBI = (SWIR1 - NIR) / (SWIR1 + NIR)
  var ndbi = image.normalizedDifference(['B11', 'B8']).rename('NDBI');
  
  // NDMI = (NIR - SWIR1) / (NIR + SWIR1)
  var ndmi = image.normalizedDifference(['B8', 'B11']).rename('NDMI');
  
  // BSI = ((SWIR1 + Red) - (NIR + Blue)) / ((SWIR1 + Red) + (NIR + Blue))
  var bsi = image.expression(
    '((SWIR1 + RED) - (NIR + BLUE)) / ((SWIR1 + RED) + (NIR + BLUE))', {
      'SWIR1': image.select('B11'),
      'RED': image.select('B4'),
      'NIR': image.select('B8'),
      'BLUE': image.select('B2')
    }).rename('BSI');
    
  return image.addBands([ndvi, ndbi, ndmi, bsi]);
}
