import json
import projectile
import pygame as pg
import components.sound as sfx


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
           item: any ClassObject'''
        self.rglist[f"{registryname}"] = item
    
    def load_from_json(self, rg_file):
        '''Load premade registry from a json file'''
        with open(rg_file) as file:
            self.rglist = json.load(file.read())

    def list_rg(self):
        '''List all objects in the registry'''
        return self.rglist
    
    def __str__(self):
        '''What to return when printing REGISTRY object'''
        return f"REGISTRY class object with: {len(self.rglist)} registered objects"


# A prime example of using a Registry
class PROJECTILE_REGISTRY(REGISTRY):
    def __init__(self, game):
        super().__init__(game)
        self.rglist: dict = {"ball_gray": (self.game, [5, 55], [16, 14], projectile.MoveInDirection, [], [6, 6]),
                             "ball_red": (self.game, [37, 55], [16, 14], projectile.MoveInDirection, [], [6, 6]),
                             "ball_green": (self.game,(181, 55), [16, 14], projectile.MoveInDirection, [], [6, 6]),
                             "ball_blue": (self.game, (101, 55), [16, 14], projectile.MoveInDirection, [], [6, 6]),
                             "ball_pink": (self.game, (69, 55), [16, 14], projectile.MoveInDirection, [], [6, 6]),
                             "ball_yellow": (self.game,(214, 55), [16, 14], projectile.MoveInDirection, [], [6, 6]),
                             "ball_light_blue": (self.game,(117, 55), [16, 14], projectile.MoveInDirection, [], [6, 6]),
                             "ball_white": (self.game,(245, 55), [16, 14], projectile.MoveInDirection, [], [6, 6]),

                             "opaque_ball_gray": (self.game, [5, 38], [16, 16], projectile.MoveInDirection, [], [8, 8]),
                             "opaque_ball_red": (self.game, [37, 38], [16, 16], projectile.MoveInDirection, [], [8, 8]),
                             "opaque_ball_green": (self.game,(181, 38), [16, 16], projectile.MoveInDirection, [], [8, 8]),
                             "opaque_ball_blue": (self.game, (101, 38), [16, 16], projectile.MoveInDirection, [], [8, 8]),
                             "opaque_ball_pink": (self.game, (69, 38), [16, 16], projectile.MoveInDirection, [], [8, 8]),
                             "opaque_ball_yellow": (self.game,(214, 38), [16, 16], projectile.MoveInDirection, [], [8, 8]),
                             "opaque_ball_light_blue": (self.game,(117, 38), [16, 16], projectile.MoveInDirection, [], [8, 8]),

                             "big_ball_gray": (self.game,(8, 308), [28, 28], projectile.MoveInDirection, [], [16, 16]),
                             "big_ball_red": (self.game,(39, 308), [28, 28], projectile.MoveInDirection, [], [16, 16]),
                             "big_ball_blue": (self.game,(103, 308), [28, 28], projectile.MoveInDirection, [], [16, 16]),
                             "big_ball_yellow": (self.game,(199, 308), [28, 28], projectile.MoveInDirection, [], [16, 16]),
                             "big_ball_green": (self.game,(167, 308), [28, 28], projectile.MoveInDirection, [], [16, 16]),
                             "big_ball_pink": (self.game,(71, 308), [28, 28], projectile.MoveInDirection, [], [16, 16]),
                             "big_ball_light_blue": (self.game,(135, 308), [28, 28], projectile.MoveInDirection, [], [16, 16]),
                             "big_ball_white": (self.game,(231, 308), [28, 28], projectile.MoveInDirection, [], [16, 16]),}
    
    def shoot(self, proj: str,pos: list, direction: tuple, speed: float, directional: bool = True):
        '''Shoots a projectile from the registry'''
        self.game.proj_list.append(projectile.TestNewFormatProjectile(self.rglist.get(proj)[0], pos, targpos=direction, speed=speed, marginxy=self.rglist.get(proj)[1], htsize=self.rglist.get(proj)[5], size=self.rglist.get(proj)[2], directional=directional))

# The same but with sounds
class SOUND_REGISTRY(REGISTRY):
    def __init__(self, game):
        super().__init__(game)
        self.rglist: dict = {"pause": sfx.Sound(self.game, "sfx/sounds/se_pause.wav"),
                             "damage00": sfx.Sound(self.game, "sfx/sounds/se_damage00.wav"),
                             "damage01": sfx.Sound(self.game, "sfx/sounds/se_damage01.wav"),
                             "power01": sfx.Sound(self.game, "sfx/sounds/se_power1.wav"),
                             "plst": sfx.Sound(self.game, "sfx/sounds/se_plst00.wav"),
                             "powerup": sfx.Sound(self.game, "sfx/sounds/se_powerup.wav"),
                             "select00": sfx.Sound(self.game, "sfx/sounds/se_select00.wav"),
                             "nice": sfx.Sound(self.game, "sfx/sounds/se_nice.wav"),
                             "ok": sfx.Sound(self.game, "sfx/sounds/se_ok00.wav"),
                             "timeout": sfx.Sound(self.game, "sfx/sounds/se_timeout.wav"),
                             "nep00": sfx.Sound(self.game, "sfx/sounds/se_nep00.wav"),
                             "kira00": sfx.Sound(self.game, "sfx/sounds/se_kira00.wav"),
                             "lazer01": sfx.Sound(self.game, "sfx/sounds/se_lazer00.wav"),
                             "pl_death": sfx.Sound(self.game, "sfx\sounds\se_pldead00.wav"),
                             "cancel": sfx.Sound(self.game, "sfx\sounds\se_cancel00.wav"),
                             "extend": sfx.Sound(self.game, "sfx\sounds\se_extend.wav"), 
                             }
    
    def get(self, item):
        return self.rglist.get(item)

if __name__ == "__main__":
    s = REGISTRY()