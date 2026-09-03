# คำแปลและวิเคราะห์โค้ด Ghidra: ฟังก์ชัน `FUN_0032e2b6` (ภาษาไทย)
### โค้ดภายใน Engine เกม Cookie Run (`libgame.so` - สถาปัตยกรรม ARM32 Thumb)

> **เลือกภาษา (Language):** **[🇹🇭 ฉบับภาษาไทย (กำลังอ่าน)](ghidra_decompiled_code_breakdown_th.md)** | **[🇬🇧 English Version](ghidra_decompiled_code_breakdown_en.md)**
>
> **ไฟล์อ้างอิง:** `GHIDRA_READY_SO/libgame_kakao_6.13_UNPACKED_ARM32.so`
> **ตำแหน่งฟังก์ชัน (Address):** `0x0032E2B6`
> **รหัสสแตทสำคัญในฟังก์ชัน:** `0x48e` (เลขฐานสิบ: **`1166`** - `EMagicStatType_WorldSpeedPropotionToCharacterHealth`)

---

## 📌 สรุปใจความสำคัญของฟังก์ชันนี้ (Executive Summary)
ฟังก์ชันนี้ทำหน้าที่เป็น **ตัวจัดการการเกิดของตัวละครและการกระจายค่าสปีด (`MainGame_SecondCookieCreated`)** โดยทำงานหลัก 4 ส่วน:
1. **ดึงค่าสแตท `0x48e` (`1166` = รถพยาบาล):** วนลูปอ่านค่าสแตทจากสมบัติที่ผู้เล่นติดตั้งไว้
2. **แปลงสเกลตัวเลขด้วยตัวคูณ `0.001`:** นำค่าดิบจากตารางเกม (เช่น `1150`) มาคูณ `0.001` เพื่อแปลงเป็นตัวคูณทศนิยม (`1.150` หรือ `+15.0%`)
3. **ตั้งค่าสปีดเริ่มต้น `1.0` (Base Speed 100%):** หากไม่มีบัฟสปีดทำงาน จะกำหนดค่าเป็น `0x3f800000` (ทศนิยม 1.0)
4. **ผูกตัวแปรเลือด `CookieMaxHp` และ `CookieCurHp`:** ดึงค่าเลือดเต็มและเลือดปัจจุบันของคุกกี้มาผูกเข้ากับระบบความเร็วเพื่อใช้คำนวณสปีดแบบแปรผันตามเลือด

---

## 📝 แปลโค้ดแบบเรียงทีละบรรทัด (Line-by-Line Breakdown)

### ส่วนที่ 1: การจองตัวแปรและ Stack Frame

```c
void FUN_0032e2b6(void)
{
  undefined4 uVar1;        // เก็บค่า Return value หรือตัวแปร Float ชั่วคราว (รีจิสเตอร์ r0)
  int *piVar2;             // ตัวชี้ (Pointer) ไปยัง Vtable ของระบบ Speed Listener
  void *pvVar3;            // Pointer ชี้ไปยัง Object ตัวละครคุกกี้ (Character Instance)
  undefined4 uVar4;        // ตัวแปรส่งค่า Argument ชั่วคราว
  int iVar5;               // ตัวแปรเช็คเงื่อนไข (Flag / Count)
  int unaff_r4;            // รีจิสเตอร์ r4 ชี้ไปยัง Container เก็บสแตทของผู้เล่น
  undefined4 *puVar6;      // Iterator ชี้ตำแหน่งค่าของสแตท 1166
  int iVar7;               // ตัวแปรเก็บ ID หรือ Pointer ย่อย
  int *unaff_r8;           // รีจิสเตอร์ r8 ชี้โครงสร้าง Player Controller หลัก
  int unaff_r10;           // รีจิสเตอร์ r10 ชี้ Game Context
  undefined8 uVar8;        // ตัวแปรทศนิยม 64-bit (Double precision สำหรับคำนวณคูณทศนิยม)
  ...
```
* **คำอธิบาย:** เป็นการจองพื้นที่ใน Stack และรีจิสเตอร์ของ ARM32 สำหรับเรียกใช้ฟังก์ชันคำนวณคณิตศาสตร์ทศนิยม (`__aeabi_*`)

---

### ส่วนที่ 2: ลูปดึงค่าสแตทรถพยาบาล (`0x48e` = 1166)

```c
  FUN_00377800(unaff_r4 + 0x3c, 0x48e, &stack0x00000058);
```
* **คำอธิบาย:** เรียกฟังก์ชันค้นหาสแตทในตัวผู้เล่น (`unaff_r4 + 0x3c`) สำหรับสแตท ID **`0x48e`**
* **ถอดรหัสเลขฐาน 16:** `0x48e` แปลงเป็นเลขฐานสิบคือ:
  $$(4 \times 256) + (8 \times 16) + 14 = \mathbf{1166}$$
  ซึ่งตรงกับสแตท `EMagicStatType_WorldSpeedPropotionToCharacterHealth` (รถพยาบาล) ของแท้แน่นอน
* ค่าที่ส่งกลับมาคือ Pointer เริ่มต้น (`in_stack_00000058`) และ Pointer สิ้นสุด (`in_stack_0000005c`)

