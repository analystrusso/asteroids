import pygame as pg
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from states import Menu, Game, States

if __name__ == "__main__":
    settings = {
        "size": (SCREEN_WIDTH, SCREEN_HEIGHT),
        "fps": 60
    }

    # Initialize and set up the Control instance
    app = States(**settings)
    
    # Create the state instances and pass them to the Control class
    state_dict = {
        "menu": Menu(),
        "game": Game()
    }
    
    # Set up initial state and start the game loop
    app.setup_states(state_dict, "menu")
    app.main_game_loop()

    pg.quit()
