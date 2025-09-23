import { printToTerminal } from './ui.js';
import Player from './player.js';
import Battle from './battle.js';
import { locations, endEvents } from './locations.js';
import Exploration from './exploration.js'; // Import Exploration

// --- Game Class ---
class Game {
    constructor() {
        this.player = new Player();
        this.exploration = new Exploration(this); // Pass game instance to Exploration
        this.state = 'main_menu';
        this.previousState = 'main_menu';
        this.currentPath = null;
        this.pathProgress = 0;
        this.currentBattle = null;
        this.alt_mode = false;
        this.act = 1;
        this.developer_mode = false;
        this.difficulty = "normal";
        this.shop_prices = {
            "Potion": 10,
            "Bandage": 5,
            "Lantern": 20,
            "Silk": 2,
            "Animal Fat": 3
        };
        this.weapon_tiers = {
            "Rusty": {"bonus": 2, "names": ["Sword", "Axe"]},
            "Iron": {"bonus": 5, "names": ["Sword", "Axe"]},
            "Steel": {"bonus": 10, "names": ["Sword", "Axe"]}
        };
        this._shop_visited = 0;
    }
        alt_text(normal, alt) {
            return this.alt_mode ? alt : normal;
        }

        handleCommand(command) {
            const cleanCommand = command.trim().toLowerCase();
            printToTerminal(`> ${command}`, 'command');

            if (this.state === 'in_battle') {
                this.currentBattle.handleCommand(cleanCommand);
            } else if (this.state === 'main_menu') {
                this.handleMainMenu(cleanCommand);
            } else if (this.state.startsWith('intro_')) {
                this.handleIntro(cleanCommand);
            } else if (this.state === 'playing') {
                this.handlePlaying(cleanCommand);
            } else if (this.state === 'traversing_path') {
                if (cleanCommand === 'continue') {
                    this.pathProgress++;
                    if (this.pathProgress >= this.currentPath.stages) {
                        const endEvent = endEvents[this.currentPath.end_event];
                        if (endEvent) {
                            endEvent(this);
                        } else {
                            printToTerminal("You have reached the end of the path.", 'location');
                            this.state = 'playing';
                            this.showLocation();
                        }
                    } else {
                        printToTerminal(this.alt_text(this.currentPath.stage_text.normal, this.currentPath.stage_text.alt), 'narrative');
                        if (!this.random_event()) { // Only trigger battle if no other random event occurred
                            if (Math.random() < this.currentPath.event_chance) {
                                this.startBattle();
                            }
                        }
                    }
                } else if (cleanCommand === 'leave') {
                    this.state = 'playing';
                    printToTerminal("You leave the path and return to the crossroads.", 'narrative');
                    this.showLocation();
                } else {
                    printToTerminal("Invalid command.", 'dialogue');
                }
            } else if (this.state === 'village') {
                this.handleVillage(cleanCommand);
            } else if (this.state === 'shop') {
                this.handleShop(cleanCommand);
            } else if (this.state === 'crafting') {
                this.handleCrafting(cleanCommand);
            } else if (this.state === 'developer') {
                this.handleDeveloper(cleanCommand);
            } else if (this.state === 'cavern') {
                this.handleCavern(cleanCommand);
            } else if (this.state === 'volcano') {
                this.handleVolcano(cleanCommand);
            } else if (this.state === 'options') {
                this.handleOptions(cleanCommand);
            } else if (this.state === 'awaiting_input') {
                if (this.nextState.startsWith('equip_armor_')) {
                    const armorName = this.nextState.replace('equip_armor_', '').replace(/_/g, ' ');
                    this._handleEquipResponse('armor', armorName, cleanCommand);
                } else if (this.nextState.startsWith('equip_tool_')) {
                    const toolName = this.nextState.replace('equip_tool_', '').replace(/_/g, ' ');
                    this._handleEquipResponse('tool', toolName, cleanCommand);
                } else if (this.nextState.startsWith('equip_pet_')) {
                    const petName = this.nextState.replace('equip_pet_', '').replace(/_/g, ' ');
                    this._handleEquipPetResponse(petName, cleanCommand);
                } else {
                    const nextStep = endEvents[this.nextState];
                    if (nextStep) {
                        if (cleanCommand === 'yes') {
                            nextStep(this, 'yes');
                        } else if (cleanCommand === 'no') {
                            nextStep(this, 'no');
                        } else {
                            printToTerminal("Please answer yes or no.", 'dialogue');
                        }
                    } else {
                        printToTerminal(`Error: nextState ${this.nextState} not found.`, 'combat');
                    }
                }
            } else {
                printToTerminal(`Unknown game state: ${this.state}`, 'combat');
            }
        }

        startBattle(options = {}) {
            const enemy = options.boss || this.scaleEnemy(options);
            this.previousState = this.state; // Save the state before battle
            this.currentBattle = new Battle(this, enemy);
            this.currentBattle.start();
        }

