import sys, os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

# Modern Dark UI Theme
plt.style.use('dark_background')
matplotlib.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'Tahoma']
matplotlib.rcParams['axes.unicode_minus'] = False

# Simulation Settings
T_total = 72.0 # Total natural lifespan without potions (72 seconds)
time = np.linspace(0, T_total, 500)
dt = time[1] - time[0]

# Natural HP Drain Curve (100% -> 0%)
hp_ratio = np.clip(1.0 - (time / T_total)**1.12, 0, 1.0)

# Model A: High HP = Faster (True Game Reality)
# Speed Bonus(t) = +15% * (HP / 100)
speed_bonus_A = 0.15 * hp_ratio
delta_dist_A = np.cumsum(speed_bonus_A * 10.0) * dt

# Model B: Low HP = Faster (Inverted / Misunderstood Tooltip)
# Speed Bonus(t) = +15% * (1 - HP / 100)
speed_bonus_B = 0.15 * (1.0 - hp_ratio)
delta_dist_B = np.cumsum(speed_bonus_B * 10.0) * dt

# Baseline (No Treasure Normal Run): Delta Distance = 0
delta_dist_baseline = np.zeros_like(time)

# ============================================================
# CREATE HIGH-RES DIFFERENTIAL DISTANCE GRAPH
# ============================================================
fig, ax = plt.subplots(figsize=(13, 7.5), dpi=300)
fig.patch.set_facecolor('#080D1A')
ax.set_facecolor('#0F172A')

# Grid
ax.grid(True, linestyle='--', alpha=0.18, color='#94A3B8')

# Area Fills for Visual Impact
ax.fill_between(time, delta_dist_A, 0, color='#10B981', alpha=0.12)
ax.fill_between(time, delta_dist_B, 0, color='#EF4444', alpha=0.10)

# 1. Plot Model A (High HP = Fast) - Vibrant Emerald
line_A, = ax.plot(time, delta_dist_A, color='#10B981', linewidth=4.0, 
                  label='Model A: High HP = Faster (True In-Game Reality)',
                  path_effects=[pe.SimpleLineShadow(shadow_color='#10B981', alpha=0.5, offset=(0,0)), pe.Normal()])

# 2. Plot Model B (Low HP = Fast) - Crimson / Coral Dashed
line_B, = ax.plot(time, delta_dist_B, color='#F87171', linewidth=3.5, linestyle='--',
                  label='Model B: Low HP = Faster (Inverted Tooltip Theory)',
                  path_effects=[pe.SimpleLineShadow(shadow_color='#EF4444', alpha=0.4, offset=(0,0)), pe.Normal()])

# 3. Plot Baseline - Cool Slate Dotted
line_base, = ax.plot(time, delta_dist_baseline, color='#94A3B8', linewidth=2.5, linestyle=':',
                     label='Baseline: Normal Run / No Treasure (Delta Distance = 0m)')

# Key Differential Markers
# Point at t=20s (Early Game Divergence)
t_20_idx = int(20.0 / T_total * 500)
ax.scatter([20], [delta_dist_A[t_20_idx]], color='#10B981', s=130, edgecolors='white', linewidth=2, zorder=6)
ax.scatter([20], [delta_dist_B[t_20_idx]], color='#F87171', s=130, edgecolors='white', linewidth=2, zorder=6)

ax.annotate('Early Gap Divergence (0-20s):\nModel A pulls away immediately!\n(Matches Actual Video Evidence)', 
            xy=(20, delta_dist_A[t_20_idx]), xytext=(7, 28),
            fontsize=10, fontweight='bold', color='#6EE7B7', ha='left',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#1E293B', edgecolor='#10B981', alpha=0.95),
            arrowprops=dict(arrowstyle='->', color='#10B981', lw=1.8))

ax.annotate('Model B would stay flat near baseline\n(No lead created in early game)', 
            xy=(20, delta_dist_B[t_20_idx]), xytext=(24, 6),
            fontsize=9.5, fontweight='bold', color='#FCA5A5', ha='left',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#1E293B', edgecolor='#EF4444', alpha=0.92),
            arrowprops=dict(arrowstyle='->', color='#EF4444', lw=1.6))

# Highlight Early Divergence Zone (0 to 25s)
ax.axvspan(0, 25, color='#3B82F6', alpha=0.08, label='Early Zone: Gap Divergence Checkpoint')

# End-point markers at t=72s
ax.scatter([72], [delta_dist_A[-1]], color='#10B981', s=140, edgecolors='white', linewidth=2.2, zorder=6)
ax.annotate(f'Total Lead: +{delta_dist_A[-1]:.1f}m\n(Slope flattens late)', xy=(72, delta_dist_A[-1]), xytext=(61, delta_dist_A[-1] + 6),
            fontsize=10, fontweight='bold', color='#6EE7B7', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#1E293B', edgecolor='#10B981', alpha=0.9))

ax.scatter([72], [delta_dist_B[-1]], color='#F87171', s=140, edgecolors='white', linewidth=2.2, zorder=6)
ax.annotate(f'Total Lead: +{delta_dist_B[-1]:.1f}m\n(Slope steepens late)', xy=(72, delta_dist_B[-1]), xytext=(61, delta_dist_B[-1] - 8),
            fontsize=10, fontweight='bold', color='#FCA5A5', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#1E293B', edgecolor='#EF4444', alpha=0.9))

# Titles and Labels
ax.set_title("Hypothesis Proof: Distance Lead Divergence Over Time (Differential Graph)", 
             fontsize=17, fontweight='bold', color='#F8FAFC', pad=22)
ax.set_xlabel("Time Elapsed from Start (Seconds)", fontsize=13, fontweight='bold', color='#E2E8F0', labelpad=12)
ax.set_ylabel("Differential Distance Lead (Meters Ahead of Baseline)", fontsize=13, fontweight='bold', color='#E2E8F0', labelpad=12)

ax.set_xlim(-2, 78)
ax.set_ylim(-3, 68)

# Legend
leg = ax.legend(loc='upper left', frameon=True, facecolor='#1E293B', edgecolor='#334155', fontsize=10.5)
for text in leg.get_texts():
    text.set_color('#E2E8F0')

# Proof Summary
plt.figtext(0.5, 0.015, "Differential Proof: Model A widens gap immediately at start (Concave). Model B widens only at the end (Convex).", 
            ha='center', fontsize=9.5, color='#94A3B8', style='italic')

plt.tight_layout()
output_path = "toy_ambulance_differential_proof.png"
plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print(f"[+] Successfully Generated Clean Differential Proof Graph: {output_path}")
