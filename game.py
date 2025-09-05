import json
import os
import random
from typing import Dict
from rich.console import Console

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


class Player:
    def __init__(self):
        self.name: str = ""
        self.backstory: str = ""
        self.hp: int = 100
        self.max_hp: int = 100
        self.exp: int = 0
        self.level: int = 1
        self.attack: int = 10
        self.inventory: Dict[str, int] = {"Potion": 2}
        self.coins: Dict[str, int] = {"gold": 10, "silver": 0, "bronze": 0, "zinc": 0}
        self.unlocked_rest: bool = False
        self.pet: str = None  # New: equipped pet
        self.armor: str = None  # equipped armor
        self.tool: str = None   # equipped tool
        self.lantern_on: bool = False
        self.lantern_fuel: int = 0
        self.poison_turns: int = 0
        self.bleed_turns: int = 0

    def to_dict(self) -> dict:
        """Converts the Player object's attributes to a dictionary for serialization."""
        return {
            "name": self.name,
            "backstory": self.backstory,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "exp": self.exp,
            "level": self.level,
            "attack": self.attack,
            "inventory": self.inventory,
            "coins": self.coins,
            "unlocked_rest": self.unlocked_rest,
            "pet": self.pet,
            "armor": self.armor,
            "tool": self.tool,
            "lantern_on": self.lantern_on,
            "lantern_fuel": self.lantern_fuel,
            "poison_turns": self.poison_turns,
            "bleed_turns": self.bleed_turns,
        }

    def from_dict(self, data: dict):
        """Loads player attributes from a dictionary, typically from a deserialized save file."""
        self.name = data.get("name", "")
        self.backstory = data.get("backstory", "")
        self.hp = data.get("hp", 100)
        self.max_hp = data.get("max_hp", 100)
        self.exp = data.get("exp", 0)
        self.level = data.get("level", 1)
        self.attack = data.get("attack", 10)
        self.inventory = data.get("inventory", {"Potion": 2})
        self.coins = data.get("coins", {"gold": 10, "silver": 0, "bronze": 0, "zinc": 0})
        self.unlocked_rest = data.get("unlocked_rest", False)
        self.pet = data.get("pet")
        self.armor = data.get("armor")
        self.tool = data.get("tool")
        self.lantern_on = data.get("lantern_on", False)
        self.lantern_fuel = data.get("lantern_fuel", 0)
        self.poison_turns = data.get("poison_turns", 0)
        self.bleed_turns = data.get("bleed_turns", 0)

        # Ensure lantern fuel is set if player has a lantern but no fuel
        if self.inventory.get("Lantern", 0) > 0 and self.lantern_fuel == 0:
            self.lantern_fuel = 6

    def take_damage(self, amount: int) -> None:
        self.hp = max(self.hp - amount, 0)

    def heal(self, amount: int) -> None:
        self.hp = min(self.hp + amount, self.max_hp)

    def add_item(self, name: str, qty: int = 1) -> None:
        self.inventory[name] = self.inventory.get(name, 0) + qty
        # Auto-fuel lantern when first acquired
        if name.lower() == "lantern" and self.lantern_fuel == 0:
            self.lantern_fuel = 6  # Base fuel value
            console.print("Your lantern is now fueled and ready to use! (6 turns of fuel)")

    def can_afford(self, cost: int) -> bool:
        return self.coins["gold"] >= cost

    def spend_gold(self, amount: int) -> None:
        self.coins["gold"] -= amount

    def gain_exp(self, amount: int) -> None:
        self.exp += amount
        self._try_level_up()

    def _try_level_up(self) -> None:
        while self.exp >= self.level * 20:
            self.exp -= self.level * 20
            self.level += 1
            self.max_hp += 20
            self.attack += 5
            self.hp = self.max_hp
            console.print(f"You leveled up! You are now level {self.level}.")

    def equip(self, item_type: str, item_name: str):
        """Equips an item of a specific type to the player."""
        if hasattr(self, item_type):
            setattr(self, item_type, item_name)
            console.print(f"You have equipped {item_name} as your {item_type}!")
        else:
            console.print(f"Cannot equip {item_name}. Invalid item type: {item_type}.")

    def use_lantern(self):
        if self.inventory.get("Lantern", 0) > 0 and self.lantern_fuel > 0:
            self.lantern_on = True
            console.print("You light your lantern. The darkness recedes.")
        elif self.inventory.get("Lantern", 0) > 0:
            console.print("Your lantern is out of fuel!")
            self.lantern_on = False
        else:
            console.print("You don't have a lantern.")
            self.lantern_on = False

    def refuel_lantern(self, fat_units: int):
        self.lantern_fuel += fat_units
        console.print(f"You refuel your lantern with {fat_units} animal fat. Lantern fuel: {self.lantern_fuel} turns.")

    def apply_poison(self, turns=2):
        self.poison_turns = turns
        console.print("You have been poisoned! You will lose 1 HP for the next 2 turns.")

    def apply_bleed(self, turns=2):
        self.bleed_turns = turns
        console.print("You are bleeding! You will lose 2 HP for the next 2 turns.")

    def process_debuffs(self):
        if self.poison_turns > 0:
            self.take_damage(1)
            self.poison_turns -= 1
            console.print("Poison deals 1 damage to you!")
        if self.bleed_turns > 0:
            self.take_damage(2)
            self.bleed_turns -= 1
            console.print("Bleeding deals 2 damage to you!")

    def get_current_attack(self, game_instance) -> int:
        base_attack = self.attack
        if self.tool:
            # Parse tier from tool name (e.g., "Common Rusty Pickaxe")
            parts = self.tool.split(" ", 1)
            if len(parts) > 1 and parts[0] in game_instance.weapon_tiers:
                tier_name = parts[0]
                tier_bonus = game_instance.weapon_tiers[tier_name]["bonus"]
                base_attack += tier_bonus
        return base_attack