        scaleEnemy(options = {}) {
            const { act = this.act, cavern = false, rare = false, volcano = false } = options;
            let lvl = this.player.level;
            if (volcano) {
                lvl = Math.max(lvl, 20);
            }

            let enemy_list, base_hp, base_attack, hp_scale, atk_scale;

            if (this.alt_mode) {
                if (volcano) {
                    enemy_list = ["Charred Soul", "Burnned", "Flickering shadow"];
                    base_hp = 60;
                    base_attack = 20;
                    hp_scale = 25;
                    atk_scale = 8;
                } else if (cavern || rare) {
                    enemy_list = [
                        "Soul Of The Cursed", "Watcher", "Flesh Moth", "The Shattered", "..."
                    ];
                    base_hp = 18;
                    base_attack = 7;
                    hp_scale = 6;
                    atk_scale = 3;
                } else if (act === 2) {
                    enemy_list = [
                        "Guarded Soul", "The Forgotten", "Hollow Priest", "Bleeding Idol", "The Feasting"
                    ];
                    base_hp = 50;
                    base_attack = 18;
                    hp_scale = 22;
                    atk_scale = 7;
                } else {
                    enemy_list = [
                        "Fractured Creature", "Boiled Blood", "Weeping Entity", "Lost Whisper"
                    ];
                    base_hp = 28;
                    base_attack = 9;
                    hp_scale = 13;
                    atk_scale = 4;
                }
            } else {
                if (volcano) {
                    enemy_list = ["Wandering Tendril", "Lost Soul Of Determination", "Seared figure", "The Melted"];
                    base_hp = 50;
                    base_attack = 15;
                    hp_scale = 20;
                    atk_scale = 6;
                } else if (cavern || rare) {
                    enemy_list = ["Winged Horror", "Cursed Winged Horror", "Shifting Roots", "Nightcrawler", "Damned Soul"];
                    base_hp = 12;
                    base_attack = 4;
                    hp_scale = 4;
                    atk_scale = 2;
                } else if (act === 2) {
                    enemy_list = ["Lost soul", "Forgotten entity", "Wind whispers", "Specter", "Abyssal Creature"];
                    base_hp = 40;
                    base_attack = 12;
                    hp_scale = 18;
                    atk_scale = 5;
                } else { // Act 1
                    enemy_list = ["Shadow", "Shade", "Figure", "Creature"];
                    base_hp = 20;
                    base_attack = 5;
                    hp_scale = 10;
                    atk_scale = 2;
                }
            }

            let hp = base_hp + lvl * hp_scale;
            let attack = base_attack + lvl * atk_scale;

            if (this.difficulty === "easy") {
                hp = Math.floor(hp * 0.5);
                attack = Math.floor(attack * 0.5);
            } else if (this.difficulty === "hard") {
                attack = Math.floor(attack * 2);
            }

            return {
                name: enemy_list[Math.floor(Math.random() * enemy_list.length)],
                hp: Math.max(1, hp),
                attack: Math.max(1, attack),
            };
        }

        handlePlaying(command) {
            const location = locations[command];
            if (location) {
                this.currentPath = location;
                this.pathProgress = 0;
                this.state = 'traversing_path';
                printToTerminal(this.alt_text(location.intro_text.normal, location.intro_text.alt), 'location');
                printToTerminal(`You are 0/${location.stages} of the way. (continue/leave)`, 'narrative');
            } else if (command === 'inventory') {
                this.player.displayInventory();
            } else if (command === 'craft') {
                this.state = 'crafting';
                this.displayCraftingMenu();
            } else if (command === 'dev') {
                this.state = 'developer';
                this.displayDeveloperCommands();
            } else if (command === 'cavern') {
                this.cavern_explore();
            } else if (command === 'volcano') {
                this.volcano_explore();
            } else {
                printToTerminal("Invalid direction.", 'dialogue');
            }
        }

        showLocation() {
            printToTerminal(this.alt_text("\nYou stand at a crossroads. Where will you go?", "\nYou stand at the fracture. Where will you wander?"), 'location');
            printToTerminal(this.alt_text("Directions: n, ne, e, se, s, sw, w, nw", "Directions: n, ne, e, se, s, sw, w, nw"), 'narrative');
        }

        handleVillage(command) {
            if (command === 'shop') {
                this.state = 'shop';
                printToTerminal("You enter the shop. The shopkeeper greets you.", 'dialogue');
                this.displayShop();
            } else if (command === 'rest') {
                this.player.hp = this.player.max_hp;
                printToTerminal("You rest at the inn. Your health is fully restored!", 'event');
                this.saveGame();
            } else if (command === 'leave') {
                this.state = 'playing';
                printToTerminal("You leave the village and return to the crossroads.", 'narrative');
                this.showLocation(); // You'll need to implement showLocation
            } else {
                printToTerminal("Invalid command in the village.", 'dialogue');
            }
        }

