// 05_ikn_distance.js
// Computes distance to IKN and buffer zones

var kalimantan = ee.Geometry.Polygon(
  [[[108.5, 4.5],
    [108.5, -4.2],
    [119.5, -4.2],
    [119.5, 4.5]]], null, false);

var ikn_point = ee.Geometry.Point([116.847, -1.128]);

// Create a distance map (in km)
var distanceToIKN = ikn_point.distance(ee.ErrorMargin(1)) // output is in meters
  .divide(1000) // convert to km
  .rename('distance_to_ikn')
  .clip(kalimantan);

// Create buffer zones
// 0: core (<10km), 1: 10-25km, 2: 25-50km, 3: 50-100km, 4: >100km
var ikn_buffer_zone = ee.Image(4) // default >100km
  .where(distanceToIKN.lte(100), 3)
  .where(distanceToIKN.lte(50), 2)
  .where(distanceToIKN.lte(25), 1)
  .where(distanceToIKN.lte(10), 0)
  .rename('ikn_buffer_zone')
  .clip(kalimantan);
