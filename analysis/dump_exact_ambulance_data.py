import struct, sys, json

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

def parse_devsisters_binary_table(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    if len(data) < 4: return []
    num_rows = struct.unpack('<I', data[:4])[0]
    offset = 4
    rows = []
    for r in range(num_rows):
        if offset >= len(data): break
        pkey = None
        if r > 0:
            pkl = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            pkey = data[offset:offset+pkl].decode('utf-8', errors='ignore')
            offset += pkl
        
        if offset + 4 > len(data): break
        col_count = struct.unpack('<I', data[offset:offset+4])[0]
        offset += 4
        
        row = {}
        if pkey:
            row['__pkey'] = pkey
            
        for c in range(col_count):
            if offset + 4 > len(data): break
            kl = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            k = data[offset:offset+kl].decode('utf-8', errors='ignore')
            offset += kl
            
            if offset + 4 > len(data): break
            vl = struct.unpack('<I', data[offset:offset+4])[0]
            offset += 4
            v = data[offset:offset+vl].decode('utf-8', errors='ignore')
            offset += vl
            row[k] = v
        rows.append(row)
    return rows

print("=" * 80)
print(" PARSING EXACT RAW DATA DIRECTLY FROM COOKIE RUN KAKAO 6.13")
print("=" * 80)

stuff_names = parse_devsisters_binary_table("kakao_613_djb/StuffName_ko.bin")
treasure_items = parse_devsisters_binary_table("kakao_613_djb/TreasureItemData.bin")
treasure_passives = parse_devsisters_binary_table("kakao_613_djb/TreasurePassiveAttr.bin")

print(f"[+] Loaded StuffName_ko: {len(stuff_names)} rows")
print(f"[+] Loaded TreasureItemData: {len(treasure_items)} rows")
print(f"[+] Loaded TreasurePassiveAttr: {len(treasure_passives)} rows")

# 1. Search StuffName_ko for Ambulance
print("\n" + "=" * 80)
print(" 1. MATCHES IN StuffName_ko.bin (Item Descriptions & Names)")
print("=" * 80)
ambulance_stuff = []
for s in stuff_names:
    desc = str(s)
    if '구급차' in desc:
        ambulance_stuff.append(s)
        print(json.dumps(s, ensure_ascii=False, indent=2))

# 2. Search TreasureItemData for Ambulance
print("\n" + "=" * 80)
print(" 2. MATCHES IN TreasureItemData.bin (Treasure Configurations)")
print("=" * 80)
ambulance_items = []
for t in treasure_items:
    desc = str(t)
    if '구급차' in desc:
        ambulance_items.append(t)
        print(json.dumps(t, ensure_ascii=False, indent=2))

# 3. Match Passive Attributes
print("\n" + "=" * 80)
print(" 3. MATCHES IN TreasurePassiveAttr.bin (Exact Stats, Rates, Proportions)")
print("=" * 80)
group_seqs = set(t.get('group_seq') for t in ambulance_items if t.get('group_seq'))
for pkey in [s.get('__pkey') for s in ambulance_stuff if s.get('__pkey')]:
    group_seqs.add(pkey)

print(f"Target Group Seqs: {group_seqs}")
for gseq in group_seqs:
    print(f"\n--- Passive Stats for GroupSeq: {gseq} ---")
    matches = [p for p in treasure_passives if p.get('group_seq') == str(gseq)]
    for m in matches:
        print(json.dumps(m, ensure_ascii=False))

with open("ambulance_game_extracted.json", "w", encoding="utf-8") as f:
    json.dump({
        "StuffName": ambulance_stuff,
        "TreasureItemData": ambulance_items,
        "Passives": [p for p in treasure_passives if p.get('group_seq') in group_seqs]
    }, f, indent=2, ensure_ascii=False)

print("\n[+] Done! Full extracted data saved to ambulance_game_extracted.json")
