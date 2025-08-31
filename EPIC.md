# Epic: Voidfallen Adventure Game

## Overview

This epic tracks the development of the text-based adventure game "Voidfallen".  
It is organized into milestones, each with acceptance criteria and a summary of progress.

---

## Milestone 1: Core Game Loop and Player System

**Acceptance Criteria:**
- Player can start a new game, load, save, and export data.
- Player has stats (HP, EXP, Level, Attack, Inventory, Coins).
- Player can take damage, heal, gain EXP, and level up.
- Main menu with options for new game, load, export, and quit.

**Progress:**  
- Implemented `Player` class with all required stats and methods.
- Save/load/export system using JSON.
- Main menu and game loop functional.

---

## Milestone 2: Exploration and Encounters

**Acceptance Criteria:**
- Player can explore multiple paths (north, west, east, village, back).
- Each path has a unique description.
- Random enemy encounters and basic battle system.
- Enemies scale with player level.

**Progress:**  
- Added exploration system with location descriptions.
- Implemented random enemy encounters and scaling.
- Battle system with attack, use item, and run options.

---

## Milestone 3: Acts and Progression

**Acceptance Criteria:**
- Game is split into Act 1 (pre-village) and Act 2 (post-village).
- Act 2 unlocks new paths (ruins, cavern).
- Enemy pools differ between acts.
- Village unlocks shop and rest.

**Progress:**  
- Act system implemented.
- Village and Act 2 content added.
- Enemy pools and scaling updated for acts.

---

## Milestone 4: Items, Shop, and Crafting

**Acceptance Criteria:**
- Shop system with buyable items (Potion, Lantern, Bandage).
- Inventory system supports adding and using items.
- Crafting system for bandages from silk.
- Crafting accessible from exploration, after battle, and in village.

**Progress:**  
- Shop and inventory system implemented.
- Crafting menu added and accessible in all required places.
- Bandages can be crafted from silk.

---

## Milestone 5: Advanced Mechanics (Lantern, Cavern, Debuffs)

**Acceptance Criteria:**
- Lantern required for cavern, with fuel system (animal fat).
- Cavern is a maze with left/right/forward/back navigation.
- Lantern fuel depletes per move; player can get lost if fuel runs out.
- Cavern and rare enemies (bats, snakes, spiders, ghosts) with special effects.
- Poison and bleed debuffs, with bandages to cure.
- Silk and animal fat as enemy drops.

**Progress:**  
- Lantern and fuel system implemented.
- Cavern navigation and fuel depletion logic complete.
- Enemy debuffs (poison, bleed) and lifesteal for bats/ghosts implemented.
- Bandage crafting and use fully functional.

---

## Milestone 6: Developer Tools and Export

**Acceptance Criteria:**
- Developer mode with commands for giving items, stats, teleport, and crafting.
- Export player data to JSON.
- All developer commands documented.

**Progress:**  
- Developer mode and commands implemented.
- Export functionality available from main menu.

---

## Milestone 7: Difficulty Settings

**Acceptance Criteria:**
- Player can choose difficulty from the main menu (Options).
- Easy: enemies have half health and attack.
- Normal: default settings.
- Hard: enemies deal double attack.
- Difficulty affects all enemy scaling.

**Progress:**  
- Difficulty selection added to main menu.
- Enemy scaling logic updated to respect difficulty.
- Difficulty can be changed before starting a new game.

---

## Milestone 8: Alternate "Dark" Game Mode & Lore

**Acceptance Criteria:**
- A very rare cutscene (0.1% chance) can trigger a new "dark" game mode.
- In dark mode, all dialog, enemy pools, and descriptions are changed.
- No original enemies spawn in dark mode; new horror-themed enemies are used.
- Developer mode allows manually triggering dark mode at any time.
- All locations, shop, and events have alternate dialog and flavor in dark mode.
- The game supports deep lore and partial horror aspects.

**Progress:**  
- Rare cutscene and alternate mode logic implemented.
- All dialog and exploration text have alternate versions for dark mode.
- Enemy pools are completely replaced in dark mode.
- Developer command `darkmode` added to trigger dark mode.
- Shop and village dialog adapt to the current mode.
- All features robust and tested for both normal and dark modes.

---

## Milestone 9: Documentation and Acceptance

**Acceptance Criteria:**
- All milestones documented in this epic.
- Each milestone has clear acceptance criteria and progress summary.
- Code reviewed for bugs and robustness.

**Progress:**  
- Epic documentation up to date.
- All major features and mechanics implemented and reviewed.

