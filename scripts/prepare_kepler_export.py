"""
prepare_kepler_export.py
Menyiapkan file CSV bersih untuk visualisasi di Kepler.gl
"""
import pandas as pd
import json
import os

CLASS_NAMES = {
    0: 'Forest',
    1: 'Shrubland/Agriculture',
    2: 'Built-up',
    3: 'Bare/Mining-like',
    4: 'Water'
}

# Warna per kelas (hex) — konsisten dengan color_palette.py
CLASS_COLORS_HEX = {
    0: '#1B7837',  # Forest — dark green
    1: '#A6D96A',  # Shrubland — light green
    2: '#E31A1C',  # Built-up — red
    3: '#C4A35A',  # Bare/Mining — tan/brown
    4: '#2166AC',  # Water — blue
}

def extract_lon_lat(geo_str):
    """Parse kolom .geo dari GEE output ke lon/lat"""
    try:
        geo = json.loads(geo_str)
        coords = geo['coordinates']
        return coords[0], coords[1]  # lon, lat
    except:
        return None, None

def prepare_kepler_csv(year, model='lgbm'):
    input_path = f"data/predictions/predictions_{model}_{year}.csv"
    output_path = f"data/predictions/kepler_{year}.csv"

    if not os.path.exists(input_path):
        print(f"[SKIP] {input_path} tidak ditemukan")
        return

    print(f"[Loading] {input_path}...")
    df = pd.read_csv(input_path)

    # Extract lon/lat — predictions CSV sudah punya kolom lon/lat langsung
    if 'lon' in df.columns and 'lat' in df.columns:
        pass  # sudah ada
    elif '.geo' in df.columns:
        coords = df['.geo'].apply(lambda x: pd.Series(extract_lon_lat(x)))
        df['lon'] = coords[0]
        df['lat'] = coords[1]
    elif 'longitude' in df.columns:
        df['lon'] = df['longitude']
        df['lat'] = df['latitude']
    else:
        print(f"[ERROR] Tidak ada kolom koordinat di {input_path}")
        return

    # Tambah nama kelas dan warna
    df['class_name'] = df['predicted_class'].map(CLASS_NAMES)
    df['color_hex'] = df['predicted_class'].map(CLASS_COLORS_HEX)
    df['year'] = year

    # Pilih kolom yang diperlukan saja (ringan untuk Kepler.gl)
    cols = ['lon', 'lat', 'predicted_class', 'class_name', 'color_hex',
            'year', 'NDVI', 'NDBI', 'BSI', 'max_prob']
    cols_exist = [c for c in cols if c in df.columns]

    # Drop baris tanpa koordinat
    df_clean = df[cols_exist].dropna(subset=['lon', 'lat'])

    df_clean.to_csv(output_path, index=False)
    print(f"[OK] Saved: {output_path} ({len(df_clean):,} rows)")

def prepare_all_years_combined():
    """Gabung semua tahun ke satu file untuk animasi temporal di Kepler.gl"""
    frames = []
    for year in [2019, 2020, 2021, 2022, 2023, 2024]:
        path = f"data/predictions/kepler_{year}.csv"
        if os.path.exists(path):
            frames.append(pd.read_csv(path))

    if frames:
        combined = pd.concat(frames, ignore_index=True)
        combined.to_csv("data/predictions/kepler_all_years.csv", index=False)
        print(f"\n[OK] Combined saved: kepler_all_years.csv ({len(combined):,} rows)")
        print("     → Gunakan filter 'year' di Kepler.gl untuk animasi temporal!")

if __name__ == "__main__":
    print("="*50)
    print("  PREPARING KEPLER.GL EXPORT FILES")
    print("="*50)

    # Export tahun 2024 saja dulu (paling relevan untuk peta final)
    prepare_kepler_csv(2024)
    prepare_kepler_csv(2021)  # baseline
    prepare_kepler_csv(2018)  # titik awal

    # Gabung semua tahun untuk animasi
    prepare_all_years_combined()

    print("\n[DONE] File siap di: data/predictions/kepler_*.csv")
    print("\n--- CARA LOAD KE KEPLER.GL ---")
    print("1. Buka kepler.gl di browser")
    print("2. Drag-drop file kepler_2024.csv")
    print("3. Set layer type: POINT")
    print("4. Lat: 'lat', Lon: 'lon'")
    print("5. Color: by 'predicted_class'")
    print("6. Set warna manual per kelas:")
    print("   0 (Forest) = #1B7837")
    print("   1 (Shrubland) = #A6D96A")
    print("   2 (Built-up) = #E31A1C")
    print("   3 (Bare/Mining) = #C4A35A")
    print("   4 (Water) = #2166AC")
    print("7. Radius: 3-5 pixels")
    print("8. Opacity: 0.8")
