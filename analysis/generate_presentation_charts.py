import sys, os
import numpy as np

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

try:
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.patheffects as pe
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "matplotlib"], check=True)
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.patheffects as pe

# Set modern dark styling
plt.style.use('dark_background')
matplotlib.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'Tahoma']
matplotlib.rcParams['axes.unicode_minus'] = False

# ==========================================
# CHART 1: SPEED VS HP PROPORTIONAL FORMULA
# ==========================================
fig, ax = plt.subplots(figsize=(12, 6.75), dpi=300)
fig.patch.set_facecolor('#0B0F19')
ax.set_facecolor('#111827')

# Data
hp = np.linspace(100, 0, 101)
speed_ambulance = 15.0 * (hp / 100.0)
speed_baseline = np.zeros_like(hp)
speed_fixed_tap = np.full_like(hp, 6.0)

# Fill high speed zone (>55%)
ax.fill_between(hp, 0, 16, where=(hp >= 55), color='#065F46', alpha=0.25, label='High Speed Zone (HP > 55% | +8.25% ~ +15%)')

# Plot Lines
ax.plot(hp, speed_ambulance, color='#F59E0B', linewidth=3.5, label='Toy Ambulance (Little Toy Ambulance: +15% Max)', 
        path_effects=[pe.SimpleLineShadow(shadow_color='#F59E0B', alpha=0.3, offset=(0,0)), pe.Normal()])
ax.plot(hp, speed_fixed_tap, color='#3B82F6', linewidth=2.5, linestyle='--', label='Fixed Speed Reference (Oak Tap: +6.0% Constant)', alpha=0.85)
ax.plot(hp, speed_baseline, color='#6B7280', linewidth=2, linestyle=':', label='No Treasure Baseline (+0.0%)', alpha=0.7)

# Scatter points for empirical user tests
test_pts = [
    (100, 15.0, 'Full HP\n+15.0%', '#10B981'),
    (89, 13.35, 'Case 1: No Hit\n(89% HP | +13.35%)', '#34D399'),
    (50, 7.50, 'Case 2: 3 Hits\n(50% HP | +7.5%)', '#FBBF24'),
    (15, 2.25, 'Post-Revive\n(20 HP | +2.25%)', '#EF4444')
]

for x_val, y_val, label, col in test_pts:
    ax.scatter([x_val], [y_val], color=col, s=140, zorder=5, edgecolors='white', linewidth=2)
    offset_y = 1.0 if y_val < 14 else -1.8
    offset_x = 0 if x_val not in [100, 15] else (-3 if x_val == 100 else 4)
    ax.annotate(label, xy=(x_val, y_val), xytext=(x_val + offset_x, y_val + offset_y),
                fontsize=10, fontweight='bold', color=col, ha='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#1F2937', edgecolor=col, alpha=0.9),
                arrowprops=dict(arrowstyle='->', color=col, lw=1.5))

# Formatting & Grid
ax.set_title("CookieRun Classic: Toy Ambulance Speed Mechanics", fontsize=18, fontweight='bold', color='#F9FAFB', pad=20)
ax.set_xlabel("Remaining Health (% HP)", fontsize=13, fontweight='bold', color='#D1D5DB', labelpad=12)
ax.set_ylabel("Speed Bonus (%)", fontsize=13, fontweight='bold', color='#D1D5DB', labelpad=12)

ax.set_xlim(102, -2) # Invert X so 100% is on left
ax.set_ylim(-0.5, 17)
ax.grid(True, linestyle='--', alpha=0.2, color='#9CA3AF')

# Legend
leg = ax.legend(loc='upper right', frameon=True, facecolor='#1F2937', edgecolor='#374151', fontsize=10.5)
for text in leg.get_texts():
    text.set_color('#E5E7EB')

# Subtitle / Watermark
plt.figtext(0.5, 0.02, "Formula: Speed Bonus = 15.0% × (Current HP / Max HP) | Verified with Game Data & In-Game Snapshots", 
            ha='center', fontsize=9.5, color='#9CA3AF', style='italic')

