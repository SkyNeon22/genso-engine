import pygame
from ui import *
import json
import logging
import enemy

logging.basicConfig(filename="log.log")

class StageSystem:
    def __init__(self, game, mapfile="test.stg"):
        self.game = game
        self.mapfile = mapfile
        #self.premidbossenemies = []
        #self.midboss = None
        #self.prebossenemies = []
        #self.stageboss = None
        self.enemies = []
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
        temp = []
        temp2 = None
        raw = self.load()
        for rc in raw:
            # if statement hell, I would try to find a solution cuz stages would load VERY SLOWLY if left untouched
            if rc.get("type") == "enemy":
                temp2 = enemy.Enemy.fromdict(asset=rc)
                temp2.game = self.game
                temp.append(temp2)
            elif rc.get("type") == "whiteflame":
                temp2 = enemy.WhiteFlame.fromdict(asset=rc)
                temp2.game = self.game
                temp.append(temp2)
            elif rc.get("type") == "testboss":
                temp2 = enemy.Testboss.fromdict(asset=rc, game=self.game)
                temp.append(temp2)
        return temp

    def save(self):
        with open(f'stages/{self.mapfile}', 'w') as file:
            temp = []
            for enemy in self.enemies:
                t = enemy.todict()
                temp.append(t)
            json.dump(temp, file)
    
    def update(self):
        pass

if __name__ == "__main__":
    stg = StageSystem(None)
    stg.init_map()