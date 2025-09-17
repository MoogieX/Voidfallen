from __future__ import annotations
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

class Player:
    def __init__(self, console_obj):
        self.console = console_obj
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
            self.console.print("Your lantern is now fueled and ready to use! (6 turns of fuel)")

    def can_afford(self, cost: int) -> bool:
        return self.coins["gold"] >= cost

    def spend_gold(self, amount: int) -> None:
        self.coins["gold"] -= amount

    def gain_gold(self, amount: int) -> None:
        self.coins["gold"] += amount

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
            self.console.print(f"You leveled up! You are now level {self.level}.")

    def equip(self, item_type: str, item_name: str):
        """Equips an item of a specific type to the player."""
        if hasattr(self, item_type):
            setattr(self, item_type, item_name)
            self.console.print(f"You have equipped {item_name} as your {item_type}!")
        else:
            self.console.print(f"Cannot equip {item_name}. Invalid item type: {item_type}.")

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
        self.console.print(f"You refuel your lantern with {fat_units} animal fat. Lantern fuel: {self.lantern_fuel} turns.")

    def apply_poison(self, turns=2):
        self.poison_turns = turns
        self.console.print("You have been poisoned! You will lose 1 HP for the next 2 turns.")

    def apply_bleed(self, turns=2):
        self.bleed_turns = turns
        self.console.print("You are bleeding! You will lose 2 HP for the next 2 turns.")

    def process_debuffs(self):
        if self.poison_turns > 0:
            self.take_damage(1)
            self.poison_turns -= 1
            self.console.print("Poison deals 1 damage to you!")
        if self.bleed_turns > 0:
            self.take_damage(2)
            self.bleed_turns -= 1
            self.console.print("Bleeding deals 2 damage to you!")

    def display_inventory(self):
        self.console.print("\n--- Your Inventory ---")
        if not self.inventory:
            self.console.print("  (Empty)")
        else:
            for item, qty in self.inventory.items():
                self.console.print(f"  {item}: {qty}")
        self.console.print(f"Equipped Armor: {self.armor if self.armor else 'None'}")
        self.console.print(f"Equipped Tool: {self.tool if self.tool else 'None'}")
        self.console.print(f"Equipped Pet: {self.pet if self.pet else 'None'}")
        self.console.print(f"Lantern Fuel: {self.lantern_fuel} turns (On: {'Yes' if self.lantern_on else 'No'})")
        self.console.print("----------------------")

    def get_current_attack(self, game_instance: "Game") -> int:
        base_attack = self.attack
        if self.tool:
            # Parse tier from tool name (e.g., "Common Rusty Pickaxe")
            parts = self.tool.split(" ", 1)
            if len(parts) > 1 and parts[0] in game_instance.weapon_tiers:
                tier_name = parts[0]
                tier_bonus = game_instance.weapon_tiers[tier_name]["bonus"]
                base_attack += tier_bonus
        return base_attack
