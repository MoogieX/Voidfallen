import json
import os
import random
import time
from typing import Dict
from rich.console import Console
from libraries import Libraries
from exploration import Exploration
SAVE_FILE = "save..json"
console = Console()
from player import Player
from battle import Battle, AzraelBattle
lib = Libraries()
class Game:
   def __init__(self):
       random.seed()
       self.console = console
       self.player = Player(self.console)
       self.exploration = Exploration(self)
       self.alt_mode = False
       self.act = 1
       self.developer_mode = False
       self.difficulty = "normal"
       self.shop_prices = {
           "Potion": 10,
           "Bandage": 5,
           "Lantern": 20,
           "Silk": 2,
           "Animal Fat": 3
       }
       self.weapon_tiers = {
           "Rusty": {"bonus": 2, "names": ["Sword", "Axe", "Dagger,"]},
           "Iron": {"bonus": 5, "names": ["Sword", "Axe", "Dagger,"]},
           "Steel": {"bonus": 10, "names": ["Sword", "Axe", "Dagger,"]},
           "Diamond": {"bonus": 20, "names":["Sword", "Axe", "Dagger,"]}
       }
       self._shop_visited = 0
       self.village_visited_first_time = False # New: Track first village visit


   # --------------------
   # Save / Load System
   # --------------------
   def save_game(self) -> None:
       """Saves the current game state (player data) to a JSON file."""
       try:
           with open(SAVE_FILE, "w") as f:
               json.dump(self.player.to_dict(), f, indent=2)
           console.print("💾 Game saved!")
       except (IOError, OSError) as e:
           console.print(f"❌ Error saving game: {e}. WOMP WOMP, make sure you have permisions enabled, or unless you are a noob with no disk space. Either way you should not be seeing this.")
       except Exception as e:
           console.print(f"❌ ERROR LOADING GAME, please flag as a bug: {e}")


   def load_game(self) -> bool:
       """Loads the game state from a JSON save file."""
       if not os.path.exists(SAVE_FILE):
           console.print("⚠ WOMP WOMP no saves on record.")
           return False
       try:
           with open(SAVE_FILE, "r") as f:
               data = json.load(f)
           self.player.from_dict(data)
           console.print("✅ Game loaded successfully! Yippie :D")
           return True
       except (IOError, OSError) as e:
           console.print(f"❌ Error reading save file: {e}. The file might be corrupted or inaccessable, this could be due to swapping between game versions or another error.")
           return False
       except json.JSONDecodeError as e:
           console.print(f"❌ Error decoding save file: {e}. The save file is corrupted or invalid for this version of the game. Please contact the boogie.")
           return False
       except Exception as e:
           console.print(f"❌ An unexpected error occurred while loading, please contact the boogie with this bug: {e}")
           return False


   def export_player_data(self) -> None:
       """Exports the current player data to a JSON file."""
       export_file = f"{self.player.name}_export.json"
       try:
           with open(export_file, "w") as f:
               json.dump(self.player.to_dict(), f, indent=2)
           console.print(f"Player data exported to {export_file}!")
       except (IOError, OSError) as e:
           console.print(f"❌ Error exporting player data: {e}. WOMP WOMP check file permisions, or unless you are a noob with no disk space. Either way you shouldn't see this")
       except Exception as e:
           console.print(f"❌ An unexpected error occurred while exporting, try again bozo: {e}")


   # --------------------
   # Game Flow
   # --------------------
   def intro(self) -> None:
       if self.player.name == "Astar":
           self._astar_intro()
           return
       self.player.name = input("Lost one... Do you remember your name? ").strip()
       if self.player.name.lower() == "moogietheboogie":
           self.developer_mode = True
           console.print("✨✦ Developer mode activated! Welcome back #001 ✦✨")
       console.print(f"Interesting name you have... {self.player.name}, most do not retain such memory.")

       lib.slow_type_font_color("Blue","Fancy", "'Where did you come from? This must be a blessing for my calls for... Nevermind'")
       lib.slow_type_font_color("Blue", "Fancy", "'Tis' not often we have visitors here in this sect of the void.'")
       input()
       self.player.backstory = input("'Before you came here, do you recall where you hailed from?' ").strip()
       print(f"Ah... {self.player.backstory}. It is a place I am yet to visit, though it is much beautiful from what I hear.")
       print(f"You must have come a long way from there, {self.player.name}... Do you ever plan to go home?")
       
       intro_ask = ["Yes","No"]

       choices = lib.select("'Care to sit down with me? Surely you must be frazzled after such a journey'", intro_ask)

       if choices == "Yes":
           console.print("'Very well then.' The figure moves aside for you to join them")
       else:
           console.print("'That's alright, just stay to talk, if you will.'")

       intro_ask2 = ["Yes", "No"]

       choices = lib.select(f"Say, {self.player.name}, have you heard the rumors? (NOTE: DO NOT SAY YES IF YOU ARE NEW TO PLAYING)", intro_ask2)
       if choices == "Yes":
           console.print(
               "So you are aware, how peculiar... Then, "
               f"{self.player.name}, there is an old trail up to the East. "
               "You may find an inn where you can stay..."
           )
       else:
           console.print(
               "'Not that I would have expected you to. '"
               "'There are creatures from the north, they have been encroaching on our void... '"
               "'Slaughtering the residents. You must learn to survive... "
               "You can ATTACK an enemy that comes near you... And RUN if you feel you won't survive... But i hope it does not come to that of course' "
               f"'And you can USE items in such situations as well, but be wary, and calculating of your actions {self.player.name}...'"
           )

       console.print("\nYou leave the clearing after giving thanks to the figure, onwards you shall go...\n")


   def new_intro(self) -> None:
       import os
       user_system_name = os.path.basename(os.path.expanduser('~'))

       # After the new intro, we can proceed to the name input from the original intro
       self.player.name = input("A brief memory flashes by... 'Lost one, do you remember your name?' ").strip()
       if self.player.name.lower() == "moogietheboogie":
           self.developer_mode = True
           lib.slow_type_font_color("Yellow", "Fancy", "✩✩✩ Developer mode activated, for the second time~ Welcome back, Boogie ✩✩✩")


   def _astar_intro(self):
       lib.slow_type_font_color("Blue", "Bold","\n✮ ⋆ ˚｡ ⋆｡°✩ Chapter 2  ✩ ⋆ ˚｡ ⋆｡°✮")
       lib.slow_type_font_color("Magenta", "Fancy", "━─┉┈◈ The end, simply known as a new begining... ◈┈┉─━")
       console.print("You awaken within the field, of which you do not recognize.")
       console.print("An entity, the soft features that it once shown you, now hardened as they stare down at your form in the grass")
       console.print("'Lost one... That was something you never were, was it?...'")
       console.print("'You did this.. Why did you do this to us...?'")
       console.print(f"'I took you in with kindness, {self.player.name}.'")


   def _create_astar_save(self):
       astar_data = {
           "name": "Astar",
           "backstory": "A sinning soul",
           "hp": 300,
           "max_hp": 300,
           "exp": 0,
           "level": 30,
           "attack": 50,
           "inventory": {"Potion": 10, "Bandage": 5, "Ectoplasm": 1},
           "coins": {"gold": 1000, "silver": 0, "bronze": 0, "zinc": 0},
           "unlocked_rest": True,
           "pet": "Spectral Fox",
           "armor": "Void Cloak",
           "tool": "Legendary Ancient Key",
           "lantern_on": True,
           "lantern_fuel": 20,
           "poison_turns": 0,
           "bleed_turns": 0,
           "act": 2,
           "alt_mode": True,
           "developer_mode": self.developer_mode # Persist dev mode
       }
       try:
           with open(SAVE_FILE, "w") as f:
               json.dump(astar_data, f, indent=2)
       except (IOError, OSError) as e:
           console.print(f"❌ Error creating Astar save, please flag to github: {e}.")


   def _dev_boss(self, cmd: str):
       parts = cmd.split()
       boss_name = " ".join(parts[1:]).title() if len(parts) > 1 else None


       if boss_name:
           # Create a generic boss with high stats for testing
           boss = {"name": boss_name, "hp": 500, "attack": 50, "boss": True}
           self.console.print(f"Spawning custom boss: {boss_name}")
       elif self.alt_mode:
           boss = {"name": "Azrael, the Death Angel", "hp": 9999, "attack": 999, "boss": True}
           self.console.print("Death approaches...")
       else:
           boss = {"name": "Ancient Dragon", "hp": 300, "attack": 30, "boss": True}
           self.console.print("The Ancient Dragon approaches...")
      
       self.battle(boss)


   def set_difficulty(self):
       while True:
        difficulty_set = [
            "Easy",
            "Normal",
            "Hard"
        ]
        choices = lib.select("Choose a difficulty:", difficulty_set)
        if choices == "Easy":
            self.difficulty = "easy"
            console.print("Difficulty set to Easy.")
            break
        elif choices == "Normal":
               self.difficulty = "normal"
               console.print("Difficulty set to Normal.")
               break
        elif choices == "Hard":
            self.difficulty = "hard"
            console.print("Difficulty set to Hard.")
            break
        else:
            console.print("If you get this message this is a bug!!!!")


   def scale_enemy(self, act=None, cavern=False, rare=False, volcano=False) -> Dict[str, int]:
       lvl = self.player.level
       if volcano:
           lvl = max(lvl, 20) 
       if self.alt_mode:
           if volcano:
               enemy_list = ["Charred Soul", "Burnned", "Flickering shadow"]
               base_hp = 60
               base_attack = 20
               hp_scale = 25
               atk_scale = 8
           elif cavern or rare:
               enemy_list = [
                   "Soul Of The Cursed", "Watcher", "Flesh Moth", "The Shattered", "..."
               ]
               base_hp = 18
               base_attack = 7
               hp_scale = 6
               atk_scale = 3
           elif act == 2 or (act is None and self.act == 2):
               enemy_list = [
                   "Guarded Soul", "The Forgotten", "Hollow heart", "Bleeding Idol", "The Feasting"
               ]
               base_hp = 50
               base_attack = 18
               hp_scale = 22
               atk_scale = 7
           else:
               enemy_list = [
                   "Fractured Creature", "Boiled Blood", "Weeping Entity", "Lost Whisper"
               ]
               base_hp = 28
               base_attack = 9
               hp_scale = 13
               atk_scale = 4
       else:
           # Normal mode enemies
           if volcano:
               enemy_list = ["Wandering Tendril", "Lost Soul Of Determination", "Seared figure", "The Melted"]
               base_hp = 50
               base_attack = 15
               hp_scale = 20
               atk_scale = 6
           elif cavern or rare:
               enemy_list = ["Winged Horror", "Cursed Winged Horror", "", "Shifting Roots", "Nightcrawler", "Damned Soul"]
               base_hp = 12
               base_attack = 4
               hp_scale = 4
               atk_scale = 2
           # Act 2 overworld enemies
           elif act == 2 or (act is None and self.act == 2):
               enemy_list = ["Lost soul", "Forgotten entity", "Wind whispers", "Specter", "Abyssal Creature"]
               base_hp = 40
               base_attack = 12
               hp_scale = 18
               atk_scale = 5
           # Act 1 enemies
           else:
               enemy_list = ["Shadow", "Shade", "Figure", "Creature"]
               base_hp = 20
               base_attack = 5
               hp_scale = 10
               atk_scale = 2
       hp = base_hp + lvl * hp_scale
       attack = base_attack + lvl * atk_scale
       # Apply difficulty modifiers
       if self.difficulty == "easy":
           hp = int(hp * 0.5)
           attack = int(attack * 0.5)
       elif self.difficulty == "hard":
           attack = int(attack * 2)
           hp = int(hp * 3)
       return {
           "name": random.choice(enemy_list),
           "hp": max(1, hp),
           "attack": max(1, attack),
       }


   def battle(self, enemy: Dict[str, int], cavern=False) -> str:
       """Initializes and runs a battle encounter."""
       battle_instance = Battle(self.player, enemy, self, cavern)
       result = battle_instance.run()


       if result == "won":
           # Boss battles have custom rewards handled in their respective methods
           if enemy.get("boss"):
               return result
           exp_gain = 10 * self.player.level
           gold_gain = random.randint(5, 10) * self.player.level
           console.print(f"You defeated the {enemy['name']} and gained {exp_gain} EXP and {gold_gain} gold!")
           self.player.gain_exp(exp_gain)
           self.player.gain_gold(gold_gain)
           battle_instance.handle_drops()
           self.save_game()
          
       elif result == "lost":
           if enemy.get("boss"):
               self._create_astar_save()
               console.print("You have been defeated... but your journey is not over.")
               exit()
           else:
               console.print("You have fallen...")
               return "lost_normal"
       elif result == "enemy_fled":
           # Message is handled in the Battle class, no further action needed.
           pass
       # If "fled" (player fled), no further action is needed here.
       return result


   # Crafting menu
   def crafting_menu(self):
       crafting_menu = [
           "Bandage",
           "Exit"
       ]
       choices = lib.select("━─┉┈◈ Crafting ◈┈┉─━", crafting_menu).lower()
       if choices == "Bandage":
        self._craft_bandage()
       elif choices == "Exit":
        console.print("Exiting crafting menu...")
        
       else:
        console.print("THIS IS AN ERROR! PLEASE FLAG TO THE BOOGIE! Attempting to exit...")
        time.sleep(.5)
        


   def inventory_menu(self):
       while True:
           self.player.display_inventory()
           inventory_choices = [
            "Use item",
            "Equip tool",
            "Unequip tool",
            "Equip armor",
            "Unequip armor",
            "Refuel lantern",
            "Drop",
            "Exit"

           ]
           action = lib.select("━─┉┈◈ Inventory ◈┈┉─━", inventory_choices)


           if action == "Exit":
               console.print("Closing inventory...")
               break
           elif action == "Use item":
            item_name = input("What would you like to use? ").strip()
            self._handle_inventory_use(item_name)
           elif action == "Equip tool":
            item_name = input("What would you like to equip? ").strip()
            self._handle_inventory_equip(f"tool {item_name}")
           elif action == "Unequip tool":
            self._handle_inventory_unequip("tool")
           elif action == "Equip armor":
            item_name = input("What would you like to equip? ").strip()
            self._handle_inventory_equip(f"armor {item_name}")
           elif action == "Unequip armor":
            self._handle_inventory_unequip("armor")
           elif action == "Refuel lantern":
            self._handle_refuel_lantern()
           elif action == "Drop":
            item_name = input("What would you like to drop? ").strip()
            self._handle_inventory_drop(item_name)
           else:
               console.print("Invalid option.")


   def _handle_inventory_use(self, item_name: str):
       # Placeholder for using items (e.g., potions)
       if item_name.lower() == "potion" and self.player.inventory.get("Potion", 0) > 0:
           self.player.inventory["Potion"] -= 1
           self.player.heal(30)
           console.print("You drink a potion and restore 30 HP.")
       elif item_name.lower() == "bandage" and self.player.inventory.get("Bandage", 0) > 0:
           self.player.inventory["Bandage"] -= 1
           self.player.poison_turns = 0
           self.player.bleed_turns = 0
           console.print("You use a bandage and wrap it around your wounds, easing them for the moment.")
       else:
           console.print(f"You don't have {item_name} or it's not usable in this location.")


   def _handle_inventory_equip(self, args: str):
       parts = args.split(maxsplit=1)
       if len(parts) < 2:
           console.print("Usage: equip [type] [item_name]")
           return
       item_type = parts[0].lower()
       item_name = parts[1].title()


       if item_type in ["armor", "tool", "pet"]:
           if item_name in self.player.inventory or (item_type == "pet" and item_name == self.player.pet): # Allow equipping if already equipped
               self.player.equip(item_type, item_name)
           else:
               console.print(f"You don't have {item_name} in your inventory.")
       else:
           console.print("Invalid equipment type. Use 'armor', 'tool', or 'pet'.")


   def _handle_inventory_unequip(self, item_type: str):
       item_type = item_type.lower()
       if item_type == "armor":
           if self.player.armor:
               self.player.add_item(self.player.armor) # Add to inventory
               console.print(f"You unequipped {self.player.armor}.")
               self.player.armor = None
           else:
               console.print("You have no armor equipped.")
       elif item_type == "tool":
           if self.player.tool:
               self.player.add_item(self.player.tool) # Add to inventory
               console.print(f"You unequipped {self.player.tool}.")
               self.player.tool = None
           else:
               console.print("You have no tool equipped.")
       elif item_type == "pet":
           if self.player.pet:
               self.player.add_item(self.player.pet) # Add to inventory
               console.print(f"You unequipped {self.player.pet}. How dare you?")
               self.player.pet = None
           else:
               console.print("You have no pet equipped.")
       else:
           console.print("Invalid equip usage")


   def _handle_refuel_lantern(self):
       if self.player.inventory.get("Animal Fat", 0) > 0:
        try:
            qty_str = input("How much Animal Fat to use? ").strip()
            if not qty_str: # Handle empty input
                return
            qty = int(qty_str)
            if qty > 0 and self.player.inventory.get("Animal Fat", 0) >= qty:
                self.player.inventory["Animal Fat"] -= qty
                self.player.refuel_lantern(qty * 3) # Assuming 1 fat = 3 fuel
                console.print(f"You used {qty} Animal Fat to refuel your lantern.")
            else:
                console.print("Invalid quantity or not enough Animal Fat.")
        except ValueError:
            console.print("Invalid input. Please enter a number.")
       else:
           console.print("You don't have any Animal Fat.")


   def _handle_inventory_drop(self, item_name: str):
       item_name = item_name.title()
       if item_name in self.player.inventory and self.player.inventory[item_name] > 0:
           if item_name == self.player.pet:
               console.print(f"You heartlessly abandon your loyal companion, {item_name}. It whimpers and scurries away into the shadows, never to be seen again.")
               self.player.pet = None # Unequip if it was equipped
           else:
               console.print(f"You dropped {item_name}.")
           self.player.inventory[item_name] -= 1
           if self.player.inventory[item_name] == 0:
               del self.player.inventory[item_name]
       else:
           console.print(f"You don't have {item_name} to drop.")


   def _craft_bandage(self):
       """Handles the crafting of a Bandage item."""
       if self.player.inventory.get("Silk", 0) >= 2:
           self.player.inventory["Silk"] -= 2
           self.player.add_item("Bandage")
           console.print("You crafted a Bandage from 2 Silk.")
       else:
           console.print("You don't have enough Silk to craft a Bandage.")


   def random_event(self):
       events = []


       # Very rare cutscene: 0.1% chance (1 in 1000)
       if not self.alt_mode:
           events.append({"chance": 0.001, "handler": self._handle_rare_cutscene})


       # 8% chance: find a chest
       events.append({"chance": 0.08, "handler": self._handle_chest_event})


       # 5% chance: find a pet
       events.append({"chance": 0.05, "handler": self._handle_pet_event})


       # Rare cavern enemies in Act 2 overworld
       if self.act == 2:
           events.append({"chance": 0.13, "handler": self._handle_rare_enemy_event})


       # Sort events by chance in descending order to ensure correct priority
       events.sort(key=lambda x: x["chance"], reverse=True)


       roll = random.random()
       for event in events:
           if roll < event["chance"]:
               event["handler"]()
               return True
       return False

