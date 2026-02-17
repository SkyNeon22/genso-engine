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
        self.rglist: dict = {"ball_gray": (self.game, [5, 55], [16, 16], projectile.MoveInDirection, [], 4),
                             "ball_red": (self.game, [37, 55], [16, 16], projectile.MoveInDirection, [], 4),
                             "ball_green": (self.game,(181, 55), [16, 16], projectile.MoveInDirection, [], 4),
                             "ball_blue": (self.game, (101, 55), [16, 16], projectile.MoveInDirection, [], 4),
                             "ball_pink": (self.game, (69, 55), [16, 16], projectile.MoveInDirection, [], 4),
                             "ball_yellow": (self.game,(214, 55), [16, 16], projectile.MoveInDirection, [], 4),
                             "ball_light_blue": (self.game,(117, 55), [16, 16], projectile.MoveInDirection, [], 4),
                             "ball_white": (self.game,(245, 55), [16, 16], projectile.MoveInDirection, [], 4),

                             "opaque_ball_gray": (self.game, [5, 38], [16, 16], projectile.MoveInDirection, [], 6),
                             "opaque_ball_red": (self.game, [37, 38], [16, 16], projectile.MoveInDirection, [], 6),
                             "opaque_ball_green": (self.game,(181, 38), [16, 16], projectile.MoveInDirection, [], 6),
                             "opaque_ball_blue": (self.game, (101, 38), [16, 16], projectile.MoveInDirection, [], 6),
                             "opaque_ball_pink": (self.game, (69, 38), [16, 16], projectile.MoveInDirection, [], 6),
                             "opaque_ball_yellow": (self.game,(214, 38), [16, 16], projectile.MoveInDirection, [], 6),
                             "opaque_ball_light_blue": (self.game,(117, 38), [16, 16], projectile.MoveInDirection, [], 6),

                             "big_ball_gray": (self.game,(8, 308), [28, 28], projectile.MoveInDirection, [], 8),
                             "big_ball_red": (self.game,(39, 308), [28, 28], projectile.MoveInDirection, [], 8),
                             "big_ball_blue": (self.game,(103, 308), [28, 28], projectile.MoveInDirection, [], 8),
                             "big_ball_yellow": (self.game,(199, 308), [28, 28], projectile.MoveInDirection, [], 8),
                             "big_ball_green": (self.game,(167, 308), [28, 28], projectile.MoveInDirection, [], 8),
                             "big_ball_pink": (self.game,(71, 308), [28, 28], projectile.MoveInDirection, [], 8),
                             "big_ball_light_blue": (self.game,(135, 308), [28, 28], projectile.MoveInDirection, [], 8),
                             "big_ball_white": (self.game,(231, 308), [28, 28], projectile.MoveInDirection, [], 8),
                             
                             "bubble_ball_dark": (self.game,(151, 248), [12, 12], projectile.MoveInDirection, [], 2),
                             "bubble_ball_red": (self.game,(167, 248), [12, 12], projectile.MoveInDirection, [], 2),
                             "bubble_ball_blue": (self.game,(183, 248), [12, 12], projectile.MoveInDirection, [], 2),
                             "bubble_ball_green": (self.game,(199, 248), [12, 12], projectile.MoveInDirection, [], 2),
                             "bubble_ball_yellow": (self.game,(215, 248), [12, 12], projectile.MoveInDirection, [], 2),

                             "butterfly_black": (self.game,(8, 338), [29, 29], projectile.MoveInDirection, [], 4),
                             "butterfly_red": (self.game,(38, 338), [29, 29], projectile.MoveInDirection, [], 4),
                             "butterfly_pink": (self.game,(70, 338), [29, 29], projectile.MoveInDirection, [], 4),
                             "butterfly_blue": (self.game,(102, 338), [29, 29], projectile.MoveInDirection, [], 4),
                             "butterfly_light_blue": (self.game,(134, 338), [29, 29], projectile.MoveInDirection, [], 4),
                             "butterfly_green": (self.game,(166, 338), [29, 29], projectile.MoveInDirection, [], 4),
                             "butterfly_yellow": (self.game,(198, 338), [29, 29], projectile.MoveInDirection, [], 4),
                             }
 
    def shoot(self, proj: str,pos: list, angle: int = 0, speed: float = 3.0):
        '''Shoots a projectile from the registry'''
        self.game.proj_list.append(projectile.NewFormatProjectile(self.rglist.get(proj)[0], pos, angle=angle, speed=speed, marginxy=self.rglist.get(proj)[1], htradius=self.rglist.get(proj)[5], size=self.rglist.get(proj)[2]))
    
    def shoottest(self, proj: str,pos: list, angle: int = 0, speed: float = 7.0):
        '''Shoots a projectile from the registry'''
        self.game.proj_list.append(projectile.AcceleratingProjectile(self.rglist.get(proj)[0], pos, angle=angle, speed=speed, marginxy=self.rglist.get(proj)[1], htradius=self.rglist.get(proj)[5], size=self.rglist.get(proj)[2]))

