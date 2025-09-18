document.addEventListener('DOMContentLoaded', () => {
    const output = document.getElementById('output');
    const commandInput = document.getElementById('command-input');

    // --- Helper Functions ---
    function printToTerminal(text, isCommand = false) { /* ... */ }

    // --- Player Class (remains the same) ---
    class Player { /* ... */ }

    // --- Exploration Class (remains the same) ---
    class Exploration { /* ... */ }

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
                // In a real implementation, we'd have a sub-state for item selection
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
            const playerDamage = Math.floor(Math.random() * 4) + this.player.attack;
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
                // In a real game, this would go to a game over screen or load last save
                this.game.state = 'main_menu';
                this.game.start();
                return;
            }
            // After battle, return to previous state
            this.game.state = this.game.previousState;
            this.game.currentBattle = null;
            if (this.game.state === 'traversing_path') {
                 printToTerminal(`You are ${this.game.pathProgress}/${this.game.currentPath.stages} of the way. (continue/leave)`);
            }
        }
    }

    // --- Game Class ---
    class Game {
        constructor() {
            this.player = new Player();
            this.exploration = new Exploration();
            this.state = 'main_menu';
            this.previousState = 'main_menu';
            this.currentPath = null;
            this.pathProgress = 0;
            this.currentBattle = null;
        }

        handleCommand(command) {
            const cleanCommand = command.trim().toLowerCase();
            printToTerminal(command, true);

            if (this.state === 'in_battle') {
                this.currentBattle.handleCommand(cleanCommand);
            } else if (this.state === 'main_menu') {
                this.handleMainMenu(cleanCommand);
            } else if (this.state.startsWith('intro_')) {
                this.handleIntro(cleanCommand);
            } else if (this.state === 'playing') {
                this.handlePlaying(cleanCommand);
            } else if (this.state === 'traversing_path') {
                this.handleTraversal(cleanCommand);
            } else if (this.state === 'awaiting_input') {
                const nextStep = endEvents[this.nextState];
                if (nextStep) nextStep(this, cleanCommand);
            } else {
                printToTerminal(`Unknown game state: ${this.state}`);
            }
        }

        startBattle() {
            const enemy = this.scaleEnemy();
            this.previousState = this.state; // Save the state before battle
            this.currentBattle = new Battle(this, enemy);
            this.currentBattle.start();
        }
        
        // ... other Game methods like start, saveGame, loadGame, scaleEnemy, etc. remain the same ...
    }

    // --- Initial Load and Stubs ---
    const game = new Game();
    // ... (The rest of the file, including stubs and event listeners, remains the same)
});