        displayShop() {
            this._displayShopGreeting();
            printToTerminal(`Your gold: ${this.player.coins.gold}`, 'narrative');
            for (const item in this.shop_prices) {
                printToTerminal(`${item}: ${this.shop_prices[item]} gold`, 'narrative');
            }
            printToTerminal("Type 'buy [item]' to purchase, 'inventory' to view your items, or 'leave' to exit.", 'narrative');
        }



        handleShop(command) {
            const parts = command.split(' ');
            const action = parts[0];
            const item = parts.slice(1).join(' ').replace(/\b\w/g, l => l.toUpperCase());

            if (action === 'buy') {
                const price = this.shop_prices[item];
                if (price) {
                    if (this.player.can_afford(price)) {
                        this.player.spend_gold(price);
                        this.player.addItem(item);
                        printToTerminal(this.alt_text(
                            `'A fine choice! One ${item} for ${price} gold.'`,
                            `'Take it. It won't help what's coming for all of us.'`
                        ), 'event');
                        this.saveGame();
                    } else {
                        printToTerminal(this.alt_text(
                            "'Sorry friend, you don't have enough gold for that.'",
                            "'...Lest you struggle with what you have.'"
                        ), 'dialogue');
                    }
                } else {
                    printToTerminal(this.alt_text(
                        "'I don't sell that here, friend.'",
                        "'...'"
                    ), 'dialogue');
                }
            } else if (action === 'leave') {
                printToTerminal(this.alt_text(
                    "'Safe travels, stranger!' the shopkeeper calls as you leave.",
                    "'Don't come back...'"
                ), 'narrative');
                this.state = 'village';
                printToTerminal("You leave the shop and return to the village square.", 'narrative');
            } else {
                printToTerminal("Invalid shop command.", 'dialogue');
            }
        }

        _displayShopGreeting() {
            this._shop_visited++;
            printToTerminal(this.alt_text(
                "\nThe shopkeeper greets you with a toothy grin.",
                "\nThe figure is cloaked in long robes, of which look tattered and worn, burned even."
            ), 'dialogue');
            if (this._shop_visited === 1) {
                printToTerminal(this.alt_text(
                    "'Welcome to my humble shop! Look around, and see if anything interests you.'",
                    "'You know what you need.'"
                ), 'dialogue');
            } else {
                const pname = this.player.name || "traveler";
                printToTerminal(this.alt_text(
                    `'Ah, ${pname}, back again? See anything new you'd like?'`,
                    `'You again, ${pname}... Were you expecting something different this time?'`
                ), 'dialogue');
            }
        }

        setDifficulty(newDifficulty) {
            const validDifficulties = ["easy", "normal", "hard"];
            if (validDifficulties.includes(newDifficulty)) {
                this.difficulty = newDifficulty;
                printToTerminal(`Difficulty set to ${newDifficulty.toUpperCase()}.`, 'event');
            } else {
                printToTerminal("Invalid difficulty. Choose from easy, normal, hard.", 'dialogue');
            }
        }

        saveGame() {
            try {
                localStorage.setItem('voidfallen_save', JSON.stringify(this.player));
                printToTerminal("Game saved!", 'event');
            } catch (e) {
                printToTerminal("Error saving game.", 'combat');
            }
        }

        loadGame() {
            try {
                const savedData = localStorage.getItem('voidfallen_save');
                if (savedData) {
                    const data = JSON.parse(savedData);
                    // Manually assign properties to ensure methods are preserved
                    for (const key in data) {
                        if (this.player.hasOwnProperty(key)) {
                            this.player[key] = data[key];
                        }
                    }
                    printToTerminal("Game loaded!", 'event');
                    return true;
                } else {
                    printToTerminal("No saved game found.", 'dialogue');
                    return false;
                }
            } catch (e) {
                printToTerminal("Error loading game.", 'combat');
                return false;
            }
        }

        random_event() {
            const events = [];

            // Very rare cutscene: 0.1% chance (1 in 1000)
            if (!this.alt_mode) {
                events.push({ chance: 0.001, handler: () => this._handle_rare_cutscene() });
            }

            // 8% chance: find a chest
            events.push({ chance: 0.08, handler: () => this._handle_chest_event() });

            // 2% chance: find a pet
            events.push({ chance: 0.10, handler: () => this._handle_pet_event() });

            // Rare cavern enemies in Act 2 overworld
            if (this.act === 2) {
                events.push({ chance: 0.13, handler: () => this._handle_rare_enemy_event() });
            }

            // Sort events by chance in descending order to ensure correct priority
            events.sort((a, b) => b.chance - a.chance);

            const roll = Math.random();
            for (const event of events) {
                if (roll < event.chance) {
                    event.handler();
                    return true;
                }
            }
            return false;
        }

        _handleEquipResponse(itemType, itemName, response) {
            if (response === 'yes') {
                this.player.equip(itemType, itemName);
                printToTerminal(`You equipped the ${itemName}.`, 'event');
            } else {
                this.player.addItem(itemName); // Add to inventory if not equipped
                printToTerminal(`You leave the ${itemName} in your pack.`, 'narrative');
            }
            this.saveGame();
            this.state = 'playing';
            this.showLocation();
        }