---

## Next Steps

- Continue to add new features as new milestones.
- Expand dark mode with more lore, events, and unique mechanics.
- Update this epic with each new milestone and progress.

---

# Voidfallen: Ultimate Path & Bug/Exploit Review

## Main Paths and Features Tested

### 1. New Game (Intro/Skip)
- **Intro path:** All dialog, name, and backstory prompts work. Developer mode triggers for "moogie".
- **Skip intro:** Name prompt works, developer mode triggers, game starts as expected.

### 2. Difficulty Selection
- **Options menu:** Difficulty can be set before starting a new game. Enemy scaling changes as expected for easy/normal/hard.

### 3. Exploration
- **All directions:** North, West, East, Village, Ruins, Cavern, Craft, Back.
- **Village:** Shop, rest, crafting, and leave all work.
- **Cavern:** Lantern/fuel checks, navigation, debuffs, and escape/lost logic all function.

### 4. Battles
- **Enemy pools:** Correct for act, cavern, and rare spawns.
- **Debuffs:** Poison and bleed apply and tick correctly. Bandages cure both.
- **Lifesteal:** Only triggers if enemy is alive after attack.
- **Run:** 50% chance to escape works.

### 5. Items & Crafting
- **Shop:** All items purchasable, gold deducted, inventory updates.
- **Crafting:** Bandages from silk in all locations (explore, after battle, village, dev).
- **Lantern:** Auto-fueled on first acquire, refuel works, fuel decrements per move.

### 6. Save/Load/Export
- **Save/load:** Works at all points, including after death in cavern.
- **Export:** Player data exports to JSON.

### 7. Developer Mode
- **All commands:** Give, gold, heal, equip, goto, stats, craft bandage, exit—all work as intended.

---

## Exploit & Game-Breaking Bug Review

### Exploits

- **Bandage Crafting:** Unlimited crafting is possible if the player has enough silk, but this is intended.
- **Shop:** No gold exploit; gold is checked before purchase.
- **Lantern Fuel:** No infinite fuel exploit; refueling requires animal fat.
- **EXP/Level:** No infinite EXP exploit; only awarded for battle wins.
- **Run from Battle:** 50% chance, no infinite escape.

### Game-Breaking Bugs

- **Cavern Escape:** If lantern fuel runs out and the player is not at the entrance, they are reset to last save. No infinite loop or softlock.
- **Difficulty:** Difficulty is session-based and not saved/loaded, but this is by design.
- **Inventory:** No negative inventory possible; all item removals are checked.
- **Battle:** No crash on death; game exits cleanly.
- **Crafting:** No crash if crafting without enough materials; proper message shown.
- **Shop:** No crash if buying without enough gold; proper message shown.
- **Save/Load:** No crash on missing save file; proper message shown.

### Minor/Edge Cases

- **Multiple Lanterns:** If player acquires multiple lanterns, only the first triggers auto-fuel. This is not exploitable.
- **Developer Mode:** Can be used to give unlimited items, but this is intentional for testing.

---

## Conclusion

**No game-breaking bugs or major exploits found.**  
All main and edge paths function as intended.  
Game is robust for all tested scenarios.

---
## Troubleshooting: PyInstaller Not Recognized

If you see:
```
pyinstaller : The term 'pyinstaller' is not recognized as the name of a cmdlet, function, script file, or operable program.
```

### Solution

1. **Make sure PyInstaller is installed:**
   ```
   pip install pyinstaller
   ```

2. **If using PowerShell or CMD, try:**
   ```
   python -m PyInstaller --onefile game.py
   ```
   or
   ```
   py -m PyInstaller --onefile game.py
   ```

3. **If still not recognized:**
   - Close and reopen your terminal after installing.
   - Make sure your Python/Scripts directory is in your PATH environment variable.
   - You can check if PyInstaller is installed by running:
     ```
     pip show pyinstaller
     ```

4. **If using a virtual environment:**
   - Activate your virtual environment first, then run the command.

---

**Summary:**  
Use `python -m PyInstaller --onefile game.py` if `pyinstaller` is not recognized.

## FAQ

### If I update the code, will that also update the .exe?

**No.**  
If you change your Python code (`game.py`), you must re-run the PyInstaller command to generate a new `.exe` file.  
The `.exe` is a snapshot of your code at the time you built it.  
To update the `.exe`:

1. Edit and save your changes to `game.py`.
2. Re-run:
   ```
   python -m PyInstaller --onefile game.py
   ```
3. Use the new `.exe` in the `dist` folder.

---