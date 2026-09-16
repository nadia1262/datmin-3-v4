import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

# Create figure with 3 panels
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 6.2), dpi=300)
fig.patch.set_facecolor('#ffffff')

# Color palette (harmonious & professional)
c_forest = '#15803d'     # Dark green
c_forest_light = '#bbf7d0'
c_shrub = '#ca8a04'      # Golden amber
c_shrub_light = '#fef08a'
c_open = '#c2410c'       # Terracotta orange
c_open_light = '#fed7aa'
c_water = '#0284c7'      # Blue
c_cloud = '#94a3b8'      # Slate grey
c_border = '#334155'

# ==========================================
# PANEL 1: Ground Truth 10m (Sentinel-2)
# ==========================================
ax1.set_facecolor('#f8fafc')
ax1.set_xlim(0, 500)
ax1.set_ylim(0, 500)
ax1.set_title("1. Ground Truth Mikro (10m)\nSentinel-2 (10m x 10m)", 
              fontsize=12, fontweight='bold', pad=12, color='#0f172a')

# Create a realistic 50x50 micro-pixel mosaic representing 10m pixels across 500m
np.random.seed(42)
mosaic = np.zeros((50, 50, 3))
# Forest base (predominant)
for r in range(50):
    for c in range(50):
        # spatial correlation for natural clusters
        val = np.sin(r/6.0) + np.cos(c/6.0) + np.random.normal(0, 0.4)
        if val > 0.3:
            mosaic[r, c] = [0.13, 0.65, 0.30] # Forest
        elif val > -0.4:
            mosaic[r, c] = [0.22, 0.78, 0.40] # Lighter Forest
        elif val > -0.9:
            mosaic[r, c] = [0.85, 0.70, 0.20] # Shrub
        else:
            mosaic[r, c] = [0.85, 0.45, 0.25] # Open land

ax1.imshow(mosaic, extent=[0, 500, 0, 500], origin='lower')
ax1.set_xlabel("Lebar Sel: 500 meter", fontsize=9, fontweight='bold', color='#475569')
ax1.set_ylabel("Panjang Sel: 500 meter", fontsize=9, fontweight='bold', color='#475569')

# Subtitle explanation box
ax1.text(250, -45, 
         "Karakteristik Lanskap:\n"
         "Heterogenitas alami Kalimantan (hutan, belukar,\ndan lahan terbuka) pada resolusi mikro 10 meter.",
         ha='center', va='top', fontsize=8.5, color='#334155',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#f1f5f9', edgecolor='#cbd5e1', lw=1),
         transform=ax1.transData, clip_on=False)

# ==========================================
# PANEL 2: Sub-Grid 5x5 Sampling Matrix
# ==========================================
ax2.set_facecolor('#ffffff')
ax2.set_xlim(0, 500)
ax2.set_ylim(0, 500)
ax2.set_title("2. Diskritasi Sub-Grid 5x5\n25 Titik Sampling (Interval 100m)", 
              fontsize=12, fontweight='bold', pad=12, color='#0f172a')

# Underlay light mosaic
ax2.imshow(mosaic, extent=[0, 500, 0, 500], origin='lower', alpha=0.35)

# Draw 5x5 grid lines
for i in range(6):
    pos = i * 100
    ax2.axvline(pos, color='#475569', linestyle='--', linewidth=1.2)
    ax2.axhline(pos, color='#475569', linestyle='--', linewidth=1.2)

# Sub-grid point values (5x5 matrix = 25 points)
# 19 Forest, 4 Shrub, 2 Open
grid_classes = [
    ['forest', 'forest', 'forest', 'forest', 'forest'],
    ['forest', 'forest', 'forest', 'shrub',  'shrub'],
    ['forest', 'forest', 'forest', 'forest', 'forest'],
    ['shrub',  'forest', 'forest', 'open',   'forest'],
    ['forest', 'shrub',  'forest', 'forest', 'open'],
]

color_defs = {
    'forest': ('#16a34a', 'Hutan'),
    'shrub':  ('#ca8a04', 'Belukar'),
    'open':   ('#dc2626', 'Terbuka')
}

counts = {'Hutan': 0, 'Belukar': 0, 'Terbuka': 0}