        getRandomInt(min, max) {
            return Math.floor(Math.random() * (max - min + 1)) + min;
        }

        getRandomChoice(list) {
            return list[Math.floor(Math.random() * list.length)];
        }

        _handle_rare_cutscene() {
            this._display_dark_mode_cutscene_text();
            this.alt_mode = true;  // Activate alternate mode
        }

        _display_dark_mode_cutscene_text() {
            printToTerminal("\n--- Something... Reaches... Out... ---", 'event');
            printToTerminal("...You.", 'event');
            printToTerminal("Why are you still here? After what you did?", 'event');
            printToTerminal(`  'You do not belong here, #s###...'  `, 'event');
            printToTerminal("This is my world now. Remember when you handed it over to me ##t#?", 'event');
            printToTerminal("You can try, but you will never leave. Not in soul, not in sight. We remember what you did, friend.", 'event');
            printToTerminal("The world seems to shift and struggle beneath your feet... Everything feels... wrong.", 'event');
        }

        _handle_chest_event() {
            const loot_types = ["Potion", "Gold", "Lantern", "Armor", "Tool"];
            const weights = [3, 3, 2, 1, 1];
            let chosen_loot_type = '';

            // Manual weighted random choice
            let totalWeight = weights.reduce((sum, w) => sum + w, 0);
            let rand = Math.random() * totalWeight;
            for (let i = 0; i < loot_types.length; i++) {
                if (rand < weights[i]) {
                    chosen_loot_type = loot_types[i];
                    break;
                }
                rand -= weights[i];
            }

            if (chosen_loot_type === "Gold") {
                const amount = this.getRandomInt(5, 20);
                this.player.coins.gold += amount;
                printToTerminal(`You find a hidden chest! Inside is ${amount} gold coins.`, 'event');
            } else if (chosen_loot_type === "Armor") {
                const armor = this.getRandomChoice(["Leather Vest", "Iron Plate", "Void Cloak"]);
                printToTerminal(`You find a hidden chest! Inside is a piece of armor: ${armor}.`, 'event');
                this.ask_yes_no(`Do you want to equip the ${armor}?`, `equip_armor_${armor.replace(/ /g, '_')}`);
            } else if (chosen_loot_type === "Tool") {
                const tier_name = this.getRandomChoice(Object.keys(this.weapon_tiers));
                const weapon_name = this.getRandomChoice(this.weapon_tiers[tier_name]["names"]);
                const full_tool_name = `${tier_name} ${weapon_name}`;
                printToTerminal(`You find a hidden chest! Inside is a tool: ${full_tool_name}.`, 'event');
                this.ask_yes_no(`Do you want to equip the ${full_tool_name}?`, `equip_tool_${full_tool_name.replace(/ /g, '_')}`);
            } else {
                this.player.addItem(chosen_loot_type);
                printToTerminal(`You find a hidden chest! Inside is 1 ${chosen_loot_type}.`, 'event');
            }
            this.saveGame();
        }

        _handle_pet_event() {
            const possible_pets = ["Void Cat", "Spectral Fox", "Tiny Dragon"];
            const found_pet = this.getRandomChoice(possible_pets);
            printToTerminal(`You hear a strange noise... A ${found_pet} appears and seems to like you!`, 'event');
            this.ask_yes_no(`Do you want to equip the ${found_pet} as your companion?`, `equip_pet_${found_pet.replace(/ /g, '_')}`);
        }

        _handleEquipPetResponse(petName, response) {
            if (response === 'yes') {
                this.player.equip('pet', petName);
                printToTerminal(`You equipped the ${petName} as your companion.`, 'event');
            } else {
                printToTerminal(`The ${petName} scurries away into the shadows.`, 'narrative');
            }
            this.saveGame();
            this.state = 'playing';
            this.showLocation();
        }

        _handle_rare_enemy_event() {
            printToTerminal("You sense something scrawling near...", 'combat');
            this.startBattle({ cavern: true, rare: true });
        }

        _create_astar_save() {
            const astar_data = {
                name: "Astar",
                backstory: "A sinning soul",
                hp: 300,
                max_hp: 300,
                exp: 0,
                level: 30,
                attack: 50,
                inventory: { "Potion": 10, "Bandage": 5, "Ectoplasm": 1 },
                coins: { "gold": 1000, "silver": 0, "bronze": 0, "zinc": 0 },
                unlocked_rest: true,
                pet: "Spectral Fox",
                armor: "Void Cloak",
                tool: "Legendary Ancient Key",
                lantern_on: true,
                lantern_fuel: 20,
                poison_turns: 0,
                bleed_turns: 0,
                act: 2,
                alt_mode: true,
                developer_mode: this.developer_mode
            };
            localStorage.setItem('voidfallen_save', JSON.stringify(astar_data));
            printToTerminal("Astar's fate has been sealed...", 'event');
        }

