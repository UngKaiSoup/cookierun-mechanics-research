import re, sys, os

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

libgame_path = "config.arm64_v8a/lib/arm64-v8a/libgame.so"
with open(libgame_path, "rb") as f:
    data = f.read()

print("=" * 80)
print(" 🔬 EXTRACTING HP DRAIN CONSTANTS & TICK MECHANICS")
print("=" * 80)

patterns = [
    b"HpDrain",
    b"HealthDecrease",
    b"HpDecrease",
    b"DrainRate",
    b"BaseHpDrain",
    b"StageDrain",
    b"HealthRatio"
]

for p in patterns:
    matches = [m.start() for m in re.finditer(re.escape(p), data, re.IGNORECASE)]
    print(f"\n[+] Pattern '{p.decode()}': Found {len(matches)} occurrences")
    for m in matches[:6]:
        start = max(0, m - 30)
        end = min(len(data), m + 60)
        snippet = data[start:end]
        readable = re.findall(r'[\x20-\x7E]{3,}', snippet.decode('utf-8', errors='ignore'))
        print(f"  • 0x{m:X}: {readable}")
