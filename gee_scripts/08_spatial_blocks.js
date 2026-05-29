// 08_spatial_blocks.js
// Visualizes and assigns the 0.5 degree spatial block grid

var kalimantan = ee.Geometry.Polygon(
  [[[108.5, 4.5], [108.5, -4.2], [119.5, -4.2], [119.5, 4.5]]], null, false);

// Get Lon/Lat image
var lonLat = ee.Image.pixelLonLat();

// Define block size in degrees
var block_size = 0.5;

// Compute block ID:
// longitude_index * 1000 + (latitude_index + offset)
var block_id = lonLat.select('longitude').divide(block_size).floor()
  .multiply(1000)
  .add(lonLat.select('latitude').divide(block_size).floor().add(90)) // add 90 to handle negative latitudes
  .rename('spatial_block_id')
  .toInt()
  .clip(kalimantan);

// Visualize blocks
// Random color for each block
var block_vis = block_id.randomVisualizer();
Map.centerObject(kalimantan, 5);
Map.addLayer(block_vis, {}, 'Spatial Blocks (0.5 deg)');

// Export block image if needed (usually just computed on the fly)