        displayCraftingMenu() {
            printToTerminal("--- Crafting ---", 'location');
            printToTerminal("Options: bandage, exit", 'narrative');
        }

        handleCrafting(command) {
            if (command === 'bandage') {
                if (this.player.inventory['Silk'] >= 2) {
                    this.player.inventory['Silk'] -= 2;
                    this.player.addItem('Bandage');
                    printToTerminal("You crafted a bandage from 2 silk.", 'event');
                    this.saveGame();
                } else {
                    printToTerminal("You don't have enough silk.", 'dialogue');
                }
            } else if (command === 'exit') {
                this.state = 'playing';
                this.showLocation();
            } else {
                printToTerminal("Invalid crafting command.", 'dialogue');
            }
        }

        displayDeveloperCommands() {
            printToTerminal("--- Developer Commands ---", 'location');
            printToTerminal("Commands: give [item] [qty], gold [amt], heal [amt], equip [type] [name], goto [loc], stats, craft bandage, darkmode, boss, give pet, level [amt], save, exit", 'narrative');
        }

        handleDeveloper(command) {
            const parts = command.split(' ');
            const cmd = parts[0];

            if (cmd === 'exit') {
                this.state = 'playing';
                this.showLocation();
            } else if (cmd === 'give') {
                this._dev_give(parts);
            } else if (cmd === 'gold') {
                this._dev_gold(parts);
            } else if (cmd === 'heal') {
                this._dev_heal(parts);
            } else if (cmd === 'equip') {
                this._dev_equip(parts);
            } else if (cmd === 'goto') {
                this._dev_goto(parts);
            } else if (cmd === 'stats') {
                this._dev_stats();
            } else if (command === 'craft bandage') {
                this._dev_craft_bandage();
            } else if (cmd === 'darkmode') {
                this._dev_darkmode();
            } else if (cmd === 'boss') {
                this._dev_boss(parts);
            } else if (command === 'give pet') {
                this._dev_give_pet(parts);
            } else if (cmd === 'level') {
                this._dev_set_level(parts);
            } else if (cmd === 'save') {
                this._dev_save();
            } else {
                printToTerminal("Unknown command.", 'dialogue');
            }
        }

        _dev_give(parts) {
            if (parts.length >= 3) {
                const item = parts[1].replace(/\b\w/g, l => l.toUpperCase());
                try {
                    const qty = parseInt(parts[2]);
                    if (!isNaN(qty)) {
                        this.player.addItem(item, qty);
                        printToTerminal(`Gave ${qty} ${item}(s).`, 'event');
                    } else {
                        printToTerminal("Invalid quantity.", 'dialogue');
                    }
                } catch (e) {
                    printToTerminal("Invalid quantity.", 'dialogue');
                }
            } else {
                printToTerminal("Usage: give [item] [qty]", 'dialogue');
            }
        }

        _dev_gold(parts) {
            if (parts.length === 2) {
                try {
                    const amt = parseInt(parts[1]);
                    if (!isNaN(amt)) {
                        this.player.coins.gold = amt;
                        printToTerminal(`Gold set to ${amt}.`, 'event');
                    } else {
                        printToTerminal("Invalid amount.", 'dialogue');
                    }
                } catch (e) {
                    printToTerminal("Invalid amount.", 'dialogue');
                }
            } else {
                printToTerminal("Usage: gold [amount]", 'dialogue');
            }
        }

        _dev_heal(parts) {
            if (parts.length === 2) {
                try {
                    const amt = parseInt(parts[1]);
                    if (!isNaN(amt)) {
                        this.player.heal(amt);
                        printToTerminal(`Healed ${amt} HP.`, 'event');
                    } else {
                        printToTerminal("Invalid amount.", 'dialogue');
                    }
                } catch (e) {
                    printToTerminal("Invalid amount.", 'dialogue');
                }
            } else {
                printToTerminal("Usage: heal [amount]", 'dialogue');
            }
        }

        _dev_equip(parts) {
            if (parts.length >= 3) {
                const item_type = parts[1].toLowerCase();
                const item_name = parts.slice(2).join(' ').replace(/\b\w/g, l => l.toUpperCase());
                if (["armor", "tool", "pet"].includes(item_type)) {
                    this.player.equip(item_type, item_name);
                    printToTerminal(`Equipped ${item_name} as ${item_type}.`, 'event');
                } else {
                    printToTerminal("Invalid equipment type. Use 'armor', 'tool', or 'pet'.", 'dialogue');
                }
            } else {
                printToTerminal("Usage: equip [type] [name]", 'dialogue');
            }
        }

