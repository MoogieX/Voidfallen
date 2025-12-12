
from __future__ import annotations
import random
from libraries import Libraries
from typing import Dict, TYPE_CHECKING
lib = Libraries()
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
                "North, Northeast, East, Southeast, South, Southwest, West, Northwest",
                "North, Northeast, East, Southeast, South, Southwest, West, Northwest"
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

            if self.game.act == 1:
                act_1_menu_options = [
                    "Village", "North", "East", "South", "West", "Inventory", "Back"
                ]
            act_2_menu_options = [
                "Ruins", "Cavern", "Volcano", "North", "Northeast", "East", "Southeast", "South", "Southwest", "West", "Northwest", "Craft", "Inventory", "Back"
            ]
            act_4_menu_options = [
                "Up", "Down", "North", "Northeast", "East", "Southeast", "South", "Southwest", "West", "Northwest", "Craft", "Inventory", "Back"
            ]

            dev_menu_options = [
                "North", "Northeast", "East", "Southeast", "South", "Southwest", "West", "Northwest", "Craft", "Inventory", "Dev", "Back"
            ]

            # Build menu options dynamically based on act to ensure displayed
            # options are actually selectable.
            if self.game.act == 1:
                menu_options = act_1_menu_options
            elif self.game.act == 2 or self.game.act == 3:
                menu_options = act_2_menu_options
            elif self.game.act == 4:
                menu_options = act_4_menu_options
            else:
                menu_options = ["North", "Northeast", "East", "Southeast", "South", "Southwest", "West", "Northwest", "Craft", "Inventory", "Back"]

            # If developer mode enabled, add dev option at end
            if self.game.developer_mode and "Dev" not in menu_options:
                menu_options.append("Dev")

            choices = lib.select("━─┉┈◈ Choose a direction ◈┈┉─━", menu_options)
            
            explore_actions = {
                "Dev": self.game.developer_commands,
                "Craft": self.game.crafting_menu,
                "Inventory": self.game.inventory_menu,
                "Village": self._explore_village, "village": self._explore_village,
                "Ruins": self._explore_ruins, "ruins": self._explore_ruins,
                "Cavern": self._explore_cavern, "cavern": self._explore_cavern,
                "Volcano": self._explore_volcano, "volcano": self._explore_volcano,
                "North": self._explore_n, "north": self._explore_n,
                "Northeast": self._explore_ne, "northeast": self._explore_ne,
                "East": self._explore_e, "east": self._explore_e,
                "Southeast": self._explore_se, "southeast": self._explore_se,
                "South": self._explore_s, "south": self._explore_s,
                "Southwest": self._explore_sw, "southwest": self._explore_sw,
                "West": self._explore_w, "west": self._explore_w,
                "Northwest": self._explore_nw, "northwest": self._explore_nw,
                "Back": self._explore_back, "back": self._explore_back,
                "Up": self._explore_up, "up": self._explore_up,
                "Down": self._explore_down, "down": self._explore_down
            }

            action = explore_actions.get(choices)
            if action:
                if choices in ["North", "Northeast", "East", "Southeast", "South", "Southwest", "West", "Northwest"]:
                    result = action()
                    if result in ["lost_boss", "lost_normal"]:
                        return result
                    if result:
                        traverse_result = self._traverse_path(result)
                        if traverse_result in ["lost_boss", "lost_normal"]:
                            return traverse_result
                elif choices == "Cavern":
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

            # Check for stage-specific events
            if "stage_events" in path_data:
                for event in path_data["stage_events"]:
                    if progress == event["stage"]:
                        self.console.print(self.game.alt_text(event["intro_text"]["normal"], event["intro_text"]["alt"]))
                        choices = lib.select("━─┉┈◈ What do you do? ◈┈┉─━", ["Yes", "No"])
                        if choices == "Yes":
                            event["handler"]()
                        # If "No", just continue on

            continue_choices = [
                "Continue",
                "Leave"
            ]
            choices = lib.select("━─┉┈◈ Do you wish to continue down the path? ◈┈┉─━", continue_choices)


            if choices == "Continue":
                progress += 1
                self.console.print(self.game.alt_text(path_data["stage_text"]["normal"], path_data["stage_text"]["alt"]))
                
                if not self.game.random_event():
                    if random.random() < path_data["event_chance"]:
                        battle_result = self.game.battle(self.game.scale_enemy(act=self.game.act))
                        if battle_result in ["lost_boss", "lost_normal"]:
                            return battle_result

                if self.player.hp <= 0:
                    return

            elif choices == "Leave":
                self.console.print(self.game.alt_text("You turn back, leaving the path for another day.", "You retreat from the path."))
                return
            else:
                self.console.print("Invalid choice. (THIS IS A BUG!!!!)")

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
            "stage_events": [
                {
                    "stage": 2,
                    "intro_text": {
                        "normal": "A figure, with a heart of light and color, walks up to you, curious. 'Hello there!'",
                        "alt": "A woman, sits by the road with a book. But she recoils at the sight of you."
                    },
                    "handler": self._n_stage_2_event
                }
            ],
            "end_event": self._n_end_event
        }
        return path_data

    def _n_stage_2_event(self):
        # If player hasn't seen this cutscene before, give a one-time reward
        if not self.game.has_seen_cutscene("loris_intro"):
            # One-time small reward: item + small heal
            if self.game.alt_mode:
                self.player.add_item("Diary")
            else:
                self.player.add_item("Curiosity's Essence")
            self.player.hp = min(self.player.max_hp, self.player.hp + 5)
            self.console.print(self.game.alt_text(
                "You receive a curious token and feel slightly restored (+5 HP).",
                "A scrap of memory lingers; you clutch a token. Pain eases slightly. (+5 HP)"
            ))
            # Persist the flag and save
            self.game.mark_cutscene_seen("loris_intro")

        lib.slow_type_font_color("Purple", "Monospace", self.game.alt_text(
            "The figure blinks, 'I haven't seen you before... Who are you?'",
            "She blinks, not sure what to make of you. As if she is digging into a hidden memory. 'I... What? No, no, no, no...'"
        ))

        loris_choices = ["Yes", "No"]
        choices = lib.select(self.game.alt_text(
            "━─┉┈◈ Do you answer with your real name? ◈┈┉─━",
            "━─┉┈◈ Do you talk with her? ◈┈┉─━"
        ), loris_choices)

        if choices == "Yes":
            lib.slow_type_font_color("Purple", "Monospace", self.game.alt_text(
                f"'That's a beautiful name, {self.player.name}' she says, her bright figure softening in intensity ever so slightly",
                "She shivers, her eyes unsure and frightened. 'I... I told you no! Like last time!' She runs off into the darkness, leaving her book behind."
            ))

        elif choices == "No":
            lib.slow_type_font_color("Purple", "Monospace", self.game.alt_text(
                "The figure of light nods, 'Well, it's nice to meet you, Alasdair? Safe travels!' She waves and dissapates into the wind.",
                "She looks away, the mushroom on her head drooping ever so slightly, tears building in her eyes. 'I... I never thought you... I... Can't even muster up the words... But... Fuck you.' And she retreats back into the darkness."
            ))

            # Track visits consistently and based on game alternate mode
            if not hasattr(self, "_loris_visit"):
                self._loris_visit = 0
            if not hasattr(self, "_light_visit"):
                self._light_visit = 0

            if self.game.alt_mode:
                self._light_visit += 1
            else:
                self._loris_visit += 1

    def _n_end_event(self):
        self.console.print(self.game.alt_text(
            "You find a small cabin in the backwoods...",
            "You find the house that once belonged to you, where you and your friends once resided."
        ))
        choices = lib.select("━─┉┈◈ Do you enter the cabin? ◈┈┉─━", ["Yes", "No"])
        if choices == "Yes":
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
            self.player.coins["gold"] += 8
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
            "Ashes lie in piles, smoke still lingering in the city"
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
                "alt": "The air grows heavy, vines writhe on the ground and you feel watched."
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
        spring_choices = [
            "Yes",
            "No"
        ]
        choices = lib.select(self.game.alt_text("━─┉┈◈ Drink from the spring? ◈┈┉─━", "━─┉┈◈ Touch the liquid? ◈┈┉─━"), spring_choices)


        if choices == "Yes":
            self.console.print(self.game.alt_text( #flag here for bug
                "You feel invigorated. Your max HP has increased by 10!",
                "A sharp pain shoots up your arm, but then fades, leaving you feeling... stronger. Your attack has increased by 4!"
            ))
            if self.game.alt_mode:
                self.player.attack += 4
            else:
                self.player.max_hp += 10
                self.player.hp += 10
            self.game.save_game()
        elif choices == "No": # Changed to elif
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
        chest_choices = [
            "Yes",
            "No"
        ]
        choices = lib.select(self.game.alt_text("━─┉┈◈ Open the chest? ◈┈┉─━", "━─┉┈◈ Take the locket? ◈┈┉─━"), chest_choices)
        if choices == "Yes":
            self.console.print(self.game.alt_text(
                "Inside, you find a handful of old coins and a rare gem!",
                "The locket contains a faded portrait of a smiling child... Perhaps it was best to leave this alone."
            ))
            
            self.player.coins["gold"] += 25
            self.player.add_item("Rare Gem")
            self.game.save_game()
        if choices == "No":
            self.console.print(self.game.alt_text("You leave the chest to the swamp.", "You let the hand sink back into the depths."))

    def _explore_se(self):
        path_data = {
            "stages": 3,
            "intro_text": {
                "normal": "You follow a path towards the coast, the sound of waves growing louder.",
                "alt": "The coastline is littered with the skeletons of great sea creatures, oceans black like oil."
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
        something_choices = [
            "Yes",
            "No"
        ]
        choices =lib.select(self.game.alt_text("━─┉┈◈ Do you look through the wreakage? ◈┈┉─━", "━─┉┈◈ Do you approach the Leviathan? ◈┈┉─━"), something_choices)
        if choices == "Yes":
            self.console.print(self.game.alt_text(
                "You find a sturdy, iron-bound chest! Inside is a new piece of armor.",
                "You find a strange, pulsating organ inside the creature. It seems to be a source of great power."
            ))
            if self.game.alt_mode:
                self.player.add_item("Pulsating Organ")
            else:
                self.player.add_item("Mariner's Armor")
            self.game.save_game()
        if choices == "No":
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
        crystal_choices = [
            "Yes",
            "No"
        ]
        choices = lib.select(self.game.alt_text("━─┉┈◈ Do you enter the cave? ◈┈┉─━", "━─┉┈◈ Do you make it past the wall? ◈┈┉─━"), crystal_choices)
        if choices == "Yes":
            self.console.print(self.game.alt_text(
                "Inside, you find a vein of glowing crystals. You carefully mine a few.",
                "The light comes from a pulsating, fleshy mass. You cut a piece of it away."
            ))
            if self.game.alt_mode:
                self.player.add_item("Pulsating Shard")
            else:
                self.player.add_item("Moonstone")
            self.game.save_game()
        if choices == "No":
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
        lib.slow_type(self.game.alt_text(
            "You see shimmering water in the distance.",
            "You see a city of gold and diamond in the distance..."
        ))
        desert_choices = [
            "Yes",
            "No"
        ]
        choices = lib.select(self.game.alt_text("━─┉┈◈ Do you approach the oasis? ◈┈┉─━", "━─┉┈◈ Do you enter the city? ◈┈┉─━"), desert_choices)
        if choices == "Yes":
            lib.slow_type(self.game.alt_text(
                "You find a pool of cool, clear water. You rest and recover your strength.",
                "The city is a mirage, and you find only a single, flower growing in the sand... And yet it thrives in this suffering."
            ))
            if self.game.alt_mode:
                lib.slow_type_font_color("Purple", "Bold", "This flower is quite strange.. But you take it with you regardless, feeling some kind of importance it holds.")
                self.player.add_item("Black Lotus")
            else:
                self.player.hp = self.player.max_hp
            self.game.save_game()
        if choices == "No":
            self.console.print(self.game.alt_text("You decide the oasis is just a mirage and turn back.", "You do not trust the mirage and turn away."))

    def _explore_up(self):
        path_data = {
            "stages": 4,
            "intro_text": {
                "normal": "You fly higher into the sky, the air growing thin and cold.",
                "alt": "You use the wings of the wind. But the bitter wind leaves frost crystals left on your skin."
            },
            "stage_text": {
                "normal": "The flight is exausting, but the view is incredible.",
                "alt": "Your wings are but meerly wax, but you press on regardless."
            },
            "event_chance": 0.6,
            "end_event": self._up_end_event
        }
        return path_data
    def _up_end_event(self):
        self.console.print(self.game.alt_text(
            "You reach a cloud, where the water particles are almost soft like feathers...",
            "You reach a floating island, where the air is thin, and the place almost looks scorched. The sky is fractured as well, much like the ground below."
        ))
        plateau_choices = [
            "Yes",
            "No"
        ]
        choices = lib.select(self.game.alt_text("━─┉┈◈ Do you rest on the cloud? ◈┈┉─━", "━─┉┈◈ Do you touch the bleeding sky? ◈┈┉─━"), plateau_choices)
        if choices == "Yes":
            self.console.print(self.game.alt_text(
                "You rest on the cloud, although it threatens to drop you, it shakily holds you where you can take flight once more. Your max HP has increased by 10!",
                "You feel an odd ripple on your hand, where something attatches itself... Your attack has increased by 4!"
            ))
            if self.game.alt_mode:
                self.player.attack += 4
            else:
                self.player.max_hp += 10
                self.player.hp += 10
            self.game.save_game()
        if choices == "No":
            self.console.print(self.game.alt_text("You decide not to rest and continue on.", "You step away from the bleeding sky."))
#flag here for more work


    def _explore_down(self):
        path_data = {
            "stages": 4,
            "intro_text": {
                "normal": "You descend into a dark chasm, the light fading as you go deeper.",
                "alt": "You descend into the veins of the earth, the darkness swallowing all light, but thankfully you have your lantern."
            },
            "stage_text": {
                "normal": "The air grows colder and damper as you go deeper.",
                "alt": "The darkness is oppressive, and the walls almost feel... Watching."
            },
            "event_chance": 0.6,
            "end_event": self._down_end_event
        }
        return path_data
    def _down_end_event(self):
        # If player is Astar (special save), show alt text; otherwise normal
        is_astar = (self.player.name == "Astar")
        if not is_astar:
            self.console.print(self.game.alt_text(
                "You reach the bottom of the chasm, where a pool of black sludge splashes against grimstone.",
                "You reach the heart, where a pool of lava bubbles, but you can still push past."
            ))
        if is_astar:
            lib.slow_type_font_color("Red", "Bold", "Welcome home.")


        spring_choices = [
            "Yes",
            "No"
        ]
        choices = lib.select(self.game.alt_text("━─┉┈◈ Pɛʀֆɨֆȶ? ◈┈┉─━", "━─┉┈◈ Persist? ◈┈┉─━"), spring_choices)
        if choices == "Yes":
            self.console.print(self.game.alt_text(
                "You push past the sludge, feeling as though...",
                "...Something is walking your same path."
            ))
            if self.game.alt_mode:
                self.player.attack += 4
                self.game.save_game()
                if self.game.act != 4:
                    lib.slow_type_font_color("Red", "Bold", self.game.alt_text(
                        "You wretch as you feel the liquid leave your body, and resurface",
                    ))
                    self._explore_heart()
            else:
                self.player.max_hp += 10
                self.player.hp += 10
                self._explore_heart()
            self.game.save_game()
        if choices == "No":
            self.console.print(self.game.alt_text("You decide to leave the sludge untouched.", "You back away slowly."))


    def _explore_heart(self):
        path_data = {
            "stages": 5,
            "intro_text": {
                "normal": "You venture into the heart of the world. The walls pulse with a strange energy.",
                "alt": "You step into the heart. The walls pulse with a sickly light, and the air is thick with the scent of decay."
            },
            "stage_text": {
                "normal": "The air is thick with danger and the unknown.",
                "alt": "The air is thick with memory and regret."
            },
            "event_chance": 0.7,
            "end_event": self._heart_end_event
        }
        return path_data

    def _heart_end_event(self):
        lib.slow_type_font_color("Red", "Bold", self.game.alt_text(
            "You find...",
            "Yourself, glancing through a mirror..."
        ))
    def _explore_past(self):
        if self.game.act == 4:
            self.game.past_explore()
            self.game.act = 5
            lib.slow_type_font_color("Red", "Bold", self.game.alt_text(
                "━─┉┈◈ Act 5 ◈┈┉─━",
                "━─┉┈◈ Act 5 ◈┈┉─━"
            ))
            lib.slow_type_font_color("Red", "Bold", self.game.alt_text(
                "...Is there much to say?",
                "...Is there much left to say?"
            ))
            lib.slow_type_font_color("Red", "Bold", self.game.alt_text(
                "You touch the mirror, where your reflection stares back at you...",
                "And you see a kinder version of yourself looking back."
            ))
            self.game.save_game()
            lib.slow_type_font_color("Blue", "Bold", self.game.alt_text(
                "And yet... Something feels different.",
                "And yet... Something feels... Final"
            ))
            lib.slow_type_font_color("Red", "Bold", self.game.alt_text(
                "...................................",
                "..................................."
            ))
            lib.slow_type_font_color("Red", "Monospace", self.game.alt_text(
                "You stand at the other side of the mirror, looking back as the darkness closes in... Yet it's calm this time",
                "You stand at the other side of the mirror, looking back as the darkness recedes"
            ))
            lib.slow_type_font_color("Purple", "Monospace", self.game.alt_text(
                "Yet even in this place, there will always be another side to face, another darker aspect",
                "And you walk away, leaving your fears behind..."
            ))
            lib.slow_type_font_color("Purple", "Monospace", self.game.alt_text(
                "..................................",
                ".................................."
            ))
            lib.slow_type_font_color("Yellow", "Bold", self.game.alt_text(
                "Yet no one will write your story for you.",
                "You see your friends, they worried about you..."
            ))
            lib.slow_type_font_color("Red", "Glitch", self.game.alt_text(
                "'And you still look yourself in the mirror, and see your reflection tinted with hate..."
                "Your friends, family, they all love you. They never held grudges that you think they do..."
            ))
            lib.slow_type_font_color("Magenta", "Fancy", self.game.alt_text(
                "'Imbrace your flaws, mistakes, and try to be a better person.'",
                "You aren't a failure, or a monster, you are just... You."
            ))
            choices_final = [
                "Become whole again",
                "Become whole again"
            ]
            choices = lib.select(self.game.alt_text("━─┉┈◈ Do you step through the mirror? ◈┈┉─━", "━─┉┈◈ Do you step through the mirror? ◈┈┉─━"), choices_final)
            if choices == "Become whole again":
                lib.slow_type_font_color("Magenta", "Fancy", self.game.alt_text(
                    "Thank you for playing Voidfallen."
                    "Thank you for playing Voidfallen."
                ))


        else:
            self.console.print(self.game.alt_text(
                "The way to the past is blocked.",
                "The mirror remains shattered, refusing to show you anything."
            ))



    def _explore_village(self):
        if not self.game.village_visited_first_time:
            self.console.print(self.game.alt_text(
                "You arrive at a small village. Lanterns flicker in the dusk, and villagers eye you warily.",
                "You arrive at the empty village. Lanterns flicker, but no one is there."
            ))
            self.console.print(self.game.alt_text(
                "A shopkeeper waves you over: 'Looking for supplies, traveler?'",
                "A figure stands in the shop, face hidden. 'Looking for something? Maybe it's the thing you broke in this world.'"
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
            self.game.act = 3
            lib.slow_type_font_color("Red", "Bold", self.game.alt_text(
                "━─┉┈◈ Act 3 ◈┈┉─━",
                "━─┉┈◈ Act 3 ◈┈┉─━"
            ))
            lib.slow_type_font_color("Red", "Bold", self.game.alt_text(
                "You have unlocked the Cavern",
                "You have unlocked the Flesh"
            ))
            lib.slow_type_font_color("Red", "Bold", self.game.alt_text(
                "You hear a faint roar from the sky, something is coming...",
                "Something makes you feel as if this is far from the end."
            ))
            self.game.save_game()
        else:
            self.console.print(self.game.alt_text(
                "The cavern is not yet accessible.",
                "The flesh is not yet ready for you."
            ))

    def _explore_volcano(self):
        if self.game.act != 3:
            self.console.print(self.game.alt_text(
                "The way to the volcano is blocked.",
                "The bleeding mountain denies you."

            ))
            return
        if self.game.act == 3:
            slow_type_font_color("Red", "Bold", self.game.alt_text(
                "━─┉┈◈ Act 4 ◈┈┉─━",
                "━─┉┈◈ Act 4 ◈┈┉─━",
                self.game.act == 4
            ))
            slow_type_font_color("Red", "Bold", self.game.alt_text(
                "The dragon lies within the depths of the volcano, for you will be the one to slay it.",
                "Face your fate, for this is the final act."
            ))

            slow_type_font_color("Red", "Bold", self.game.alt_text(
                "You have unlocked the Volcano, and the skylands!",
                "You have unlocked the Bleeding Mountain, and the Depths!"
            ))

        self.console.print(self.game.alt_text(
            "You begin the treacherous climb up the volcano. The air is hot and smells of sulfur.",
            "You ascend the bleeding mountain... The air is thick with the stench of burnt flesh and regret."
        ))

        ascent_progress = 0
        max_ascent = 3

        while ascent_progress < max_ascent:
            self.console.print(f"\nYou are {ascent_progress}/{max_ascent} of the way up the volcano.")
            volcano_choices = [
                "Yes",
                "No"
            ]
            choice = lib.select("━─┉┈◈ Do you continue to accend? ◈┈┉─━", volcano_choices)

            if choice == "Yes":
                ascent_progress += 1
                self.console.print(self.game.alt_text(
                    "You continue your ascent, the heat growing more intense.",
                    "You climb higher, the fleshy ground squirming beneath your feet."
                ))
                if random.random() < 0.6:
                    self.game.battle(self.game.scale_enemy(volcano=True))
                if self.player.hp <= 0:
                    return
            elif choice == "No":
                self.console.print(self.game.alt_text(
                    "You carefully climb back down, leaving the volcano for another day.",
                    "You retreat from the bleeding mountain."
                ))
                return
            else:
                self.console.print("Invalid choice.")

        if self.game.alt_mode:
            boss = {"name": "Azrael, Archangel of death", "hp": 9999, "attack": 999, "boss": True}
            azrael_battle = AzraelBattle(self.player, boss, self.game)
            azrael_battle.run()
            return # End exploration after this special battle
        else:
            boss = {"name": "Ancient Dragon", "hp": 1000, "attack": 30, "boss": True}
        
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
