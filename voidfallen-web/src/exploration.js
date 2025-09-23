import { printToTerminal } from './ui.js';
import { locations, endEvents } from './locations.js';

class Exploration {
    constructor(game) {
        this.game = game;
    }

    // This explore method will be simplified as the main game loop handles traversal
    // It will primarily be used to initiate a path traversal
    explore(direction) {
        const pathData = locations[direction];
        if (pathData) {
            this.game.currentPath = pathData;
            this.game.pathProgress = 0;
            this.game.state = 'traversing_path';
            printToTerminal(this.game.alt_text(pathData.intro_text.normal, pathData.intro_text.alt), 'location');
            printToTerminal(`You are 0/${pathData.stages} of the way. (continue/leave)`, 'narrative');
        } else {
            printToTerminal("You can't go that way.", 'dialogue');
        }
    }
}

export default Exploration;