import pygame
from core.visuals.ui import *
import json
import logging
import core.game.enemy as enemy

logging.basicConfig(filename="log.log")

class StageSystem:
    def __init__(self, game, mapfile: str ="test.stg", stagedirectory: str ="assets/stages/"):
        self.game = game
        self.mapfile = mapfile
        self.stgdir = stagedirectory
        self.enemies = []
        logging.info("initialized a stage system")
    
    def load(self, mapfile):
        try:
            with open(f'{self.stgdir}{mapfile}', 'r') as file:
                logging.info(f"loaded into {mapfile} operation succesful")
                return json.load(file)
        except FileNotFoundError:
            logging.error(f"stage '{mapfile}' was not found in game/stages directory")
            Text(self.game, text=f"Stage {mapfile} is not found, game is probably corrupted or have been modified and cannot be loaded normaly.Check if mod is installed correctly")
            Text(self.game, pos=(0,50), text=f"or reinstall the game. If it didn't help go to game/stages directory and change stage names from 1 to 7. If that also didn't help, contact the dev or install stage files separately from itch.io page.")
            Text(self.game, pos=(0,100), text="Log was written inside the game folder.")

    def init_map(self, mapfile):
        logging.info(f"stage '{mapfile}' loading into the memory")
        temp = []
        temp2 = None
        raw = self.load(mapfile)
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
        with open(f'{self.stgdir}{self.mapfile}', 'w') as file:
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