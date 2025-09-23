export const locations = {
    "n": {
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
        "end_event": "cabin"
    },
    "w": {
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
        "end_event": "woods_clearing"
    },
    "e": {
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
        "end_event": "village"
    },
    "nw": {
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
        "end_event": "hidden_spring"
    },
    "sw": {
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
        "end_event": "swamp_chest"
    },
    "se": {
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
        "end_event": "shipwreck"
    },
    "ne": {
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
        "end_event": "mountain_cave"
    },
    "s": {
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
        "end_event": "desert_oasis"
    },
    "ruins": {
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
        "end_event": "ruins_altar"
    },
    "cavern": {
        "stages": 0, // Cavern has special exploration logic
        "intro_text": {
            "normal": "A dark cavern mouth gapes in the hillside.",
            "alt": "The flesh, it feeds."
        },
        "stage_text": {
            "normal": "",
            "alt": ""
        },
        "event_chance": 0.6,
        "end_event": "cavern_explore"
    },
    "volcano": {
        "stages": 0, // Volcano has special exploration logic
        "intro_text": {
            "normal": "A fiery volcano looms in the distance.",
            "alt": "A bleeding mountain of flesh and stone."
        },
        "stage_text": {
            "normal": "",
            "alt": ""
        },
        "event_chance": 0.6,
        "end_event": "volcano_explore"
    }
};