#yippie!
   def _handle_rare_cutscene(self):
       """Handles the rare cutscene event, triggering the alternate game mode."""
       self.rare_cutscene()


   def _handle_chest_event(self):
       """Handles the event of finding a chest and distributing loot."""
       loot_type = random.choices(
           ["Potion", "Gold", "Lantern", "Armor", "Tool"],
           weights=[3, 3, 2, 1, 1], k=1
       )[0]
       if loot_type == "Gold":
           amount = random.randint(5, 20)
           self.player.coins["gold"] += amount
           console.print(f"You find a hidden chest! Inside is {amount} gold coins.")
       elif loot_type == "Armor":
           armor = random.choice(["Leather Vest", "Iron Plate", "Void Cloak"])
           console.print(f"You find a hidden chest! Inside is a piece of armor: {armor}.")
           armor_choices = ["Yes", "No"]
           choices = lib.select(f"Do you want to equip the {armor}?", armor_choices)
           if choices == "Yes":
               self.player.equip("armor", armor)
               self.save_game()
           else:
               console.print(f"You leave the {armor} in your inventory.")
               self.player.add_item(armor)
       elif loot_type == "Tool":
           tier_name = random.choice(list(self.weapon_tiers.keys()))
           weapon_name = random.choice(self.weapon_tiers[tier_name]["names"])
           full_tool_name = f"{tier_name} {weapon_name}"
           console.print(f"You find a hidden chest! Inside is a tool: {full_tool_name}.")
           chest_found = [
            "Yes",
            "No"
           ]
           choices = lib.select(f"Do you want to equip the {full_tool_name}?", chest_found)
           if choices == "Yes":
            self.player.equip("tool", full_tool_name)
            self.save_game()
           else:
            console.print(f"You leave the {full_tool_name} in your pack.")
            self.player.add_item(full_tool_name)
       else:
        self.player.add_item(loot_type)
        console.print(f"You find a hidden chest! Inside is 1 {loot_type}.")
       self.save_game()


   def _handle_pet_event(self):
       """Handles the event of finding a pet."""
       possible_pets = ["Void Cat", "Spectral Fox", "Tiny Dragon"]
       found_pet = random.choice(possible_pets)
       console.print(f"You hear a strange noise... A {found_pet} appears and seems to like you!")
       pet_found = [
        "Yes",
        "No"
       ]
       
       choices = lib.select(f"Do you want to equip the {found_pet} as your companion?", pet_found)
       if choices == "Yes" :
        self.player.equip("pet", found_pet)
        self.save_game()
       else:
           console.print(f"The {found_pet} scurries away into the shadows. How dare.")


   def _handle_rare_enemy_event(self):
       """Handles the event of encountering a rare enemy."""
       console.print("You sense something scrawling near...")
       self.battle(self.scale_enemy(cavern=True, rare=True), cavern=True)


   def rare_cutscene(self):
       self._display_dark_mode_cutscene_text()
       self.alt_mode = True  # Trauma mode activated


   def _display_dark_mode_cutscene_text(self):
       """Displays the text for the rare dark mode cutscene."""
       console.print("\n--- Something... Reaches... Out... ---")
       console.print("...You.")
       console.print("Why are you still here? After what you did?")
       console.print(f"  'You do not belong here, #s###...'  ")
       console.print("This is my world now. Remember when you handed it over to me ##t#?")
       console.print("You can try, but you will never leave. Not in soul, not in sight. We remember what you did, friend.")
       console.print("The world seems to shift and struggle beneath your feet... Everything feels... wrong.")


   # --- Alternate mode dialog/logic wrappers ---
   def alt_text(self, normal, alt):
       return alt if self.alt_mode else normal


   def explore(self) -> str:
       return self.exploration.explore()


   def _transition_to_act_2(self):
       
       console.print(self.alt_text(
           "\n ━─┉┈◈ Act 2: The Ruins Unveiled ◈┈┉─━",
           "\n ━─┉┈◈ Act 2: The world remembers you. Run if you must, but first they must catch you ◈┈┉─━"
       ))
       console.print(self.alt_text(
           "The villagers whisper of ancient ruins now accessible beyond the village...",
           "The wind carries tales of the past, of what was lost and what remains. You have now unlocked the <ruins>."
       ))


   def _display_shop_greeting(self):
       """Displays the appropriate greeting when entering the shop."""
       # Track if player has visited shop before
       if not hasattr(self, "_shop_visited"):
           self._shop_visited = 0
       self._shop_visited += 1
       console.print(self.alt_text(
           "\nThe shopkeeper greets you with a toothy grin.",
           "\nThe figure is cloaked in long robes, of which look tattered and worn, burned even."
       ))
       if self._shop_visited == 1:
           console.print(self.alt_text(
               "'Welcome to my humble shop! Look around, and see if anything interests you.'",
               "'You know what you need, don't waste my time.'"
           ))
       else:
           pname = self.player.name if self.player.name else "traveler"
           console.print(self.alt_text(
               f"'Ah, {pname}, back again? See anything new you'd like?'",
               f"'You again, {pname}... Were you expecting something different this time?'"
           ))


   def shop(self) -> None:
       self._display_shop_greeting()
       while True:
           console.print(f"Your gold: {self.player.coins['gold']}")
           for item, price in self.shop_prices.items():
               console.print(f"{item}: {price} gold")
           shop_menu = list(self.shop_prices.keys()) + ["Inventory", "Leave"]

           choices = lib.select("What would you like to buy?", shop_menu)
           if choices == "Leave":
               console.print(self.alt_text(
                   "'Safe travels, stranger!' the shopkeeper calls as you leave.",
                   "'Don't come back...'"
               ))
               break
           elif choices == "Inventory":
               console.print("\n━─┉┈◈ Inventory ◈┈┉─━")
               for item, qty in self.player.inventory.items():
                   console.print(f"  {item}: {qty}")
               console.print(f"Equipped Armor: {self.player.armor if self.player.armor else 'None'}")
               console.print(f"Equipped Tool: {self.player.tool if self.player.tool else 'None'}")
               console.print(f"Pet: {self.player.pet if self.player.pet else 'None'}")
               console.print(f"Lantern fuel: {self.player.lantern_fuel} turns")
           elif choices in self.shop_prices or choices.title() in self.shop_prices:
               # Handle both exact match and title case
               item_to_buy = choices if choices in self.shop_prices else choices.title()
               cost = self.shop_prices[item_to_buy]
               if self.player.can_afford(cost):
                   self.player.spend_gold(cost)
                   self.player.add_item(item_to_buy)
                   console.print(self.alt_text(
                       f"'A fine choice! One {item_to_buy} for {cost} gold.'",
                       f"'Take it. It won't help what's coming for all of us.'"
                   ))
                   self.save_game()
               else:
                   console.print(self.alt_text(
                       "'Sorry friend, you don't have enough gold for that.'",
                       "'...Lest you struggle with what you have.'"
                   ))
           else:
               console.print(self.alt_text(
                   "'I don't sell that here, friend.'",
                   "'...'"
               ))


   def developer_commands(self):
       console.print("\n━─┉┈◈ Developer Menu ◈┈┉─━")
       console.print("Commands: give [item] [qty], gold [amt], heal [amt], equip [type] [name], goto [loc], stats, craft bandage, darkmode, boss, give pet, level [amt], save, exit")
       while True:
           cmd = input("DEV> ").strip().lower()
           if cmd == "exit":
               break


           dev_actions = {
               "give": self._dev_give,
               "gold": self._dev_gold,
               "heal": self._dev_heal,
               "equip": self._dev_equip,
               "goto": self._dev_goto,
               "stats": self._dev_stats,
               "craft bandage": self._dev_craft_bandage,
               "darkmode": self._dev_darkmode,
               "boss": self._dev_boss,
               "give pet": self._dev_give_pet,
               "level": self._dev_set_level,
               "save": self._dev_save,
           }


           # Handle commands that start with a keyword
           handled = False
           for key, action_func in dev_actions.items():
               if cmd.startswith(key):
                   action_func(cmd)
                   handled = True
                   break
          
           if not handled:
               console.print("Unknown command.")


   def _dev_give(self, cmd: str):
       """Developer command to give items to the player."""
       parts = cmd.split()
       if len(parts) >= 3:
           item = parts[1].capitalize()
           try:
               qty = int(parts[2])
               self.player.add_item(item, qty)
               console.print(f"Gave {qty} {item}(s).")
           except ValueError:
               console.print("Invalid quantity.")
       else:
           console.print("Usage: give [item] [qty]")


   def _dev_gold(self, cmd: str):
       """Developer command to set the player's gold amount."""
       parts = cmd.split()
       if len(parts) == 2:
           try:
               amt = int(parts[1])
               self.player.coins["gold"] = amt
               console.print(f"Gold set to {amt}.")
           except ValueError:
               console.print("Invalid amount.")
       else:
           console.print("Usage: gold [amount]")


   def _dev_heal(self, cmd: str):
       """Developer command to heal the player."""
       parts = cmd.split()
       if len(parts) == 2:
           try:
               amt = int(parts[1])
               self.player.heal(amt)
               console.print(f"Healed {amt} HP.")
           except ValueError:
               console.print("Invalid amount.")
       else:
           console.print("Usage: heal [amount]")


   def _dev_equip(self, cmd: str):
       """Developer command to equip armor, tool, or pet."""
       parts = cmd.split()
       if len(parts) >= 3:
           item_type = parts[1].lower()
           item_name = " ".join(parts[2:]).title()
           if item_type in ["armor", "tool", "pet"]:
               self.player.equip(item_type, item_name)
           else:
               console.print("Invalid equipment type. Use 'armor', 'tool', or 'pet'.")
       else:
           console.print("Usage: equip [type] [name]")


   def _dev_goto(self, cmd: str):
       """Developer command to teleport the player to a specific location."""
       parts = cmd.split()
       if len(parts) == 2:
           loc = parts[1]
           console.print(f"Teleporting to {loc}...")
           # Directly call the location logic




           if loc == "n": self.exploration._traverse_path(self.exploration._explore_n())
           elif loc == "w": self.exploration._traverse_path(self.exploration._explore_w())
           elif loc == "e": self.exploration._traverse_path(self.exploration._explore_e())
           elif loc == "s": self.exploration._traverse_path(self.exploration._explore_s())
           elif loc == "nw": self.exploration._traverse_path(self.exploration._explore_nw())
           elif loc == "ne": self.exploration._traverse_path(self.exploration._explore_ne())
           elif loc == "sw": self.exploration._traverse_path(self.exploration._explore_sw())
           elif loc == "se": self.exploration._traverse_path(self.exploration._explore_se())
           elif loc == "village": self.exploration._explore_village()
           elif loc == "ruins": self.exploration._traverse_path(self.exploration._explore_ruins())
           elif loc == "cavern": self.exploration._explore_cavern()
           elif loc == "volcano": self.exploration._explore_volcano()
           elif loc == "back": self.exploration._explore_back()
           else: console.print("Unknown location.")
       else:
           console.print("Usage: goto [location]")


   def _dev_stats(self, cmd: str):
       """Developer command to display player statistics."""
       console.print(f"Name: {self.player.name}, HP: {self.player.hp}/{self.player.max_hp}, Level: {self.player.level}, EXP: {self.player.exp}, Gold: {self.player.coins['gold']}")
       console.print("Inventory:", self.player.inventory)
       console.print("Pet:", self.player.pet if self.player.pet else "None")
       console.print("Armor:", self.player.armor if self.player.armor else "None")
       console.print("Tool:", self.player.tool if self.player.tool else "None")
       console.print("Lantern fuel:", self.player.lantern_fuel)
       console.print("Lantern on:", "Yes" if self.player.lantern_on else "No")


   def _dev_craft_bandage(self, cmd: str):
       """Developer command to craft a bandage."""
       self._craft_bandage()


   def _dev_darkmode(self, cmd: str):
       """Developer command to toggle or activate dark mode."""
       if not self.alt_mode:
           console.print("Triggering alternate dark gamemode...")
           self.rare_cutscene()
       else:
           console.print("Dark gamemode is already active.")


   def _dev_give_pet(self, cmd: str):
       parts = cmd.split()
       if len(parts) >= 3 and parts[1].lower() == "pet":
           pet_name = " ".join(parts[2:]).title()
           self.player.equip("pet", pet_name)
           self.console.print(f"Gave you the pet: {pet_name}.")
       else:
           self.console.print("Usage: give pet [name]")


   def _dev_set_level(self, cmd: str):
       """Developer command to set the player's level."""
       parts = cmd.split()
       if len(parts) == 2:
           try:
               level = int(parts[1])
               self.player.level = level
               self.console.print(f"Player level set to {level}.")
           except ValueError:
               self.console.print("Invalid level amount.")
       else:
           self.console.print("Usage: level [amount]")


   def _dev_save(self, cmd: str):
       """Developer command to instantly save the game."""
       self.save_game()


   def village(self):
       while True:
        village_choices = [
            "Shop",
            "Inn",
            "Crafting Bench",
            "Leave"
           ]
        choices = lib.select("━─┉┈◈ You are in the town square ◈┈┉─━", village_choices)

        if choices == "Shop":
            self.shop()
        elif choices == "Inn":
            self.player.hp = self.player.max_hp
            console.print("You rest at the inn. You have successfully rested!")
            self.save_game()
        elif choices == "Crafting Bench":
            self.crafting_menu()
        elif choices == "Leave":
            console.print("You leave the village and return to the crossroads.")
            break
        else:
            console.print("Invalid choice. THIS IS AN ERROR!")
