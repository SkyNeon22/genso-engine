import pygame
from core.visuals.ui import *
import json
import logging
import core.game.enemy as enemy
import core.game.triggers as trigger

logging.basicConfig(filename="log.log")

class StageSystem:
    def __init__(self, game, mapfile: str ="test.stg", stagedirectory: str ="assets/stages/"):
        self.game = game
        self.mapfile = mapfile
        self.stgdir = stagedirectory
        self.dialoguetriggercount = -1
        self.map = self.load(self.mapfile)
        self.enemies = self.init_enemies(self.mapfile)
        self.triggers = self.init_triggers(self.mapfile)
        self.map_dict = {}
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
    
    def init_triggers(self, mapfile):
        logging.info(f"stage '{mapfile}' loading into the memory")
        temp = []
        temp2 = None
        if len(self.map.get('triggers')) >= 1:
            for rc in self.map.get('triggers'):
                # if statement hell, I would try to find a solution cuz stages would load VERY SLOWLY if left untouched
                if rc.get("type") == "rotatecamera":
                    temp2 = trigger.RotateCamera.fromdict(rc, self.game.camera)
                    temp.append(temp2)
                elif rc.get("type") == "movecameratodestpos":
                    temp2 = trigger.MoveCameraToDestPos.fromdict(rc, self.game.camera)
                    temp.append(temp2)
                elif rc.get("type") == "dialogueactivate":
                    self.dialoguetriggercount += 1
                    temp2 = trigger.DialogueActivate.fromdict(rc, self.game)
                    temp2.dialoguenum = self.dialoguetriggercount
                    temp.append(temp2)
            self.dialoguetriggercount = -1
            return temp
        else:
            return []

    def init_enemies(self, mapfile):
        logging.info(f"stage '{mapfile}' loading into the memory")
        temp = []
        temp2 = None
        try:
            for rc in self.map.get('enemies'):
                # if statement hell, I would try to find a solution cuz stages would load VERY SLOWLY if left untouched
                if rc.get("type") == "enemy":
                    temp2 = enemy.Enemy.fromdict(asset=rc)
                    temp2.game = self.game
                    temp.append(temp2)
                elif rc.get("type") == "testboss":
                    temp2 = enemy.Testboss.fromdict(asset=rc, game=self.game)
                    temp.append(temp2)
            return temp
        except TypeError:
            return []

    def save(self):
        with open(f'{self.stgdir}{self.mapfile}', 'w') as file:
            temp = []
            for enemy in self.enemies:
                t = enemy.todict()
                temp.append(t)
            self.map_dict["enemies"] = temp
            temp = []
            for trigger in self.triggers:
                t = trigger.todict()
                temp.append(t)
            self.map_dict["triggers"] = temp
            print(self.map_dict)
            json.dump(self.map_dict, file, indent=5)
    
    def update(self):
        pass

if __name__ == "__main__":
    stg = StageSystem(None)
    stg.init_map()