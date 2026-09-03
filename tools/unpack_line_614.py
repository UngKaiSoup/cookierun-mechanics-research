import zipfile, os, sys, shutil, subprocess, struct, json, glob

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

apk_path = r"C:\Users\Passakorn\Downloads\LINE+Cookie+Run_6.1.4_APKPure.apk"
base_out = r"C:\Users\Passakorn\Downloads\CookieRun+Classic_26.8.02_APKPure\LINE_6.1.4_EXTRACTED"

dir_ghidra = os.path.join(base_out, "01_FOR_GHIDRA_SO")
dir_json = os.path.join(base_out, "02_JSON_DATA")
dir_raw = os.path.join(base_out, "03_RAW_BIN_AND_DJB")

os.makedirs(dir_ghidra, exist_ok=True)
os.makedirs(dir_json, exist_ok=True)
os.makedirs(dir_raw, exist_ok=True)

print("=" * 85)
print(" 🚀 UNPACKING & ORGANIZING: LINE Cookie Run v6.1.4")
print("=" * 85)

# Step 1: Extract libgame.so and .djb files from APK
print("\n[*] 1. Extracting APK files...")
with zipfile.ZipFile(apk_path, "r") as z:
    # 1.1 Extract libgame.so for Ghidra
    libgame_armeabi_v7a = "lib/armeabi-v7a/libgame.so"
    target_so = os.path.join(dir_ghidra, "libgame_line_6.1.4_armeabi_v7a.so")
    if libgame_armeabi_v7a in z.namelist():
        with open(target_so, "wb") as f:
            f.write(z.read(libgame_armeabi_v7a))
        print(f"  [+] Saved Ghidra SO file: {os.path.basename(target_so)} ({os.path.getsize(target_so):,} bytes)")
    
    # Also save standard name libgame.so in that folder for convenience
    std_so = os.path.join(dir_ghidra, "libgame.so")
    shutil.copy2(target_so, std_so)

    # 1.2 Extract all .djb balance files to 03_RAW_BIN_AND_DJB
    djb_names = [n for n in z.namelist() if n.startswith("assets/lineBC_BalanceData/") and n.endswith(".djb")]
    print(f"  [+] Extracting {len(djb_names)} .djb files to RAW folder...")
    for name in djb_names:
        fname = os.path.basename(name)
        out_path = os.path.join(dir_raw, fname)
        with open(out_path, "wb") as f:
            f.write(z.read(name))

# Step 2: Decrypt .djb files using CookieRunDJBFConverter.exe
print("\n[*] 2. Decrypting .djb files to .bin...")
converter_exe = "CookieRunDJBFConverter.exe"
cmd = [converter_exe, "-m", "decrypt", "-k", "kakao", "-d", dir_raw, "-s", "*.djb"]
proc = subprocess.run(cmd, capture_output=True, text=True)

bin_files = glob.glob(os.path.join(dir_raw, "*.bin"))
print(f"  [+] Successfully decrypted {len(bin_files)} .bin files!")

# Step 3: Convert .bin to readable .json into 02_JSON_DATA
def bin_to_json(bin_filepath):
    with open(bin_filepath, "rb") as f:
        data = f.read()
    if len(data) < 4: return []
    num_rows = struct.unpack("<I", data[:4])[0]
    offset = 4
    rows = []
    for r in range(num_rows):
        if offset >= len(data): break
        pkey = None
        if r > 0:
            pkl = struct.unpack("<I", data[offset:offset+4])[0]; offset += 4
            pkey = data[offset:offset+pkl].decode("utf-8", errors="ignore"); offset += pkl
        col_count = struct.unpack("<I", data[offset:offset+4])[0]; offset += 4
        row = {"__pkey": pkey} if pkey else {}
        for c in range(col_count):
            kl = struct.unpack("<I", data[offset:offset+4])[0]; offset += 4
            k = data[offset:offset+kl].decode("utf-8", errors="ignore"); offset += kl
            vl = struct.unpack("<I", data[offset:offset+4])[0]; offset += 4
            v = data[offset:offset+vl].decode("utf-8", errors="ignore"); offset += vl
            row[k] = v
        rows.append(row)
    return rows

print("\n[*] 3. Converting .bin tables to .json in 02_JSON_DATA...")
converted_count = 0
for bf in bin_files:
    fname = os.path.basename(bf).replace(".bin", ".json")
    out_json = os.path.join(dir_json, fname)
    try:
        data = bin_to_json(bf)
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        converted_count += 1
    except Exception as e:
        print(f"  [-] Error on {fname}: {e}")

print(f"  [+] Successfully generated {converted_count} JSON tables!")

# Step 4: Write a quick instruction guide right inside 01_FOR_GHIDRA_SO
readme_content = """=== HOW TO ANALYZE IN GHIDRA (LINE Cookie Run v6.1.4) ===

1. Open Ghidra and create a new project.
2. Drag and drop the file:
   -> libgame.so (or libgame_line_6.1.4_armeabi_v7a.so)
   
3. Recommended Ghidra Import Settings:
   - Format: ELF
   - Language: ARM:LE:32:v7 (little endian)
   
4. Press Analyze (wait 2-3 minutes).

5. Useful strings to Search (Search -> For Strings...):
   - EMagicStatType_WorldSpeedPropotionToCharacterHealth (Toy Ambulance speed logic)
   - Cookie_HpDecrease (HP drain tick function)
   - Character_EnergyDiminishValueNew (HP drain base value)
   - CRXWorldSpeed (World scroll speed manager)
"""

with open(os.path.join(dir_ghidra, "README_GHIDRA_GUIDE.txt"), "w", encoding="utf-8") as f:
    f.write(readme_content)

print("\n" + "=" * 85)
print(" 🎉 ALL DONE! FOLDERS ARE BEAUTIFULLY ORGANIZED:")
print("=" * 85)
print(f"📁 Root: {base_out}")
print(f"  ├── 📁 01_FOR_GHIDRA_SO/   --> ลากไฟล์ libgame.so จากโฟลเดอร์นี้เข้า Ghidra ได้ทันที!")
print(f"  ├── 📁 02_JSON_DATA/       --> รวมไฟล์ตารางเกมทั้งหมด {converted_count} ไฟล์ (.json) สำหรับค้นหา")
print(f"  └── 📁 03_RAW_BIN_AND_DJB/ --> รวมไฟล์ดิบ .djb และ .bin เก็บแยกไว้ไม่ให้รก")
