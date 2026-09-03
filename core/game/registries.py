import json
import core.game.projectile as projectile
import pygame as pg
import core.sound as sfx


# a registry class for managing a lot of object (enemy types, projectile types etc...)
# NOT DOCUMENTED
class REGISTRY:
    def __init__(self, game):
        '''Registry class'''
        self.game = game
        self.rglist: dict = {}
    
    def register(self, registryname, item):
        '''Register an item in the registry:
           registryname: Id for an object
           item: any Object'''
        self.rglist[f"{registryname}"] = item
    
    def __getitem__(self, key):
        return self.rglist[key]
    
    def load_from_json(self, rg_file):
        '''Load premade registry from a json file'''
        with open(rg_file) as file:
            self.rglist = json.load(file.read())

    def list_rg(self):
        '''List all objects in the registry'''
        return f"Objects:{self.rglist}"
    
    def __str__(self):
        '''What to return when printing REGISTRY object'''
        return f"REGISTRY class object with: {len(self.rglist)} registered objects"


# A prime example of using a Registry
class PROJECTILE_REGISTRY(REGISTRY):
    def __init__(self, game):
        super().__init__(game)
        self.rglist: dict = {}
 
    def shoot(self,group:int = 0, proj: str="",pos: list=[0, 0], angle: int = 0, speed: float = 3.0):
        '''Shoots a projectile from the registry'''
        if len(self.game.proj_list) < self.game.proj_cap:
            self.game.proj_list.append(projectile.Projectile(self.rglist.get(proj)[0], group, pos, angle=angle, speed=speed, marginxy=self.rglist.get(proj)[1], htradius=self.rglist.get(proj)[5], size=self.rglist.get(proj)[2] ))

# The same but with sounds
class SOUND_REGISTRY(REGISTRY):
    def __init__(self, game):
        super().__init__(game)
        self.rglist: dict = {}
    
    def get(self, item):
        return self.rglist.get(item)

class MUSIC_REGISTRY(REGISTRY):
    def __init__(self, game):
        super().__init__(game)
        self.rglist: dict = {}
    

    
    def get(self, item):
        return self.rglist.get(item)

if __name__ == "__main__":
    s = REGISTRY()
    s[0]