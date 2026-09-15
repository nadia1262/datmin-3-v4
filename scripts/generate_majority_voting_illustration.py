import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), dpi=300)
fig.patch.set_facecolor('#f8fafc')

# Colors
c_forest = '#22c55e'
c_shrub = '#eab308'
c_cloud = '#94a3b8'

# ----------------- PANEL 1: Centroid (Lama) -----------------
ax1.set_facecolor('#ffffff')
ax1.set_xlim(0, 500)
ax1.set_ylim(0, 500)
ax1.set_title("METODE LAMA: Single Centroid Sampling\n(Hanya Ambil 1 Titik di Tengah Sel 500m)", 
              fontsize=12, fontweight='bold', pad=15, color='#0f172a')

# Simulated actual landscape: mostly forest
bg_forest = patches.Rectangle((0, 0), 500, 500, color='#dcfce7', alpha=0.6, 
                              label='Kondisi Lahan Sebenarnya: Mayoritas Hutan (80%)')
ax1.add_patch(bg_forest)

# Small cloud patch right in the center
cloud_patch = patches.Ellipse((250, 250), 140, 100, angle=15, color='#cbd5e1', alpha=0.9, 
                              label='Awan Tropis Pas Menutupi Centroid')
ax1.add_patch(cloud_patch)

# Centroid point
ax1.plot(250, 250, marker='X', markersize=16, color='#ef4444', markeredgecolor='black', 
         markeredgewidth=2, label='Titik Centroid (1 Piksel)')

ax1.annotate("Centroid tertutup AWAN!\nAkibatnya: Seluruh blok 500m x 500m\ndianggap NoData / TERBUANG!", 
             xy=(250, 250), xytext=(40, 390),
             arrowprops=dict(facecolor='#ef4444', edgecolor='black', arrowstyle='->', lw=2),
             fontsize=10, fontweight='bold', color='#b91c1c',
             bbox=dict(boxstyle='round,pad=0.6', facecolor='#fee2e2', edgecolor='#ef4444', alpha=0.95))

ax1.text(250, -45, 
         "KELEMAHAN SISTEMATIK:\n"
         "- Gambling: 1 titik menentukan nasib area 25 hektar (500m x 500m)\n"
         "- 24 titik lainnya diabaikan begitu saja\n"
         "- Kehilangan data masif akibat tutupan awan di Kalimantan",
         ha='center', va='top', fontsize=9, fontweight='bold', color='#991b1b',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#fef2f2', edgecolor='#f87171', lw=1.2),
         transform=ax1.transData, clip_on=False)

ax1.set_xlabel('Lebar Sel (500 meter)', fontsize=10, fontweight='bold')
ax1.set_ylabel('Panjang Sel (500 meter)', fontsize=10, fontweight='bold')
ax1.legend(loc='lower left', frameon=True, fontsize=8)
ax1.grid(True, linestyle='--', color='#e2e8f0')

# ----------------- PANEL 2: Majority Voting 25 Titik -----------------
ax2.set_facecolor('#ffffff')
ax2.set_xlim(0, 500)
ax2.set_ylim(0, 500)
ax2.set_title("METODE BARU: Sub-Grid 5x5 Majority Voting\n(25 Titik Sub-Piksel per Sel 500m)", 
              fontsize=12, fontweight='bold', pad=15, color='#0f172a')

# Draw 5x5 grid lines (each 100m)
for i in range(6):
    pos = i * 100
    ax2.axvline(pos, color='#94a3b8', linestyle='-', linewidth=1.2)
    ax2.axhline(pos, color='#94a3b8', linestyle='-', linewidth=1.2)

# Sub-grid point values (5x5 matrix = 25 points at cell centers)
grid_classes = [
    ['forest', 'forest', 'forest', 'forest', 'forest'],
    ['forest', 'shrub',  'forest', 'forest', 'forest'],
    ['forest', 'cloud',  'cloud',  'forest', 'forest'],
    ['shrub',  'forest', 'forest', 'forest', 'forest'],
    ['forest', 'forest', 'forest', 'forest', 'forest'],
]

color_map = {
    'forest': ('#22c55e', 'HUTAN'),
    'shrub': ('#eab308', 'BELUKAR'),
    'cloud': ('#94a3b8', 'AWAN')
}

counts = {'HUTAN': 0, 'BELUKAR': 0, 'AWAN': 0}

for r in range(5):
    for c in range(5):
        cx = c * 100 + 50
        cy = (4 - r) * 100 + 50
        cls_name = grid_classes[r][c]
        hex_c, label = color_map[cls_name]
        counts[label] += 1
        
        # Color the sub-cell
        rect = patches.Rectangle((c*100+2, (4-r)*100+2), 96, 96, color=hex_c, alpha=0.3)
        ax2.add_patch(rect)
        
        # Draw marker
        ax2.plot(cx, cy, marker='o', markersize=8, color=hex_c, markeredgecolor='#0f172a', markeredgewidth=1.2)
        ax2.text(cx, cy-22, label, ha='center', va='center', fontsize=7, fontweight='bold', color='#1e293b')

# Summary Box
result_text = (
    f"HASIL VOTING DARI 25 TITIK SUB-GRID:\n"
    f"- HUTAN   : {counts['HUTAN']} titik (80%)  <-- MODUS TERBANYAK (MENANG!)\n"
    f"- BELUKAR : {counts['BELUKAR']} titik (8%)\n"
    f"- AWAN    : {counts['AWAN']} titik (12%)  (diabaikan / filtered out)\n"
    f"--------------------------------------------------\n"
    f"STATUS AKHIR SEL: KELAS HUTAN (TERSELAMATKAN & AKURAT)"
)

ax2.text(250, -45, result_text, ha='center', va='top', fontsize=9, fontweight='bold', color='#065f46',
         bbox=dict(boxstyle='round,pad=0.6', facecolor='#d1fae5', edgecolor='#10b981', lw=1.5),
         transform=ax2.transData, clip_on=False)

ax2.set_xlabel('Lebar Sel 500m (5 x 100m sub-grid)', fontsize=10, fontweight='bold')
ax2.set_ylabel('Panjang Sel 500m (5 x 100m sub-grid)', fontsize=10, fontweight='bold')
ax2.grid(False)

plt.tight_layout()
fig.subplots_adjust(bottom=0.25)

os.makedirs('reports', exist_ok=True)
out_path = 'reports/ilustrasi_majority_voting.png'
plt.savefig(out_path, dpi=300)
print('Saved to', out_path)