#patched bug here

   def cavern_explore(self):
       if not self._check_cavern_entry_conditions():
           return
       console.print(self.alt_text(
           "You step into the darkness, lantern held high.",
           "You step into the flesh, lantern threatening to flicker out"
       ))
       path = []
       while self.player.lantern_fuel > 0:
           self._display_cavern_status()
           move = input("Which way? (left/right/forward/back): ").strip().lower()
           if self._handle_cavern_move(path, move):
               break
           if self._handle_lantern_depletion(path):
               break
       else:
           print(self.alt_text(
               "You sense your lantern is about to die and hurry out of the cavern.",
               "The gods are cruel, yet so am I."
           ))
       self.player.lantern_on = False


   def _check_cavern_entry_conditions(self) -> bool:
       """Checks if the player meets the conditions to enter the cavern."""
       if self.player.inventory.get("Lantern", 0) == 0:
           console.print(self.alt_text(
               "It's too dark to enter the cavern without a lantern.",
               "The flesh bleeds..."
           ))
           return False
       if self.player.lantern_fuel <= 0 or not self.player.lantern_on:
           console.print(self.alt_text(
               "You need to light your lantern to enter the cavern.",
               "You need to strike a fading light before entering. The flesh it seeks."
           ))
           if self.player.lantern_fuel <= 0:
               console.print(self.alt_text(
                   "Your lantern is out of fuel. Find animal fat to refuel your lantern.",
                   "...You know what to do, A####"
               ))
               return False
           lantern_ask = [
            "Yes",
            "No"
           ]
           choices = lib.select(self.alt_text(
               "━─┉┈◈ Do you want to use your lantern? ◈┈┉─━",
               "━─┉┈◈ Will you light your lantern and face your mistakes? ◈┈┉─━"
           ), lantern_ask)
           if choices == "Yes":
            self.player.use_lantern()
            return True
           if choices == "No":
            console.print(self.alt_text(
                "You decide not to enter the cavern.",
                "You hesitate. The flesh does not."
                ))
            return False
       return True


   def _display_cavern_status(self):
       """Displays the current lantern fuel and processes player debuffs in the cavern."""
       console.print(self.alt_text(
           f"\nLantern fuel remaining: {self.player.lantern_fuel} turns.",
           f"\nLantern fuel: {self.player.lantern_fuel} flickers left."
       ))
       self.player.process_debuffs()


   def _handle_cavern_move(self, path: list, move: str) -> bool:
       """Handles player movement within the cavern, including 'back' and random events."""
       if move == "back":
           if path:
               console.print(self.alt_text(
                   "You retrace your steps...",
                   "You try to retrace your steps, but the walls shift strangely."
               ))
               path.pop()
               if not path:
                   console.print(self.alt_text(
                       "You have escaped the cavern safely!",
                       "The flesh whispers your name, beckoning you where you belong."
                   ))
                   return True  # Player escaped
           else:
               console.print(self.alt_text(
                   "You are at the entrance and leave the cavern.",
                   "You step into the shadows, leaving the teeth behind."
               ))
               return True  # Player escaped
       elif move in ("left", "right", "forward"):
           path.append(move)
           # 60% chance for enemy, 10% for chest, 10% for nothing, 20% for flavor
           event_roll = random.random()
           if event_roll < 0.6:
               battle_result = self.battle(self.scale_enemy(cavern=True), cavern=True)
               if battle_result in ["lost_boss", "lost_normal"]:
                   return battle_result
           elif event_roll < 0.7:
               self.random_event()
           elif event_roll < 0.8:
               console.print(self.alt_text(
                   "You find a strange marking on the wall.",
                   "You find a symbol, drawn in something that glistens in red."
               ))
           else:
               console.print(self.alt_text(
                   "The darkness presses in, but your lantern keeps it at bay.",
                   "The shadows peer at you from all directions, but your light keeps you from seeing them for what they are..."
               ))
       else:
           console.print(self.alt_text(
           "You hesitate, unsure which way to go.",
           "You hesitate. The flesh does not."
       ))
       return False  # Player did not escape


   def _handle_lantern_depletion(self, path: list) -> bool:
       """Handles the depletion of lantern fuel and consequences of getting lost in the cavern."""
       self.player.lantern_fuel -= 1
       if self.player.lantern_fuel <= 0:
           console.print(self.alt_text(
               "Your lantern flickers and goes out!",
               "Your lantern dies. The darkness closes in."
           ))
           if path: # If path is not empty, means player is lost inside
               console.print(self.alt_text(
                   "Lost in the darkness, you stumble and collapse...",
                   "You see those that you once knew, You see their faces at last..."
               ))
               console.print(self.alt_text(
                   "You awaken at your last save point, shaken but alive.",
                   "You awaken in the last you remembered, they are angry."
               ))
               return "lost_normal"
           self.player.lantern_on = False # Ensure lantern is off
           return True # Indicate that the loop should break
       return False # Indicate that the loop should continue