plt.tight_layout()
chart1_path = "toy_ambulance_speed_mechanics.png"
plt.savefig(chart1_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print(f"[+] Saved High-Res Chart 1: {chart1_path}")

# ==========================================
# CHART 2: CUMULATIVE DISTANCE RACE OVER TIME
# ==========================================
fig, ax = plt.subplots(figsize=(12, 6.75), dpi=300)
fig.patch.set_facecolor('#0B0F19')
ax.set_facecolor('#111827')

time = np.linspace(0, 60, 300) # 60 seconds run

# Case 4: HP Drain 37% + Potions (Sustained HP 85% avg -> Speed +12.75%)
dist_case4 = (1.0 + 0.1275) * time * 10.0

# Case 1: Ambulance No Hit (Natural Drain 100% -> 40% avg speed +10.5%)
speed_t1 = 1.0 + 0.15 * np.clip(1.0 - time/90.0, 0, 1.0)
dist_case1 = np.cumsum(speed_t1) * (time[1]-time[0]) * 10.0

# Case 2: Ambulance 3 Hits (Stun penalty 1.2s at t=5, then HP 50% avg speed +7.5%)
dist_case2 = np.zeros_like(time)
for idx, t in enumerate(time):
    if t < 5.0:
        dist_case2[idx] = (1.0 + 0.14) * t * 10.0
    elif t < 6.5: # 1.5s stun
        dist_case2[idx] = dist_case2[int(5.0/(time[1]-time[0]))]
    else: # Run at 50% HP (+7.5%)
        dt = t - 6.5
        dist_case2[idx] = dist_case2[int(5.0/(time[1]-time[0]))] + (1.0 + 0.075) * dt * 10.0

# Case 3: Baseline No Treasure (Speed 1.0)
dist_case3 = 1.0 * time * 10.0

# Plot distance lines
ax.plot(time, dist_case4, color='#10B981', linewidth=3.5, label='Case 4: Ambulance + HP Drain 37% + Big Potions (HP > 55%)',
        path_effects=[pe.SimpleLineShadow(shadow_color='#10B981', alpha=0.3, offset=(0,0)), pe.Normal()])
ax.plot(time, dist_case1, color='#F59E0B', linewidth=3, label='Case 1: Ambulance (No Hit | HP 100% → 60%)')
ax.plot(time, dist_case2, color='#EC4899', linewidth=2.8, linestyle='-.', label='Case 2: Ambulance (3 Hits Stun Penalty → HP 50%)')
ax.plot(time, dist_case3, color='#9CA3AF', linewidth=2, linestyle=':', label='Case 3: No Treasure Baseline (Standard Speed +0%)')

# Annotations at t=60
ax.scatter([60], [dist_case4[-1]], color='#10B981', s=120, zorder=5)
ax.annotate(f"Rank 1: +12.8% Lead\n({dist_case4[-1]:.0f}m)", xy=(60, dist_case4[-1]), xytext=(52, dist_case4[-1] + 15),
            fontsize=10, fontweight='bold', color='#10B981', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#1F2937', edgecolor='#10B981', alpha=0.9))

ax.scatter([60], [dist_case1[-1]], color='#F59E0B', s=120, zorder=5)
ax.annotate(f"Rank 2: +10.2% Lead\n({dist_case1[-1]:.0f}m)", xy=(60, dist_case1[-1]), xytext=(52, dist_case1[-1] - 30),
            fontsize=10, fontweight='bold', color='#F59E0B', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#1F2937', edgecolor='#F59E0B', alpha=0.9))

ax.scatter([60], [dist_case2[-1]], color='#EC4899', s=120, zorder=5)
ax.annotate(f"Rank 3: Recovers & Passes Baseline\n({dist_case2[-1]:.0f}m)", xy=(60, dist_case2[-1]), xytext=(48, dist_case2[-1] - 45),
            fontsize=9.5, fontweight='bold', color='#EC4899', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#1F2937', edgecolor='#EC4899', alpha=0.9))

# Stun event callout
ax.annotate("3 Hits Hit-Stun (~1.5s Lost)", xy=(5.5, dist_case2[int(5.5/(time[1]-time[0]))]), 
            xytext=(16, 30), fontsize=9, fontweight='bold', color='#F87171',
            arrowprops=dict(arrowstyle='->', color='#F87171', lw=1.5),
            bbox=dict(boxstyle='round,pad=0.2', facecolor='#1F2937', edgecolor='#EF4444', alpha=0.85))

# Formatting & Grid
ax.set_title("Distance Traveled Over Time (Test Comparison)", fontsize=18, fontweight='bold', color='#F9FAFB', pad=20)
ax.set_xlabel("Time (Seconds)", fontsize=13, fontweight='bold', color='#D1D5DB', labelpad=12)
ax.set_ylabel("Cumulative Distance Traveled (Meters)", fontsize=13, fontweight='bold', color='#D1D5DB', labelpad=12)

ax.set_xlim(-1, 65)
ax.set_ylim(0, max(dist_case4) * 1.08)
ax.grid(True, linestyle='--', alpha=0.2, color='#9CA3AF')

# Legend
leg2 = ax.legend(loc='upper left', frameon=True, facecolor='#1F2937', edgecolor='#374151', fontsize=10)
for text in leg2.get_texts():
    text.set_color('#E5E7EB')

plt.figtext(0.5, 0.02, "Real-world test simulation: Stun penalty reduces initial lead, but HP > 55% sustains massive distance advantage.", 
            ha='center', fontsize=9.5, color='#9CA3AF', style='italic')

plt.tight_layout()
chart2_path = "toy_ambulance_distance_comparison.png"
plt.savefig(chart2_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print(f"[+] Saved High-Res Chart 2: {chart2_path}")
