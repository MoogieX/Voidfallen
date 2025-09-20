function printToTerminal(text, isCommand = false) {
    console.log(`Printing to terminal: ${text}`);
    const output = document.getElementById('output');
    const line = document.createElement('div');
    if (isCommand) {
        line.innerHTML = `<span class="prompt">&gt;</span> ${text}`;
    } else {
        line.textContent = text;
    }
    output.appendChild(line);
    output.scrollTop = output.scrollHeight;
}

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

const output = document.getElementById('output');
const commandInput = document.getElementById('command-input');

document.addEventListener('DOMContentLoaded', () => {

    // --- Player Class ---
    class Player {
        constructor() {
            this.name = "";
            this.backstory = "";
            this.hp = 100;
            this.maxHp = 100;
            this.exp = 0;
            this.level = 1;
            this.attack = 10;
            this.inventory = {"Potion": 2};
            this.coins = {"gold": 10, "silver": 0, "bronze": 0, "zinc": 0};
            this.unlockedRest = false;
            this.pet = null;
            this.armor = null;
            this.tool = null;
            this.lanternOn = false;
            this.lanternFuel = 0;
            this.poisonTurns = 0;
            this.bleedTurns = 0;
        }

        takeDamage(amount) {
            this.hp = Math.max(this.hp - amount, 0);
        }

        heal(amount) {
            this.hp = Math.min(this.hp + amount, this.maxHp);
        }

        addItem(name, qty = 1) {
            this.inventory[name] = (this.inventory[name] || 0) + qty;
            if (name.toLowerCase() === "lantern" && this.lanternFuel === 0) {
                this.lanternFuel = 6;
                printToTerminal("Your lantern is now fueled and ready to use! (6 turns of fuel)");
            }
        }

        equip(item) {
            if (this.inventory[item]) {
                this.tool = item;
                printToTerminal(`You have equipped the ${item}.`);
            } else {
                printToTerminal(`You don't have a ${item} in your inventory.`);
            }
        }

        gainExp(amount) {
            this.exp += amount;
            this._tryLevelUp();
        }

        _tryLevelUp() {
            while (this.exp >= this.level * 20) {
                this.exp -= this.level * 20;
                this.level++;
                this.maxHp += 20;
                this.attack += 5;
                this.hp = this.maxHp;
                printToTerminal(`You leveled up! You are now level ${this.level}.`);
            }
        }

        displayInventory() {
            printToTerminal("--- Your Inventory ---");
            if (Object.keys(this.inventory).length === 0) {
                printToTerminal("  (Empty)");
            } else {
                for (const [item, qty] of Object.entries(this.inventory)) {
                    printToTerminal(`  ${item}: ${qty}`);
                }
            }
            printToTerminal(`Equipped Armor: ${this.armor ? this.armor : 'None'}`);
            printToTerminal(`Equipped Tool: ${this.tool ? this.tool : 'None'}`);
            printToTerminal(`Equipped Pet: ${this.pet ? this.pet : 'None'}`);
            printToTerminal(`Lantern Fuel: ${this.lanternFuel} turns (On: ${this.lanternOn ? 'Yes' : 'No'})`);
            printToTerminal("----------------------");
        }
    }

    // --- Exploration Class ---
    class Exploration {
        constructor(game) {
            this.game = game;
        }

        explore(direction) {
            const pathData = locations[direction];
            if (pathData) {
                this.game.currentPath = pathData;
                this.game.pathProgress = 0;
                this.game.state = 'traversing_path';
                printToTerminal(pathData.intro_text.normal);
                printToTerminal(`You are 0/${pathData.stages} of the way. (continue/leave)`);
            } else {
                printToTerminal("You can't go that way.");
            }
        }
    }

    // --- Battle Class ---
    class Battle {
        constructor(game, enemy) {
            this.game = game;
            this.player = game.player;
            this.enemy = enemy;
            this.enemy.maxHp = enemy.hp;
        }

        start() {
            this.game.state = 'in_battle';
            printToTerminal(`--- A wild ${this.enemy.name} appears! ---`);
            this.showStatus();
        }

        showStatus() {
            printToTerminal(`Your HP: ${this.player.hp}/${this.player.maxHp} | Enemy HP: ${this.enemy.hp}/${this.enemy.maxHp}`);
            printToTerminal("Do you (attack/item/run)?");
        }

        handleCommand(command) {
            if (command === 'attack') {
                this.playerTurn();
            } else if (command === 'item') {
                printToTerminal("Use which item? (e.g., 'use potion')");
                printToTerminal(`You have: ${JSON.stringify(this.player.inventory)}`);
            } else if (command.startsWith('use ')) {
                const item = command.split(' ')[1];
                this.useItem(item);
            } else if (command === 'run') {
                this.run();
            } else {
                printToTerminal("Invalid battle command.");
            }
        }

        playerTurn() {
            let playerDamage = Math.floor(Math.random() * 4) + this.player.attack;
            if (this.player.tool === 'Rusty Sword') {
                playerDamage += 5;
            }
            this.enemy.hp = Math.max(0, this.enemy.hp - playerDamage);
            printToTerminal(`You strike the ${this.enemy.name} for ${playerDamage} damage!`);

            if (this.enemy.hp <= 0) {
                this.endBattle('win');
            } else {
                this.enemyTurn();
            }
        }

        enemyTurn() {
            const enemyDamage = Math.floor(Math.random() * 3) + this.enemy.attack;
            this.player.takeDamage(enemyDamage);
            printToTerminal(`The ${this.enemy.name} hits you for ${enemyDamage} damage!`);

            if (this.player.hp <= 0) {
                this.endBattle('loss');
            } else {
                this.showStatus();
            }
        }

        useItem(item) {
            if (item.toLowerCase() === 'potion' && this.player.inventory['Potion'] > 0) {
                this.player.inventory['Potion']--
                this.player.heal(30);
                printToTerminal("You drink a potion and restore 30 HP.");
                this.enemyTurn();
            } else {
                printToTerminal("You don't have that item or it's not usable.");
            }
        }

        run() {
            if (Math.random() < 0.5) {
                printToTerminal("You escaped successfully!");
                this.endBattle('fled');
            } else {
                printToTerminal("You failed to escape!");
                this.enemyTurn();
            }
        }

        endBattle(outcome) {
            if (outcome === 'win') {
                const expGain = 10 * this.player.level;
                const goldGain = Math.floor(Math.random() * 5 * this.player.level) + 1;
                printToTerminal(`You defeated the ${this.enemy.name} and gained ${expGain} EXP and ${goldGain} gold!`);
                this.player.gainExp(expGain);
                this.player.coins.gold += goldGain;
            } else if (outcome === 'loss') {
                printToTerminal("You have fallen in battle... The world fades to black.");
                this.game.state = 'main_menu';
                this.game.start();
                return;
            }
            this.game.state = this.game.previousState;
            this.game.currentBattle = null;
            if (this.game.state === 'traversing_path') {
                 printToTerminal(`You are ${this.game.pathProgress}/${this.game.currentPath.stages} of the way. (continue/leave)`);
            }
        }
    }

    // --- Game Class ---
    class Game {
        constructor(endEvents) {
            this.player = new Player();
            this.exploration = new Exploration(this);
            this.state = 'main_menu';
            this.previousState = 'main_menu';
            this.currentPath = null;
            this.pathProgress = 0;
            this.currentBattle = null;
            this.endEvents = endEvents;
        }

        start() {
            this.state = 'main_menu';
            printToTerminal("Voidfallen");
            printToTerminal("1. New Game");
            printToTerminal("2. Load Game");
        }

        handleMainMenu(command) {
            if (command === '1' || command === 'new game') {
                this.state = 'playing';
                this.showLocation();
            } else if (command === '2' || command === 'load game') {
                this.loadGame();
            } else {
                printToTerminal("Invalid choice.");
            }
        }

        handlePlaying(command) {
            if (['n', 'w', 'e', 's'].includes(command)) {
                this.exploration.explore(command);
            } else if (command === 'inventory') {
                this.player.displayInventory();
            } else if (command.startsWith('equip ')) {
                const item = command.split(' ')[1];
                this.player.equip(item);
            } else if (command === 'save') {
                this.saveGame();
            } else if (command === 'load') {
                this.loadGame();
            } else {
                printToTerminal("Unknown command.");
            }
        }

        handleTraversal(command) {
            if (command === 'continue') {
                this.pathProgress++;
                if (this.pathProgress >= this.currentPath.stages) {
                    const endEvent = this.endEvents[this.currentPath.end_event];
                    if (endEvent) {
                        endEvent(this);
                    } else {
                        this.state = 'playing';
                        this.showLocation();
                    }
                } else {
                    if (Math.random() < this.currentPath.event_chance) {
                        this.startBattle();
                    } else {
                        printToTerminal(`You are ${this.pathProgress}/${this.currentPath.stages} of the way. (continue/leave)`);
                    }
                }
            } else if (command === 'leave') {
                this.state = 'playing';
                this.showLocation();
            } else {
                printToTerminal("Invalid command.");
            }
        }

        showLocation() {
            printToTerminal("You are at a crossroads. Available directions: n, w, e, s");
        }

        startBattle() {
            const enemy = this.scaleEnemy();
            this.previousState = this.state;
            this.currentBattle = new Battle(this, enemy);
            this.currentBattle.start();
        }

        scaleEnemy() {
            const level = this.player.level;
            const enemies = [
                {
                    name: "Goblin",
                    hp: 30 + (level - 1) * 10,
                    attack: 5 + (level - 1) * 2,
                },
                {
                    name: "Bat",
                    hp: 20 + (level - 1) * 5,
                    attack: 8 + (level - 1) * 3,
                },
            ];
            return enemies[Math.floor(Math.random() * enemies.length)];
        }

        saveGame() {
            const gameState = {
                player: this.player,
                state: this.state,
                previousState: this.previousState,
                currentPath: this.currentPath,
                pathProgress: this.pathProgress,
            };
            localStorage.setItem('voidfallenSave', JSON.stringify(gameState));
            printToTerminal("Game saved.");
        }

        loadGame() {
            const savedState = localStorage.getItem('voidfallenSave');
            if (savedState) {
                const gameState = JSON.parse(savedState);
                this.player = Object.assign(new Player(), gameState.player);
                this.state = gameState.state;
                this.previousState = gameState.previousState;
                this.currentPath = gameState.currentPath;
                this.pathProgress = gameState.pathProgress;
                printToTerminal("Game loaded.");
                this.showLocation();
            } else {
                printToTerminal("No saved game found.");
            }
        }

    }

    const game = new Game(endEvents);
    game.start();

    commandInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const command = commandInput.value;
            const cleanCommand = command.trim().toLowerCase();
            printToTerminal(command, true);

            if (game.state === 'in_battle') {
                game.currentBattle.handleCommand(cleanCommand);
            } else if (game.state === 'main_menu') {
                game.handleMainMenu(cleanCommand);
            } else if (game.state === 'playing') {
                game.handlePlaying(cleanCommand);
            } else if (game.state === 'traversing_path') {
                game.handleTraversal(cleanCommand);
            } else if (game.state === 'awaiting_input') {
                const nextStep = game.endEvents[game.nextState];
                if (nextStep) nextStep(game, cleanCommand);
            } else {
                printToTerminal(`Unknown game state: ${game.state}`);
            }
            commandInput.value = '';
        }
    });
});
