import sys, os
import numpy as np

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

exp_base = 1802
exp_amb = 1658
t_base_raw = exp_base / 20.0 # 90.10 s
t_amb_raw = exp_amb / 20.0   # 82.90 s
hp_end = 0.11                # 11% remaining HP

print("=" * 90)
print(" 🚀 RE-CALCULATION WITH 1 SPEED BLAST ITEM (ลูกไฟวิ่งเร็ว 1 อัน)")
print("=" * 90)

# True integral average HP for Cookie Run non-linear drain (gamma = 1.12)
mean_hp_integral = 1.0 - (1.0 - hp_end) / (1.0 + 1.12) # 0.58019
mean_hp_linear = (1.0 + hp_end) / 2.0                  # 0.55500

print(f"• Raw Baseline Time: {t_base_raw:.2f} s")
print(f"• Raw Ambulance Time: {t_amb_raw:.2f} s")
print(f"• Remaining HP at End: {hp_end*100:.1f} %")
print(f"• True Mean HP (Calculus Integral): {mean_hp_integral*100:.2f} %\n")

print(f"{'Blast Time (s)':<16} | {'Net Base (s)':<14} | {'Net Amb (s)':<14} | {'Net Ratio':<12} | {'Integral S_max (%)':<20} | {'Linear S_max (%)':<20}")
print("-" * 105)

for t_blast in [0.0, 1.5, 2.0, 2.2, 2.5, 3.0]:
    tb_net = t_base_raw - t_blast
    ta_net = t_amb_raw - t_blast
    r_net = tb_net / ta_net
    s_int = (r_net - 1.0) / mean_hp_integral * 100.0
    s_lin = (r_net - 1.0) / mean_hp_linear * 100.0
    print(f"{t_blast:<16.1f} | {tb_net:<14.2f} | {ta_net:<14.2f} | {r_net:<12.5f} | {s_int:<19.2f}% | {s_lin:<19.2f}%")

print("\n" + "=" * 90)
print(" 💡 INSIGHT ON 1 SPEED BLAST:")
print(" Because both runs collected the same 1 Speed Blast (2.0s duration),")
print(" subtracting 2.0s of identical blast time gives a net normal running ratio of 88.10s / 80.90s = 1.0890.")
print(f" With the game's actual HP decay integral, S_max = (1.0890 - 1) / 0.5802 = 15.34%!")
print("=" * 90)
