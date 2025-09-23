import { printToTerminal } from './ui.js';

class Player {
    constructor() {
        this.name = "";
        this.backstory = "";
        this.hp = 100;
        this.max_hp = 100;
        this.exp = 0;
        this.level = 1;
        this.attack = 10;
        this.inventory = {"Potion": 2};
        this.coins = {"gold": 10};
        this.poison_turns = 0;
        this.bleed_turns = 0;
        this.lantern_on = false;
        this.lantern_fuel = 0;
        this.pet = null;
        this.armor = null;
        this.tool = null;
    }

    take_damage(amount) {
        this.hp = Math.max(this.hp - amount, 0);
    }

    heal(amount) {
        this.hp = Math.min(this.hp + amount, this.max_hp);
    }

    process_debuffs() {
        if (this.poison_turns > 0) {
            this.take_damage(1);
            this.poison_turns--;
            printToTerminal("Poison deals 1 damage to you!", 'combat');
        }
        if (this.bleed_turns > 0) {
            this.take_damage(2);
            this.bleed_turns--;
            printToTerminal("Bleeding deals 2 damage to you!", 'combat');
        }
    }

    addItem(name, qty = 1) {
        this.inventory[name] = (this.inventory[name] || 0) + qty;
        // Auto-fuel lantern when first acquired
        if (name.toLowerCase() === "lantern" && this.lantern_fuel === 0) {
            this.lantern_fuel = 6;  // Base fuel value
            printToTerminal("Your lantern is now fueled and ready to use! (6 turns of fuel)", 'event');
        }
    }

    displayInventory() {
        printToTerminal("--- Inventory ---", 'location');
        for (const item in this.inventory) {
            printToTerminal(`${item}: ${this.inventory[item]}`);
        }
        printToTerminal(`Equipped Pet: ${this.pet ? this.pet : 'None'}`);
        printToTerminal(`Equipped Armor: ${this.armor ? this.armor : 'None'}`);
        printToTerminal(`Equipped Tool: ${this.tool ? this.tool : 'None'}`);
        printToTerminal(`Lantern Fuel: ${this.lantern_fuel} turns (On: ${this.lantern_on ? 'Yes' : 'No'})`);
    }

    use_lantern() {
        if (this.inventory['Lantern'] > 0 && this.lantern_fuel > 0) {
            this.lantern_on = true;
            printToTerminal("You light your lantern. The darkness recedes.", 'event');
        } else if (this.inventory['Lantern'] > 0) {
            printToTerminal("Your lantern is out of fuel!", 'dialogue');
            this.lantern_on = false;
        } else {
            printToTerminal("You don't have a lantern.", 'dialogue');
            this.lantern_on = false;
        }
    }

    refuel_lantern(fat_units) {
        this.lantern_fuel += fat_units;
        printToTerminal(`You refuel your lantern with ${fat_units} animal fat. Lantern fuel: ${this.lantern_fuel} turns.`, 'event');
    }

    equip(type, name) {
        type = type.toLowerCase();
        // Unequip existing item of the same type, if any
        if (this[type]) {
            this.addItem(this[type]);
        }
        this[type] = name;
        // Remove from inventory if it was there
        if (this.inventory[name]) {
            this.inventory[name]--;
            if (this.inventory[name] === 0) {
                delete this.inventory[name];
            }
        }
    }

    can_afford(amount) {
        return this.coins.gold >= amount;
    }

    spend_gold(amount) {
        if (this.can_afford(amount)) {
            this.coins.gold -= amount;
            return true;
        }
        return false;
    }

    gainExp(amount) {
        this.exp += amount;
        while (this.exp >= this.level * 20) {
            this.exp -= this.level * 20;
            this.level++;
            this.max_hp += 20;
            this.attack += 5;
            this.hp = this.max_hp;
            printToTerminal(`You leveled up! You are now level ${this.level}.`, 'event');
        }
    }
}

export default Player;
