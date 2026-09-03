import json, sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

with open("all_speed_treasures_kakao827.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

categories = {
    "1039": ("🏃‍♂️ กลุ่ม 1: เพิ่มความเร็วพื้นฐานตลอดเวลา (Base World Speed Multiplier)", []),
    "1166": ("🚑 กลุ่ม 2: เพิ่มความเร็วแปรผันตามสัดส่วนเลือด (HP-Proportional Speed)", []),
    "1035": ("⚡ กลุ่ม 3: เพิ่มความเร็วขณะเก็บไอเทมความเร็วแสง / Blast Speed", []),
    "1204": ("🍄 กลุ่ม 4: เพิ่มความเร็วขณะตัวยักษ์ (Giant Speed)", []),
    "1080": ("🌈 กลุ่ม 5: เพิ่มความเร็วในแดนโบนัสไทม์ (Bonus Time Speed)", [])
}

for grp, info in catalog.items():
    items = info['all_items']
    # Check which speed ID
    first_e = items[0]
    last_e = items[-1]
    s_ids = [sid for sid, sval in first_e['matched_speed']]
    
    for sid in s_ids:
        if sid in categories:
            categories[sid][1].append({
                'group': grp,
                'name': info['name'],
                'min_b': f"{first_e['b1']} {first_e['b2']}".strip(),
                'max_b': f"{last_e['b1']} {last_e['b2']}".strip(),
                'min_stat': f"{first_e['id1']}={first_e['v1']} {first_e['id2']}={first_e['v2']}".strip(),
                'max_stat': f"{last_e['id1']}={last_e['v1']} {last_e['id2']}={last_e['v2']}".strip()
            })

for sid, (cat_title, item_list) in categories.items():
    print(f"\n================================================================================")
    print(f" {cat_title} (พบทั้งหมด {len(item_list)} ชิ้น/กลุ่ม)")
    print(f"================================================================================")
    # Remove duplicate names in same category
    seen = set()
    for it in item_list:
        if it['name'] not in seen and it['name']:
            seen.add(it['name'])
            print(f"  • {it['name']:36s} | [+0]: {it['min_b']} | [+9]: {it['max_b']}")
