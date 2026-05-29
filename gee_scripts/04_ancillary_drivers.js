// 04_ancillary_drivers.js
// Extracts SRTM elevation and CHIRPS rainfall

var kalimantan = ee.Geometry.Polygon(
  [[[108.5, 4.5],
    [108.5, -4.2],
    [119.5, -4.2],
    [119.5, 4.5]]], null, false);

// 1. SRTM Elevation
var elevation = ee.Image('USGS/SRTMGL1_003')
  .select('elevation')
  .clip(kalimantan);

// 2. CHIRPS Rainfall (Annual Total)
function getAnnualRainfall(year) {
  var start = ee.Date.fromYMD(year, 1, 1);
  var end = ee.Date.fromYMD(year, 12, 31);
  
  var rainfall = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
    .filterDate(start, end)
    .sum()
    .rename('rainfall_annual')
    .clip(kalimantan);
    
  return rainfall;
}

var rain_2021 = getAnnualRainfall(2021);
