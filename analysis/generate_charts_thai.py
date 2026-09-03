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
T_full = 72.0 # 72 seconds for 100% HP
T_half = 36.0 # 36 seconds for 50% HP

time_full = np.linspace(0, T_full, 500)
time_half = np.linspace(0, T_half, 250)
dt_full = time_full[1] - time_full[0]
dt_half = time_half[1] - time_half[0]

# HP curves
hp_ratio_full = np.clip(1.0 - (time_full / T_full)**1.12, 0, 1.0)
hp_ratio_half = np.clip(0.5 * (1.0 - (time_half / T_half)**1.12), 0, 0.5)

# =========================================================================
# GRAPH 1: MODEL A "เลือดเยอะวิ่งไว" (ความจริงในเกม - ปรากฏการณ์เส้นไม่ไขว้)
# =========================================================================
# Speed = +15% * (HP / 100)
spd_A1 = 0.15 * hp_ratio_full # Starts at +15%, drops to 0% at 72s
spd_A2 = 0.15 * hp_ratio_half # Starts at +7.5%, drops to 0% at 36s

# Distance Lead (Integral of speed * BaseSpeed 10 m/s)
dist_A1 = np.cumsum(spd_A1 * 10.0) * dt_full
dist_A2 = np.cumsum(spd_A2 * 10.0) * dt_half

fig1, ax1 = plt.subplots(figsize=(12, 7.2), dpi=300)
fig1.patch.set_facecolor('#080D1A')
ax1.set_facecolor('#0F172A')
ax1.grid(True, linestyle='--', alpha=0.18, color='#94A3B8')

ax1.fill_between(time_full, dist_A1, 0, color='#10B981', alpha=0.14)
ax1.fill_between(time_half, dist_A2, 0, color='#F59E0B', alpha=0.14)

# Line 1: 100% HP Start
ax1.plot(time_full, dist_A1, color='#10B981', linewidth=4.0, 
         label='เคสที่ 1: เลือดเต็ม 100% (สปีดเริ่มที่ +15% สูงสุด)',
         path_effects=[pe.SimpleLineShadow(shadow_color='#10B981', alpha=0.45, offset=(0,0)), pe.Normal()])

# Line 2: 50% HP Start
ax1.plot(time_half, dist_A2, color='#F59E0B', linewidth=3.5,
         label='เคสที่ 2: เลือดเหลือ 50% (สปีดเริ่มที่ +7.5% ปานกลาง)',
         path_effects=[pe.SimpleLineShadow(shadow_color='#F59E0B', alpha=0.45, offset=(0,0)), pe.Normal()])

# Baseline
ax1.axhline(0, color='#64748B', linestyle=':', linewidth=2, label='ตัวเปล่า (ไม่ใส่สมบัติ ระยะนำ = 0m)')

# Points & Annotations
ax1.scatter([0], [0], color='white', s=90, zorder=6)
ax1.scatter([20], [dist_A1[int(20/T_full*500)]], color='#10B981', s=120, edgecolors='white', linewidth=2, zorder=6)
ax1.scatter([20], [dist_A2[int(20/T_half*250)]], color='#F59E0B', s=120, edgecolors='white', linewidth=2, zorder=6)

ax1.annotate('ออกตัวปุ๊บพุ่งนำทันที (+15%)\nเส้นถ่างห่างขึ้นเรื่อยๆ ไม่มีการไขว้กัน', 
             xy=(20, dist_A1[int(20/T_full*500)]), xytext=(6, 32),
             fontsize=10, fontweight='bold', color='#6EE7B7',
             bbox=dict(boxstyle='round,pad=0.35', facecolor='#1E293B', edgecolor='#10B981', alpha=0.92),
             arrowprops=dict(arrowstyle='->', color='#10B981', lw=1.6))

ax1.annotate('เลือด 50% ออกตัวช้ากว่า (+7.5%)\nตามหลังเส้น 100% ตลอดทั้งเกม', 
             xy=(20, dist_A2[int(20/T_half*250)]), xytext=(25, 8),
             fontsize=9.5, fontweight='bold', color='#FCD34D',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#1E293B', edgecolor='#F59E0B', alpha=0.92),
             arrowprops=dict(arrowstyle='->', color='#F59E0B', lw=1.5))

