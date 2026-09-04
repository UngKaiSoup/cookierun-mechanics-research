# Ghidra Decompiled Code Breakdown: Function `FUN_0032e2b6` (English)
### Cookie Run Native Engine (`libgame.so` - ARM32 Thumb)

> **Language Switcher:** **[🇬🇧 English (Current)](ghidra_decompiled_code_breakdown_en.md)** | **[🇹🇭 ฉบับภาษาไทย (Thai Version)](ghidra_decompiled_code_breakdown_th.md)**
>
> **Binary Source:** `GHIDRA_READY_SO/libgame_kakao_6.13_UNPACKED_ARM32.so`
> **Function Address:** `0x0032E2B6`
> **Primary Stat ID:** `0x48e` (Decimal: **`1166`** - `EMagicStatType_WorldSpeedPropotionToCharacterHealth`)

---

## 📌 Executive Summary
This function handles **Character Spawning and Speed Stat Dispatching (`MainGame_SecondCookieCreated`)**. It performs four critical operations:
1. **Queries Stat `0x48e` (`1166` - Toy Ambulance):** Loops through equipped player items to find stat ID 1166.
2. **Applies the `0.001` Scale Factor:** Multiplies raw table values (e.g. `1150`) by `0.001` to convert them into floating-point multipliers (`1.150` or `+15.0%`).
3. **Establishes the Base Speed Baseline `1.0`:** Defaults to `0x3f800000` (float `1.0` / 100% normal speed) if no buffs are active.
4. **Binds Health Parameters (`CookieMaxHp` & `CookieCurHp`):** Binds the maximum and current health of the cookie to evaluate relative health ratios in real-time.

---

## 📝 Line-by-Line Code Breakdown

### Part 1: Variable Declarations & Stack Frame Allocation

```c
void FUN_0032e2b6(void)
{
  undefined4 uVar1;        // Return value or temporary 32-bit float (ARM register r0)
  int *piVar2;             // Pointer to the Speed Listener Vtable
  void *pvVar3;            // Pointer to the active Character Controller Instance
  undefined4 uVar4;        // Temporary argument / handle
  int iVar5;               // Condition check / count flag
  int unaff_r4;            // Register r4: points to the Player Stat Container
  undefined4 *puVar6;      // Iterator pointer for Stat 1166 values
  int iVar7;               // Sub-object ID / pointer
  int *unaff_r8;           // Register r8: points to the Master Player Controller
  int unaff_r10;           // Register r10: points to Game Context
  undefined8 uVar8;        // 64-bit double precision float for mathematical operations
  ...
```
* **Explanation:** Allocates local stack frame variables and preserves ARM32 registers used by GCC/Clang ABI floating-point helper routines (`__aeabi_*`).

---

### Part 2: Querying and Applying Stat `0x48e` (1166 - Toy Ambulance)

```c
  FUN_00377800(unaff_r4 + 0x3c, 0x48e, &stack0x00000058);
```
* **Explanation:** Calls the stat lookup method on the player's active equip container (`unaff_r4 + 0x3c`) for stat ID **`0x48e`**.
* **Hex Decoding:** `0x48e` in decimal is $(4 \times 256) + (8 \times 16) + 14 = \mathbf{1166}$, which maps directly to `EMagicStatType_WorldSpeedPropotionToCharacterHealth`.
* Returns an iterator range: start pointer (`in_stack_00000058`) and end pointer (`in_stack_0000005c`).

```c
  puVar6 = in_stack_00000058;
  while (in_stack_0000005c != puVar6) {
```
* **Explanation:** Begins a `while` loop that iterates through every equipped instance of stat 1166 (supporting multiple treasures or combi buffs).

```c
    in_stack_00000068 = __aeabi_i2f(*puVar6);
    puVar6 = puVar6 + 1;
```
* **Explanation:** Dereferences the raw integer value (e.g. `1150`), converts it from Integer to 32-bit Float (`__aeabi_i2f`), and advances the iterator pointer.

