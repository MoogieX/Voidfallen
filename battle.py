from __future__ import annotations
import random
from typing import Dict, TYPE_CHECKING
from rich.console import Console
from player import Player
from libraries import Libraries
if TYPE_CHECKING:
    from game import Game
lib = Libraries()   

console = Console()

class Battle:
    def __init__(self, player: Player, enemy: Dict[str, int], game: "Game", cavern: bool = False):
        self.player = player
        self.enemy = enemy
        self.game = game
        self.cavern = cavern
        self.enemy_max_hp = enemy['hp']  # Store max HP for flee check

        # Define enemy properties based on name
        self.poison_inflictors = ["snake", "nightcrawler"]
        self.bleed_inflictors = ["winged horror"]
        self.silk_droppers = ["nightcrawler"]
        self.animal_fat_droppers = ["winged horror"]
        self.ghost_lifesteal = ["ghost"]
        self.ectoplasm_droppers = []

        # Dark mode specific properties
        if self.game.alt_mode:
            self.poison_inflictors.append("flesh moth")
            self.bleed_inflictors.extend(["bleeding idol", "the feasting"])
            self.silk_droppers.append("flesh moth")
            self.ectoplasm_droppers.append("watcher")

    def run(self) -> str:
        """
        Runs the main battle loop.
        
        Returns:
            str: The outcome of the battle ('won', 'lost', 'fled', 'enemy_fled').
        """
        console.print(f"A wild {self.enemy['name']} appears!")
        
        while self.enemy["hp"] > 0 and self.player.hp > 0:
            self.player.process_debuffs()
            if self.player.hp <= 0:
                break # Check if debuffs were fatal

            console.print(f"\nYour HP: {self.player.hp}/{self.player.max_hp} | Enemy HP: {self.enemy['hp']} ")
            attack_menu = [
                "✦Attack✦",
                "✦Run✦",
                "✦Inventory✦"
            ]

            action = lib.select("What will you do?", attack_menu)

            if action == "✦Attack✦":
                self._handle_player_attack()
            elif action == "✦Inventory✦":
                self.player.display_inventory()
                self._handle_use_item()
            elif action == "✦Run✦":
                if self._handle_run():
                    return "fled"
            else:
                console.print("Invalid action.")
                continue

            if self.enemy["hp"] > 0:
                # Enemy turn: check for flee, then attack
                is_low_health = self.enemy['hp'] < self.enemy_max_hp * 0.2
                if is_low_health and random.random() < 0.1:
                    console.print(f"The {self.enemy['name']} flees! But you have the feeling this isn't the end.")
                    return "enemy_fled"

                self._handle_enemy_attack()

        return "won" if self.player.hp > 0 else "lost"

    def _handle_player_attack(self):
        """Handles the player's attack action."""
        dmg = self.player.get_current_attack(self.game) + random.randint(0, 4)
        self.enemy["hp"] -= dmg
        console.print(f"You slash at the {self.enemy['name']} for {dmg}!")
        
        # Lifesteal for specific enemies if player is bleeding
        is_lifesteal_enemy = any(e in self.enemy["name"].lower() for e in self.bleed_inflictors + self.ghost_lifesteal)
        if self.enemy["hp"] > 0 and is_lifesteal_enemy and self.player.bleed_turns > 0:
            heal = 2
            self.enemy["hp"] += heal
            console.print(f"{self.enemy['name']} absorbs {heal} HP from your lifeblood!")

    def _handle_use_item(self):
        """Handles the player's 'use item' action."""
        usable_items = []
        if self.player.inventory.get("Potion", 0) > 0:
            usable_items.append("Potion")
        if self.cavern and self.player.inventory.get("Animal Fat", 0) > 0:
            usable_items.append("Animal Fat")
        if self.player.inventory.get("Bandage", 0) > 0:
            usable_items.append("Bandage")

        if not usable_items:
            console.print("You have no usable items!")
            return

        usable_items.append("Back")
        choice = lib.select("Which item will you use?", usable_items)

        if choice == "Potion":
            self.player.inventory["Potion"] -= 1
            self.player.heal(30)
            console.print("You drink a potion and restore 30 HP.")
        elif choice == "Animal Fat":
            self.player.inventory["Animal Fat"] -= 1
            self.player.refuel_lantern(3)
        elif choice == "Bandage":
            self.player.inventory["Bandage"] -= 1
            self.player.poison_turns = 0
            self.player.bleed_turns = 0
            console.print("You use a bandage ease your wounds.")
        elif choice == "Back":
            return

    def _handle_run(self) -> bool:
        """Handles the player's attempt to run from battle."""
        if random.random() < 0.5:
            console.print("You have fled successfully, cheers to living another day!")
            return True
        console.print("You try to flee, but you are held back by the enemy encroaching")
        return False

    def _handle_enemy_attack(self):
        """Handles the enemy's attack and special abilities."""
        dmg = self.enemy["attack"] + random.randint(0, 3)
        self.player.take_damage(dmg)
        console.print(f"The {self.enemy['name']} hits you for {dmg} damage!")
        
        # 25% chance to inflict debuffs
        if any(e in self.enemy["name"].lower() for e in self.poison_inflictors) and random.random() < 0.25:
            self.player.apply_poison()
        if any(e in self.enemy["name"].lower() for e in self.bleed_inflictors) and random.random() < 0.25:
            self.player.apply_bleed()

    def handle_drops(self):
        """Handles item drops after winning a battle."""
        if any(e in self.enemy["name"].lower() for e in self.animal_fat_droppers):
            console.print("You collect animal fat from the winged horror's remains.")
            self.player.add_item("Animal Fat")
        if any(e in self.enemy["name"].lower() for e in self.silk_droppers):
            console.print("You collect silk from the nightcrawler's remains.")
            self.player.add_item("Silk")
        if any(e in self.enemy["name"].lower() for e in self.ectoplasm_droppers):
            console.print("You collect a strange, shimmering ectoplasm from the watcher's remains.")
            self.player.add_item("Ectoplasm")

class AzraelBattle(Battle):
    def __init__(self, player: Player, enemy: Dict[str, int], game: "Game", cavern: bool = False):
        super().__init__(player, enemy, game, cavern)
        self.turns = 0

    def run(self) -> str:
        console.print(f"You face Azrael, Archangel of death itself. There is no escaping your fate now")
        
        while self.enemy["hp"] > 0 and self.player.hp > 0:
            self.turns += 1
            if self.turns > 10:
                self.player.hp = 0
                break

            self.player.process_debuffs()
            if self.player.hp <= 0:
                break

            console.print(f"\nYour HP: {self.player.hp}/{self.player.max_hp} | Azrael's HP: ???")
            action = input("What do you do?").strip().lower()

            if action == "attack":
                self._handle_player_attack()
            elif action == "use item":
                self._handle_use_item()
            else:
                console.print("Invalid action.")
                continue

            if self.enemy["hp"] > 0:
                self._handle_enemy_attack()

        if self.player.hp <= 0:
            self.game._create_astar_save()
            console.print("You have been defeated... but your journey is not over, not yet.")
            exit()
        
        return "won" # This should not be reachable
