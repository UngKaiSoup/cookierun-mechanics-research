import sys, os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib import font_manager

# Set Thai Font
thai_fonts = ['Leelawadee UI', 'Tahoma', 'Segoe UI', 'Angsana New', 'Cordia New']
available_fonts = [f.name for f in font_manager.fontManager.ttflist]
chosen_font = 'Tahoma'
for tf in thai_fonts:
    if tf in available_fonts:
        chosen_font = tf
        break

plt.style.use('dark_background')
matplotlib.rcParams['font.sans-serif'] = [chosen_font, 'DejaVu Sans', 'Arial']
matplotlib.rcParams['axes.unicode_minus'] = False

# Simulation Setup
T_full = 72.0
T_half = 36.0

time_full = np.linspace(0, T_full, 500)
time_half = np.linspace(0, T_half, 250)
dt_full = time_full[1] - time_full[0]
dt_half = time_half[1] - time_half[0]

hp_ratio_full = np.clip(1.0 - (time_full / T_full)**1.12, 0, 1.0)
hp_ratio_half = np.clip(0.5 * (1.0 - (time_half / T_half)**1.12), 0, 0.5)

# =========================================================================
# MODEL 1: เลือดเยอะยิ่งวิ่งไว (แปรผันตรง)
# =========================================================================
spd_A1 = 0.15 * hp_ratio_full
spd_A2 = 0.15 * hp_ratio_half

dist_A1 = np.cumsum(spd_A1 * 10.0) * dt_full
dist_A2 = np.cumsum(spd_A2 * 10.0) * dt_half

fig1, ax1 = plt.subplots(figsize=(11, 6.5), dpi=300)
fig1.patch.set_facecolor('#080D1A')
ax1.set_facecolor('#0F172A')
ax1.grid(True, linestyle='--', alpha=0.18, color='#94A3B8')

ax1.fill_between(time_full, dist_A1, 0, color='#10B981', alpha=0.14)
ax1.fill_between(time_half, dist_A2, 0, color='#F59E0B', alpha=0.14)

# Lines
ax1.plot(time_full, dist_A1, color='#10B981', linewidth=3.8, label='เริ่มต้นที่เลือด 100%',
         path_effects=[pe.SimpleLineShadow(shadow_color='#10B981', alpha=0.45, offset=(0,0)), pe.Normal()])
ax1.plot(time_half, dist_A2, color='#F59E0B', linewidth=3.2, label='เริ่มต้นที่เลือด 50%',
         path_effects=[pe.SimpleLineShadow(shadow_color='#F59E0B', alpha=0.45, offset=(0,0)), pe.Normal()])
ax1.axhline(0, color='#64748B', linestyle=':', linewidth=2, label='ตัวเปล่า (ความเร็วปกติ)')

ax1.set_title("โมเดลที่ 1: เลือดเยอะยิ่งวิ่งไว (ความเร็วแปรผันตรงกับเลือด)", 
              fontsize=16, fontweight='bold', color='#F8FAFC', pad=18)
ax1.set_xlabel("เวลา (วินาที)", fontsize=12.5, fontweight='bold', color='#E2E8F0', labelpad=10)
ax1.set_ylabel("ระยะทางสะสมที่นำหน้าตัวเปล่า", fontsize=12.5, fontweight='bold', color='#E2E8F0', labelpad=10)
ax1.set_xlim(-2, 78)
ax1.set_ylim(-3, 65)

leg1 = ax1.legend(loc='upper left', frameon=True, facecolor='#1E293B', edgecolor='#334155', fontsize=11)
for t in leg1.get_texts(): t.set_color('#E2E8F0')

plt.tight_layout()
out1 = "graph1_high_hp_faster_thai.png"
plt.savefig(out1, dpi=300, facecolor=fig1.get_facecolor(), edgecolor='none')
plt.close()
print(f"[+] Saved Clean Graph 1: {out1}")

# =========================================================================
# MODEL 2: เลือดน้อยยิ่งวิ่งไว (แปรผกผัน)
# =========================================================================
spd_B1 = 0.15 * (1.0 - hp_ratio_full)
spd_B2 = 0.15 * (1.0 - hp_ratio_half / 0.5 * 0.5)

dist_B1 = np.cumsum(spd_B1 * 10.0) * dt_full
dist_B2 = np.cumsum(spd_B2 * 10.0) * dt_half

fig2, ax2 = plt.subplots(figsize=(11, 6.5), dpi=300)
fig2.patch.set_facecolor('#080D1A')
ax2.set_facecolor('#0F172A')
ax2.grid(True, linestyle='--', alpha=0.18, color='#94A3B8')

ax2.fill_between(time_full, dist_B1, 0, color='#38BDF8', alpha=0.12)
ax2.fill_between(time_half, dist_B2, 0, color='#F43F5E', alpha=0.14)

# Lines
ax2.plot(time_full, dist_B1, color='#38BDF8', linewidth=3.8, label='เริ่มต้นที่เลือด 100%',
         path_effects=[pe.SimpleLineShadow(shadow_color='#0284C7', alpha=0.45, offset=(0,0)), pe.Normal()])
