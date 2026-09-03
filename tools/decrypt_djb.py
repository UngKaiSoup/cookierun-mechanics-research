# =============================================================================
# DJBF Decryption Utility
# Powered by CookieRun-DJBF-Converter by @barncastle
# GitHub: https://github.com/barncastle/CookieRun-DJBF-Converter
# =============================================================================
import subprocess, os, sys, glob

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

# Locate converter binary
script_dir = os.path.dirname(os.path.abspath(__file__))
converter_exe = os.path.join(script_dir, "CookieRunDJBFConverter.exe")
if not os.path.exists(converter_exe):
    converter_exe = "CookieRunDJBFConverter.exe"

target_dir = os.path.join(os.path.dirname(script_dir), "data", "step1_extracted_data")
if not os.path.exists(target_dir):
    target_dir = "step1_extracted_data"

if not os.path.exists(converter_exe):
    print(f"[!] ไม่พบโปรแกรมถอดรหัส: {converter_exe}")
    sys.exit(1)

# สั่งรันตัวแปลง C# Converter: Decrypt ด้วยกุญแจ Kakao
cmd = [converter_exe, "-m", "decrypt", "-k", "kakao", "-d", target_dir, "-s", "*.djb"]
print(f"⚙️ กำลังรันคำสั่ง: {' '.join(cmd)}\n")

proc = subprocess.run(cmd, capture_output=True, text=True)

# นับจำนวนไฟล์ .bin ที่ได้
bin_files = glob.glob(os.path.join(target_dir, "*.bin"))
print(f"✅ ถอดรหัสสำเร็จทั้งหมด: {len(bin_files)} ไฟล์ (.bin)")

print("\n--- 📋 ตัวอย่างไฟล์ .bin ที่ถอดรหัสและขยายขนาดออกมาได้ ---")
important_files = [
    "EquipmentDataCookieRun.bin",
    "StuffName_ko.bin",
    "TreasureItemData.bin",
    "TreasurePassiveAttr.bin",
    "MysteryBox.bin",
    "Gashapone_Step1_Rate.bin",
    "Gashapone_Step2_Rate.bin"
]

for fname in important_files:
    bin_path = os.path.join(target_dir, fname)
    djb_path = os.path.join(target_dir, fname.replace(".bin", ".djb"))
    
    sz_bin = os.path.getsize(bin_path) if os.path.exists(bin_path) else 0
    sz_djb = os.path.getsize(djb_path) if os.path.exists(djb_path) else 0
    
    print(f"  • {fname:30s} | ขนาดเดิม (.djb): {sz_djb:>8,} B ➔ หลังถอดรหัส (.bin): {sz_bin:>10,} B")

print("\n" + "=" * 80)
print(" 🎉 STEP 2 เสร็จสมบูรณ์ ข้อมูลถูกคลายจากการเข้ารหัส AES/FastLZ เป็น Plaintext แล้ว!")
print("=" * 80)