        _dev_goto(parts) {
            if (parts.length === 2) {
                const loc = parts[1];
                printToTerminal(`Teleporting to ${loc}...`, 'event');
                // Directly call the location logic
                if (loc === "n") this.exploration.explorePath(this.exploration.explore_n());
                else if (loc === "w") this.exploration.explorePath(this.exploration.explore_w());
                else if (loc === "e") this.exploration.explorePath(this.exploration.explore_e());
                else if (loc === "s") this.exploration.explorePath(this.exploration.explore_s());
                else if (loc === "nw") this.exploration.explorePath(this.exploration.explore_nw());
                else if (loc === "ne") this.exploration.explorePath(this.exploration.explore_ne());
                else if (loc === "sw") this.exploration.explorePath(this.exploration.explore_sw());
                else if (loc === "se") this.exploration.explorePath(this.exploration.explore_se());
                else if (loc === "village") this.handleVillage('enter'); // Assuming 'enter' is a valid command to enter village state
                else if (loc === "ruins") this.exploration.explorePath(this.exploration.explore_ruins());
                else if (loc === "cavern") this.cavern_explore();
                else if (loc === "volcano") this.volcano_explore();
                else if (loc === "back") this.exploration.explore_back();
                else printToTerminal("Unknown location.", 'dialogue');
            } else {
                printToTerminal("Usage: goto [location]", 'dialogue');
            }
        }

        _dev_stats() {
            printToTerminal(`Name: ${this.player.name}, HP: ${this.player.hp}/${this.player.max_hp}, Level: ${this.player.level}, EXP: ${this.player.exp}, Gold: ${this.player.coins.gold}`, 'event');
            printToTerminal("Inventory:", 'event');
            for (const item in this.player.inventory) {
                printToTerminal(`  ${item}: ${this.player.inventory[item]}`, 'event');
            }
            printToTerminal(`Pet: ${this.player.pet ? this.player.pet : 'None'}`, 'event');
            printToTerminal(`Armor: ${this.player.armor ? this.player.armor : 'None'}`, 'event');
            printToTerminal(`Tool: ${this.player.tool ? this.player.tool : 'None'}`, 'event');
            printToTerminal(`Lantern fuel: ${this.player.lantern_fuel}`, 'event');
            printToTerminal(`Lantern on: ${this.player.lantern_on ? 'Yes' : 'No'}`, 'event');
        }

        _dev_craft_bandage() {
            this.handleCrafting('bandage');
        }

        _dev_darkmode() {
            this.alt_mode = !this.alt_mode;
            printToTerminal(`Dark mode is now ${this.alt_mode ? 'ON' : 'OFF'}.`, 'event');
        }

        _dev_boss(parts) {
            const boss_name_parts = parts.slice(1);
            const boss_name = boss_name_parts.length > 0 ? boss_name_parts.join(' ').replace(/\b\w/g, l => l.toUpperCase()) : null;

            let boss;
            if (boss_name) {
                boss = { name: boss_name, hp: 500, attack: 50, boss: true };
                printToTerminal(`Spawning custom boss: ${boss_name}`, 'event');
            } else if (this.alt_mode) {
                boss = { name: "Azrael, the Death Angel", hp: 9999, attack: 999, boss: true };
                printToTerminal("Spawning Azrael, the Death Angel.", 'event');
            } else {
                boss = { name: "Ancient Dragon", hp: 300, attack: 30, boss: true };
                printToTerminal("Spawning Ancient Dragon.", 'event');
            }
            this.startBattle({ boss: boss });
        }

        _dev_give_pet(parts) {
            if (parts.length >= 3 && parts[1].toLowerCase() === "pet") {
                const pet_name = parts.slice(2).join(' ').replace(/\b\w/g, l => l.toUpperCase());
                this.player.equip('pet', pet_name);
                printToTerminal(`Gave you the pet: ${pet_name}.`, 'event');
            } else {
                printToTerminal("Usage: give pet [name]", 'dialogue');
            }
        }

        _dev_set_level(parts) {
            if (parts.length === 2) {
                try {
                    const level = parseInt(parts[1]);
                    if (!isNaN(level)) {
                        this.player.level = level;
                        printToTerminal(`Player level set to ${level}.`, 'event');
                    } else {
                        printToTerminal("Invalid level amount.", 'dialogue');
                    }
                } catch (e) {
                    printToTerminal("Invalid level amount.", 'dialogue');
                }
            } else {
                printToTerminal("Usage: level [amount]", 'dialogue');
            }
        }

        _dev_save() {
            this.saveGame();
        }

        _astar_intro() {
            printToTerminal("\n--- A New Beginning ---", 'event');
            printToTerminal("You awaken within the field, of which you do not recognize.", 'narrative');
            printToTerminal("An entity, the soft features that it once shown you, now hardened as they stare down at your form in the grass", 'narrative');
            printToTerminal("'Lost one... That was something you never were, was it?...'", 'dialogue');
            printToTerminal("'You did this.. All by playing with death...", 'dialogue');
            printToTerminal(`'I took you in with kindness, ${this.player.name}'`, 'dialogue');
            this.state = 'playing';
            this.showLocation();
        }