for r in range(5):
    for c in range(5):
        cx = c * 100 + 50
        cy = (4 - r) * 100 + 50
        cls_key = grid_classes[r][c]
        hex_c, label = color_defs[cls_key]
        counts[label] += 1
        
        # Sub-point marker
        ax2.plot(cx, cy, marker='o', markersize=9, color=hex_c, 
                 markeredgecolor='#0f172a', markeredgewidth=1.4)

ax2.set_xlabel("Lebar Sel 500m (5 x 100m)", fontsize=9, fontweight='bold', color='#475569')
ax2.set_ylabel("Panjang Sel 500m (5 x 100m)", fontsize=9, fontweight='bold', color='#475569')

# Subtitle explanation box
ax2.text(250, -45, 
         "Arsitektur Sampling:\n"
         "25 titik sub-grid ditempatkan secara sistematis\nsetiap 100m di dalam area 25 Hektar (500m x 500m).",
         ha='center', va='top', fontsize=8.5, color='#334155',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#f1f5f9', edgecolor='#cbd5e1', lw=1),
         transform=ax2.transData, clip_on=False)

# ==========================================
# PANEL 3: Majority Voting & Final 500m Cell
# ==========================================
ax3.set_facecolor('#ffffff')
ax3.set_xlim(0, 500)
ax3.set_ylim(0, 500)
ax3.set_title("3. Konsensus Majority Voting\nOutput Sel Makro (500m x 500m)", 
              fontsize=12, fontweight='bold', pad=12, color='#0f172a')

# The final cell is solid Forest green (since Forest won overwhelmingly)
final_rect = patches.Rectangle((15, 15), 470, 470, color='#22c55e', alpha=0.85, 
                               edgecolor='#15803d', linewidth=3)
ax3.add_patch(final_rect)

# Add stats card inside the cell
summary_box = (
    "HASIL MAJORITY VOTING (N = 25):\n\n"
    f"  * Hutan    : {counts['Hutan']} titik (76.0%)  [MODUS]\n"
    f"  * Belukar  : {counts['Belukar']} titik (16.0%)\n"
    f"  * Terbuka  : {counts['Terbuka']} titik ( 8.0%)\n"
    "--------------------------------------\n"
    "  KONSENSUS FINAL: KELAS HUTAN\n"
    "  (Representatif, Robust & Bebas Bias)"
)

ax3.text(250, 250, summary_box, ha='center', va='center', fontsize=10, fontweight='bold',
         color='#064e3b',
         bbox=dict(boxstyle='round,pad=0.8', facecolor='#ffffff', edgecolor='#059669', lw=2))

ax3.set_xlabel("Lebar Sel Makro: 500 meter", fontsize=9, fontweight='bold', color='#475569')
ax3.set_ylabel("Panjang Sel Makro: 500 meter", fontsize=9, fontweight='bold', color='#475569')
ax3.set_xticks([])
ax3.set_yticks([])

# Subtitle explanation box
ax3.text(250, -45, 
         "Pemberian Label Objektif:\n"
         "Kelas modus terbanyak menjadi label resmi sel makro.\nMenghilangkan bias spasial & menstabilkan estimasi.",
         ha='center', va='top', fontsize=8.5, color='#065f46',
         bbox=dict(boxstyle='round,pad=0.5', facecolor='#ecfdf5', edgecolor='#10b981', lw=1.2),
         transform=ax3.transData, clip_on=False)

# Position text boxes safely below axes using transform=fig.transFigure or tight margins
plt.tight_layout()
fig.subplots_adjust(bottom=0.24, top=0.88, wspace=0.25)

# Adjust bbox positions relative to axes
ax1.set_xlabel("Lebar Sel: 500 meter", fontsize=9, fontweight='bold', color='#475569', labelpad=8)
ax2.set_xlabel("Lebar Sel 500m (5 x 100m)", fontsize=9, fontweight='bold', color='#475569', labelpad=8)
ax3.set_xlabel("Lebar Sel Makro: 500 meter", fontsize=9, fontweight='bold', color='#475569', labelpad=8)

os.makedirs('reports', exist_ok=True)
out_file = 'reports/diagram_majority_voting_pure.png'
plt.savefig(out_file, dpi=300, bbox_inches='tight')
plt.close()
print("Diagram regenerated successfully at:", out_file)
