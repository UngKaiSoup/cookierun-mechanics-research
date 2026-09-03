import capstone, sys, os, struct, re

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

libgame_path = "config.arm64_v8a/lib/arm64-v8a/libgame.so"
if not os.path.exists(libgame_path):
    for root, dirs, files in os.walk("."):
        if "libgame.so" in files and "arm64-v8a" in root:
            libgame_path = os.path.join(root, "libgame.so")
            break

with open(libgame_path, "rb") as f:
    data = f.read()

print(f"[*] Disassembling ARM64 CRXWorldSpeedRelatedToPercentageBuff in: {libgame_path}")

# Find symbol string
pos = data.find(b"CRXWorldSpeedRelatedToPercentageBuff")
print(f"Symbol found at: 0x{pos:X}")

# Let's search ARM32 binary if available
arm32_path = None
for root, dirs, files in os.walk("."):
    if "libgame.so" in files and "armeabi-v7a" in root:
        arm32_path = os.path.join(root, "libgame.so")
        break

if arm32_path:
    print(f"\n[*] Found ARM32 binary: {arm32_path}")
    with open(arm32_path, "rb") as f:
        data32 = f.read()
    
    # Search for functions in ARM32
    # In ARM32: _ZN10DSXLibrary36CRXWorldSpeedRelatedToPercentageBuff...
    matches = [m.start() for m in re.finditer(rb"CRXWorldSpeedRelatedToPercentageBuff", data32)]
    print(f"Found {len(matches)} occurrences in ARM32")
    
    # Disassemble functions around 0x2BDB00 - 0x2BDD00
    md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_ARM)
    for addr in range(0x2BDB00, 0x2BDD00, 4):
        code = data32[addr:addr+16]
        for insn in md.disasm(code, addr):
            print(f"  0x{insn.address:X}:  {insn.mnemonic:8s} {insn.op_str}")