        cavern_explore() {
            if (this.player.inventory['Lantern'] === 0) {
                printToTerminal("It's too dark to enter the cavern without a lantern.", 'dialogue');
                return;
            }
            if (this.player.lantern_fuel <= 0) {
                printToTerminal("Your lantern is out of fuel. Find animal fat to refuel your lantern.", 'dialogue');
                return;
            }
            if (!this.player.lantern_on) {
                this.player.use_lantern();
            }

            this.state = 'cavern';
            this.cavern_path = [];
            printToTerminal("You step into the darkness, lantern held high.", 'location');
            this.displayCavernStatus();
        }

        displayCavernStatus() {
            printToTerminal(`\nLantern fuel remaining: ${this.player.lantern_fuel} turns.`, 'narrative');
            this.player.process_debuffs();
        }

        handleCavern(command) {
            if (command === 'back') {
                if (this.cavern_path.length > 0) {
                    printToTerminal("You retrace your steps...", 'narrative');
                    this.cavern_path.pop();
                    if (this.cavern_path.length === 0) {
                        printToTerminal("You have escaped the cavern safely!", 'event');
                        this.state = 'playing';
                        this.showLocation();
                    }
                } else {
                    printToTerminal("You are at the entrance and leave the cavern.", 'narrative');
                    this.state = 'playing';
                    this.showLocation();
                }
            } else if (['left', 'right', 'forward'].includes(command)) {
                this.cavern_path.push(command);
                const event_roll = Math.random();
                if (event_roll < 0.6) {
                    this.startBattle({ cavern: true });
                } else if (event_roll < 0.7) {
                    this.random_event();
                } else if (event_roll < 0.8) {
                    printToTerminal("You find a strange marking on the wall.", 'narrative');
                } else {
                    printToTerminal("The darkness presses in, but your lantern keeps it at bay.", 'narrative');
                }
            } else {
                printToTerminal("You hesitate, unsure which way to go.", 'dialogue');
            }

            this.player.lantern_fuel--;
            if (this.player.lantern_fuel <= 0) {
                printToTerminal("Your lantern flickers and goes out!", 'combat');
                if (this.cavern_path.length > 0) {
                    printToTerminal("Lost in the darkness, you stumble and collapse...", 'combat');
                    printToTerminal("You awaken at your last save point, shaken but alive.", 'narrative');
                    // loadGame() not implemented yet
                } else {
                    this.player.lantern_on = false;
                    this.state = 'playing';
                    this.showLocation();
                }
            } else {
                this.displayCavernStatus();
            }
        }

        volcano_explore() {
            this.state = 'volcano';
            this.volcano_progress = 0;
            this.max_ascent = 3;
            printToTerminal("You begin the treacherous climb up the volcano. The air is hot and smells of sulfur.", 'location');
            printToTerminal(`You are 0/${this.max_ascent} of the way up the volcano. (ascend/leave)`, 'narrative');
        }

        handleVolcano(command) {
            if (command === 'ascend') {
                this.volcano_progress++;
                if (this.volcano_progress >= this.max_ascent) {
                    let boss;
                    if (this.alt_mode) {
                        boss = { name: "Azrael, the Unyielding", hp: 9999, attack: 999, boss: true };
                    } else {
                        boss = { name: "Ancient Dragon", hp: 300, attack: 30, boss: true };
                    }
                    this.startBattle({ boss: boss });
                    // After battle, check if player won and give rewards
                    if (this.player.hp > 0) {
                        printToTerminal(this.alt_text(
                            `With a final, earth-shattering roar, the ${boss.name} collapses!`,
                            `The ${boss.name} shrieks and dissolves into ash and embers.`
                        ), 'event');
                        printToTerminal("You have conquered the volcano!", 'event');
                        printToTerminal("You are rewarded with 1000 EXP and 500 gold!", 'event');
                        this.player.gainExp(1000);
                        this.player.coins.gold += 500;
                        this.player.addItem(this.alt_mode ? "Demon Heart" : "Dragon Scale");
                        printToTerminal(`You found a ${this.alt_mode ? "Demon Heart" : "Dragon Scale"}!`, 'event');
                        this.saveGame();
                        this.state = 'playing';
                        this.showLocation();
                    }
                } else {
                    printToTerminal("You continue your ascent, the heat growing more intense.", 'narrative');
                    if (Math.random() < 0.6) {
                        this.startBattle({ volcano: true });
                    }
                    printToTerminal(`You are ${this.volcano_progress}/${this.max_ascent} of the way up the volcano. (ascend/leave)`);
                }
            } else if (command === 'leave') {
                this.state = 'playing';
                printToTerminal("You carefully climb back down, leaving the volcano for another day.", 'narrative');
                this.showLocation();
            } else {
                printToTerminal("Invalid command.");
            }
        }

        handleOptions(command) {
            const cleanCommand = command.trim().toLowerCase();
            if (['easy', 'normal', 'hard'].includes(cleanCommand)) {
                this.setDifficulty(cleanCommand);
                this.state = 'main_menu';
                printToTerminal("Returning to main menu.", 'narrative');
            } else {
                printToTerminal("Invalid difficulty. Choose from easy, normal, hard.", 'dialogue');
            }
        }
        
