
from __future__ import annotations
import random
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game
    from battle import AzraelBattle

class Exploration:
    def __init__(self, game: "Game"):
        self.game = game
        self.player = game.player
        self.console = game.console

    def explore(self) -> None:
        while True:
            self.console.print(self.game.alt_text(
                "\nYou stand at a crossroads. Where will you go?",
                "\nYou stand at the fracture. Where will you wander?"
            ))
            self.console.print(self.game.alt_text(
                "Directions: n, ne, e, se, s, sw, w, nw",
                "Directions: n, ne, e, se, s, sw, w, nw"
            ))
            if self.game.act == 1:
                self.console.print(self.game.alt_text(
                    "Village: A settlement where you may rest and trade.",
                    "Village: The burned remains of a once-thriving community. The air is thick with ash."
                ))
            if self.game.act == 2:
                self.console.print(self.game.alt_text(
                    "Ruins: The forbidden ruins, now revealed beyond the village.",
                    "Ruins: The ruins, crawling with things that remember."
                ))
                self.console.print(self.game.alt_text(
                    "Cavern: A dark cavern mouth gapes in the hillside.",
                    "Cavern: The flesh, it feeds."
                ))
                self.console.print(self.game.alt_text(
                    "Volcano: A fiery volcano looms in the distance.",
                    "Volcano: A bleeding mountain of flesh and stone."
                ))
            self.console.print(self.game.alt_text(
                "Craft: Craft items from your materials.",
                "Craft: Stitch together what you can."
            ))
            self.console.print(self.game.alt_text(
                "Back: Return to the clearing.",
                "Back: Return to the place you were reborn."
            ))
            if self.game.developer_mode:
                self.console.print("[DEV] Type 'dev' for developer commands.")

            choice = input("Choose a direction: ").strip().lower()

            explore_actions = {
                "dev": self.game.developer_commands,
                "craft": self.game.crafting_menu,
                "inventory": self.game.inventory_menu,
                "n": self._explore_n, "north": self._explore_n,
                "ne": self._explore_ne, "northeast": self._explore_ne,
                "e": self._explore_e, "east": self._explore_e,
                "se": self._explore_se, "southeast": self._explore_se,
                "s": self._explore_s, "south": self._explore_s,
                "sw": self._explore_sw, "southwest": self._explore_sw,
                "w": self._explore_w, "west": self._explore_w,
                "nw": self._explore_nw, "northwest": self._explore_nw,
                "village": self._explore_village,
                "ruins": self._explore_ruins,
                "cavern": self._explore_cavern,
                "volcano": self._explore_volcano,
                "back": self._explore_back,
            }

            action = explore_actions.get(choice)
            if action:
                if choice in ["n", "ne", "e", "se", "s", "sw", "w", "nw", "ruins"]:
                    result = action()
                    if result in ["lost_boss", "lost_normal"]:
                        return result
                    if result:
                        traverse_result = self._traverse_path(result)
                        if traverse_result in ["lost_boss", "lost_normal"]:
                            return traverse_result
                elif choice == "cavern":
                    result = self.game.cavern_explore()
                    if result in ["lost_boss", "lost_normal"]:
                        return result
                else:
                    action()
            else:
                print(self.game.alt_text(
                    "Invalid choice.",
                    "A door forever shut, you may not return."
                ))

    def _traverse_path(self, path_data: Dict):
        self.console.print(self.game.alt_text(path_data["intro_text"]["normal"], path_data["intro_text"]["alt"]))

        progress = 0
        max_progress = path_data["stages"]

        while progress < max_progress:
            self.console.print(f"\nYou are {progress}/{max_progress} of the way along the path.")
            choice = input("Do you (continue/leave)? ").strip().lower()

            if choice == "continue":
                progress += 1
                self.console.print(self.game.alt_text(path_data["stage_text"]["normal"], path_data["stage_text"]["alt"]))
                
                if not self.game.random_event():
                    if random.random() < path_data["event_chance"]:
                        battle_result = self.game.battle(self.game.scale_enemy(act=self.game.act))
                        if battle_result in ["lost_boss", "lost_normal"]:
                            return battle_result

                if self.player.hp <= 0:
                    return

            elif choice == "leave":
                self.console.print(self.game.alt_text("You turn back, leaving the path for another day.", "You retreat from the path."))
                return
            else:
                self.console.print("Invalid choice.")

        if path_data.get("end_event"):
            path_data["end_event"]()

    def _explore_n(self):
        path_data = {
            "stages": 3,
            "intro_text": {
                "normal": "You walk north. The air grows colder as you approach a lonely cabin, its windows dark and silent.",
                "alt": "You walk north... An abandoned cabin stands, the ground still bloody from that night."
            },
            "stage_text": {
                "normal": "You press on, the cabin looming closer.",
                "alt": "You continue, the wind calls your name."
            },
            "event_chance": 0.4,
            "end_event": self._n_end_event
        }
        return path_data

    def _n_end_event(self):
        if self.game.ask_yes_no(self.game.alt_text(
            "You find a small cabin. Do you enter?",
            "You find the house that once belonged to you. Do you step inside?"
        )):
            self.console.print(self.game.alt_text(
                "Inside the cabin, you find a lantern. +1 Lantern",
                "Inside, you find a flickering lantern. +1 Lantern"
            ))
            self.player.add_item("Lantern")
            self.game.save_game()
        else:
            self.console.print(self.game.alt_text(
                "You decide not to enter. The cabin looms silently.",
                "You decide to turn away from the past."
            ))

    def _explore_w(self):
        path_data = {
            "stages": 4,
            "intro_text": {
                "normal": "You head west into the dark woods. The trees are twisted, and strange sounds echo between them.",
                "alt": "You head west. The obelisks, once trees, now stand as silent sentinels."
            },
            "stage_text": {
                "normal": "Deeper into the woods you go...",
                "alt": "The silence deepens..."
            },
            "event_chance": 0.6,
            "end_event": self._w_end_event
        }
        return path_data

    def _w_end_event(self):
        self.console.print(self.game.alt_text(
            "You reach a clearing in the woods. A sense of peace settles over you.",
            "You find the heart of the woods. It is a place of quiet sorrow."
        ))
        if not self.game.random_event():
            self.console.print("You find a small pouch of gold.")
            self.player.coins["gold"] += 15
            self.game.save_game()

    def _explore_e(self):
        path_data = {
            "stages": 3,
            "intro_text": {
                "normal": "You follow the path east. An ancient stone stands here, humming with strange energy.",
                "alt": "You follow the path east. The stone sits there, shattered as if hit by a force beyond humanity. It is weak."
            },
            "stage_text": {
                "normal": "The humming of the stone grows louder.",
                "alt": "The stone weeps."
            },
            "event_chance": 0.5,
            "end_event": self._e_end_event_village # Changed end_event
        }
        return path_data

    def _e_end_event(self):
        self.console.print(self.game.alt_text(
            "You stand before the ancient stone. It radiates a faint warmth.",
            "You stand before the shattered stone. It is cold to the touch."
        ))
        if not self.game.random_event():
            self.console.print(self.game.alt_text(
                "You feel a chill as you touch the stone, but nothing else happens.",
                "You touch the egg. It feels warm, and something inside it moves."
            ))

    def _e_end_event_village(self):
        self.console.print(self.game.alt_text(
            "You arrive at the village entrance.",
            "The village beckons."
        ))
        self.game.village()

    def _explore_nw(self):
        path_data = {
            "stages": 3,
            "intro_text": {
                "normal": "You venture into a secluded grove, sunlight filtering through the canopy.",
                "alt": "The grove is unnaturally silent, the trees here are pale and leafless."
            },
            "stage_text": {
                "normal": "The path is overgrown, but you press on.",
                "alt": "The air grows heavy, and you feel watched."
            },
            "event_chance": 0.3,
            "end_event": self._nw_end_event
        }
        return path_data

    def _nw_end_event(self):
        self.console.print(self.game.alt_text(
            "You discover a hidden spring, its water shimmering with a faint light.",
            "You find a pool of black, oily liquid. It ripples, though there is no wind."
        ))
        if self.game.ask_yes_no(self.game.alt_text("Do you drink from the spring?", "Do you touch the liquid?")):
            self.console.print(self.game.alt_text(
                "You feel invigorated. Your max HP has increased by 10!",
                "A sharp pain shoots up your arm, but then fades, leaving you feeling... stronger. Your attack has increased by 2!"
            ))
            if self.game.alt_mode:
                self.player.attack += 2
            else:
                self.player.max_hp += 10
                self.player.hp += 10
            self.game.save_game()
        else:
            self.console.print(self.game.alt_text("You decide to leave the spring untouched.", "You back away slowly."))

    def _explore_sw(self):
        path_data = {
            "stages": 4,
            "intro_text": {
                "normal": "The ground becomes soft and marshy as you head southwest into a swamp.",
                "alt": "The swamp is a field of grasping hands and whispers from below the murky water."
            },
            "stage_text": {
                "normal": "You navigate through the murky water, the air thick with the smell of decay.",
                "alt": "The whispers grow louder, calling your name."
            },
            "event_chance": 0.7,
            "end_event": self._sw_end_event
        }
        return path_data

    def _sw_end_event(self):
        self.console.print(self.game.alt_text(
            "You find a half-submerged chest, covered in moss and algae.",
            "A skeletal hand emerges from the water, offering you a rusted locket."
        ))
        if self.game.ask_yes_no(self.game.alt_text("Do you open the chest?", "Do you take the locket?")):
            self.console.print(self.game.alt_text(
                "Inside, you find a handful of old coins and a rare gem!",
                "The locket contains a faded portrait of a smiling child. You feel a deep sense of loss."
            ))
            self.player.coins["gold"] += 25
            self.player.add_item("Rare Gem")
            self.game.save_game()
        else:
            self.console.print(self.game.alt_text("You leave the chest to the swamp.", "You let the hand sink back into the depths."))

    def _explore_se(self):
        path_data = {
            "stages": 3,
            "intro_text": {
                "normal": "You follow a path towards the coast, the sound of waves growing louder.",
                "alt": "The coastline is littered with the skeletons of great sea creatures."
            },
            "stage_text": {
                "normal": "The salty air whips your face as you walk along the beach.",
                "alt": "The waves are black and oily, leaving a residue on the sand."
            },
            "event_chance": 0.4,
            "end_event": self._se_end_event
        }
        return path_data

    def _se_end_event(self):
        self.console.print(self.game.alt_text(
            "You come across the wreckage of a ship, half-buried in the sand.",
            "A beached leviathan lies on the shore, its eye staring blankly at the sky."
        ))
        if self.game.ask_yes_no(self.game.alt_text("Do you search the wreckage?", "Do you approach the leviathan?")):
            self.console.print(self.game.alt_text(
                "You find a sturdy, iron-bound chest! Inside is a new piece of armor.",
                "You find a strange, pulsating organ inside the creature. It seems to be a source of great power."
            ))
            if self.game.alt_mode:
                self.player.add_item("Pulsating Organ")
            else:
                self.player.add_item("Mariner's Armor")
            self.game.save_game()
        else:
            self.console.print(self.game.alt_text("You leave the shipwreck to the sea.", "You give the dead creature a wide berth."))

    def _explore_ne(self):
        path_data = {
            "stages": 4,
            "intro_text": {
                "normal": "The path leads you into the foothills of a mountain range.",
                "alt": "The mountains are jagged and cruel, like broken teeth against the sky."
            },
            "stage_text": {
                "normal": "The climb is steep, but the view is breathtaking.",
                "alt": "The rocks are sharp, and the wind howls like a tormented spirit."
            },
            "event_chance": 0.6,
            "end_event": self._ne_end_event
        }
        return path_data

    def _ne_end_event(self):
        self.console.print(self.game.alt_text(
            "You find a small cave, a cool breeze flowing from its entrance.",
            "You find a crack in the mountainside, from which a faint, sickly light emanates."
        ))
        if self.game.ask_yes_no(self.game.alt_text("Do you enter the cave?", "Do you squeeze through the crack?")):
            self.console.print(self.game.alt_text(
                "Inside, you find a vein of glowing crystals. You carefully mine a few.",
                "The light comes from a pulsating, fleshy mass. You cut a piece of it away."
            ))
            if self.game.alt_mode:
                self.player.add_item("Pulsating Shard")
            else:
                self.player.add_item("Glowing Crystal")
            self.game.save_game()
        else:
            self.console.print(self.game.alt_text("You decide not to risk entering the cave.", "You back away from the unsettling light."))

    def _explore_s(self):
        path_data = {
            "stages": 5,
            "intro_text": {
                "normal": "The path leads south into a vast, arid desert.",
                "alt": "The ground is covered with sand, sand... You remember them to be once mighty giants, eroded by the endless flow of time"
            },
            "stage_text": {
                "normal": "The sun beats down on you as you trudge through the endless sand.",
                "alt": "The air is colder than it should be, but you continue on regardless. A grain of sand for each sin that was borne to your skin"
            },
            "event_chance": 0.5,
            "end_event": self._s_end_event
        }
        return path_data

    def _s_end_event(self):
        self.console.print(self.game.alt_text(
            "You see a shimmering oasis in the distance.",
            "You see a city of gold and diamond in the distance..."
        ))
        if self.game.ask_yes_no(self.game.alt_text("Do you head towards the oasis?", "Do you approach the city?")):
            self.console.print(self.game.alt_text(
                "You find a pool of cool, clear water. You rest and recover your strength.",
                "The city is a mirage, and you find only a single, wilting flower growing in the sand."
            ))
            if self.game.alt_mode:
                self.player.add_item("Black Lotus")
            else:
                self.player.hp = self.player.max_hp
            self.game.save_game()
        else:
            self.console.print(self.game.alt_text("You decide the oasis is just a mirage and turn back.", "You do not trust the mirage and turn away."))

    def _explore_village(self):
        if not self.game.village_visited_first_time:
            self.console.print(self.game.alt_text(
                "You arrive at a small village. Lanterns flicker in the dusk, and villagers eye you warily.",
                "You arrive at the empty village. Lanterns flicker, but no one is there."
            ))
            self.console.print(self.game.alt_text(
                "A shopkeeper waves you over: 'Looking for supplies, traveler?'",
                "A figure stands in the shop, face hidden. 'Looking for something you shattered?'"
            ))
            self.player.unlocked_rest = True
            self.game.act = 2
            self.game._transition_to_act_2()
            self.game.village()
        else:
            self.game.village()

    def _explore_ruins(self):
        if self.game.act != 2:
            self.console.print(self.game.alt_text(
                "The ruins are not yet accessible.",
                "The ruins have not shown itself to you yet..."
            ))
            return None

        path_data = {
            "stages": 5,
            "intro_text": {
                "normal": "You venture into the forbidden ruins. Crumbling pillars and shattered statues hint at a lost civilization.",
                "alt": "You step into the ruin. The statues weep with the lost souls of this place. The pillars, once great marvels of prosperity, now bleed."
            },
            "stage_text": {
                "normal": "The air is thick with danger and the unknown.",
                "alt": "The air is thick with memory and regret."
            },
            "event_chance": 0.7,
            "end_event": self._ruins_end_event
        }
        return path_data

    def _ruins_end_event(self):
        self.console.print(self.game.alt_text(
            "You discover a hidden altar, where a rare herb grows.",
            "You find a place of sacrifice. Something was taken from here."
        ))
        self.player.add_item("Kingsfoil")
        self.game.save_game()

    def _explore_cavern(self):
        if self.game.act == 2:
            self.game.cavern_explore()
        else:
            self.console.print(self.game.alt_text(
                "The cavern is not yet accessible.",
                "The flesh is not yet ready for you."
            ))

    def _explore_volcano(self):
        if self.game.act != 2:
            self.console.print(self.game.alt_text(
                "The way to the volcano is blocked.",
                "The bleedingmountain denies you."
            ))
            return

        self.console.print(self.game.alt_text(
            "You begin the treacherous climb up the volcano. The air is hot and smells of sulfur.",
            "You ascend the bleeding mountain... The air is thick with the stench of burnt flesh and regret."
        ))

        ascent_progress = 0
        max_ascent = 3

        while ascent_progress < max_ascent:
            self.console.print(f"\nYou are {ascent_progress}/{max_ascent} of the way up the volcano.")
            choice = input("Do you (ascend/leave)? ").strip().lower()

            if choice == "ascend":
                ascent_progress += 1
                self.console.print(self.game.alt_text(
                    "You continue your ascent, the heat growing more intense.",
                    "You climb higher, the fleshy ground squirming beneath your feet."
                ))
                if random.random() < 0.6:
                    self.game.battle(self.game.scale_enemy(volcano=True))
                if self.player.hp <= 0:
                    return
            elif choice == "leave":
                self.console.print(self.game.alt_text(
                    "You carefully climb back down, leaving the volcano for another day.",
                    "You retreat from the bleeding mountain."
                ))
                return
            else:
                self.console.print("Invalid choice.")

        if self.game.alt_mode:
            boss = {"name": "Azrael, the Unyielding", "hp": 9999, "attack": 999, "boss": True}
            azrael_battle = AzraelBattle(self.player, boss, self.game)
            azrael_battle.run()
            return # End exploration after this special battle
        else:
            boss = {"name": "Ancient Dragon", "hp": 300, "attack": 30, "boss": True}
        
        result = self.game.battle(boss)

        if result == "won":
            self.console.print(self.game.alt_text(
                f"With a final, earth-shattering roar, the {boss['name']} collapses!",
                f"The {boss['name']} shrieks and dissolves into ash and embers."
            ))
            self.console.print("You have conquered the volcano!")
            self.console.print("You are rewarded with 1000 EXP and 500 gold!")
            self.player.gain_exp(1000)
            self.player.coins["gold"] += 500
            self.player.add_item("Dragon Scale" if not self.game.alt_mode else "Demon Heart")
            self.console.print(f"You found a {'Dragon Scale' if not self.game.alt_mode else 'Demon Heart'}!")
            self.game.save_game()

    def _explore_back(self):
        self.console.print(self.game.alt_text(
            "You return to the clearing where it all began. The grass is soft beneath your feet, and the world feels quiet here.",
            "You return to the place you were reborn, the grass visibly shivers in your presense. Flowers wilt. You did this, ####r."
        ))
