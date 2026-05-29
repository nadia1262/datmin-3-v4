// 06_mining_proximity.js
// Computes distance to mining and mining density using ESA WorldCover 'Bare' class as proxy for mining

var kalimantan = ee.Geometry.Polygon(
  [[[108.5, 4.5],
    [108.5, -4.2],
    [119.5, -4.2],
    [119.5, 4.5]]], null, false);

// Proxy: WorldCover Bare/sparse vegetation (60)
var worldcover = ee.ImageCollection('ESA/WorldCover/v200').first().clip(kalimantan);
var bare_proxy = worldcover.eq(60); // Binary image: 1 if bare, 0 otherwise

// NOTE: Ideally, we would load the Maus et al. dataset as an asset.
// Since we don't have it here, we use the bare_proxy as a surrogate for demonstration in this GEE script.

// Calculate distance to nearest mining (bare proxy)
// We use fastDistanceTransform for efficiency
var distanceToMining = bare_proxy.fastDistanceTransform().sqrt()
  .multiply(ee.Image.pixelArea().sqrt()) // Convert pixel distance to meters
  .divide(1000) // Convert to km
  .rename('distance_to_mining')
  .clip(kalimantan);

// Calculate mining density in 10km buffer
// Use focal_sum or reduceNeighborhood
// To do this over large areas, reduceResolution or aggregate
var kernel_10km = ee.Kernel.circle({radius: 10000, units: 'meters'});
var mining_density_10km = bare_proxy.reduceNeighborhood({
  reducer: ee.Reducer.mean(), // Fraction of area that is bare
  kernel: kernel_10km,
  optimization: 'boxcar' // Fast computation
}).multiply(100) // Convert to percentage
  .rename('mining_density_10km')
  .clip(kalimantan);

// Calculate mining density in 25km buffer
var kernel_25km = ee.Kernel.circle({radius: 25000, units: 'meters'});
var mining_density_25km = bare_proxy.reduceNeighborhood({
  reducer: ee.Reducer.mean(),
  kernel: kernel_25km,
  optimization: 'boxcar'
}).multiply(100)
  .rename('mining_density_25km')
  .clip(kalimantan);