ax1.scatter([T_half], [dist_A2[-1]], color='#F59E0B', s=120, edgecolors='white', zorder=6)
ax1.annotate(f'เลือด 50% หมดหลอด (36 วิ)\nนำตัวเปล่า +{dist_A2[-1]:.1f}m', xy=(T_half, dist_A2[-1]), xytext=(T_half - 2, dist_A2[-1] + 6),
             fontsize=9.5, fontweight='bold', color='#FCD34D', ha='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#1E293B', edgecolor='#F59E0B', alpha=0.9))

ax1.scatter([T_full], [dist_A1[-1]], color='#10B981', s=130, edgecolors='white', zorder=6)
ax1.annotate(f'เลือด 100% หมดหลอด (72 วิ)\nนำตัวเปล่า +{dist_A1[-1]:.1f}m', xy=(T_full, dist_A1[-1]), xytext=(T_full - 6, dist_A1[-1] + 6),
             fontsize=10, fontweight='bold', color='#6EE7B7', ha='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#1E293B', edgecolor='#10B981', alpha=0.9))

ax1.set_title("กราฟที่ 1: ทฤษฎี 'เลือดเยอะยิ่งวิ่งไว' (ความจริงในเกม - เส้นไม่ไขว้กัน)", 
              fontsize=16, fontweight='bold', color='#F8FAFC', pad=18)
ax1.set_xlabel("เวลาที่ผ่านไปนับจากเริ่มออกตัว (วินาที)", fontsize=12.5, fontweight='bold', color='#E2E8F0', labelpad=10)
ax1.set_ylabel("ระยะทางที่วิ่งนำหน้าตัวเปล่า (เมตร)", fontsize=12.5, fontweight='bold', color='#E2E8F0', labelpad=10)
ax1.set_xlim(-2, 78)
ax1.set_ylim(-3, 68)

leg1 = ax1.legend(loc='upper left', frameon=True, facecolor='#1E293B', edgecolor='#334155', fontsize=10.5)
for t in leg1.get_texts(): t.set_color('#E2E8F0')

plt.figtext(0.5, 0.015, "ข้อสังเกต: เส้นเลือด 100% จะพุ่งชันขึ้นทันทีตั้งแต่เริ่มเกม และวิ่งนำหน้าเส้นเลือด 50% ตลอดทั้งเกม (ตรงกับคลิปวิดีโอจริง)", 
            ha='center', fontsize=9.5, color='#94A3B8', style='italic')

plt.tight_layout()
out1 = "graph1_high_hp_faster_thai.png"
plt.savefig(out1, dpi=300, facecolor=fig1.get_facecolor(), edgecolor='none')
plt.close()
print(f"[+] Saved Graph 1: {out1}")

# =========================================================================
# GRAPH 2: MODEL B "เลือดน้อยยิ่งวิ่งไว" (ตามที่เข้าใจผิด - ปรากฏการณ์เส้นไขว้)
# =========================================================================
# Speed = +15% * (1 - HP / 100)
spd_B1 = 0.15 * (1.0 - hp_ratio_full)
spd_B2 = 0.15 * (1.0 - hp_ratio_half / 0.5 * 0.5)

dist_B1 = np.cumsum(spd_B1 * 10.0) * dt_full
dist_B2 = np.cumsum(spd_B2 * 10.0) * dt_half

fig2, ax2 = plt.subplots(figsize=(12, 7.2), dpi=300)
fig2.patch.set_facecolor('#080D1A')
ax2.set_facecolor('#0F172A')
ax2.grid(True, linestyle='--', alpha=0.18, color='#94A3B8')

ax2.fill_between(time_full, dist_B1, 0, color='#38BDF8', alpha=0.12)
ax2.fill_between(time_half, dist_B2, 0, color='#F43F5E', alpha=0.14)