export const endEvents = {
    "cabin": (game) => {
        game.state = 'awaiting_input';
        game.nextState = 'cabin_enter';
        game.print("You find a small cabin. Do you enter? (yes/no)", 'location');
    },
    "cabin_enter": (game, command) => {
        if (['y', 'yes'].includes(command)) {
            game.print("Inside the cabin, you find a lantern. +1 Lantern", 'event');
            game.player.addItem("Lantern");
            game.saveGame();
        } else {
            game.print("You decide not to enter. The cabin looms silently.", 'narrative');
        }
        game.state = 'playing';
        game.showLocation();
    },
    "woods_clearing": (game) => {
        game.print("You reach a clearing in the woods. A sense of peace settles over you.", 'location');
        game.print("You find a small pouch of gold.", 'event');
        game.player.coins.gold += 15;
        game.saveGame();
        game.state = 'playing';
        game.showLocation();
    },
    "village_entrance": (game) => {
        game.print("You arrive at the village entrance.", 'location');
        // In a more complete version, this would transition to the village state
        game.print("(Village not yet implemented)");
        game.state = 'playing';
        game.showLocation();
    },
    "village": (game) => {
        game.state = 'village';
        game.print("You are in the village square. What would you like to do?");
        game.print("Options: shop, rest, leave");
    },
    "hidden_spring": (game) => {
        game.state = 'awaiting_input';
        game.nextState = 'hidden_spring_drink';
        game.print(game.alt_text("You discover a hidden spring, its water shimmering with a faint light.", "You find a pool of black, oily liquid. It ripples, though there is no wind."), 'location');
        game.print(game.alt_text("Do you drink from the spring?", "Do you touch the liquid?"), 'dialogue');
    },
    "hidden_spring_drink": (game, command) => {
        if (['y', 'yes'].includes(command)) {
            game.print(game.alt_text("You feel invigorated. Your max HP has increased by 10!", "A sharp pain shoots up your arm, but then fades, leaving you feeling... stronger. Your attack has increased by 2!"), 'event');
            if (game.alt_mode) {
                game.player.attack += 2;
            } else {
                game.player.max_hp += 10;
                game.player.hp += 10;
            }
            game.saveGame();
        } else {
            game.print(game.alt_text("You decide to leave the spring untouched.", "You back away slowly."), 'narrative');
        }
        game.state = 'playing';
        game.showLocation();
    },
    "swamp_chest": (game) => {
        game.state = 'awaiting_input';
        game.nextState = 'swamp_chest_open';
        game.print(game.alt_text("You find a half-submerged chest, covered in moss and algae.", "A skeletal hand emerges from the water, offering you a rusted locket."), 'location');
        game.print(game.alt_text("Do you open the chest?", "Do you take the locket?"), 'dialogue');
    },
    "swamp_chest_open": (game, command) => {
        if (['y', 'yes'].includes(command)) {
            game.print(game.alt_text("Inside, you find a handful of old coins and a rare gem!", "The locket contains a faded portrait of a smiling child. You feel a deep sense of loss."), 'event');
            game.player.coins.gold += 25;
            game.player.addItem("Rare Gem");
            game.saveGame();
        } else {
            game.print(game.alt_text("You leave the chest to the swamp.", "You let the hand sink back into the depths."), 'narrative');
        }
        game.state = 'playing';
        game.showLocation();
    },
    "shipwreck": (game) => {
        game.state = 'awaiting_input';
        game.nextState = 'shipwreck_search';
        game.print(game.alt_text("You come across the wreckage of a ship, half-buried in the sand.", "A beached leviathan lies on the shore, its eye staring blankly at the sky."), 'location');
        game.print(game.alt_text("Do you search the wreckage?", "Do you approach the leviathan?"), 'dialogue');
    },
    "shipwreck_search": (game, command) => {
        if (['y', 'yes'].includes(command)) {
            game.print(game.alt_text("You find a sturdy, iron-bound chest! Inside is a new piece of armor.", "You find a strange, pulsating organ inside the creature. It seems to be a source of great power."), 'event');
            if (game.alt_mode) {
                game.player.addItem("Pulsating Organ");
            } else {
                game.player.addItem("Mariner's Armor");
            }
            game.saveGame();
        } else {
            game.print(game.alt_text("You leave the shipwreck to the sea.", "You give the dead creature a wide berth."), 'narrative');
        }
        game.state = 'playing';
        game.showLocation();
    },
    "mountain_cave": (game) => {
        game.state = 'awaiting_input';
        game.nextState = 'mountain_cave_enter';
        game.print(game.alt_text("You find a small cave, a cool breeze flowing from its entrance.", "You find a crack in the mountainside, from which a faint, sickly light emanates."), 'location');
        game.print(game.alt_text("Do you enter the cave?", "Do you squeeze through the crack?"), 'dialogue');
    },
    "mountain_cave_enter": (game, command) => {
        if (['y', 'yes'].includes(command)) {
            game.print(game.alt_text("Inside, you find a vein of glowing crystals. You carefully mine a few.", "The light comes from a pulsating, fleshy mass. You cut a piece of it away."), 'event');
            if (game.alt_mode) {
                game.player.addItem("Pulsating Shard");
            } else {
                game.player.addItem("Glowing Crystal");
            }
            game.saveGame();
        } else {
            game.print(game.alt_text("You decide not to risk entering the cave.", "You back away from the unsettling light."), 'narrative');
        }
        game.state = 'playing';
        game.showLocation();
    },
    "desert_oasis": (game) => {
        game.state = 'awaiting_input';
        game.nextState = 'desert_oasis_approach';
        game.print(game.alt_text("You see a shimmering oasis in the distance.", "You see a city of gold and diamond in the distance..."), 'location');
        game.print(game.alt_text("Do you head towards the oasis?", "Do you approach the city?"), 'dialogue');
    },
    "desert_oasis_approach": (game, command) => {
        if (['y', 'yes'].includes(command)) {
            game.print(game.alt_text("You find a pool of cool, clear water. You rest and recover your strength.", "The city is a mirage, and you find only a single, wilting flower growing in the sand."), 'event');
            if (game.alt_mode) {
                game.player.addItem("Black Lotus");
            } else {
                game.player.hp = game.player.max_hp;
            }
            game.saveGame();
        } else {
            game.print(game.alt_text("You decide the oasis is just a mirage and turn back.", "You do not trust the mirage and turn away."), 'narrative');
        }
        game.state = 'playing';
        game.showLocation();
    },
    "ruins_altar": (game) => {
        game.print(game.alt_text("You discover a hidden altar, where a rare herb grows.", "You find a place of sacrifice. Something was taken from here."), 'location');
        game.player.addItem("Kingsfoil");
        game.saveGame();
        game.state = 'playing';
        game.showLocation();
    },
    "cavern_explore": (game) => {
        game.cavern_explore();
    },
    "volcano_explore": (game) => {
        game.volcano_explore();
    }
};