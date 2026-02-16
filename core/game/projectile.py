import pygame as pg
from math import *
from core.visuals.particles import *
from core.game.behaviors import *
from core.additions.utils import is_negative
from core.visuals.tileset import Tileset
from core.game.colliders import CircleCollider

tileset = Tileset("assets/img/sprites/bullets/bullets.png")

class Projectile:
    def __init__(self, game, pos=(0, 0), team="en", speed=0.4, targpos=(0, 0), color=(200, 0, 0), behavior=MoveInDirection, bh_args=[], angle=0, size=[16,14], htradius=6, marginxy=[5, 55], directional=True):
        self.game = game
        self.speed = speed
        self.pos = list(pos)
        self.trgt = targpos
        self.size = size
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))
        self.directional = directional
        self.marginxy = marginxy
        self.ref = pg.transform.rotate(pg.Surface(self.size), angle)
        self.hitbox = CircleCollider(htradius, self.center)
        self.team = team

        self.color = color
        self.angle = radians(angle)

        self.dx, self.dy = 0, 0

        self.bh_args = bh_args
        self.behavior = behavior(self.game, self, self.trgt)

        self.kill = False
        self.can_die = True

        self.launch()
    
    def set_atributes(self):
        pass
    
    def todict(self): # method for saving an projectile object to a registry file
        return {"game": None,
                "pos": self.pos,
                "team": self.team,
                "speed": self.speed,
                "targpos": self.trgt,
                "color": self.color,
                "behavior": self.behavior,
                "bj_args": self.bh_args,
                "angle": self.angle,
                "size": self.size,
                "htsize": self.hitboxsize,
                "marginxy": self.marginxy,
        }

    @classmethod
    def fromdict(cls, asset, game=None): # method for loading an projectile object from a registry file
        return cls(asset["game"] or game,asset["pos"], asset["team"], asset["speed"], asset["targpos"], asset["color"], asset["behavior"], asset["bh_args"], asset["angle"], asset["size"], asset["htsize"], asset["marginxy"])
    
    def draw(self):
        tileset.draw_sprite_from_tile(self.game.fight_area, size=self.size, pos=self.pos, marginxy=self.marginxy, angle=self.angle)
        #pg.draw.rect(self.game.fight_area, self.color, self.hitbox)
    
    def launch(self):
        self.dx, self.dy = cos(self.angle) * self.speed, sin(self.angle) * self.speed
        self.ref = pg.transform.rotate(pg.Surface(self.size), degrees(self.angle))
    
    def destroy(self):
        self.can_die = True
        self.kill = True
    
    def update(self): 
        self.draw()
        self.pos[0] += self.dx
        self.pos[1] += self.dy
        if self.pos[1] <= -10 or self.pos[1] >= 494:
            self.kill = True
        if self.pos[0] <= -10 or self.pos[0] >= 478:
            self.kill = True
        self.center = (self.pos[0] + (self.ref.get_width() / 2), self.pos[1] + (self.ref.get_height() / 2))
        self.hitbox.update(self.center)

