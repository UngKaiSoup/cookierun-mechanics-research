import sys, os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

# Clean fonts and dark styling
plt.style.use('dark_background')
matplotlib.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'Tahoma']
matplotlib.rcParams['axes.unicode_minus'] = False

# Simulation parameters: Natural Run (No Potions, No HP Drain)
T_total = 72.0 # Standard full lifespan in seconds without potions
time = np.linspace(0, T_total, 500)

# Natural HP drain curve (Drain exponent gamma = 1.12)
hp_curve = np.clip(100.0 * (1.0 - (time / T_total)**1.12), 0, 100.0)
speed_curve = 15.0 * (hp_curve / 100.0)

# ============================================================
# CHART A: 2-PANEL SYNCHRONIZED DECAY GRAPH
# ============================================================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8.5), dpi=300, sharex=True)
fig.patch.set_facecolor('#080D1A')

for ax in [ax1, ax2]:
    ax.set_facecolor('#0F172A')
    ax.grid(True, linestyle='--', alpha=0.18, color='#94A3B8')

# Panel 1: HP Decay
ax1.fill_between(time, hp_curve, 0, color='#10B981', alpha=0.18)
ax1.plot(time, hp_curve, color='#10B981', linewidth=3.5, label='Remaining Health (% HP)',
         path_effects=[pe.SimpleLineShadow(shadow_color='#10B981', alpha=0.4, offset=(0,0)), pe.Normal()])

hp_pts = [(0, 100.0, 'Start: 100% HP'), (25, hp_curve[int(25/T_total*500)], f'{hp_curve[int(25/T_total*500)]:.0f}% HP'),
          (50, hp_curve[int(50/T_total*500)], f'{hp_curve[int(50/T_total*500)]:.0f}% HP'), (72, 0.0, '0% HP (Depleted)')]

for t_m, hp_m, txt in hp_pts:
    ax1.scatter([t_m], [hp_m], color='#10B981', s=100, edgecolors='white', linewidth=2, zorder=5)
    offset_y = -14 if t_m == 72 else 8
    ax1.annotate(txt, xy=(t_m, hp_m), xytext=(t_m, hp_m + offset_y),
                 fontsize=9.5, fontweight='bold', color='#6EE7B7', ha='center',
                 bbox=dict(boxstyle='round,pad=0.25', facecolor='#1E293B', edgecolor='#10B981', alpha=0.85))

ax1.set_ylabel("Health (% HP)", fontsize=12.5, fontweight='bold', color='#6EE7B7', labelpad=10)
ax1.set_ylim(-5, 115)
ax1.set_title("CookieRun Classic: Natural HP Drain & Toy Ambulance Speed Curve", 
              fontsize=16, fontweight='bold', color='#F8FAFC', pad=15)
ax1.legend(loc='upper right', frameon=True, facecolor='#1E293B', edgecolor='#334155', fontsize=10.5)

# Panel 2: Speed Curve
ax2.fill_between(time, speed_curve, 0, color='#F59E0B', alpha=0.22)
ax2.plot(time, speed_curve, color='#F59E0B', linewidth=3.5, label='Toy Ambulance Speed Bonus (% Speed)',
         path_effects=[pe.SimpleLineShadow(shadow_color='#F59E0B', alpha=0.4, offset=(0,0)), pe.Normal()])
ax2.axhline(0, color='#64748B', linestyle=':', linewidth=2, label='Baseline (+0% Normal Speed)')

spd_pts = [
    (0, 15.0, 'Peak Sprint\n+15.00% Speed', '#F59E0B'),
    (25, speed_curve[int(25/T_total*500)], f'Cruising\n+{speed_curve[int(25/T_total*500)]:.2f}% Speed', '#FBBF24'),
    (50, speed_curve[int(50/T_total*500)], f'Deceleration\n+{speed_curve[int(50/T_total*500)]:.2f}% Speed', '#FCD34D'),
    (72, 0.0, 'Base Speed\n+0.00%', '#EF4444')
]

for t_m, spd_m, txt, col in spd_pts:
    ax2.scatter([t_m], [spd_m], color=col, s=110, edgecolors='white', linewidth=2, zorder=5)
    offset_y = 2.0 if t_m in [25, 50] else (1.5 if t_m == 0 else 2.5)
    ax2.annotate(txt, xy=(t_m, spd_m), xytext=(t_m, spd_m + offset_y),
                 fontsize=9.5, fontweight='bold', color=col, ha='center',
                 bbox=dict(boxstyle='round,pad=0.25', facecolor='#1E293B', edgecolor=col, alpha=0.85),
                 arrowprops=dict(arrowstyle='->', color=col, lw=1.2))