# The same but with sounds
class SOUND_REGISTRY(REGISTRY):
    def __init__(self, game):
        super().__init__(game)
        self.rglist: dict = {"pause": sfx.Sound(self.game, "assets/sfx/sounds/se_pause.wav"),
                             "damage00": sfx.Sound(self.game, "assets/sfx/sounds/se_damage00.wav"),
                             "damage01": sfx.Sound(self.game, "assets/sfx/sounds/se_damage01.wav"),
                             "power01": sfx.Sound(self.game, "assets/sfx/sounds/se_power1.wav"),
                             "plst": sfx.Sound(self.game, "assets/sfx/sounds/se_plst00.wav"),
                             "powerup": sfx.Sound(self.game, "assets/sfx/sounds/se_powerup.wav"),
                             "select00": sfx.Sound(self.game, "assets/sfx/sounds/se_select00.wav"),
                             "nice": sfx.Sound(self.game, "assets/sfx/sounds/se_nice.wav"),
                             "ok": sfx.Sound(self.game, "assets/sfx/sounds/se_ok00.wav"),
                             "timeout": sfx.Sound(self.game, "assets/sfx/sounds/se_timeout.wav"),
                             "nep00": sfx.Sound(self.game, "assets/sfx/sounds/se_nep00.wav"),
                             "kira00": sfx.Sound(self.game, "assets/sfx/sounds/se_kira00.wav"),
                             "lazer01": sfx.Sound(self.game, "assets/sfx/sounds/se_lazer00.wav"),
                             "pl_death": sfx.Sound(self.game, "assets/sfx\sounds\se_pldead00.wav"),
                             "cancel": sfx.Sound(self.game, "assets/sfx\sounds\se_cancel00.wav"),
                             "extend": sfx.Sound(self.game, "assets/sfx\sounds\se_extend.wav"), 
                             "graze": sfx.Sound(self.game, "assets\\sfx\\sounds\\se_graze.wav"),
                             "piyo": sfx.Sound(self.game, "assets\\sfx\\sounds\\se_piyo.wav"),
                             }
    
    def get(self, item):
        return self.rglist.get(item)

class MUSIC_REGISTRY(REGISTRY):
    def __init__(self, game):
        super().__init__(game)
        self.rglist: dict = {0: sfx.Music(self.game, "assets\\sfx\\music\\hr_1.mp3"),
                             1: sfx.Music(self.game, "assets\\sfx\\music\\hr_2.mp3"),
                             2: sfx.Music(self.game, "assets\\sfx\\music\\hr_3.mp3"),
                             3: sfx.Music(self.game, "assets\\sfx\\music\\hr_4.mp3"),
                             4: sfx.Music(self.game, "assets\\sfx\\music\\hr_5.mp3"),
                             5: sfx.Music(self.game, "assets\\sfx\\music\\hr_6.mp3"),
                             6: sfx.Music(self.game, "assets\\sfx\\music\\hr_7.mp3"),
                             7: sfx.Music(self.game, "assets\\sfx\\music\\hr_8.mp3"),
                             8: sfx.Music(self.game, "assets\\sfx\\music\\hr_9.mp3"),
                             9: sfx.Music(self.game, "assets\\sfx\\music\\hr_10.mp3"),
                             10: sfx.Music(self.game, "assets\\sfx\\music\\hr_11.mp3"),
                             11: sfx.Music(self.game, "assets\\sfx\\music\\hr_12.mp3"),
                             12: sfx.Music(self.game, "assets\\sfx\\music\\hr_13.mp3"),
                             }
    
    def get(self, item):
        return self.rglist.get(item)

if __name__ == "__main__":
    s = REGISTRY()