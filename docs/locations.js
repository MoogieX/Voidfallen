const locations = {
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
        "end_event": "village_entrance"
    },
    "s": {
        "stages": 5,
        "intro_text": {
            "normal": "You venture south, drawn by a chilling breeze from a dark cave.",
            "alt": "You return to the cave where you once sought refuge. The darkness feels... familiar."
        },
        "stage_text": {
            "normal": "You delve deeper into the cave, the darkness enveloping you.",
            "alt": "The cave's oppressive silence is a constant reminder of what you've lost."
        },
        "event_chance": 0.7,
        "end_event": "cave"
    }
    // ... other locations will be added here
};

const endEvents = {
    "cabin": (game) => {
        game.state = 'awaiting_input';
        game.nextState = 'cabin_enter';
        printToTerminal("You find a small cabin. Do you enter? (yes/no)");
    },
    "cabin_enter": (game, command) => {
        if (['y', 'yes'].includes(command)) {
            printToTerminal("Inside the cabin, you find a lantern. +1 Lantern");
            game.player.addItem("Lantern");
            game.saveGame();
        } else {
            printToTerminal("You decide not to enter. The cabin looms silently.");
        }
        game.state = 'playing';
        game.showLocation();
    },
    "woods_clearing": (game) => {
        printToTerminal("You reach a clearing in the woods. A sense of peace settles over you.");
        printToTerminal("You find a small pouch of gold.");
        game.player.coins.gold += 15;
        game.saveGame();
        game.state = 'playing';
        game.showLocation();
    },
    "village_entrance": (game) => {
        printToTerminal("You arrive at the village entrance.");
        // In a more complete version, this would transition to the village state
        printToTerminal("(Village not yet implemented)");
        game.state = 'playing';
        game.showLocation();
    },
    "cave": (game) => {
        printToTerminal("You reach the deepest part of the cave. A faint light emanates from a crack in the wall.");
        printToTerminal("You find a rusty sword lodged in the stone.");
        game.player.addItem("Rusty Sword");
        game.saveGame();
        game.state = 'playing';
        game.showLocation();
    }
};