# Line 1: 100% HP Start
ax2.plot(time_full, dist_B1, color='#38BDF8', linewidth=4.0, linestyle='--',
         label='เคสที่ 1: เลือดเต็ม 100% (เริ่มสปีด +0% -> โค้งชันท้ายเกมแบบ Expo)',
         path_effects=[pe.SimpleLineShadow(shadow_color='#0284C7', alpha=0.45, offset=(0,0)), pe.Normal()])

# Line 2: 50% HP Start
ax2.plot(time_half, dist_B2, color='#F43F5E', linewidth=3.5,
         label='เคสที่ 2: เลือดเหลือ 50% (เริ่มสปีด +7.5% ทันที -> ออกตัวเร็วกว่า!)',
         path_effects=[pe.SimpleLineShadow(shadow_color='#E11D48', alpha=0.45, offset=(0,0)), pe.Normal()])

# Baseline
ax2.axhline(0, color='#64748B', linestyle=':', linewidth=2, label='ตัวเปล่า (ไม่ใส่สมบัติ ระยะนำ = 0m)')

cross_t = 36.0
cross_val = dist_B2[-1]
ax2.scatter([cross_t], [cross_val], color='#F43F5E', s=130, edgecolors='white', zorder=6)

ax2.annotate('เกิดปรากฏการณ์เส้นไขว้ (Cross-Over):\nเลือด 50% จะแซงนำเลือด 100% ในช่วงต้นเกม!\n(เพราะเริ่มที่ +7.5% ส่วน 100% เริ่มที่ +0%)', 
             xy=(18, dist_B2[int(18/T_half*250)]), xytext=(4, 28),
             fontsize=10, fontweight='bold', color='#FDA4AF',
             bbox=dict(boxstyle='round,pad=0.35', facecolor='#1E293B', edgecolor='#F43F5E', alpha=0.92),
             arrowprops=dict(arrowstyle='->', color='#F43F5E', lw=1.6))

ax2.annotate('เลือด 100% ช่วงต้นเกมจะแบนราบติดตัวเปล่า\nแล้วเพิ่งมาเร่งแซงคืนช่วงหลังวินาทีที่ 45+', 
             xy=(50, dist_B1[int(50/T_full*500)]), xytext=(35, 12),
             fontsize=9.5, fontweight='bold', color='#BAE6FD',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#1E293B', edgecolor='#38BDF8', alpha=0.92),
             arrowprops=dict(arrowstyle='->', color='#38BDF8', lw=1.5))

ax2.set_title("กราฟที่ 2: ทฤษฎี 'เลือดน้อยยิ่งวิ่งไว' (ตามข้อความที่เข้าใจผิด - เกิดเส้นไขว้กัน)", 
              fontsize=16, fontweight='bold', color='#F8FAFC', pad=18)
ax2.set_xlabel("เวลาที่ผ่านไปนับจากเริ่มออกตัว (วินาที)", fontsize=12.5, fontweight='bold', color='#E2E8F0', labelpad=10)
ax2.set_ylabel("ระยะทางที่วิ่งนำหน้าตัวเปล่า (เมตร)", fontsize=12.5, fontweight='bold', color='#E2E8F0', labelpad=10)
ax2.set_xlim(-2, 78)
ax2.set_ylim(-3, 68)

leg2 = ax2.legend(loc='upper left', frameon=True, facecolor='#1E293B', edgecolor='#334155', fontsize=10.5)
for t in leg2.get_texts(): t.set_color('#E2E8F0')

plt.figtext(0.5, 0.015, "ข้อสังเกต: ถ้าสูตรเป็นเลือดน้อยวิ่งไว ตัวที่เลือด 50% จะต้องแซงตัวเลือด 100% ในช่วงต้นเกม (ซึ่งในคลิปจริงไม่เคยเกิดขึ้น!)", 
            ha='center', fontsize=9.5, color='#94A3B8', style='italic')

plt.tight_layout()
out2 = "graph2_low_hp_faster_thai.png"
plt.savefig(out2, dpi=300, facecolor=fig2.get_facecolor(), edgecolor='none')
plt.close()
print(f"[+] Saved Graph 2: {out2}")