```c
    if (DAT_00b7576c == (void *)0x0) {
      pvVar3 = operator.new(0x1ec);
      FUN_004f0f3c();
      DAT_00b7576c = pvVar3;
    }
    pvVar3 = DAT_00b7576c;
```
* **Explanation:** Checks if the character controller instance (`DAT_00b7576c`) is instantiated. If `null`, it allocates `0x1ec` bytes (492 bytes struct) via `operator.new` and invokes the constructor.

```c
    uVar1 = __aeabi_f2iz(in_stack_00000068);
    FUN_003777e4((int)pvVar3 + 0x3c, 0x48e, uVar1);
```
* **Explanation:** Truncates float to integer (`__aeabi_f2iz`) and registers stat `0x48e` (1166) into the character's active stat container (`pvVar3 + 0x3c`).

```c
    in_stack_00000064 = __aeabi_i2f();
    in_stack_0000006c = 0x312171;
    iVar7 = unaff_r8[0xc4];
    piVar2 = (int *)FUN_002ccf94(iVar7, &stack0x00000064);
    iVar5 = 0;
    if (piVar2 != (int *)0x0) {
      iVar5 = (int)piVar2 + *(int *)(*piVar2 + -0xc);
    }
    FUN_002ccd10(iVar7, iVar5);
    (**(code **)(*(int *)((int)piVar2 + *(int *)(*piVar2 + -0xc)) + 0x44))();
  }
```
* **Explanation:** Dispatches a virtual method call (`vtable + 0x44`) to notify the world scroll and physics listener that an active health-proportional speed modifier has been attached.

---

### Part 3: Scale Factor Conversion (`0.001` Multiplier & `1.0` Baseline)

```c
  iVar5 = FUN_00315e90();
  if (iVar5 < 1) {
    uVar1 = 0x3f800000;
  }
```
* **Explanation:** Evaluates if a speed modifier is active. If `< 1` (no bonus), it defaults to `0x3f800000`.
* **Hex Decoding:** In IEEE-754 Single-Precision Float, `0x3f800000` is **`1.0`** (100% normal base speed).

```c
  else {
    FUN_00315e90();
    __aeabi_i2f();
    uVar8 = __aeabi_f2d();
    __aeabi_dmul((int)uVar8, (int)((ulonglong)uVar8 >> 0x20), 0xd2f1a9fc, 0x3f50624d);
    uVar1 = __aeabi_d2f();
  }
  FUN_002e124c(unaff_r8 + 0x2e, uVar1);
```
* **Explanation:** If a speed buff is present:
  1. Converts the integer stat to single float (`__aeabi_i2f`).
  2. Promotes to 64-bit double float (`__aeabi_f2d`).
  3. Multiplies via `__aeabi_dmul` by the double constant `(0x3f50624d, 0xd2f1a9fc)`.
  4. **Constant Decoding:** In IEEE-754 Double Precision, `0x3f50624d:d2f1a9fc` equals **`0.001`**.
     * Example: An integer table value of `1150` yields $1150 \times 0.001 = \mathbf{1.150}$ (or $+15.0\%$).
  5. Converts double back to single float (`__aeabi_d2f`) and stores it into the player speed modifier at offset `unaff_r8 + 0x2e`.

---

### Part 4: Processing Secondary Speed Stats (`0x410` & `0x424`)

```c
  iVar5 = FUN_003777e4((int)DAT_00b7576c + 0x3c, 0x410, 0);
  ...
  __aeabi_dmul(..., 0xd2f1a9fc, 0x3f50624d);
  FUN_002e124c(unaff_r8 + 0x32, uVar1);
```
* **Explanation:** Queries Stat ID **`0x410`** (Decimal: **`1040`** - `EMagicStatType_BasicWorldSpeedRate`). Multiplies by `0.001` and writes the resulting float multiplier to offset `+0x32`.