ax2.plot(time_half, dist_B2, color='#F43F5E', linewidth=3.2, label='เริ่มต้นที่เลือด 50%',
         path_effects=[pe.SimpleLineShadow(shadow_color='#E11D48', alpha=0.45, offset=(0,0)), pe.Normal()])
ax2.axhline(0, color='#64748B', linestyle=':', linewidth=2, label='ตัวเปล่า (ความเร็วปกติ)')

ax2.set_title("โมเดลที่ 2: เลือดน้อยยิ่งวิ่งไว (ความเร็วแปรผกผันกับเลือด)", 
              fontsize=16, fontweight='bold', color='#F8FAFC', pad=18)
ax2.set_xlabel("เวลา (วินาที)", fontsize=12.5, fontweight='bold', color='#E2E8F0', labelpad=10)
ax2.set_ylabel("ระยะทางสะสมที่นำหน้าตัวเปล่า", fontsize=12.5, fontweight='bold', color='#E2E8F0', labelpad=10)
ax2.set_xlim(-2, 78)
ax2.set_ylim(-3, 65)

leg2 = ax2.legend(loc='upper left', frameon=True, facecolor='#1E293B', edgecolor='#334155', fontsize=11)
for t in leg2.get_texts(): t.set_color('#E2E8F0')

plt.tight_layout()
out2 = "graph2_low_hp_faster_thai.png"
plt.savefig(out2, dpi=300, facecolor=fig2.get_facecolor(), edgecolor='none')
plt.close()
print(f"[+] Saved Clean Graph 2: {out2}")

# =========================================================================
# COMBINED COMPARISON GRAPH
# =========================================================================
fig3, (gax1, gax2) = plt.subplots(1, 2, figsize=(16, 6.5), dpi=300)
fig3.patch.set_facecolor('#080D1A')

for gax in [gax1, gax2]:
    gax.set_facecolor('#0F172A')
    gax.grid(True, linestyle='--', alpha=0.18, color='#94A3B8')
    gax.set_xlim(-2, 78)
    gax.set_ylim(-3, 65)
    gax.set_xlabel("เวลา (วินาที)", fontsize=11.5, fontweight='bold', color='#E2E8F0', labelpad=8)
    gax.set_ylabel("ระยะทางสะสมที่นำหน้าตัวเปล่า", fontsize=11.5, fontweight='bold', color='#E2E8F0', labelpad=8)

# Panel 1: Model 1
gax1.fill_between(time_full, dist_A1, 0, color='#10B981', alpha=0.14)
gax1.fill_between(time_half, dist_A2, 0, color='#F59E0B', alpha=0.14)
gax1.plot(time_full, dist_A1, color='#10B981', linewidth=3.5, label='เริ่มต้นที่เลือด 100%')
gax1.plot(time_half, dist_A2, color='#F59E0B', linewidth=3.0, label='เริ่มต้นที่เลือด 50%')
gax1.axhline(0, color='#64748B', linestyle=':', linewidth=1.8, label='ตัวเปล่า (ความเร็วปกติ)')
gax1.set_title("โมเดลที่ 1: เลือดเยอะยิ่งวิ่งไว (แปรผันตรง)", fontsize=13.5, fontweight='bold', color='#10B981', pad=12)
l1 = gax1.legend(loc='upper left', frameon=True, facecolor='#1E293B', edgecolor='#334155', fontsize=10)
for t in l1.get_texts(): t.set_color('#E2E8F0')

# Panel 2: Model 2
gax2.fill_between(time_full, dist_B1, 0, color='#38BDF8', alpha=0.12)
gax2.fill_between(time_half, dist_B2, 0, color='#F43F5E', alpha=0.14)
gax2.plot(time_full, dist_B1, color='#38BDF8', linewidth=3.5, label='เริ่มต้นที่เลือด 100%')
gax2.plot(time_half, dist_B2, color='#F43F5E', linewidth=3.0, label='เริ่มต้นที่เลือด 50%')
gax2.axhline(0, color='#64748B', linestyle=':', linewidth=1.8, label='ตัวเปล่า (ความเร็วปกติ)')
gax2.set_title("โมเดลที่ 2: เลือดน้อยยิ่งวิ่งไว (แปรผกผัน)", fontsize=13.5, fontweight='bold', color='#F43F5E', pad=12)
l2 = gax2.legend(loc='upper left', frameon=True, facecolor='#1E293B', edgecolor='#334155', fontsize=10)
for t in l2.get_texts(): t.set_color('#E2E8F0')

fig3.suptitle("เปรียบเทียบแนวโน้มระยะทางสะสมระหว่าง 2 โมเดล", 
              fontsize=16, fontweight='bold', color='#F8FAFC', y=0.98)

plt.tight_layout()
out3 = "graph_comparison_both_theories_thai.png"
plt.savefig(out3, dpi=300, facecolor=fig3.get_facecolor(), edgecolor='none')
plt.close()
print(f"[+] Saved Clean Combined Graph: {out3}")
