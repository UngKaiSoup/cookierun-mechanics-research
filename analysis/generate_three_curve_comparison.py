import sys, os
import numpy as np

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

# Modern Sleek Dark Theme
plt.style.use('dark_background')
matplotlib.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'Tahoma']
matplotlib.rcParams['axes.unicode_minus'] = False

# Simulation Settings
T_full = 72.0 # Full lifespan from 100% HP (72s)
T_half = 36.0 # Lifespan from 50% HP (36s)

t_full = np.linspace(0, T_full, 400)
t_half = np.linspace(0, T_half, 200)

# Curve 1: Toy Ambulance (Full HP Start - 100% HP)
# HP decays from 100% -> 0%
hp_1 = np.clip(100.0 * (1.0 - (t_full / T_full)**1.12), 0, 100.0)
speed_1 = 15.0 * (hp_1 / 100.0)

# Curve 2: Toy Ambulance (50% HP Start / Post-Hit Condition)
# HP decays from 50% -> 0%
hp_2 = np.clip(50.0 * (1.0 - (t_half / T_half)**1.12), 0, 50.0)
speed_2 = 15.0 * (hp_2 / 100.0)

# Curve 3: Normal Baseline (No Treasure - Constant +0.0%)
speed_3 = np.zeros_like(t_full)

# ============================================================
# CREATE HIGH-RES 3-CURVE COMPARISON GRAPH
# ============================================================
fig, ax = plt.subplots(figsize=(12.5, 7.2), dpi=300)
fig.patch.set_facecolor('#080D1A') # Deep dark background
ax.set_facecolor('#0F172A') # Card slate background

# Grid
ax.grid(True, linestyle='--', alpha=0.18, color='#94A3B8')

# Area fills under curves for glowing aesthetic
ax.fill_between(t_full, speed_1, 0, color='#10B981', alpha=0.15)
ax.fill_between(t_half, speed_2, 0, color='#F59E0B', alpha=0.18)

# 1. Plot Curve 1: Full HP Ambulance
line1, = ax.plot(t_full, speed_1, color='#10B981', linewidth=3.8, 
                 label='Ambulance (100% HP Start -> Starts at +15.0% Speed)',
                 path_effects=[pe.SimpleLineShadow(shadow_color='#10B981', alpha=0.45, offset=(0,0)), pe.Normal()])

# 2. Plot Curve 2: 50% HP Ambulance
line2, = ax.plot(t_half, speed_2, color='#F59E0B', linewidth=3.5, 
                 label='Ambulance (50% HP Start -> Starts at +7.5% Speed)',
                 path_effects=[pe.SimpleLineShadow(shadow_color='#F59E0B', alpha=0.45, offset=(0,0)), pe.Normal()])

# 3. Plot Curve 3: Normal Baseline
line3, = ax.plot(t_full, speed_3, color='#94A3B8', linewidth=2.5, linestyle='--', 
                 label='Normal Baseline (No Treasure -> Constant +0.0% Speed)', alpha=0.9)

# Scatter points at t=0 for starting speeds
ax.scatter([0], [15.0], color='#10B981', s=140, edgecolors='white', linewidth=2.2, zorder=6)
ax.scatter([0], [7.5], color='#F59E0B', s=140, edgecolors='white', linewidth=2.2, zorder=6)
ax.scatter([0], [0.0], color='#94A3B8', s=110, edgecolors='white', linewidth=2, zorder=6)

# Annotations for Starting Speeds
ax.annotate('Full HP Start (100% HP)\nPeak Speed: +15.00%', xy=(0, 15.0), xytext=(15, 15.6),
            fontsize=10, fontweight='bold', color='#6EE7B7', ha='left',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#1E293B', edgecolor='#10B981', alpha=0.92),
            arrowprops=dict(arrowstyle='->', color='#10B981', lw=1.8))

ax.annotate('Reduced HP Start (50% HP)\nInitial Speed: +7.50%', xy=(0, 7.5), xytext=(15, 8.4),
            fontsize=10, fontweight='bold', color='#FCD34D', ha='left',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#1E293B', edgecolor='#F59E0B', alpha=0.92),
            arrowprops=dict(arrowstyle='->', color='#F59E0B', lw=1.8))

ax.annotate('Normal Run Baseline\nConstant: +0.00% Speed', xy=(0, 0.0), xytext=(15, 1.2),
            fontsize=9.5, fontweight='bold', color='#CBD5E1', ha='left',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#1E293B', edgecolor='#94A3B8', alpha=0.88),
            arrowprops=dict(arrowstyle='->', color='#94A3B8', lw=1.5))

# End-of-life Markers
ax.scatter([T_half], [0.0], color='#F59E0B', s=100, edgecolors='white', linewidth=1.8, zorder=6)
ax.annotate('50% HP Depleted\n(t = 36s | Speed -> 0%)', xy=(T_half, 0.0), xytext=(T_half, 3.2),
            fontsize=9, fontweight='bold', color='#FCD34D', ha='center',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#1E293B', edgecolor='#F59E0B', alpha=0.88),
            arrowprops=dict(arrowstyle='->', color='#F59E0B', lw=1.4))

ax.scatter([T_full], [0.0], color='#10B981', s=100, edgecolors='white', linewidth=1.8, zorder=6)
ax.annotate('100% HP Depleted\n(t = 72s | Speed -> 0%)', xy=(T_full, 0.0), xytext=(T_full - 3, 3.2),
            fontsize=9, fontweight='bold', color='#6EE7B7', ha='center',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='#1E293B', edgecolor='#10B981', alpha=0.88),
            arrowprops=dict(arrowstyle='->', color='#10B981', lw=1.4))

# Titles and Axis Labels
ax.set_title("CookieRun Classic: Toy Ambulance Speed Decay Curves vs Normal Run", 
             fontsize=17, fontweight='bold', color='#F8FAFC', pad=22)
ax.set_xlabel("Time Elapsed in Run (Seconds / Ticks)", fontsize=13, fontweight='bold', color='#E2E8F0', labelpad=12)
ax.set_ylabel("Speed Bonus (%)", fontsize=13, fontweight='bold', color='#E2E8F0', labelpad=12)

ax.set_xlim(-2, 78)
ax.set_ylim(-1, 18)

# Legend
leg = ax.legend(loc='upper right', frameon=True, facecolor='#1E293B', edgecolor='#334155', fontsize=10.5)
for text in leg.get_texts():
    text.set_color('#E2E8F0')

# Watermark / Footer
plt.figtext(0.5, 0.018, "Formula: Speed Bonus = 15.0% * (Current HP / Max HP) | Pure Natural Drain Curves without HP Drain Buffs", 
            ha='center', fontsize=9.5, color='#94A3B8', style='italic')

plt.tight_layout()
output_path = "toy_ambulance_3_curves_comparison.png"
plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print(f"[+] Successfully Generated 3-Curve Graph: {output_path}")
