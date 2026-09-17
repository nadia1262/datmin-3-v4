import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np
import os

# Create figure with high DPI
fig, ax = plt.subplots(figsize=(11, 7.5), dpi=300)
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#ffffff')
ax.set_xlim(0, 1000)
ax.set_ylim(0, 760)
ax.axis('off')

# Color palette (Clean, modern academic)
c_forest = '#15803d'      # Vibrant deep green
c_forest_flow = '#86efac' # Light green flow
c_shrub = '#ca8a04'       # Amber gold
c_shrub_flow = '#fef08a'  # Light gold flow
c_built = '#dc2626'       # Crimson red
c_bare = '#ea580c'        # Orange
c_water = '#0284c7'       # Blue

# Title / Header of the chart
ax.text(500, 730, "Dekomposisi Alih Fungsi Lahan Makro (2019 → 2024)", 
        ha='center', va='center', fontsize=14, fontweight='bold', color='#0f172a')
ax.text(500, 705, "Analisis Trajektori Agregasi Spasial Majority Voting 500m (N = 1.499.024 Sel Grid Valid)", 
        ha='center', va='center', fontsize=10, color='#475569')

# Bar positions
x_left = 140
x_right = 860
bar_w = 45

y_top = 660
# Left Bar segments (2019)
h_f19 = 310
h_s19 = 85

y_f19_b = y_top - h_f19
y_f19_t = y_top

y_s19_b = y_f19_b - 30 - h_s19
y_s19_t = y_f19_b - 30

# Right Bar segments (2024)
h_f24 = 320
h_s24 = 75

y_f24_b = y_top - h_f24
y_f24_t = y_top

y_s24_b = y_f24_b - 30 - h_s24
y_s24_t = y_f24_b - 30

# Draw Left Bars
ax.add_patch(patches.Rectangle((x_left, y_f19_b), bar_w, h_f19, facecolor=c_forest, edgecolor='#0f172a', lw=1.2))
ax.text(x_left - 15, (y_f19_b + y_f19_t)/2, "Forest (2019)\n1.185.974 sel (79,1%)", ha='right', va='center', fontsize=9, fontweight='bold', color='#14532d')

ax.add_patch(patches.Rectangle((x_left, y_s19_b), bar_w, h_s19, facecolor=c_shrub, edgecolor='#0f172a', lw=1.2))
ax.text(x_left - 15, (y_s19_b + y_s19_t)/2, "Shrubland (2019)\n264.273 sel (17,6%)", ha='right', va='center', fontsize=9, fontweight='bold', color='#854d0e')

# Draw Right Bars
ax.add_patch(patches.Rectangle((x_right - bar_w, y_f24_b), bar_w, h_f24, facecolor=c_forest, edgecolor='#0f172a', lw=1.2))
ax.text(x_right + 15, (y_f24_b + y_f24_t)/2, "Forest (2024)\n1.215.945 sel (81,1%)", ha='left', va='center', fontsize=9, fontweight='bold', color='#14532d')

ax.add_patch(patches.Rectangle((x_right - bar_w, y_s24_b), bar_w, h_s24, facecolor=c_shrub, edgecolor='#0f172a', lw=1.2))
ax.text(x_right + 15, (y_s24_b + y_s24_t)/2, "Shrubland (2024)\n228.783 sel (15,3%)", ha='left', va='center', fontsize=9, fontweight='bold', color='#854d0e')

# Helper function to draw smooth Bezier flow ribbon
def draw_flow(y1_b, y1_t, y2_b, y2_t, color, alpha=0.55):
    x0 = x_left + bar_w
    x1 = x_right - bar_w
    cx0 = x0 + (x1 - x0) * 0.5
    cx1 = x1 - (x1 - x0) * 0.5
    
    verts = [
        (x0, y1_t),
        (cx0, y1_t),
        (cx1, y2_t),
        (x1, y2_t),
        (x1, y2_b),
        (cx1, y2_b),
        (cx0, y1_b),
        (x0, y1_b),
        (x0, y1_t)
    ]
    codes = [
        Path.MOVETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.LINETO,
        Path.CURVE4,
        Path.CURVE4,
        Path.CURVE4,
        Path.CLOSEPOLY
    ]
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor=color, edgecolor='none', alpha=alpha)
    ax.add_patch(patch)

