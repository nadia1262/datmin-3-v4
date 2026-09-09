import os
import urllib.request
import ssl

out_dir = r"d:\POLSTAT STIS\Tingkat 3\Semester 6\DATMIN\Kelompok_3_v4\data\external\global_mining_areas"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "global_mining_polygons_v2.gpkg")

url = "https://download.pangaea.de/dataset/942325/files/global_mining_polygons_v2.gpkg"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print(f"Downloading {url} to {out_file}...")
try:
    with urllib.request.urlopen(url, context=ctx) as response, open(out_file, 'wb') as out:
        out.write(response.read())
    print("Download complete.")
except Exception as e:
    print("Error:", e)