# =========================================================================
# GRAPH 3: COMBINED SIDE-BY-SIDE
# =========================================================================
fig3, (gax1, gax2) = plt.subplots(1, 2, figsize=(18, 7.5), dpi=300)
fig3.patch.set_facecolor('#080D1A')

for gax in [gax1, gax2]:
    gax.set_facecolor('#0F172A')
    gax.grid(True, linestyle='--', alpha=0.18, color='#94A3B8')
    gax.set_xlim(-2, 78)
    gax.set_ylim(-3, 68)
    gax.set_xlabel("เวลาที่ผ่านไปนับจากเริ่มออกตัว (วินาที)", fontsize=11.5, fontweight='bold', color='#E2E8F0', labelpad=8)
    gax.set_ylabel("ระยะทางที่วิ่งนำหน้าตัวเปล่า (เมตร)", fontsize=11.5, fontweight='bold', color='#E2E8F0', labelpad=8)

# Panel 1: Real
gax1.fill_between(time_full, dist_A1, 0, color='#10B981', alpha=0.14)
gax1.fill_between(time_half, dist_A2, 0, color='#F59E0B', alpha=0.14)
gax1.plot(time_full, dist_A1, color='#10B981', linewidth=3.5, label='เลือดเต็ม 100% (เริ่มสปีด +15%)')
gax1.plot(time_half, dist_A2, color='#F59E0B', linewidth=3.0, label='เลือดเหลือ 50% (เริ่มสปีด +7.5%)')
gax1.axhline(0, color='#64748B', linestyle=':', linewidth=1.8, label='ตัวเปล่า (0m)')
gax1.set_title("ทฤษฎี A: เลือดเยอะวิ่งไว [ตรงกับคลิปจริง]\n(เส้นไม่ไขว้กัน เลือด 100% นำขาดตั้งแต่เริ่ม)", 
               fontsize=13.5, fontweight='bold', color='#10B981', pad=12)
l1 = gax1.legend(loc='upper left', frameon=True, facecolor='#1E293B', edgecolor='#334155', fontsize=9.5)
for t in l1.get_texts(): t.set_color('#E2E8F0')

# Panel 2: Inverted
gax2.fill_between(time_full, dist_B1, 0, color='#38BDF8', alpha=0.12)
gax2.fill_between(time_half, dist_B2, 0, color='#F43F5E', alpha=0.14)
gax2.plot(time_full, dist_B1, color='#38BDF8', linewidth=3.5, linestyle='--', label='เลือดเต็ม 100% (เริ่ม +0% โค้งพุ่งท้ายแบบ Expo)')
gax2.plot(time_half, dist_B2, color='#F43F5E', linewidth=3.0, label='เลือดเหลือ 50% (เริ่ม +7.5% แซงนำก่อน!)')
gax2.axhline(0, color='#64748B', linestyle=':', linewidth=1.8, label='ตัวเปล่า (0m)')
gax2.set_title("ทฤษฎี B: เลือดน้อยวิ่งไว [ข้อความที่เข้าใจผิด]\n(เกิดปรากฏการณ์เส้นไขว้ เลือด 50% ต้องแซงก่อน)", 
               fontsize=13.5, fontweight='bold', color='#EF4444', pad=12)
l2 = gax2.legend(loc='upper left', frameon=True, facecolor='#1E293B', edgecolor='#334155', fontsize=9.5)
for t in l2.get_texts(): t.set_color('#E2E8F0')

fig3.suptitle("การพิสูจน์สมมุติฐาน: เปรียบเทียบพฤติกรรมการถ่างของระยะทาง (Differential Lead)", 
              fontsize=16, fontweight='bold', color='#F8FAFC', y=0.98)

plt.tight_layout()
out3 = "graph_comparison_both_theories_thai.png"
plt.savefig(out3, dpi=300, facecolor=fig3.get_facecolor(), edgecolor='none')
plt.close()
print(f"[+] All 3 Thai Graphs Flawlessly Generated!")