# 1. Flow Forest Persistent (1.106.197 sel = 93.27% of 2019 forest)
h_f_persist = h_f19 * (1106197.0 / 1185974.0)
y_f_persist_t19 = y_f19_t
y_f_persist_b19 = y_f19_t - h_f_persist

y_f_persist_t24 = y_f24_t
y_f_persist_b24 = y_f24_t - h_f_persist
draw_flow(y_f_persist_b19, y_f_persist_t19, y_f_persist_b24, y_f_persist_t24, '#16a34a', alpha=0.45)

ax.text(500, (y_f_persist_t19 + y_f_persist_b19)/2, 
        "Hutan Persisten (Stabil)\n1.106.197 Sel Grid (93,3% dari Hutan 2019)", 
        ha='center', va='center', fontsize=10, fontweight='bold', color='#064e3b',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#dcfce7', edgecolor='#22c55e', alpha=0.9))

# 2. Flow Forest Loss (Forest -> Shrubland/Others: 79.777 sel)
y_loss_t19 = y_f_persist_b19
y_loss_b19 = y_f19_b
# Into top of Shrubland 2024
y_loss_t24 = y_s24_t
y_loss_b24 = y_s24_t - (h_s19 * (68678.0 / 264273.0))
draw_flow(y_loss_b19, y_loss_t19, y_loss_b24, y_loss_t24, '#ef4444', alpha=0.55)

# 3. Flow Forest Gain (Shrubland -> Forest: 104.412 sel + others = 109.748 sel)
y_gain_t19 = y_s19_t
y_gain_b19 = y_s19_t - (h_s19 * (104412.0 / 264273.0))
# Into bottom of Forest 2024
y_gain_t24 = y_f_persist_b24
y_gain_b24 = y_f24_b
draw_flow(y_gain_b19, y_gain_t19, y_gain_b24, y_gain_t24, '#10b981', alpha=0.6)

# 4. Flow Shrubland Persistent
y_s_persist_t19 = y_gain_b19
y_s_persist_b19 = y_s19_b
y_s_persist_t24 = y_loss_b24
y_s_persist_b24 = y_s24_b
draw_flow(y_s_persist_b19, y_s_persist_t19, y_s_persist_b24, y_s_persist_t24, '#eab308', alpha=0.35)

# ----------------- BOTTOM COMPARISON CARD -----------------
card_y = 35
card_h = 120

# Background card
card_rect = patches.FancyBboxPatch((70, card_y), 860, card_h,
                                   boxstyle="round,pad=10,rounding_size=12",
                                   facecolor='#f8fafc', edgecolor='#cbd5e1', lw=1.5)
ax.add_patch(card_rect)

# Left column: Metrics
ax.text(95, card_y + 90, "NERACA PERUBAHAN HUTAN MAKRO (5 TAHUN):", fontsize=9.5, fontweight='bold', color='#1e293b')
ax.text(95, card_y + 58, "[LOSS] Forest Loss : 79.777 sel (5,3% total Kalimantan)", fontsize=9, fontweight='bold', color='#b91c1c')
ax.text(95, card_y + 26, "[GAIN] Forest Gain : 109.748 sel (7,3% reklasifikasi semu)", fontsize=9, fontweight='bold', color='#047857')

# Vertical divider
ax.plot([500, 500], [card_y + 12, card_y + 108], color='#cbd5e1', lw=1.5, linestyle='--')

# Right column: The Ecological Paradox & Transition to Slide 9
ax.text(520, card_y + 90, "TEMUAN KRITIS (PARADOKS FOREST GAIN):", fontsize=9.5, fontweight='bold', color='#b45309')
ax.text(520, card_y + 50, 
        "• Gain (109.748 sel) > Loss (79.777 sel) mustahil secara biologis.\n"
        "• Bukan penghijauan riil, melainkan DISTORSI PIKSEL CAMPURAN (500m).\n"
        "• Dekonstruksi ilmiah & validasi KIPP dibedah pada Slide 9.",
        fontsize=8.5, fontweight='medium', color='#334155', linespacing=1.35)

plt.tight_layout()
os.makedirs('reports', exist_ok=True)
out_path = 'reports/slide8_sankey_clean.png'
plt.savefig(out_path, dpi=300, bbox_inches='tight')
plt.close()
print("Saved clean Slide 8 Sankey visual to", out_path)