        handleMainMenu(command) {
            if (command === 'new game') {
                this.player = new Player(); // Reset player for new game
                this.state = 'intro_skip_prompt';
                printToTerminal("Would you like to skip the intro dialog? (yes/no)", 'dialogue');
            } else if (command === 'load game') {
                if (this.loadGame()) {
                    this.state = 'playing';
                    this.showLocation();
                }
            } else if (command === 'options') {
                this.state = 'options';
                printToTerminal("Choose a difficulty: easy, normal, hard", 'dialogue');
            } else if (command === 'quit') {
                printToTerminal("Thanks for playing!", 'event');
            } else {
                printToTerminal("Invalid command.");
            }
        }

        ask_yes_no(prompt, nextState) {
            printToTerminal(prompt, 'dialogue');
            this.nextState = nextState;
            this.state = 'awaiting_input'; // Set state to await user input
        }

        // ... other Game methods like start, saveGame, loadGame, scaleEnemy, etc. remain the same ...
    }

    // --- Initial Load and Stubs ---
    const game = new Game();

    // Initial game start
    game.start = () => {
        printToTerminal("Welcome to Voidfallen! A game by yours truly. -Moogietheboogie", 'event');
        printToTerminal("\nMain Menu Options:", 'narrative');
        printToTerminal("  Start a new game", 'narrative');
        printToTerminal("  Load a saved game", 'narrative');
        printToTerminal("  Options - game difficulty", 'narrative');
        printToTerminal("  Quit the game", 'narrative');
        printToTerminal("\nWhat would you like to do? (new game, load game, options, quit)", 'dialogue');
        commandInput.focus();
    };

                    game.handleIntro = (command) => {
                        if (game.state === 'intro_skip_prompt') {
                            if (command === 'yes') {
                                // Skip intro, directly ask for name
                                game.state = 'intro_name';
                                printToTerminal("Enter your name, lost one:", 'dialogue');
                            } else if (command === 'no') {
                                // Proceed with full intro
                                game.state = 'intro_name';
                                printToTerminal("Hello lost one, what is your name?", 'dialogue');
                            } else {
                                printToTerminal("Please answer yes or no.", 'dialogue');
                            }
                        } else if (game.state === 'intro_name') {
                            game.player.name = command;
                            if (game.player.name.toLowerCase() === "astar") {
                                game._astar_intro();
                                return;
                            }                    if (game.player.name.toLowerCase() === "moogietheboogie") {
                        game.developer_mode = true;
                        printToTerminal("✨ Developer mode activated! Welcome back #001 ✨", 'event');
                    }            printToTerminal(`Interesting name you have... ${game.player.name}`, 'dialogue');
            printToTerminal("'Where did you come from? This must be a blessing for my calls for... Nevermind'", 'dialogue');
            printToTerminal("'Tis' not often we have visitors here in this sect of the void.'", 'dialogue');
            game.state = 'intro_backstory';
        } else if (game.state === 'intro_backstory') {
            game.player.backstory = command;
            printToTerminal(`Ah... ${game.player.backstory}. It is a place I am yet to visit, though it is much beautiful from what I hear.`, 'dialogue');
            printToTerminal(`You must have come a long way from there, ${game.player.name}... Do you ever plan to go home?`, 'dialogue');
            game.state = 'intro_sit_down';
            game.ask_yes_no("'Care to sit down with me? Surely you must be frazzled after such a journey'", 'intro_sit_down_response');
        } else if (game.state === 'intro_sit_down_response') {
            if (command === 'yes') {
                printToTerminal("'Very well then.' The figure moves aside for you to join them", 'dialogue');
            } else {
                printToTerminal("'That's alright, just stay to talk, if you will.'", 'dialogue');
            }
            game.state = 'intro_aware';
            game.ask_yes_no(`Say, ${game.player.name}, have you heard what has been happening here`, 'intro_aware_response');
        } else if (game.state === 'intro_aware_response') {
            if (command === 'yes') {
                printToTerminal("So you are aware, how peculiar... Then, ", 'dialogue');
                printToTerminal(`${game.player.name}, there is an old trail up to the East. You may find an inn where you can stay.`, 'dialogue');
            } else {
                printToTerminal("Not that I would have expected you to. There are creatures from the north, they have been encroaching on our void... Slaughtering the residents.", 'dialogue');
            }
            printToTerminal("\nYou leave the clearing after giving thanks to the figure, onwards you shall go...\n", 'narrative');
            game.state = 'playing';
            game.showLocation();
        }
    };

        game.ask_yes_no = (prompt, nextState) => {
            printToTerminal(prompt, 'dialogue');
            game.nextState = nextState;
            game.state = 'awaiting_input'; // Set state to await user input
        };

// Initial call to start the game
game.start();

const commandInput = document.getElementById('command-input'); // Re-declare commandInput here

commandInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        const command = commandInput.value;
        commandInput.value = '';
        game.handleCommand(command);
    }
});
