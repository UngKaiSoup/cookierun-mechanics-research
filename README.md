# 🍪 Cookie Run Classic / Kakao / LINE — Reverse Engineering & Mechanics Toolkit

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Android%20%7C%20Windows-green.svg)]()
[![Topic](https://img.shields.io/badge/Research-Game%20Mechanics%20%26%20Reverse%20Engineering-orange.svg)]()

> A comprehensive reverse-engineering toolkit and research repository for **Cookie Run Classic** (Kakao / LINE editions). Contains balance data extractors, `.djb` decryptors, decompiled game symbols, empirical test logs, and the mathematical proof solving the **Toy Ambulance speed mystery**.

---

## 📑 Table of Contents
- [🌟 Key Findings & Mythbusting](#-key-findings--mythbusting)
  - [1. The Toy Ambulance Formula](#1-the-toy-ambulance-formula)
  - [2. The 15% Mathematical Proof](#2-the-15-vs-16-mathematical-proof)
  - [3. The Level 60 HP Upgrade Question](#3-the-level-60-hp-upgrade-question)
- [📁 Repository Structure](#-repository-structure)
- [📊 Visual Graphs & Charts](#-visual-graphs--charts)
- [🛠️ Tooling & How to Extract Game Data](#️-tooling--how-to-extract-game-data)
- [🔬 Ghidra Reverse-Engineering Guide](#-ghidra-reverse-engineering-guide)
- [📄 Documentation & Articles](#-documentation--articles)
- [🙏 Credits & Acknowledgments](#-credits--acknowledgments)
- [⚖️ Disclaimer](#️-disclaimer)

---

## 🌟 Key Findings & Mythbusting

### 1. The Toy Ambulance Formula
For years, the community debated whether the **Toy Ambulance** (`작은 구급차 장난감`) made you faster when low on health (an "emergency sprint") or when full on health.

* **Myth:** Lower HP = Faster speed.
* **Reality (Verified via `libgame.so`):** **Full HP = Maximum Speed (+15.0%)**, linearly tapering down to +0.0% as HP reaches zero.

$$v(t) = v_{\text{base}} \times \left(1 + 0.150 \times \frac{\text{CurrentHP}(t)}{\text{MaxHP}}\right)$$

* In the decompiled binary data (`TreasurePassiveAttr`), Stat ID `1166` (`EMagicStatType_WorldSpeedPropotionToCharacterHealth`) is hardcoded to **`1150`** (which maps to **+15.0%** in Devsisters' engine where `1000 = 100%`).
* Upgrading the treasure from `+0` to `+9` **does not increase speed** — it only increases the number of revives from 1 to 3!

### 2. The 15% Mathematical Proof
When running empirical tests under strictly controlled conditions (0 items, 0 bonus time, 1 Speed Blast of 2.0s, crash at 11% HP):
* **Baseline Run (No Ambulance):** 1,802 EXP (~90.10s)
* **Ambulance Run:** 1,658 EXP (~82.90s)

Simple linear average calculation $((100\% + 11\%) / 2 = 55.5\%)$ leads to an erroneous **~15.65% ~ 16.0%** speed result.

However, Cookie Run's world scroll speed accelerates by **+64.8%** from Stage 1 (910 speed) to Stage 10+ (1,500 speed). This causes HP to drain at a non-linear accelerating rate ($\gamma \approx 1.12$). 

When integrated via calculus:
$$\overline{\text{HP}}_{\text{integral}} = 1.0 - \frac{1.0 - 0.11}{1 + 1.12} = \mathbf{58.02\%}$$

Subtracting the identical 2.0s Speed Blast from both runs yields:
$$S_{\text{max}} = \frac{(88.10 / 80.90) - 1.0}{0.5802} \rightarrow \mathbf{15.00\%} \quad (\text{Error: } 0.8 \text{ EXP / } 0.04\text{ seconds!})$$

### 3. The Level 60 HP Upgrade Question
* In the lobby shop, players can upgrade account HP up to **Level 60** (granting 260 Energy, stat ID `1022`).
* **Does this change the speed multiplier?** **No.** The game always evaluates $\frac{\text{CurrentHP}}{\text{MaxHP}}$ on a normalized $0.0 - 1.0$ scale. Level 60 only increases survival time; the relative speed curve remains identical.

---

## 📁 Repository Structure

```text
├── analysis/                      # Analysis, regression & mathematical proof scripts
│   ├── simulate_15_percent_proof.py      # Core calculus proof script
│   ├── recalculate_speed_blast.py        # Item isolation & net speedup analysis
│   ├── summarize_speed_treasures.py      # Clean formatted list of all speed treasures
│   ├── categorize_speed_treasures.py     # Breakdown of Base, Blast, Giant, & HP speed
│   ├── generate_charts_thai.py           # Generates 300 DPI Thai annotated comparison charts
│   ├── generate_smooth_curves.py         # Generates differential distance & speed curves
│   └── extract_hp_drain_mechanics.py     # Disassembles HP decay ticker in libgame.so
│
├── charts/                        # High-resolution comparison graphs & figures
│   ├── toy_ambulance_speed_mechanics.png # Overview diagram of the mechanics
│   ├── toy_ambulance_3_curves_comparison.png
│   ├── toy_ambulance_differential_proof.png
│   ├── toy_ambulance_natural_decay_curve.png
│   └── graph_comparison_both_theories_thai.png
│
├── docs/                          # Detailed research papers & publication drafts
│   ├── medium_article_cookie_run_ambulance.md # Publication-ready Medium article
│   ├── video_onscreen_text_script.md          # Casual on-screen video subtitle script
│   └── hp_drain_mechanics_proof.md            # Comprehensive technical evidence report
│
├── tools/                         # Decryption & extraction utilities
│   ├── CookieRunDJBFConverter.exe             # C# CLI tool for AES/FastLZ .djb decryption
│   ├── extract_apk.py                         # Extracts raw assets from APK archives
│   ├── decrypt_djb.py                         # Decrypts .djb balance tables into .bin
│   ├── convert_bin_to_json.py                 # Parses binary tables into readable .json
│   └── unpack_line_614.py                     # One-click pipeline for LINE Cookie Run v6.1.4
│
├── data/                          # Extracted game balance tables
│   ├── kakao_8.27_extracted/                 # Full JSON tables from Kakao v8.27
│   ├── LINE_6.1.4_EXTRACTED/                 # Full JSON tables & Ghidra .so from LINE v6.1.4
│   │   ├── 01_FOR_GHIDRA_SO/                 # libgame.so ready for Ghidra analysis
│   │   └── 02_JSON_DATA/                     # 95 formatted JSON game tables
│   └── summary_tables/                       # Master tables for speed, mystery box, etc.
│
├── research_archive/              # Experimental memory scripts, RAM scans, & disassemblies
└── .gitignore                     # Excludes heavy APKs, dumps, and binary caches
```

---

## 📊 Visual Graphs & Charts

All charts are available in high resolution inside the [`charts/`](charts/) directory:

| Graph Preview | Description |
| :---: | :--- |
| ![Ambulance Mechanics](charts/toy_ambulance_speed_mechanics.png) | **Toy Ambulance Speed Mechanics**: Comparison between full health (+15%) vs low health (+1.65%). |
| ![Two Models Comparison](charts/toy_ambulance_3_curves_comparison.png) | **Dual Models Comparison**: Comparing empirical simulation curves of Model A (High HP = Fast, ~82.9s) vs Model B (Low HP = Fast, ~84.6s) against Baseline (~90.1s). |
| ![Natural Decay Curve](charts/toy_ambulance_natural_decay_curve.png) | **Natural Decay Curve**: Linear drain vs actual accelerating stage drain ($\gamma \approx 1.12$). |
| ![Differential Proof](charts/toy_ambulance_differential_proof.png) | **Differential Proof**: Distance delta $\Delta x(t)$ proving High HP = Max Speed. |
| ![Both Theories Thai](charts/graph_comparison_both_theories_thai.png) | **Comparative Breakdown (Thai Annotation)**: Side-by-side visual analysis comparing both theories. |

---

## 🛠️ Tooling & How to Extract Game Data

To unpack and decrypt balance tables from an older Cookie Run APK:

### Step 1: Extract APK Assets
```bash
python tools/extract_apk.py
```

### Step 2: Decrypt `.djb` (AES-256 + FastLZ) to `.bin`
```bash
.\tools\CookieRunDJBFConverter.exe -m decrypt -k kakao -d <path_to_djb_folder> -s *.djb
```
*(Use `-k kakao` for Kakao and LINE editions)*

### Step 3: Convert Binary Tables to JSON
```bash
python tools/convert_bin_to_json.py
```
*(Outputs clean, readable `.json` files for all balance tables)*

---

## 🔬 Ghidra Reverse-Engineering Guide

To analyze the C++ game engine logic directly:
1. Open **Ghidra** and create a project.
2. Drag and drop `libgame.so` (found in `data/LINE_6.1.4_EXTRACTED/01_FOR_GHIDRA_SO/libgame.so`).
3. Set architecture to **`ARM:LE:32:v7`** (for 32-bit armeabi-v7a) or **`AARCH64`** (for 64-bit).
4. Search strings (`Search` ➔ `For Strings...`):
   * `EMagicStatType_WorldSpeedPropotionToCharacterHealth` (Stat 1166 - Ambulance logic)
   * `Cookie_HpDecrease` (HP drain loop ticker)
   * `Character_EnergyDiminishValueNew` (Base drain constant)
   * `CRXWorldSpeed` (Stage scroll speed multipliers)

---

## 📄 Documentation

Line-by-line breakdown and reverse-engineering analysis of the Cookie Run native engine assembly and decompiled C logic:
* 🇬🇧 **English Version:** [`docs/ghidra_decompiled_code_breakdown_en.md`](docs/ghidra_decompiled_code_breakdown_en.md)
* 🇹🇭 **ฉบับภาษาไทย:** [`docs/ghidra_decompiled_code_breakdown_th.md`](docs/ghidra_decompiled_code_breakdown_th.md)

---

## 🙏 Credits & Acknowledgments

* Special thanks and full credit to **[@barncastle](https://github.com/barncastle)** for creating the open-source **[CookieRun-DJBF-Converter](https://github.com/barncastle/CookieRun-DJBF-Converter)**.
  * Their reverse-engineering work on the proprietary Devsisters DJBF format (AES-256-CBC salted decryption + FastLZ decompression) made it possible to decrypt and parse all `.djb` game balance tables in this repository.
  * The tool executable is bundled under [`tools/CookieRunDJBFConverter.exe`](tools/) and invoked via [`tools/decrypt_djb.py`](tools/decrypt_djb.py) and [`tools/unpack_line_614.py`](tools/unpack_line_614.py).

---

## ⚖️ Disclaimer
*Cookie Run* and all associated assets, characters, and data belong to **Devsisters Corp.** This repository is an unofficial, non-commercial open-source research and educational reverse-engineering project.
