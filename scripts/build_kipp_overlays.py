"""
Generate KIPP IKN 10m classification overlay PNGs and stats JSON
for the swipe map component in the dashboard.

Output:
  dashboard/data/cache/kipp_10m_2019_overlay.png
  dashboard/data/cache/kipp_10m_2024_overlay.png
  dashboard/data/cache/kipp_10m_stats.json
"""
import os
import sys
import json
import numpy as np
import pandas as pd
from PIL import Image

# --- Paths ---
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
PRED_DIR = os.path.join(ROOT, 'data', 'predictions')
CACHE_DIR = os.path.join(ROOT, 'dashboard', 'data', 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)

# --- Class color map (RGBA) matching the legend in kipp_swipe_map.py ---
# 0: Forest       → #2D6A4F (deep forest green)
# 1: Shrubland    → #6E9A2E (yellow-green)
# 2: Built-up     → #C6371F (brick red)
# 3: Bare/Mining  → #D97706 (orange)
# 4: Water        → #1B5FA8 (blue)
CLASS_COLORS = {
    0: (45, 106, 79, 220),    # Forest
    1: (110, 154, 46, 220),   # Shrubland/Agriculture
    2: (198, 55, 31, 220),    # Built-up
    3: (217, 119, 6, 220),    # Bare/Mining-like
    4: (27, 95, 168, 220),    # Water
}
TRANSPARENT = (0, 0, 0, 0)

def build_overlay(csv_path, out_png, bounds):
    """Read prediction CSV→ rasterize into RGBA PNG aligned to bounds."""
    df = pd.read_csv(csv_path)
    
    lon_min, lat_min, lon_max, lat_max = bounds
    
    # Determine pixel spacing from data
    lons_u = np.sort(df['lon'].unique())
    lats_u = np.sort(df['lat'].unique())
    lon_step = float(np.median(np.diff(lons_u)))
    lat_step = float(np.median(np.diff(lats_u)))
    
    # Image dimensions covering the full overlay bounds
    img_w = int(round((lon_max - lon_min) / lon_step)) + 1
    img_h = int(round((lat_max - lat_min) / lat_step)) + 1
    
    print(f"  Image size: {img_w} x {img_h} px (step={lon_step:.8f}°)")
    
    # Create transparent RGBA image
    img_arr = np.zeros((img_h, img_w, 4), dtype=np.uint8)
    
    # Map data points to pixel coordinates
    cols = np.round((df['lon'].values - lon_min) / lon_step).astype(int)
    rows = np.round((lat_max - df['lat'].values) / lat_step).astype(int)  # flip Y
    classes = df['predicted_class'].values
    
    # Filter valid pixels
    valid = (cols >= 0) & (cols < img_w) & (rows >= 0) & (rows < img_h)
    cols, rows, classes = cols[valid], rows[valid], classes[valid]
    
    for cls, color in CLASS_COLORS.items():
        mask = classes == cls
        if mask.any():
            img_arr[rows[mask], cols[mask]] = color
    
    img = Image.fromarray(img_arr, 'RGBA')
    img.save(out_png, optimize=True)
    print(f"  Saved: {out_png} ({os.path.getsize(out_png) / 1024:.0f} KB)")
    return df

def build_stats(df19, df24, out_json):
    """Compute KIPP 10m change stats and save as JSON."""
    label_map = {
        0: 'Forest (Hutan)',
        1: 'Shrubland (Semak)',
        2: 'Built-up (Terbangun)',
        3: 'Bare/Mining (Terbuka)',
        4: 'Water (Air)'
    }
    
    counts_19 = df19['predicted_class'].value_counts().sort_index()
    counts_24 = df24['predicted_class'].value_counts().sort_index()
    
    all_classes = sorted(set(counts_19.index) | set(counts_24.index))
    stats = []
    for cls in all_classes:
        n19 = int(counts_19.get(cls, 0))
        n24 = int(counts_24.get(cls, 0))
        ha19 = n19 * 0.01
        ha24 = n24 * 0.01
        delta = ha24 - ha19
        pct = (delta / ha19 * 100) if ha19 > 0 else 0
        stats.append({
            'Kelas Lahan': label_map.get(cls, f'Kelas {cls}'),
            'Piksel 2019': n19,
            'Piksel 2024': n24,
            'Area 2019 (Ha)': round(ha19, 1),
            'Area 2024 (Ha)': round(ha24, 1),
            'Delta (Ha)': round(delta, 1),
            'Perubahan (%)': round(pct, 1)
        })
    
    payload = {'total_pixels': len(df19), 'stats': stats}
    with open(out_json, 'w') as f:
        json.dump(payload, f, indent=2)
    print(f"  Saved: {out_json}")


def main():
    print("=" * 60)
    print("  BUILDING KIPP IKN 10m OVERLAY PNGs + STATS")
    print("=" * 60)
    
    csv_19 = os.path.join(PRED_DIR, 'ikn_10m_predicted_2019.csv')
    csv_24 = os.path.join(PRED_DIR, 'ikn_10m_predicted_2024.csv')
    
    if not os.path.exists(csv_19) or not os.path.exists(csv_24):
        print("ERROR: Prediction CSVs not found.")
        sys.exit(1)
    
    # Read one file to determine data extent
    df_ref = pd.read_csv(csv_19)
    lon_min = min(df_ref['lon'].min(), pd.read_csv(csv_24, usecols=['lon'])['lon'].min())
    lon_max = max(df_ref['lon'].max(), pd.read_csv(csv_24, usecols=['lon'])['lon'].max())
    lat_min = min(df_ref['lat'].min(), pd.read_csv(csv_24, usecols=['lat'])['lat'].min())
    lat_max = max(df_ref['lat'].max(), pd.read_csv(csv_24, usecols=['lat'])['lat'].max())
    
    # Use exact data bounds (the Leaflet component will be updated to match)
    bounds = (lon_min, lat_min, lon_max, lat_max)
    print(f"  Bounds: lon [{lon_min:.6f}, {lon_max:.6f}], lat [{lat_min:.6f}, {lat_max:.6f}]")
    
    print("\n[1/3] Building 2019 overlay...")
    df19 = build_overlay(csv_19, os.path.join(CACHE_DIR, 'kipp_10m_2019_overlay.png'), bounds)
    
    print("\n[2/3] Building 2024 overlay...")
    df24 = build_overlay(csv_24, os.path.join(CACHE_DIR, 'kipp_10m_2024_overlay.png'), bounds)
    
    print("\n[3/3] Building stats JSON...")
    build_stats(df19, df24, os.path.join(CACHE_DIR, 'kipp_10m_stats.json'))
    
    # Print the bounds for updating the Leaflet component
    print(f"\n  ✅ DONE! Update Leaflet bounds to:")
    print(f"     [[{lat_min:.6f}, {lon_min:.6f}], [{lat_max:.6f}, {lon_max:.6f}]]")
    print(f"     Center: [{(lat_min+lat_max)/2:.6f}, {(lon_min+lon_max)/2:.6f}]")

if __name__ == '__main__':
    main()