```c
  puVar6 = in_stack_00000058;
  while (in_stack_0000005c != puVar6) {
```
* **คำอธิบาย:** เริ่มลูป `while` เพื่อวนอ่านค่าสแตท 1166 ทั้งหมดที่ผู้เล่นติดตั้งไว้ (รองรับกรณีใส่สมบัติหลายชิ้นหรือมีคอมบี้โบนัสซ้อนกัน)

```c
    in_stack_00000068 = __aeabi_i2f(*puVar6);
    puVar6 = puVar6 + 1;
```
* **คำอธิบาย:** ดึงค่าสแตทดิบจากตาราง (เช่น `1150`) แปลงจากเลขจำนวนเต็ม (Integer) เป็นเลขทศนิยม 32-bit Float ด้วยคำสั่ง `__aeabi_i2f` แล้วเลื่อนตัวชี้ไปยังตำแหน่งถัดไป

```c
    if (DAT_00b7576c == (void *)0x0) {
      pvVar3 = operator.new(0x1ec);
      FUN_004f0f3c();
      DAT_00b7576c = pvVar3;
    }
    pvVar3 = DAT_00b7576c;
```
* **คำอธิบาย:** ตรวจสอบว่าออบเจกต์ตัวละครคุกกี้ (`DAT_00b7576c`) ถูกสร้างขึ้นหรือยัง ถ้ายังเป็น `null` ให้จัดสรรหน่วยความจำขนาด `0x1ec` (492 ไบต์) ด้วย `operator.new` แล้วเรียก Constructor สร้างตัวละครขึ้นมา

```c
    uVar1 = __aeabi_f2iz(in_stack_00000068);
    FUN_003777e4((int)pvVar3 + 0x3c, 0x48e, uVar1);
```
* **คำอธิบาย:** แปลงค่า Float กลับเป็น Integer (`__aeabi_f2iz`) แล้วนำสแตท `0x48e` (1166) ไปบันทึกเก็บไว้ใน Container สแตทของตัวคุกกี้ (`pvVar3 + 0x3c`) เพื่อเปิดใช้งานระบบสปีดแปรผันตามเลือด

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
* **คำอธิบาย:** สั่งรันฟังก์ชันเสมือน (Vtable Dispatch Call ผ่าน offset `+0x44`) เพื่อแจ้งระบบคำนวณการเลื่อนฉากและระบบฟิสิกส์ว่ามีสแตทความเร็วตามเลือดติดตั้งอยู่ ให้เริ่มคำนวณสปีดแบบไดนามิก

---

### ส่วนที่ 3: การแปลงสเกลตัวคูณความเร็ว (คูณด้วย `0.001` และฐาน `1.0`)

```c
  iVar5 = FUN_00315e90();
  if (iVar5 < 1) {
    uVar1 = 0x3f800000;
  }
```
* **คำอธิบาย:** ตรวจสอบว่ามีค่าบัฟความเร็วหรือไม่ ถ้าไม่มี (`< 1`) ให้กำหนดค่าความเร็วเป็น `0x3f800000`
* **ถอดรหัสเลขฐาน 16:** ในมาตรฐาน IEEE-754 Single-Precision Float เลข `0x3f800000` คือค่าทศนิยม **`1.0`** (ความเร็วมาตรฐาน 100% ฐานปกติ)

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
* **คำอธิบาย:** หากมีค่าบัฟความเร็ว:
  1. แปลงตัวเลขเป็น Float (`__aeabi_i2f`)
  2. ขยายความแม่นยำเป็น Double 64-bit (`__aeabi_f2d`)
  3. นำไปคูณด้วยฟังก์ชัน `__aeabi_dmul` กับค่าคงที่ Double `(0x3f50624d, 0xd2f1a9fc)`
  4. **ถอดรหัสค่าคงที่:** ค่า `0x3f50624d:d2f1a9fc` คือทศนิยม **`0.001`**
     * ตัวอย่าง: เมื่อนำค่าดิบจากตารางสมบัติ `1150` มาคูณ จะได้:
       $$1150 \times 0.001 = \mathbf{1.150} \quad (\text{หรือความเร็ว } +15.0\%)$$
  5. แปลง Double กลับเป็น Float (`__aeabi_d2f`) แล้วบันทึกลงตัวแปรสปีดของตัวละครที่ offset `unaff_r8 + 0x2e`

---

### ส่วนที่ 4: การประมวลผลสปีดสแตทตัวอื่น (`0x410` และ `0x424`)

```c
  iVar5 = FUN_003777e4((int)DAT_00b7576c + 0x3c, 0x410, 0);
  ...
  __aeabi_dmul(..., 0xd2f1a9fc, 0x3f50624d);
  FUN_002e124c(unaff_r8 + 0x32, uVar1);
```
* **คำอธิบาย:** ตรวจสอบสแตท ID **`0x410`** (เลขฐานสิบคือ **`1040`** = `EMagicStatType_BasicWorldSpeedRate` ความเร็วพื้นฐานปกติ) แล้วคูณด้วย `0.001` เช่นกัน เก็บไว้ที่ offset `+0x32`

