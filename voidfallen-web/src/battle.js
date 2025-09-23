import { printToTerminal } from './ui.js';

class Battle {
    constructor(game, enemy) {
        this.game = game;
        this.player = game.player;
        this.enemy = enemy;
        this.enemy.maxHp = enemy.hp;
        this.poison_inflictors = ["snake", "nightcrawler"];
        this.bleed_inflictors = ["winged horror"];
        this.ghost_lifesteal = ["ghost"];
        this.silk_droppers = ["nightcrawler"];
        this.animal_fat_droppers = ["winged horror"];
    }

    start() {
        this.game.state = 'in_battle';
        printToTerminal(`--- A wild ${this.enemy.name} appears! ---`, 'combat');
        this.showStatus();
    }

    showStatus() {
        printToTerminal(`Your HP: ${this.player.hp}/${this.player.maxHp} | Enemy HP: ${this.enemy.hp}/${this.enemy.maxHp}`, 'combat');
        printToTerminal("Do you (attack/item/run)?");
    }

    handleCommand(command) {
        this.player.process_debuffs();
        if (this.player.hp <= 0) {
            this.endBattle('loss');
            return;
        }

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
        printToTerminal(`You strike the ${this.enemy.name} for ${playerDamage} damage!`, 'combat');

        // Lifesteal for specific enemies if player is bleeding
        const isLifestealEnemy = this.bleed_inflictors.concat(this.ghost_lifesteal).some(inflictor => this.enemy.name.toLowerCase().includes(inflictor));
        if (this.enemy.hp > 0 && isLifestealEnemy && this.player.bleed_turns > 0) {
            const heal = 2;
            this.enemy.hp += heal;
            printToTerminal(`${this.enemy.name} absorbs ${heal} HP from your bleeding!`, 'combat');
        }

        if (this.enemy.hp <= 0) {
            this.endBattle('win');
        } else {
            this.enemyTurn();
        }
    }

    enemyTurn() {
        // Enemy turn: check for flee, then attack
        const isLowHealth = this.enemy.hp < this.enemy.maxHp * 0.2;
        if (isLowHealth && Math.random() < 0.1) {
            printToTerminal(`The ${this.enemy.name} is low on health and flees from the battle!`, 'event');
            this.endBattle('enemy_fled');
            return;
        }

        const enemyDamage = Math.floor(Math.random() * 3) + this.enemy.attack;
        this.player.take_damage(enemyDamage);
        printToTerminal(`The ${this.enemy.name} hits you for ${enemyDamage} damage!`, 'combat');

        // 25% chance to inflict debuffs
        if (this.poison_inflictors.some(inflictor => this.enemy.name.toLowerCase().includes(inflictor)) && Math.random() < 0.25) {
            this.player.poison_turns = 2;
            printToTerminal("You have been poisoned!", 'combat');
        }
        if (this.bleed_inflictors.some(inflictor => this.enemy.name.toLowerCase().includes(inflictor)) && Math.random() < 0.25) {
            this.player.bleed_turns = 2;
            printToTerminal("You are bleeding!", 'combat');
        }

        if (this.player.hp <= 0) {
            this.endBattle('loss');
        }
        else {
            this.showStatus();
        }
    }

    useItem(item) {
        item = item.toLowerCase();
        if (item === 'potion' && this.player.inventory['Potion'] > 0) {
            this.player.inventory['Potion']--
            this.player.heal(30);
            printToTerminal("You drink a potion and restore 30 HP.", 'event');
            this.enemyTurn();
        } else if (item === 'bandage' && this.player.inventory['Bandage'] > 0) {
            this.player.inventory['Bandage']--
            this.player.poison_turns = 0;
            this.player.bleed_turns = 0;
            printToTerminal("You use a bandage and cure all bleeding and poison effects!", 'event');
            this.enemyTurn();
        } else {
            printToTerminal("You don't have that item or it's not usable.");
        }
    }

    run() {
        if (Math.random() < 0.5) {
            printToTerminal("You escaped successfully!", 'event');
            this.endBattle('fled');
        } else {
            printToTerminal("You failed to escape!", 'combat');
            this.enemyTurn();
        }
    }

            endBattle(outcome) {
                if (outcome === 'win') {
                    const expGain = 10 * this.player.level;
                    const goldGain = Math.floor(Math.random() * 5 * this.player.level) + 1;
                    printToTerminal(`You defeated the ${this.enemy.name} and gained ${expGain} EXP and ${goldGain} gold!`, 'event');
                    this.player.gainExp(expGain);
                    this.player.coins.gold += goldGain;
                    this.handle_drops();
                } else if (outcome === 'loss') {
                    if (this.enemy.name === "Azrael, the Unyielding" && this.game.alt_mode) {
                        this.game._create_astar_save();
                        printToTerminal("You have been defeated... but your journey is not over.", 'combat');
                        this.game.state = 'main_menu';
                        this.game.start();
                        return;
                    } else {
                        printToTerminal("You have fallen in battle... The world fades to black.", 'combat');
                        this.game.state = 'main_menu';
                        this.game.start();
                        return;
                    }
                }
                // After battle, return to previous state
                this.game.state = this.game.previousState;
                this.game.currentBattle = null;
                if (this.game.state === 'traversing_path') {
                     printToTerminal(`You are ${this.game.pathProgress}/${this.game.currentPath.stages} of the way. (continue/leave)`);
                }
            }
    handle_drops() {
        if (this.silk_droppers.some(dropper => this.enemy.name.toLowerCase().includes(dropper))) {
            printToTerminal("You collect silk from the nightcrawler's remains.", 'event');
            this.player.addItem("Silk");
        }
        if (this.animal_fat_droppers.some(dropper => this.enemy.name.toLowerCase().includes(dropper))) {
            printToTerminal("You collect animal fat from the winged horror's remains.", 'event');
            this.player.addItem("Animal Fat");
        }
    }
}

export default Battle;
