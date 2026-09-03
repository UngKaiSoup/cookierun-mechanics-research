import json, sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

with open("all_speed_treasures_kakao827.json", "r", encoding="utf-8") as f:
    data_dict = json.load(f)

# Group by MagicStat Type and Base Name
grouped = {}
for pkey, r in data_dict.items():
    name = r.get('Name_KO', 'Unknown')
    base_name = name.split('+')[0].strip()
    stat1 = str(r.get('MagicStat_Type_Id_1', ''))
    stat2 = str(r.get('MagicStat_Type_Id_2', ''))
    
    stype = stat1 if stat1 in ['1039', '1166', '1035', '1204', '1080'] else stat2
    if not stype: stype = stat1 or stat2
    
    if stype not in grouped:
        grouped[stype] = {}
    if base_name not in grouped[stype]:
        grouped[stype][base_name] = []
    r['PKEY'] = pkey
    grouped[stype][base_name].append(r)

stat_titles = {
    '1039': '🏃‍♂️ 1. BASE SPEED (ความเร็วพื้นฐานปกติ / EMagicStatType_BasicWorldSpeedRate)',
    '1166': '🚑 2. HP-PROPORTIONAL SPEED (ความเร็วตามสัดส่วนเลือด / Toy Ambulance)',
    '1035': '⚡ 3. BLAST / FAST RUN SPEED (ความเร็วตอนวิ่งแสง / EMagicStatType_FastRunSpeedRate)',
    '1204': '🍄 4. GIANT SPEED (ความเร็วตอนตัวใหญ่ / EMagicStatType_BasicWorldSpeedRateWhenGiant)',
    '1080': '🌌 5. BONUS TIME SPEED (ความเร็วในโบนัสไทม์ / EMagicStatType_BonusTimeSpeedRate)'
}

for stype, items in grouped.items():
    title = stat_titles.get(stype, f"🌟 TYPE {stype}")
    print("\n" + "=" * 100)
    print(f" {title}")
    print("=" * 100)
    for bname, rows in items.items():
        rows.sort(key=lambda x: int(x['PKEY']))
        first = rows[0]
        last = rows[-1]
        
        v0 = first.get('Value_1_Raw') if str(first.get('MagicStat_Type_Id_1')) == stype else first.get('Value_2_Raw')
        v9 = last.get('Value_1_Raw') if str(last.get('MagicStat_Type_Id_1')) == stype else last.get('Value_2_Raw')
        
        p0 = (int(v0) - 1000) / 10.0 if v0 and int(v0) > 1000 else 0
        p9 = (int(v9) - 1000) / 10.0 if v9 and int(v9) > 1000 else 0
        print(f"  • {bname:45s} | ระดับ +0: +{p0:4.1f}%  ➔  ระดับ +9: +{p9:4.1f}%")