```c
  iVar5 = FUN_003777e4((int)DAT_00b7576c + 0x3c, 0x424, 0);
  ...
  __aeabi_dmul(..., 0xd2f1a9fc, 0x3f50624d);
  FUN_002e124c(unaff_r8 + 0x36, uVar1);
```
* **คำอธิบาย:** ตรวจสอบสแตท ID **`0x424`** (เลขฐานสิบคือ **`1060`** = ความเร็วเสริมอีกประเภท) แล้วคูณด้วย `0.001` เก็บไว้ที่ offset `+0x36`

---

### ส่วนที่ 5: การผูกข้อมูลเลือด `CookieMaxHp` และ `CookieCurHp`

```c
  uVar1 = FUN_005da718();
  uVar4 = FUN_005db844(unaff_r10 + 0xc);
  thunk_FUN_008f5b98(&stack0x00000034, "CookieName", &stack0x00000004);
  FUN_005da244(uVar1, uVar4, &stack0x00000034);
```
* **คำอธิบาย:** บันทึกชื่อตัวละครคุกกี้ (`CookieName`)

```c
  uVar4 = FUN_004e7b84(DAT_00b7576c);
  uVar4 = FUN_005db8d4(&DAT_009de314, uVar4);
  thunk_FUN_008f5b98(&stack0x00000038, "CookieMaxHp", &stack0x00000008);
  FUN_005da244(uVar1, uVar4, &stack0x00000038);
```
* **คำอธิบาย:** ดึงค่าเลือดเต็มของคุกกี้ผ่านฟังก์ชัน `FUN_004e7b84(DAT_00b7576c)` แล้วผูกเข้ากับตัวแปรระบบชื่อ **`CookieMaxHp`**

```c
  uVar4 = FUN_004e7b18(DAT_00b7576c);
  uVar4 = FUN_005db8d4(&DAT_009de314, uVar4);
  thunk_FUN_008f5b98(&stack0x0000003c, "CookieCurHp", &stack0x0000000c);
  FUN_005da244(uVar1, uVar4, &stack0x0000003c);
```
* **คำอธิบาย:** ดึงค่าเลือดปัจจุบันของคุกกี้ผ่านฟังก์ชัน `FUN_004e7b18(DAT_00b7576c)` แล้วผูกเข้ากับตัวแปรระบบชื่อ **`CookieCurHp`**

```c
  thunk_FUN_008f5b98(&stack0x00000040, "PatternCreationCount", ...);
  thunk_FUN_008f5b98(&stack0x00000044, "PatternId", ...);
  thunk_FUN_008f5b98(&stack0x00000048, "PlayTime", ...);
```
* **คำอธิบาย:** บันทึกข้อมูลการเกิดสิ่งกีดขวาง (`PatternCreationCount`), รหัสด่าน (`PatternId`), และเวลาวิ่งรวม (`PlayTime`)

```c
  FUN_004e5a30(DAT_00b7576c, "MainGame_SecondCookieCreated", uVar1, 0);
```
* **คำอธิบาย:** ส่งสัญญาณเรียก Event **`MainGame_SecondCookieCreated`** (เมื่อตัวผลัดลงมาวิ่ง หรือเริ่มเกมใหม่) เพื่อถ่ายทอดค่าตัวคูณความเร็วและข้อมูลเลือดทั้งหมดที่คำนวณไว้ข้างต้นไปยังตัวละครที่กำลังวิ่งอยู่!

---

## 🎯 ตารางสรุปการจับคู่สัญลักษณ์ที่สำคัญในโค้ด

| รหัสใน Ghidra | ชนิดข้อมูล | ค่าแท้จริง | ความหมายในระบบเกม Cookie Run |
| :--- | :---: | :---: | :--- |
| **`0x48e`** | Hex Int | **`1166`** | รหัสสแตท `EMagicStatType_WorldSpeedPropotionToCharacterHealth` (รถพยาบาล) |
| **`0x410`** | Hex Int | **`1040`** | รหัสสแตท `EMagicStatType_BasicWorldSpeedRate` (ความเร็วพื้นฐานปกติ) |
| **`0x424`** | Hex Int | **`1060`** | รหัสสแตทความเร็วรอง |
| **`0x3f800000`** | Float 32 | **`1.0`** | ความเร็วฐานปกติ (Base Speed 100%) |
| **`0xd2f1a9fc, 0x3f50624d`** | Double 64 | **`0.001`** | ตัวคูณปรับสเกลค่าดิบ ($1150 \times 0.001 = 1.150$ หรือ $+15.0\%$) |
| **`"CookieMaxHp"`** | String | เลือดเต็ม | ตัวแปรเพดานเลือดสูงสุดที่ใช้เป็นตัวหาร |
| **`"CookieCurHp"`** | String | เลือดปัจจุบัน | ตัวแปรเลือดที่เหลืออยู่จริง ณ ขณะนั้น |
| **`"MainGame_SecondCookieCreated"`**| String | Event Name | อีเวนต์สร้างตัวละครและสั่งให้เริ่มประมวลผลสแตทความเร็ว |
