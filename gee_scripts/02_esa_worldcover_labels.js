// 02_esa_worldcover_labels.js
// Extracts ESA WorldCover 2021 labels and remaps them to 5 project classes

var kalimantan = ee.Geometry.Polygon(
  [[[108.5, 4.5],
    [108.5, -4.2],
    [119.5, -4.2],
    [119.5, 4.5]]], null, false);

// Load ESA WorldCover v200 (2021)
var worldcover = ee.ImageCollection('ESA/WorldCover/v200')
  .first()
  .clip(kalimantan);

// Remap classes
// 0: Forest (10, 90, 95)
// 1: Shrubland/Agriculture (20, 30, 40)
// 2: Built-up (50)
// 3: Bare/Mining (60)
// 4: Water (80)

var fromClasses = [10, 20, 30, 40, 50, 60, 80, 90, 95];
var toClasses   = [ 0,  1,  1,  1,  2,  3,  4,  0,  0];

var labels = worldcover.remap(fromClasses, toClasses).rename('land_cover_class');

print('Remapped Labels', labels);
