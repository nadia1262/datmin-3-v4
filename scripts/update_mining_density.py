import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import time

PREDICTIONS_DIR = r"d:\POLSTAT STIS\Tingkat 3\Semester 6\DATMIN\Kelompok_3_v4\data\predictions"
MINING_FILE = r"d:\POLSTAT STIS\Tingkat 3\Semester 6\DATMIN\Kelompok_3_v4\data\external\global_mining_areas\global_mining_polygons_v2.gpkg"
KALIMANTAN_GEOJSON = r"d:\POLSTAT STIS\Tingkat 3\Semester 6\DATMIN\Kelompok_3_v4\data\external\kalimantan_boundary.geojson"

print("Loading mining polygons...")
mining_gdf = gpd.read_file(MINING_FILE)

print("Loading kalimantan boundary...")
kali_gdf = gpd.read_file(KALIMANTAN_GEOJSON)

print("Filtering mining polygons to Kalimantan...")
mining_gdf = gpd.sjoin(mining_gdf, kali_gdf, how="inner", predicate="intersects")
print(f"Filtered to {len(mining_gdf)} mining polygons in Kalimantan.")

# Project to World Cylindrical Equal Area (EPSG:6933) for accurate area calculations
kali_proj = kali_gdf.to_crs(epsg=6933)
mining_proj = mining_gdf.to_crs(epsg=6933)

if 'index_right' in mining_proj.columns:
    mining_proj = mining_proj.drop(columns=['index_right'])

print("Loading common domain points...")
common_file = os.path.join(PREDICTIONS_DIR, "common_domain_2019_2024.csv")
points_df = pd.read_csv(common_file)
print(f"Loaded {len(points_df)} points.")

# Convert points to GeoDataFrame
geometry = [Point(xy) for xy in zip(points_df.lon, points_df.lat)]
pts_gdf = gpd.GeoDataFrame(points_df, geometry=geometry, crs="EPSG:4326")
pts_proj = pts_gdf.to_crs(epsg=6933)

print("Buffering points by 10km...")
pts_buffered = pts_proj.copy()
pts_buffered.geometry = pts_proj.geometry.buffer(10000)

print("Finding intersecting points (sjoin)...")
sjoin_res = gpd.sjoin(pts_buffered, mining_proj, how='inner', predicate='intersects')
intersecting_indices = sjoin_res.index.unique()
print(f"Found {len(intersecting_indices)} points within 10km of mining areas.")

print("Dissolving mining polygons for accurate area calculation...")
mining_dissolved = mining_proj.dissolve()
mining_geom = mining_dissolved.geometry.iloc[0]

print("Calculating exact densities...")
densities = [0.0] * len(pts_buffered)
start_time = time.time()

for idx, i in enumerate(intersecting_indices):
    if idx % 1000 == 0 and idx > 0:
        print(f"Processed {idx}/{len(intersecting_indices)}...")
    buf = pts_buffered.geometry.iloc[i]
    intersect_area = buf.intersection(mining_geom).area
    densities[i] = (intersect_area / buf.area) * 100

print(f"Calculation finished in {time.time() - start_time:.1f} seconds.")

points_df['mining_density_10km'] = densities
out_csv = os.path.join(PREDICTIONS_DIR, "mining_density_maus.csv")
points_df[['lon', 'lat', 'mining_density_10km']].to_csv(out_csv, index=False)
print(f"Saved exact mining density to {out_csv}")