if __name__ == "__main__":
    game = Game()
    console.print("Version 1.2 (THIS IS AN SOMEWHAT UNSTABLE ALPHA BUILD! For developers and beta testers ONLY!")
    lib.slow_type_font_color("Magenta", "Fancy", 'Welcome to Voidfallen! A game by yours truly. -Moogietheboogie✦✦✦')

    menu_choices = [
        "✦Start a new game✦",
        "✦Load a saved game✦",
        "✦Export player data✦",
        "✦Options✦",
        "✦Exit✦",
    ]

    while True:
        choices = lib.select("━─┉┈◈ Main Menu ◈┈┉─━", menu_choices)
        if choices == "✦Start a new game✦":
            intro_skip = [
                "Yes",
                "No"
            ]
            intro_choice = lib.select("━─┉┈◈ Would you like to skip the intro dialoge ? ◈┈┉─━", intro_skip)

            if intro_choice == "Yes":
                # Reset player to default and skip intro
                game.player = Player(game.console)
                # Prompt for username
                game.player.name = input("Enter your name:").strip()
                if not game.player.name:
                    game.player.name = "✦Traveler✦"
                if game.player.name.lower() == "moogietheboogie":
                    game.developer_mode = True
                    lib.slow_type_font_color("Magenta", "Fancy", "✩✩✩Developer mode activated! Welcome back #001 ✩✩✩")
                console.print(f"Welcome, {game.player.name}. Your journey begins...")
                result = game.explore()
                if result in ["lost_boss", "lost_normal"]:
                    continue
            elif intro_choice == "No":
                game.new_intro()
                result = game.explore()
                if result in ["lost_boss", "lost_normal"]:
                    continue
        elif choices == "✦Load a saved game✦":
            if game.load_game():
                result = game.explore()
                if result in ["lost_boss", "lost_normal"]:
                    continue
        elif choices == "✦Export player data✦":
            game.export_player_data()
        elif choices == "✦Options✦":
            options(game)
        elif choices == "✦Exit✦":
            lib.slow_type_font_color("Magenta", "Fancy", "·̩̩̥͙＊*•̩̩͙✩•̩̩͙*˚Thank you for playing Voidfallen˚*•̩̩͙✩•̩̩͙*˚＊·̩̩̥͙")
            break
        else:
            console.print("THERE WAS AN ERROR HERE! please flag to github")


def options(game: Game):
    lib.slow_type_font_color("Blue", "Fancy", "━─┉┈◈◉◈┈┉─━")
    while True:
        options_choices = [
            "Music",
            "Difficulty",
            "Colorization",
            "Fonts",
            "Exit"
        ]

        choices = lib.select("━─┉┈◈◉◈┈┉─━", options_choices)

        if choices == "Music":
            while True:
                lib.slow_type("⭒☆━━━━━━━━━━━━━━━☆⭒")  # placeholder for slider
                music_menu_choices = [
                    "Sound effects",
                    "BGM",
                    "Exit"
                ]
                music_choice = lib.select("━─┉┈◈◉◈┈┉─━", music_menu_choices)

                if music_choice == "Exit":
                    break
                elif music_choice == "Sound effects":
                    lib.slow_type_font_color("Blue", "Bold", "Sound effects are now off(note, this does nothing as of now)")
                elif music_choice == "BGM":
                    lib.slow_type_font_color("Blue", "Bold", "BGM is now off")
        elif choices == "Difficulty":
            game.set_difficulty()

        # placeholder here

        elif choices == "Exit":
            break





