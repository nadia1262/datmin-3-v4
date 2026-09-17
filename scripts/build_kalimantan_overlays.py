"""
Generate full-Kalimantan classification overlay PNGs (2019 & 2024)
from the majority_voting_kalimantan.csv for the swipe map dashboard.

Output:
  dashboard/data/cache/kalimantan_2019_overlay.png
  dashboard/data/cache/kalimantan_2024_overlay.png
  dashboard/data/cache/kalimantan_overlay_meta.json
"""
import os, sys, json, time
import numpy as np
import pandas as pd
from PIL import Image

ROOT      = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CACHE_DIR = os.path.join(ROOT, 'dashboard', 'data', 'cache')
MV_CSV    = os.path.join(ROOT, 'reports', 'majority_voting_kalimantan.csv')
os.makedirs(CACHE_DIR, exist_ok=True)

# Class label -> RGBA colour (matching the swipe-map legend)
LABEL_COLOR = {
    'Forest':                (45, 106,  79, 230),
    'Shrubland/Agriculture': (110, 154,  46, 230),
    'Built-up':              (198,  55,  31, 230),
    'Bare/Mining-like':      (217, 119,   6, 230),
    'Water':                 ( 27,  95, 168, 230),
}

# Pixel size in degrees  (~500 m at equator ≈ 0.0045°)
STEP = 0.0045


def build_overlay(lons, lats, labels, bounds, out_path, tag):
    t0 = time.time()
    lon_min, lat_min, lon_max, lat_max = bounds
    img_w = int(np.ceil((lon_max - lon_min) / STEP)) + 1
    img_h = int(np.ceil((lat_max - lat_min) / STEP)) + 1
    print(f"  [{tag}] Image size: {img_w} x {img_h} px")

    img = np.zeros((img_h, img_w, 4), dtype=np.uint8)

    cols = np.round((lons - lon_min) / STEP).astype(np.int32)
    rows = np.round((lat_max - lats) / STEP).astype(np.int32)

    valid = (cols >= 0) & (cols < img_w) & (rows >= 0) & (rows < img_h)
    cols, rows, labels_v = cols[valid], rows[valid], labels[valid]

    for label, color in LABEL_COLOR.items():
        mask = labels_v == label
        if mask.any():
            rr, cc = rows[mask], cols[mask]
            # Paint a 2x2 block per point so there are no gaps at zoom-out
            for dr in range(2):
                for dc in range(2):
                    r2 = np.clip(rr + dr, 0, img_h - 1)
                    c2 = np.clip(cc + dc, 0, img_w - 1)
                    img[r2, c2] = color

    im = Image.fromarray(img, 'RGBA')
    im.save(out_path, optimize=True)
    sz = os.path.getsize(out_path)
    print(f"  [{tag}] Saved {out_path}  ({sz/1024:.0f} KB, {time.time()-t0:.1f}s)")
    return img_w, img_h


def main():
    print("=" * 60)
    print("  BUILDING FULL-KALIMANTAN OVERLAY PNGs")
    print("=" * 60)

    if not os.path.exists(MV_CSV):
        print(f"ERROR: {MV_CSV} not found"); sys.exit(1)

    print("  Loading majority voting CSV ...")
    df = pd.read_csv(MV_CSV, usecols=[
        'lon_2019', 'lat_2019', 'majority_label_2019', 'majority_label_2024'
    ])
    print(f"  Loaded {len(df):,} rows")

    lons = df['lon_2019'].values
    lats = df['lat_2019'].values

    # Compute tight bounds + small padding
    PAD = STEP * 3
    lon_min, lon_max = float(lons.min()) - PAD, float(lons.max()) + PAD
    lat_min, lat_max = float(lats.min()) - PAD, float(lats.max()) + PAD
    bounds = (lon_min, lat_min, lon_max, lat_max)
    print(f"  Bounds: lon [{lon_min:.4f}, {lon_max:.4f}], lat [{lat_min:.4f}, {lat_max:.4f}]")

    # --- 2019 ---
    w, h = build_overlay(
        lons, lats, df['majority_label_2019'].values, bounds,
        os.path.join(CACHE_DIR, 'kalimantan_2019_overlay.png'), '2019'
    )

    # --- 2024 ---
    build_overlay(
        lons, lats, df['majority_label_2024'].values, bounds,
        os.path.join(CACHE_DIR, 'kalimantan_2024_overlay.png'), '2024'
    )

    # --- Meta JSON (bounds for Leaflet) ---
    meta = {
        'south': lat_min, 'north': lat_max,
        'west': lon_min, 'east': lon_max,
        'center_lat': (lat_min + lat_max) / 2,
        'center_lon': (lon_min + lon_max) / 2,
        'img_w': w, 'img_h': h,
    }
    meta_path = os.path.join(CACHE_DIR, 'kalimantan_overlay_meta.json')
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)
    print(f"  Saved meta: {meta_path}")
    print(f"\n  DONE!")


if __name__ == '__main__':
    main()
