import zipfile, os, sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

apk_path = "CookieRun_Kakao_6.13.apk"
out_dir = "step1_extracted_data"
os.makedirs(out_dir, exist_ok=True)

print("=" * 80)
print(f" 🚀 STEP 1: กำลังแตกไฟล์จาก APK [{apk_path}]")
print("=" * 80)

if not os.path.exists(apk_path):
    print(f"[!] ไม่พบไฟล์ APK: {apk_path}")
    sys.exit(1)

extracted_djb = []
extracted_so = []

with zipfile.ZipFile(apk_path, "r") as z:
    all_files = z.namelist()
    print(f"📦 จำนวนไฟล์ทั้งหมดใน APK: {len(all_files):,} ไฟล์\n")

    for f in all_files:
        # 1. แตกไฟล์ .djb ใน BalanceData
        if f.endswith(".djb"):
            filename = os.path.basename(f)
            dest_path = os.path.join(out_dir, filename)
            with open(dest_path, "wb") as out:
                out.write(z.read(f))
            extracted_djb.append((filename, z.getinfo(f).file_size))

        # 2. แตกไฟล์ Engine libgame.so
        elif "libgame.so" in f:
            filename = os.path.basename(f)
            dest_path = os.path.join(out_dir, filename)
            with open(dest_path, "wb") as out:
                out.write(z.read(f))
            extracted_so.append((filename, z.getinfo(f).file_size))

print(f"✅ สกัดไฟล์ .djb สำเร็จ: {len(extracted_djb)} ไฟล์")
print(f"✅ สกัดไฟล์ .so สำเร็จ: {len(extracted_so)} ไฟล์")
print(f"📁 บันทึกไว้ที่โฟลเดอร์: {os.path.abspath(out_dir)}\n")

print("--- 📋 ตัวอย่างไฟล์ .djb สำคัญที่สกัดได้ ---")
important_files = [
    "EquipmentDataCookieRun.djb",
    "StuffName_ko.djb",
    "TreasureItemData.djb",
    "TreasurePassiveAttr.djb",
    "MysteryBox.djb",
    "Gashapone_Step1_Rate.djb",
    "Gashapone_Step2_Rate.djb"
]
for fname in important_files:
    size = os.path.getsize(os.path.join(out_dir, fname)) if os.path.exists(os.path.join(out_dir, fname)) else 0
    print(f"  • {fname:30s} ขนาด: {size:>10,} ไบต์")

for fname, sz in extracted_so:
    print(f"  • {fname:30s} ขนาด: {sz:>10,} ไบต์ (Game Engine Native Binary)")

print("\n" + "=" * 80)
print(" 🎉 STEP 1 เสร็จสมบูรณ์ พร้อมไปต่อ STEP 2 (ถอดรหัส DJBF)")
print("=" * 80)
