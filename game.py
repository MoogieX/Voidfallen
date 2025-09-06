import json
import os
import random
from typing import Dict
from rich.console import Console

from exploration import Exploration

SAVE_FILE = "save.json"
console = Console()


def ask_yes_no(prompt: str) -> bool:
    """Prompt the player for a yes/no answer and return True for yes."""
    while True:
        resp = input(f"{prompt} (yes/no) ").strip().lower()
        if resp in ("yes", "y"):
            return True
        if resp in ("no", "n"):
            return False
        console.print("Please answer yes or no.")


from player import Player
from battle import Battle, AzraelBattle


class Game:
    def __init__(self):
        random.seed()
        self.console = console
        self.player = Player(self.console)

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
            console.print(f"❌ Error saving game: {e}. Check file permissions or disk space.")
        except Exception as e:
            console.print(f"❌ An unexpected error occurred while saving: {e}")

    def load_game(self) -> bool:
        """Loads the game state from a JSON save file."""
        if not os.path.exists(SAVE_FILE):
            console.print("⚠ No save file found.")
            return False
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
            self.player.from_dict(data)
            console.print("✅ Game loaded successfully!")
            return True
        except (IOError, OSError) as e:
            console.print(f"❌ Error reading save file: {e}. The file might be corrupted or inaccessible.")
            return False
        except json.JSONDecodeError as e:
            console.print(f"❌ Error decoding save file: {e}. The save file is corrupted.")
            return False
        except Exception as e:
            console.print(f"❌ An unexpected error occurred while loading: {e}")
            return False

    def export_player_data(self) -> None:
        """Exports the current player data to a JSON file."""
        export_file = "player_export.json"
        try:
            with open(export_file, "w") as f:
                json.dump(self.player.to_dict(), f, indent=2)
            console.print(f"Player data exported to {export_file}!")
        except (IOError, OSError) as e:
            console.print(f"❌ Error exporting player data: {e}. Check file permissions or disk space.")
        except Exception as e:
            console.print(f"❌ An unexpected error occurred while exporting: {e}")

    # --------------------
    # Game Flow
    # --------------------
    def intro(self) -> None:
        if self.player.name == "Astar":
            self._astar_intro()
            return

        self.player.name = input("Hello lost one, what is your name? ").strip()
        if self.player.name.lower() == "moogietheboogie":
            self.developer_mode = True
            console.print("✨ Developer mode activated! Welcome back #001 ✨")
        console.print(f"Interesting name you have... {self.player.name}")

        self.player.backstory = input(
            "'Where did you come from? This must be a blessing for my calls for... Nevermind'"
            "'Tis' not often we have visitors here in this sect of the void.'"
        ).strip()
        console.print(
            f"Ah... {self.player.backstory}. It is a place I am yet to visit, though it is much beautiful from what I hear."
            f"You must have come a long way from there, {self.player.name}... Do you ever plan to go home?"
        )

        if ask_yes_no("'Care to sit down with me? Surely you must be frazzled after such a journey'"):
            console.print("'Very well then.' The figure moves aside for you to join them")
        else:
            console.print("'That's alright, just stay to talk, if you will.'")

        if ask_yes_no(f"Say, {self.player.name}, have you heard what has been happening here"):
            console.print(
                "So you are aware, how peculiar... Then, "
                f"{self.player.name}, there is an old trail up to the East. "
                "You may find an inn where you can stay."
            )
        else:
            console.print(
                "Not that I would have expected you to. "
                "There are creatures from the north, they have been encroaching on our void... "
                "Slaughtering the residents."
            )

        console.print("\nYou leave the clearing after giving thanks to the figure, onwards you shall go...\n")

    def _astar_intro(self):
        console.print("\n--- A New Beginning ---")
        console.print("You awaken with a gasp, the memories of your defeat still fresh.")
        console.print("But you are not in the volcano. You are somewhere else... somewhere familiar.")
        console.print("A figure stands before you, the same one from the clearing.")
        console.print("'So, you have returned,' the figure says, their voice a low hum.")
        console.print("'Astar... a name I have not heard in a long time.'")
        console.print("'The demon thought it had claimed you, but I have given you another chance.'")
        console.print("'Your journey is far from over. The world needs you.'")
        console.print("'Go now, and fulfill your destiny.'")

    def _create_astar_save(self):
        astar_data = {
            "name": "Astar",
            "backstory": "A forgotten soul, given a second chance.",
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
            console.print(f"❌ Error creating Astar save: {e}.")

    def _dev_boss(self, cmd: str):
        parts = cmd.split()
        boss_name = " ".join(parts[1:]).title() if len(parts) > 1 else None

        if boss_name:
            # Create a generic boss with high stats for testing
            boss = {"name": boss_name, "hp": 500, "attack": 50, "boss": True}
            self.console.print(f"Spawning custom boss: {boss_name}")
        elif self.alt_mode:
            boss = {"name": "Azrael, the Unyielding", "hp": 9999, "attack": 999, "boss": True}
            self.console.print("Spawning Azrael, the Unyielding.")
        else:
            boss = {"name": "Ancient Dragon", "hp": 300, "attack": 30, "boss": True}
            self.console.print("Spawning Ancient Dragon.")
        
        self.battle(boss)

    def set_difficulty(self):
        console.print("\nChoose a difficulty: easy, normal, hard")
        while True:
            choice = input("Type difficulty: ").strip().lower()
            if choice == "easy":
                self.difficulty = "easy"
                console.print("Difficulty set to Easy.")
                break
            elif choice == "normal":
                self.difficulty = "normal"
                console.print("Difficulty set to Normal.")
                break
            elif choice == "hard":
                self.difficulty = "hard"
                console.print("Difficulty set to Hard.")
                break
            else:
                console.print("Invalid choice. Type: easy, normal, or hard.")

    def scale_enemy(self, act=None, cavern=False, rare=False, volcano=False) -> Dict[str, int]:
        lvl = self.player.level
        # Alternate mode: completely new enemy pools
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
                    "Guarded Soul", "The Forgotten", "Hollow Priest", "Bleeding Idol", "The Feasting"
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
            console.print(f"You defeated the {enemy['name']} and gained 10 EXP!")
            self.player.gain_exp(10)
            battle_instance.handle_drops()
            self.save_game()
            # Only show crafting menu if NOT in cavern
            if not cavern:
                self.crafting_menu()
        elif result == "lost":
            if enemy.get("boss"):
                self._create_astar_save()
                console.print("You have been defeated... but your journey is not over.")
                exit()
            else:
                console.print("You have fallen in battle...")
                exit()
        elif result == "enemy_fled":
            # Message is handled in the Battle class, no further action needed.
            pass
        # If "fled" (player fled), no further action is needed here.
        return result

    # Crafting menu
    def crafting_menu(self):
        console.print("\n--- Crafting Menu ---")
        console.print("Options: bandage, exit")
        while True:
            choice = input("Type your choice: ").strip().lower()
            if choice == "bandage":
                self._craft_bandage()
            elif choice == "exit":
                console.print("Exiting crafting menu.")
                break
            else:
                console.print("Invalid choice. Type 'bandage' or 'exit'.")

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

        # 2% chance: find a pet
        events.append({"chance": 0.10, "handler": self._handle_pet_event})

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
            if ask_yes_no(f"Do you want to equip the {armor}?"):
                self.player.equip("armor", armor)
                self.save_game()
            else:
                console.print(f"You leave the {armor} in your pack.")
                self.player.add_item(armor)
        elif loot_type == "Tool":
            tool_base_name = random.choice(["Rusty Pickaxe", "Enchanted Lantern", "Ancient Key"])
            tier_name = random.choice(list(self.weapon_tiers.keys()))
            full_tool_name = f"{tier_name} {tool_base_name}"
            console.print(f"You find a hidden chest! Inside is a tool: {full_tool_name}.")
            if ask_yes_no(f"Do you want to equip the {full_tool_name}?"):
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
        if ask_yes_no(f"Do you want to equip the {found_pet} as your companion?"):
            self.player.equip("pet", found_pet)
            self.save_game()
        else:
            console.print(f"The {found_pet} scurries away into the shadows.")

    def _handle_rare_enemy_event(self):
        """Handles the event of encountering a rare enemy."""
        console.print("You sense something scrawling near...")
        self.battle(self.scale_enemy(cavern=True, rare=True), cavern=True)

    def rare_cutscene(self):
        self._display_dark_mode_cutscene_text()
        self.alt_mode = True  # Activate alternate mode

    def _display_dark_mode_cutscene_text(self):
        """Displays the text for the rare dark mode cutscene."""
        console.print("\n--- Something... Reaches... Out... ---")
        console.print("...You.")
        console.print("Why are you still here? After what you did?")
        console.print(f"  'You do not belong here, #s###...'  ")
        console.print("This is my world now. Remember when you handed it over to me ####?")
        console.print("You can try, but you will never leave. Not in soul, not in sight. We remember what you did, friend.")
        console.print("The world seems to shift and struggle beneath your feet... Everything feels... wrong.")

    # --- Alternate mode dialog/logic wrappers ---
    def alt_text(self, normal, alt):
        return alt if self.alt_mode else normal

    def explore(self) -> None:
        self.exploration.explore()

    def _transition_to_act_2(self):
        """Handles the transition to Act 2 of the game."""

        console.print(self.alt_text(
            "\n--- Act 2: The Ruins Unveiled ---",
            "\n--- Act 2: The world remembers you. Run if you must, but first they must catch you. ---"
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
                "'You know what you need.'"
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
            console.print("Type the item name to buy it, 'inventory' to view your items, or 'leave' to exit.")

            choice = input("Buy what? ").strip().title()
            if choice == "Leave":
                console.print(self.alt_text(
                    "'Safe travels, stranger!' the shopkeeper calls as you leave.",
                    "'Don't come back...'"
                ))
                break
            elif choice == "Inventory":
                console.print("Your inventory:")
                for item, qty in self.player.inventory.items():
                    console.print(f"  {item}: {qty}")
                console.print(f"Equipped Armor: {self.player.armor if self.player.armor else 'None'}")
                console.print(f"Equipped Tool: {self.player.tool if self.player.tool else 'None'}")
                console.print(f"Pet: {self.player.pet if self.player.pet else 'None'}")
                console.print(f"Lantern fuel: {self.player.lantern_fuel} turns")
            elif choice in self.shop_prices:
                cost = self.shop_prices[choice]
                if self.player.can_afford(cost):
                    self.player.spend_gold(cost)
                    self.player.add_item(choice)
                    console.print(self.alt_text(
                        f"'A fine choice! One {choice} for {cost} gold.'",
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
        console.print("\n--- Developer Commands ---")
        console.print("Commands: give [item] [qty], gold [amt], heal [amt], equip [type] [name], goto [loc], stats, craft bandage, darkmode, exit")
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

    def village(self):
        while True:
            console.print("\nYou are in the village square. What would you like to do?")
            console.print("Options: shop, rest, craft, leave")
            choice = input("Type your choice: ").strip().lower()
            if choice == "shop":
                self.shop()
            elif choice == "rest":
                self.player.hp = self.player.max_hp
                console.print("You rest at the inn. You have successfully rested!")
                self.save_game()
            elif choice == "craft":
                self.crafting_menu()
            elif choice == "leave":
                console.print("You leave the village and return to the crossroads.")
                break
            else:
                console.print("Invalid choice.")

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
            if ask_yes_no(self.alt_text(
                "Do you want to use your lantern?",
                "Will you light your lantern and face your mistakes?"
            )):
                self.player.use_lantern()
                return True
            else:
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
                self.battle(self.scale_enemy(cavern=True), cavern=True)
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
                self.load_game()
            self.player.lantern_on = False # Ensure lantern is off
            return True # Indicate that the loop should break
        return False # Indicate that the loop should continue


if __name__ == "__main__":
    game = Game()
    console.print("Welcome to Voidfallen! A game by yours truly. -Moogietheboogie")
    console.print("\nMain Menu Options:")
    console.print("  Start a new game")
    console.print("  Load a saved game")
    console.print("  Export player data")
    console.print("  Options- game difficulty")
    console.print("  Exit the game")
    while True:
        console.print("\nWhat would you like to do? (new game, load game, export data, options, quit)")
        choice = input("Type your choice: ").strip().lower()
        if choice == "new" or "new game" in choice:
            skip = ask_yes_no("Would you like to skip the intro dialog?")
            if skip:
                # Reset player to default and skip intro
                game.player = Player()
                # Prompt for username
                game.player.name = input("Enter your name, lost one: ").strip()
                if not game.player.name:
                    game.player.name = "traveler"
                if game.player.name.lower() == "moogietheboogie":
                    game.developer_mode = True
                    print("✨ Developer mode activated! Welcome back #001 ✨")
                console.print(f"Welcome, {game.player.name}. Your journey begins...")
            else:
                game.intro()
            game.explore()
            break
        elif choice == "load" or "load game" in choice:
            if game.load_game():
                game.explore()
                break
        elif choice == "export" or "export data" in choice:
            game.export_player_data()
        elif choice == "options":
            game.set_difficulty()
        elif choice == "quit" or "exit" in choice:
            console.print("Thanks for playing the demo!")
            break
        else:
            console.print("Invalid choice")