```c
  iVar5 = FUN_003777e4((int)DAT_00b7576c + 0x3c, 0x424, 0);
  ...
  __aeabi_dmul(..., 0xd2f1a9fc, 0x3f50624d);
  FUN_002e124c(unaff_r8 + 0x36, uVar1);
```
* **Explanation:** Queries Stat ID **`0x424`** (Decimal: **`1060`** - secondary speed stat). Multiplies by `0.001` and writes the resulting multiplier to offset `+0x36`.

---

### Part 5: Binding Health Tracking Properties (`CookieMaxHp` & `CookieCurHp`)

```c
  uVar1 = FUN_005da718();
  uVar4 = FUN_005db844(unaff_r10 + 0xc);
  thunk_FUN_008f5b98(&stack0x00000034, "CookieName", &stack0x00000004);
  FUN_005da244(uVar1, uVar4, &stack0x00000034);
```
* **Explanation:** Attaches the character's identifier string (`CookieName`).

```c
  uVar4 = FUN_004e7b84(DAT_00b7576c);
  uVar4 = FUN_005db8d4(&DAT_009de314, uVar4);
  thunk_FUN_008f5b98(&stack0x00000038, "CookieMaxHp", &stack0x00000008);
  FUN_005da244(uVar1, uVar4, &stack0x00000038);
```
* **Explanation:** Retrieves maximum health via `FUN_004e7b84(DAT_00b7576c)` and binds it to the parameter name **`CookieMaxHp`**.

```c
  uVar4 = FUN_004e7b18(DAT_00b7576c);
  uVar4 = FUN_005db8d4(&DAT_009de314, uVar4);
  thunk_FUN_008f5b98(&stack0x0000003c, "CookieCurHp", &stack0x0000000c);
  FUN_005da244(uVar1, uVar4, &stack0x0000003c);
```
* **Explanation:** Retrieves current remaining health via `FUN_004e7b18(DAT_00b7576c)` and binds it to the parameter name **`CookieCurHp`**.

```c
  thunk_FUN_008f5b98(&stack0x00000040, "PatternCreationCount", ...);
  thunk_FUN_008f5b98(&stack0x00000044, "PatternId", ...);
  thunk_FUN_008f5b98(&stack0x00000048, "PlayTime", ...);
```
* **Explanation:** Binds active obstacle generation counts (`PatternCreationCount`), stage pattern ID (`PatternId`), and elapsed run time (`PlayTime`).

```c
  FUN_004e5a30(DAT_00b7576c, "MainGame_SecondCookieCreated", uVar1, 0);
```
* **Explanation:** Triggers the event handler **`MainGame_SecondCookieCreated`** (e.g. when spawning the relay cookie or initializing gameplay), passing all calculated speed multipliers and health bindings to the active runner.

---

## 🎯 Symbol & Constant Cross-Reference Table

| Ghidra Identifier | Data Type | Decimal Value | Meaning in Cookie Run Engine |
| :--- | :---: | :---: | :--- |
| **`0x48e`** | Hex Int | **`1166`** | Stat ID: `EMagicStatType_WorldSpeedPropotionToCharacterHealth` (Toy Ambulance) |
| **`0x410`** | Hex Int | **`1040`** | Stat ID: `EMagicStatType_BasicWorldSpeedRate` (Base Speed Modifier) |
| **`0x424`** | Hex Int | **`1060`** | Stat ID: Secondary Speed Modifier |
| **`0x3f800000`** | Float 32 | **`1.0`** | Normal baseline speed (1.0x / 100%) |
| **`0xd2f1a9fc, 0x3f50624d`** | Double 64 | **`0.001`** | Scale factor: converts raw integer `1150` to `1.150` (+15.0%) |
| **`"CookieMaxHp"`** | String | Max HP | Maximum health capacity of the cookie |
| **`"CookieCurHp"`** | String | Current HP | Real-time health remaining on the cookie |
| **`"MainGame_SecondCookieCreated"`**| String | Event Name | Spawning event that applies stats to the active cookie |
