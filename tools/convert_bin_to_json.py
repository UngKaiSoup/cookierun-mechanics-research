import struct, json, glob, os, sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

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

target_dir = "kakao_827_extracted"
bin_files = glob.glob(os.path.join(target_dir, "*.bin"))
print(f"[*] Converting {len(bin_files)} .bin tables in {target_dir} to readable .json ...")

converted = 0
for bf in bin_files:
    jf = bf.replace(".bin", ".json")
    try:
        data = bin_to_json(bf)
        with open(jf, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        converted += 1
    except Exception as e:
        print(f"[-] Error converting {bf}: {e}")

print(f"✅ Successfully converted {converted} / {len(bin_files)} tables into JSON!")