class Game:
    def __init__(self):
        random.seed()
        self.player = Player()
        self.shop_prices = {"Potion": 5, "Lantern": 3, "Bandage": 4}
        self.developer_mode = False  # Track if dev mode is enabled
        self.act = 1  # 1 = Act 1, 2 = Act 2
        self.difficulty = "normal"  # "easy", "normal", "hard"
        self.alt_mode = False  # New: alternate game mode flag
        self.weapon_tiers = {
            "Common": {"bonus": 0, "color": "white"},
            "Uncommon": {"bonus": 2, "color": "green"},
            "Rare": {"bonus": 5, "color": "blue"},
            "Epic": {"bonus": 10, "color": "purple"},
            "Legendary": {"bonus": 20, "color": "yellow"},
        }

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
        self.player.name = input("Hello lost one, what is your name? ").strip()
        if self.player.name.lower() == "moogie":
            self.developer_mode = True
            console.print("✨ Developer mode activated! Welcome back #001 ✨")
        console.print(f"Interesting name you have... {self.player.name}")

        self.player.backstory = input(
            "Where do you come from? "
            "Not often we have visitors here in this sect of the void. "
        ).strip()
        console.print(
            f"Ah... {self.player.backstory}. "
            f"You must have come a long way from there, {self.player.name}."
        )

        if ask_yes_no("Care to sit down with me? Surely you must be frazzled"):
            console.print("Very well then. *The figure moves aside for you to sit beside them*")
        else:
            console.print("That's alright, just stay to talk, if you will.")

        if ask_yes_no(f"Say, {self.player.name}, have you heard what has been happening here"):
            console.print(
                "So you are aware, how peculiar... Then, "
                f"{self.player.name}, there is an old trail up to the north. "
                "You may find an inn where you can stay."
            )
        else:
            console.print(
                "Not that I would have expected you to. "
                "There are creatures from the north, they have been encroaching on our void... "
                "Slaughtering the residents."
            )

        console.print("\nYou leave the clearing after giving thanks to the figure, onwards you shall go...\n")

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

    def scale_enemy(self, act=None, cavern=False, rare=False) -> Dict[str, int]:
        lvl = self.player.level
        # Alternate mode: completely new enemy pools
        if self.alt_mode:
            if cavern or rare:
                enemy_list = [
                    "Shambling Husk", "The Watcher", "Flesh Moth", "Echoing Maw", "..."
                ]
                base_hp = 18
                base_attack = 7
                hp_scale = 6
                atk_scale = 3
            elif act == 2 or (act is None and self.act == 2):
                enemy_list = [
                    "Remnant", "The Forgotten", "Hollow Priest", "Bleeding Idol", "The Hunger"
                ]
                base_hp = 50
                base_attack = 18
                hp_scale = 22
                atk_scale = 7
            else:
                enemy_list = [
                    "Lost Shade", "Broken Doll", "Wailing Child", "Crawling Grin"
                ]
                base_hp = 28
                base_attack = 9
                hp_scale = 13
                atk_scale = 4
        else:
            # Cavern or rare enemies
            if cavern or rare:
                enemy_list = ["Bat", "Giant Bat", "Blind Lizard", "Cave Snake", "Cave Spider", "Ghost"]
                base_hp = 12
                base_attack = 4
                hp_scale = 4
                atk_scale = 2
            # Act 2 overworld enemies
            elif act == 2 or (act is None and self.act == 2):
                enemy_list = ["Wraith", "Voidspawn", "Corrupted Knight", "Specter", "Abyssal Beast"]
                base_hp = 40
                base_attack = 12
                hp_scale = 18
                atk_scale = 5
            # Act 1 enemies
            else:
                enemy_list = ["Goblin", "Shade", "Bandit", "Wolf"]
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

    def battle(self, enemy: Dict[str, int], cavern=False) -> None:
        console.print(f"A wild {enemy['name']} appears!")
        poison_inflictors = ["snake", "spider"]
        bleed_inflictors = ["bat"]
        silk_droppers = ["spider"]
        animal_fat_droppers = ["bat"]
        ghost_lifesteal = ["ghost"]
        # Add "moth" as a silk dropper in dark cavern mode
        if self.alt_mode and cavern:
            silk_droppers = ["spider", "moth"]
        # Remove unused variables: enemy_bleed, enemy_poison
        while enemy["hp"] > 0 and self.player.hp > 0:
            self.player.process_debuffs()
            console.print(f"\nYour HP: {self.player.hp}/{self.player.max_hp} | Enemy HP: {enemy['hp']} ")
            action = input("Do you (attack/use item/run)? ").strip().lower()
            if action == "attack":
                dmg = self.player.get_current_attack(self) + random.randint(0, 4)
                enemy["hp"] -= dmg
                console.print(f"You strike the {enemy['name']} for {dmg} damage!")
                # Bleed lifesteal for bats and ghosts
                # Only heal if enemy is still alive after attack and not dead from this hit
                if enemy["hp"] > 0 and any(e in enemy["name"].lower() for e in bleed_inflictors + ghost_lifesteal) and self.player.bleed_turns > 0:
                    heal = 2
                    enemy["hp"] += heal
                    console.print(f"{enemy['name']} absorbs {heal} HP from your bleeding!")
            elif action == "use item":
                if self.player.inventory.get("Potion", 0) > 0:
                    heal_amount = 30
                    self.player.heal(heal_amount)
                    self.player.inventory["Potion"] -= 1
                    console.print(f"You drink a potion and restore {heal_amount} HP.")
                elif cavern and self.player.inventory.get("Animal Fat", 0) > 0:
                    self.player.inventory["Animal Fat"] -= 1
                    self.player.refuel_lantern(3)
                elif self.player.inventory.get("Bandage", 0) > 0:
                    self.player.inventory["Bandage"] -= 1
                    self.player.poison_turns = 0
                    self.player.bleed_turns = 0
                    console.print("You use a bandage and cure all bleeding and poison effects!")
                else:
                    console.print("You have no usable items!")
            elif action == "run":
                if random.random() < 0.5:
                    console.print("You escaped successfully!")
                    return
                console.print("You failed to escape!")
            else:
                console.print("Invalid action.")
                continue
            if enemy["hp"] > 0:
                dmg = enemy["attack"] + random.randint(0, 3)
                self.player.take_damage(dmg)
                console.print(f"The {enemy['name']} hits you for {dmg} damage!")
                # 25% chance to inflict poison or bleed
                if any(e in enemy["name"].lower() for e in poison_inflictors) and random.random() < 0.25:
                    self.player.apply_poison()
                if any(e in enemy["name"].lower() for e in bleed_inflictors) and random.random() < 0.25:
                    self.player.apply_bleed()
        if self.player.hp <= 0:
            console.print("You have fallen in battle...")
            exit()
        console.print(f"You defeated the {enemy['name']} and gained 10 EXP!")
        self.player.gain_exp(10)
        # Drops
        if any(e in enemy["name"].lower() for e in animal_fat_droppers):
            console.print("You collect animal fat from the bat's remains.")
            self.player.add_item("Animal Fat")
        if any(e in enemy["name"].lower() for e in silk_droppers):
            console.print("You collect silk from the remains.")
            self.player.add_item("Silk")
        self.save_game()
        # Only show crafting menu if NOT in cavern
        if not cavern:
            self.crafting_menu()

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
        console.print("You sense something unnatural...")
        self.battle(self.scale_enemy(cavern=True, rare=True), cavern=True)

    def rare_cutscene(self):
        self._display_dark_mode_cutscene_text()
        self.alt_mode = True  # Activate alternate mode

    def _display_dark_mode_cutscene_text(self):
        """Displays the text for the rare dark mode cutscene."""
        console.print("\n--- Something Unsettling Occurs ---")
        console.print("...You return to that place.")
        console.print("Why are you still here? After what you did?")
        console.print(f"  'You do not belong here, {self.player.name if self.player.name else 'traveler'}...'")
        console.print("This is my world now. Remember when you handed it over to me?")
        console.print("You can try, but you will never leave. Not in soul, not in sight. We remember what you did, friend.")
        console.print("--- Why. Did. They. Have. To. Remember. ---")
        console.print("The world seems to shift. Everything feels... wrong.")

    # --- Alternate mode dialog/logic wrappers ---
    def alt_text(self, normal, alt):
        return alt if self.alt_mode else normal

    def explore(self) -> None:
        while True:
            console.print(self.alt_text(
                "\nYou stand at a crossroads. Where will you go?",
                "\nYou stand at the fracture. Where will you wander?"
            ))
            console.print(self.alt_text(
                "North: The trail towards the cabin and beyond.",
                "North: The path to where it came from."
            ))
            console.print(self.alt_text(
                "West: Dark woods filled with strange sounds.",
                "West: The woods, now silent in your presence."
            ))
            console.print(self.alt_text(
                "East: A path toward the old stone.",
                "East: The stone, cracked and bleeding. The very ground seeming to reject you."
            ))
            if self.act == 1:
                console.print(self.alt_text(
                    "Village: A settlement where you may rest and trade.",
                    "Village: The burned remains of a once-thriving community. The air is thick with ash."
                ))
            if self.act == 2:
                console.print(self.alt_text(
                    "Ruins: The forbidden ruins, now revealed beyond the village.",
                    "Ruins: The ruins, crawling with things that remember."
                ))
                console.print(self.alt_text(
                    "Cavern: A dark cavern mouth gapes in the hillside.",
                    "Cavern: The flesh, it feeds."
                ))
            console.print(self.alt_text(
                "Craft: Craft items from your materials.",
                "Craft: Stitch together what you can."
            ))
            console.print(self.alt_text(
                "Back: Return to the clearing.",
                "Back: Return to the place you were reborn."
            ))
            if self.developer_mode:
                console.print("[DEV] Type 'dev' for developer commands.")

            choice = input("Choose a direction: ").strip().lower()

            explore_actions = {
                "dev": self.developer_commands,
                "craft": self.crafting_menu,
                "north": self._explore_north,
                "west": self._explore_west,
                "east": self._explore_east,
                "village": self._explore_village,
                "ruins": self._explore_ruins,
                "cavern": self._explore_cavern,
                "back": self._explore_back,
            }

            action = explore_actions.get(choice)
            if action:
                action()
            else:
                print(self.alt_text(
                    "Invalid choice.",
                    "A door forever shut, you may not return."
                ))

    def _explore_north(self):
        """Handles the player's action when choosing to go North."""
        console.print(self.alt_text(
            "You walk north. The air grows colder as you approach a lonely cabin, its windows dark and silent.",
            "You walk north... An abandoned cabin stands, the ground still bloody from that night."
        ))
        if ask_yes_no(self.alt_text(
            "You find a small cabin. Do you enter?",
            "You find the house that once belonged to you. Do you step inside?"
        )):
            console.print(self.alt_text(
                "Inside the cabin, you find a lantern. +1 Lantern",
                "Inside, you find a flickering lantern. +1 Lantern"
            ))
            self.player.add_item("Lantern")
            self.save_game()
        else:
            console.print(self.alt_text(
                "You decide not to enter. The cabin looms silently.",
                "You decide to turn away from the past."
            ))
        if not self.random_event():
            if random.random() < 0.3:
                self.battle(self.scale_enemy())

    def _explore_west(self):
        """Handles the player's action when choosing to go West."""
        console.print(self.alt_text(
            "You head west into the dark woods. The trees are twisted, and strange sounds echo between them.",
            "You head west. The obelisks, once trees, now stand as silent sentinels."
        ))
        console.print(self.alt_text(
            "A silhouette emerges from the shadows!",
            "A shape, familiar and wrong."
        ))
        if not self.random_event():
            if self.act == 2 and random.random() < 0.1:
                self.battle(self.scale_enemy(cavern=True), cavern=True)
            else:
                self.battle(self.scale_enemy())

    def _explore_east(self):
        """Handles the player's action when choosing to go East."""
        console.print(self.alt_text(
            "You follow the path east. An ancient stone stands here, humming with strange energy.",
            "You follow the path east. The stone sits there, shattered as if hit by a force beyond humanity. It is weak."
        ))
        if not self.random_event():
            if random.random() < 0.5:
                if self.act == 2 and random.random() < 0.1:
                    self.battle(self.scale_enemy(cavern=True), cavern=True)
                else:
                    self.battle(self.scale_enemy())
            else:
                console.print(self.alt_text(
                    "You feel a chill as you touch the stone, but nothing else happens.",
                    "You touch the egg. It feels warm, and something inside it moves."
                ))

    def _explore_village(self):
        """Handles the player's action when choosing to go to the Village."""
        if self.act == 1:
            console.print(self.alt_text(
                "You arrive at a small village. Lanterns flicker in the dusk, and villagers eye you warily.",
                "You arrive at the empty village. Lanterns flicker, but no one is there."
            ))
            console.print(self.alt_text(
                "A shopkeeper waves you over: 'Looking for supplies, traveler?'",
                "A figure stands in the shop, face hidden. 'Looking for something you shattered?'"
            ))
            self.player.unlocked_rest = True
            self.act = 2
            self._transition_to_act_2()
            self.village()
        else:
            print(self.alt_text(
                "You can only visit the village in Act 1.",
                "There is nothing left for you here."
            ))

    def _explore_ruins(self):
        """Handles the player's action when choosing to go to the Ruins."""
        if self.act == 2:
            console.print(self.alt_text(
                "You venture into the forbidden ruins. Crumbling pillars and shattered statues hint at a lost civilization.",
                "You step into the ruins. The statues watch, and the pillars bleed."
            ))
            console.print(self.alt_text(
                "The air is thick with danger and the unknown.",
                "The air is thick with memory and regret."
            ))
            if not self.random_event():
                if random.random() < 0.7:
                    if random.random() < 0.1:
                        self.battle(self.scale_enemy(cavern=True), cavern=True)
                    else:
                        self.battle(self.scale_enemy(act=2))
                else:
                    console.print(self.alt_text(
                        "You find eerie silence among the crumbling stones... for now.",
                        "You find quietude, but it is thick with possibilities, like whispers waiting to be heard."
                    ))
        else:
            console.print(self.alt_text(
                "The ruins are not yet accessible.",
                "The ruins are not yet open to you. The flesh is not ready."
            ))

    def _explore_cavern(self):
        """Handles the player's action when choosing to go to the Cavern."""
        if self.act == 2:
            self.cavern_explore()
        else:
            console.print(self.alt_text(
                "The cavern is not yet accessible.",
                "The flesh is not yet ready for you."
            ))

    def _explore_back(self):
        """Handles the player's action when choosing to go Back to the clearing."""
        console.print(self.alt_text(
            "You return to the clearing where it all began. The grass is soft beneath your feet, and the world feels quiet here.",
            "You return to the place you were reborn, the grass visibly shivers in your presense. Flowers wilt. You did this."
            ))

    def _transition_to_act_2(self):
        """Handles the transition to Act 2 of the game."""

        console.print(self.alt_text(
            "\n--- Act 2: The Ruins Unveiled ---",
            "\n--- Act 2: The world remembers you. Run if you must, but they will always catch you. ---"
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
                f"'You again, {pname}. The shelves are emptier every time you come...'"
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
                        f"'Take it. It won't help what's coming.'"
                    ))
                    self.save_game()
                else:
                    console.print(self.alt_text(
                        "'Sorry friend, you don't have enough gold for that.'",
                        "'You can't get that with what you have now.'"
                    ))
            else:
                console.print(self.alt_text(
                    "'I don't sell that here, friend.'",
                    "'That isn't for sale.'"
                ))

    while True:
            cmd = input("DEV> ").strip().lower()
            if cmd == "exit":
                break

            dev_actions = {
                "give": self._dev_give,
                "gold": self._dev_gold,
                "heal": self._dev_heal,
                "equip": self._dev_equip, # This will need special handling for sub-commands
                "goto": self._dev_goto,
                "stats": self._dev_stats,
                "craft bandage": self._dev_craft_bandage,
                "darkmode": self._dev_darkmode,
            }

            # Handle commands that start with a keyword (e.g., "give", "gold", "heal", "equip", "goto")
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
        if cmd.startswith("equip armor "):
            item_name = cmd[len("equip armor "):].strip().title()
            self.player.equip("armor", item_name)
        elif cmd.startswith("equip tool "):
            item_name = cmd[len("equip tool "):].strip().title()
            self.player.equip("tool", item_name)
        elif cmd.startswith("equip pet "):
            item_name = cmd[len("equip pet "):].strip().title()
            self.player.equip("pet", item_name)
        else:
            console.print("Usage: equip [armor/tool/pet] [name]")

    def _dev_goto(self, cmd: str):
        """Developer command to teleport the player to a specific location."""
        parts = cmd.split()
        if len(parts) == 2:
            loc = parts[1]
            console.print(f"Teleporting to {loc}...")
            # Directly call the location logic
            if loc == "north":
                self._explore_north()
            elif loc == "west":
                self._explore_west()
            elif loc == "east":
                self._explore_east()
            elif loc == "village":
                self._explore_village()
            elif loc == "ruins": # Added for completeness, though not in original goto
                self._explore_ruins()
            elif loc == "cavern": # Added for completeness, though not in original goto
                self._explore_cavern()
            elif loc == "back":
                self._explore_back()
            else:
                console.print("Unknown location.")
        else:
            console.print("Usage: goto [location]")

    def _dev_stats(self):
        """Developer command to display player statistics."""
        console.print(f"Name: {self.player.name}, HP: {self.player.hp}/{self.player.max_hp}, Level: {self.player.level}, EXP: {self.player.exp}, Gold: {self.player.coins['gold']}")
        console.print("Inventory:", self.player.inventory)
        console.print("Pet:", self.player.pet if self.player.pet else "None")
        console.print("Armor:", self.player.armor if self.player.armor else "None")
        console.print("Tool:", self.player.tool if self.player.tool else "None")
        console.print("Lantern fuel:", self.player.lantern_fuel)
        console.print("Lantern on:", "Yes" if self.player.lantern_on else "No")

    def _dev_craft_bandage(self):
        """Developer command to craft a bandage."""
        if self.player.inventory.get("Silk", 0) >= 2:
            self.player.inventory["Silk"] -= 2
            self.player.add_item("Bandage")
            print("You crafted a Bandage from 2 Silk.")
        else:
            print("You don't have enough Silk to craft a Bandage.")

    def _dev_darkmode(self):
        """Developer command to toggle or activate dark mode."""
        if not self.alt_mode:
            console.print("Triggering alternate dark gamemode...")
            self.rare_cutscene()
        else:
            console.print("Dark gamemode is already active.")

    def village(self):
        while True:
            console.print("\nYou are in the village square. What would you like to do?")
            console.print("Options: shop, rest, craft, leave")
            choice = input("Type your choice: ").strip().lower()
            if choice == "shop":
                self.shop()
            elif choice == "rest":
                self.player.hp = self.player.max_hp
                console.print("You rest at the inn. Your HP is fully restored!")
                self.save_game()
            elif choice == "craft":
                self.crafting_menu()
            elif choice == "leave":
                console.print("You leave the village and return to the crossroads.")
                break
            else:
                console.print("Invalid choice. Type one of: shop, rest, craft, leave")

    def cavern_explore(self):
        if not self._check_cavern_entry_conditions():
            return
        console.print(self.alt_text(
            "You step into the darkness, lantern held high.",
            "You step into the flesh, lantern trembling in your hand."
        ))
        path = []
        while self.player.lantern_fuel > 0:
            self._display_cavern_status()
            console.print(self.alt_text(
                "You can go left, right, forward, or back.",
                "You can go left, right, forward, or back. The walls pulse."
            ))
            move = input("Which way? (left/right/forward/back): ").strip().lower()
            if self._handle_cavern_move(path):
                break
            if self._handle_lantern_depletion(path):
                break
        else:
            print(self.alt_text(
                "You sense your lantern is about to die and hurry out of the cavern.",
                "You sense your lantern is dying and run for the exit."
            ))
        self.player.lantern_on = False

    def _check_cavern_entry_conditions(self) -> bool:
        """Checks if the player meets the conditions to enter the cavern."""
        if self.player.inventory.get("Lantern", 0) == 0:
            console.print(self.alt_text(
                "It's too dark to enter the cavern without a lantern.",
                "You cannot enter the flesh without a light. It hungers for you."
            ))
            return False
        if self.player.lantern_fuel <= 0 or not self.player.lantern_on:
            console.print(self.alt_text(
                "You need to light your lantern to enter the cavern.",
                "You need to light your lantern before entering. The flesh is alive."
            ))
            if self.player.lantern_fuel <= 0:
                console.print(self.alt_text(
                    "Your lantern is out of fuel. Find animal fat to refuel your lantern.",
                    "Your lantern runs dry. The flesh will consume you without fuel."
                ))
                return False
            if ask_yes_no(self.alt_text(
                "Do you want to use your lantern?",
                "Will you light your lantern and face what waits?"
            )):
                self.player.use_lantern()
                return True
            else:
                console.print(self.alt_text(
                    "You decide not to enter the cavern.",
                    "You hesitate. The mouth closes for now."
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

    def _handle_cavern_move(self, path: list) -> bool:
        """Handles player movement within the cavern, including 'back' and random events."""
        move = input("Which way? (left/right/forward/back): ").strip().lower()
        if move == "back":
            if path:
                console.print(self.alt_text(
                    "You retrace your steps...",
                    "You try to retrace your steps, but the walls shift."
                ))
                path.pop()
                if not path:
                    console.print(self.alt_text(
                        "You have escaped the cavern safely!",
                        "You stumble out of the flesh, gasping for air."
                    ))
                    return True  # Player escaped
            else:
                console.print(self.alt_text(
                    "You are at the entrance and leave the cavern.",
                    "You are at the mouth and escape its hunger."
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
                    "You find a symbol, drawn in something that glistens."
                ))
            else:
                console.print(self.alt_text(
                    "The darkness presses in, but your lantern keeps it at bay.",
                    "The walls pulse, but your lantern keeps them away."
                ))
        else:
            console.print(self.alt_text(
            "You hesitate, unsure which way to go.",
            "You hesitate. The flesh waits."
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
                    "Lost in the flesh, you collapse, the walls closing in..."
                ))
                console.print(self.alt_text(
                    "You awaken at your last save point, shaken but alive.",
                    "You awaken in the last place you remember, the taste of blood in your mouth."
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
                if game.player.name.lower() == "moogie":
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