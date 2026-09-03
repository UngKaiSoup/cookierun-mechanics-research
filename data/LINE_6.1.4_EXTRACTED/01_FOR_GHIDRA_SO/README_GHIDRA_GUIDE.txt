=== HOW TO ANALYZE IN GHIDRA (LINE Cookie Run v6.1.4) ===

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
