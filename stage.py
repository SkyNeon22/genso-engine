import pygame
from ui import *
import json
import logging

logging.basicConfig(filename="log.log")

class MAP:
    def __init__(self, game, mapfile="test.stage"):
        self.game = game
        self.mapfile = mapfile
        self.premidbossenemies = []
        self.midboss = None
        self.prebossenemies = []
        self.stageboss = None
        logging.info("initialized a stage system")
    
    def load(self):
        try:
            with open(f'stages/{self.mapfile}', 'r') as file:
                logging.info(f"loaded into {self.mapfile} operation succesful")
                return json.load(file)
        except FileNotFoundError:
            logging.error(f"stage '{self.mapfile}' was not found in game/stages directory")
            Text(self.game, text=f"Stage {self.mapfile} is not found, game is probably corrupted or have been modified and cannot be loaded normaly.Check if mod is installed correctly")
            Text(self.game, pos=(0,50), text=f"or reinstall the game. If it didn't help go to game/stages directory and change stage names from 1 to 7. If that also didn't help, contact the dev or install stage files separately from itch.io page.")
            Text(self.game, pos=(0,100), text="Log was written inside the game folder.")

    def init_map(self):
        logging.info(f"stage '{self.mapfile}' loading into the memory")
        raw = self.load()
        temp = []

    def save(self):
        with open(f'stages/{self.mapfile}', 'w') as file:
            temp = []
            json.dump(temp, file)
    
    def update(self):
        pass