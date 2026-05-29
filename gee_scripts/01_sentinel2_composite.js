// 01_sentinel2_composite.js
// Extracts annual median composites of Sentinel-2 SR Harmonized imagery for Kalimantan

var kalimantan = ee.Geometry.Polygon(
  [[[108.5, 4.5],
    [108.5, -4.2],
    [119.5, -4.2],
    [119.5, 4.5]]], null, false);

function getSentinel2Composite(year) {
  var start = ee.Date.fromYMD(year, 1, 1);
  var end = ee.Date.fromYMD(year, 12, 31);
  
  // Cloud masking function using QA60
  function maskS2clouds(image) {
    var qa = image.select('QA60');
    // Bits 10 and 11 are clouds and cirrus, respectively.
    var cloudBitMask = 1 << 10;
    var cirrusBitMask = 1 << 11;
    // Both flags should be set to zero, indicating clear conditions.
    var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
      .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
    return image.updateMask(mask).divide(10000);
  }

  var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(kalimantan)
    .filterDate(start, end)
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
    .map(maskS2clouds)
    .select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12'])
    .median()
    .clip(kalimantan);
    
  return s2;
}

// Example: export 2021 composite
var s2_2021 = getSentinel2Composite(2021);
print('Sentinel-2 2021 Composite', s2_2021);