ax2.set_xlabel("Time Elapsed in Run (Seconds)", fontsize=12.5, fontweight='bold', color='#E2E8F0', labelpad=10)
ax2.set_ylabel("Speed Bonus (%)", fontsize=12.5, fontweight='bold', color='#FCD34D', labelpad=10)
ax2.set_xlim(-1, 76)
ax2.set_ylim(-1, 18)
ax2.legend(loc='upper right', frameon=True, facecolor='#1E293B', edgecolor='#334155', fontsize=10.5)

plt.figtext(0.5, 0.015, "Pure Natural Drain: Speed starts at +15.0% peak and smoothly curves down as HP decreases.", 
            ha='center', fontsize=9.5, color='#94A3B8', style='italic')

plt.subplots_adjust(top=0.92, bottom=0.08, left=0.08, right=0.95, hspace=0.18)
chart_path = "toy_ambulance_natural_decay_curve.png"
plt.savefig(chart_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()

# ============================================================
# CHART B: SINGLE-PANEL DUAL-AXIS OVERLAY GRAPH
# ============================================================
fig, ax1 = plt.subplots(figsize=(12, 6.75), dpi=300)
fig.patch.set_facecolor('#080D1A')
ax1.set_facecolor('#0F172A')
ax2 = ax1.twinx()

# HP (Left Axis - Emerald)
l1 = ax1.plot(time, hp_curve, color='#10B981', linewidth=3.5, label='Health (% HP) [Left Axis]',
              path_effects=[pe.SimpleLineShadow(shadow_color='#10B981', alpha=0.4, offset=(0,0)), pe.Normal()])
ax1.fill_between(time, hp_curve, 0, color='#10B981', alpha=0.12)
ax1.set_ylabel("Remaining Health (% HP)", fontsize=13, fontweight='bold', color='#10B981', labelpad=12)
ax1.tick_params(axis='y', labelcolor='#10B981')
ax1.set_ylim(-5, 115)

# Speed (Right Axis - Gold)
l2 = ax2.plot(time, speed_curve, color='#F59E0B', linewidth=3.5, linestyle='-', label='Ambulance Speed Bonus (%) [Right Axis]',
              path_effects=[pe.SimpleLineShadow(shadow_color='#F59E0B', alpha=0.4, offset=(0,0)), pe.Normal()])
ax2.fill_between(time, speed_curve, 0, color='#F59E0B', alpha=0.12)
ax2.set_ylabel("Speed Bonus (%)", fontsize=13, fontweight='bold', color='#F59E0B', labelpad=12)
ax2.tick_params(axis='y', labelcolor='#F59E0B')
ax2.set_ylim(-0.75, 17.25)

# Key Callouts
ax1.scatter([0, 25, 50, 72], [100, hp_curve[int(25/T_total*500)], hp_curve[int(50/T_total*500)], 0], 
            color='#10B981', s=90, edgecolors='white', zorder=5)
ax2.scatter([0, 25, 50, 72], [15, speed_curve[int(25/T_total*500)], speed_curve[int(50/T_total*500)], 0], 
            color='#F59E0B', s=90, edgecolors='white', zorder=5)

ax1.annotate("Start: 100% HP -> +15.0% Speed (Peak)", xy=(0, 100), xytext=(15, 106),
             fontsize=9.5, fontweight='bold', color='#FBBF24',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#1E293B', edgecolor='#F59E0B', alpha=0.9),
             arrowprops=dict(arrowstyle='->', color='#F59E0B', lw=1.5))

ax1.annotate("50s: 34% HP -> +5.1% Speed (Deceleration)", xy=(50, 34), xytext=(45, 55),
             fontsize=9.5, fontweight='bold', color='#93C5FD',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#1E293B', edgecolor='#3B82F6', alpha=0.9),
             arrowprops=dict(arrowstyle='->', color='#3B82F6', lw=1.5))

ax1.set_title("CookieRun Classic: Toy Ambulance Speed & Natural HP Drain Decay", 
              fontsize=16, fontweight='bold', color='#F8FAFC', pad=18)
ax1.set_xlabel("Time Elapsed (Seconds)", fontsize=13, fontweight='bold', color='#E2E8F0', labelpad=12)
ax1.set_xlim(-1, 76)
ax1.grid(True, linestyle='--', alpha=0.18, color='#94A3B8')

lines = l1 + l2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper right', frameon=True, facecolor='#1E293B', edgecolor='#334155', fontsize=10.5)

plt.figtext(0.5, 0.02, "Formula: Speed(t) = 15.0% * (HP(t) / 100%) | Natural Lifespan ≈ 72s without Potions", 
            ha='center', fontsize=9.5, color='#94A3B8', style='italic')

plt.tight_layout()
chart_overlay_path = "toy_ambulance_overlay_curve.png"
plt.savefig(chart_overlay_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print(f"[+] Clean Curves Rendered: {chart_path} and {chart_overlay_path}")
