import pygame as pg
from math import *
from core.visuals.particles import *
from core.game.behaviors import *
from core.additions.utils import is_negative
from core.visuals.tileset import Tileset
from core.game.colliders import CircleCollider

tileset = Tileset("assets/img/sprites/bullets/bullets.png")

class Projectile:
    def __init__(self, game, pos=(0, 0), team="en", speed=0.4, color=(200, 0, 0), angle=0, size=[16,14], htradius=6, marginxy=[5, 55]):
        self.game = game
        self.speed = speed
        self.pos = list(pos)
        self.size = size
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))
        self.marginxy = marginxy
        self.ref = pg.transform.rotate(pg.Surface(self.size), angle)
        self.hitbox = CircleCollider(htradius, self.center)
        self.team = team

        self.color = color
        self.angle = radians(angle)

        self.dx, self.dy = 0, 0

        self.kill = False
        self.can_die = True

        self.launch()

    def change_speed(self, speed: float):
        self.speed = speed
        self.launch()
    
    def change_angle(self, angle: float):
        self.angle = radians(angle)
        self.launch()
    
    def todict(self):
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
    def fromdict(cls, asset, game=None):
        return cls(asset["game"] or game,asset["pos"], asset["team"], asset["speed"], asset["targpos"], asset["color"], asset["behavior"], asset["bh_args"], asset["angle"], asset["size"], asset["htsize"], asset["marginxy"])
    
    def draw(self):
        tileset.draw_sprite_from_tile(self.game.fight_area, size=self.size, pos=self.pos, marginxy=self.marginxy, angle=self.angle)
    
    def launch(self):
        self.dx, self.dy = cos(self.angle) * self.speed, sin(self.angle) * self.speed
        self.ref = pg.transform.rotate(pg.Surface(self.size), degrees(self.angle))
    
    def logic(self):
        self.pos[0] += self.dx
        self.pos[1] += self.dy
    
    def destroy(self):
        self.can_die = True
        self.kill = True
    
    def update(self): 
        self.draw()
        if self.pos[1] <= -50 or self.pos[1] >= 600:
            self.destroy()
        if self.pos[0] <= -50 or self.pos[0] >= 600:
            self.destroy()
        self.center = (self.pos[0] + (self.ref.get_width() / 2), self.pos[1] + (self.ref.get_height() / 2))
        self.hitbox.update(self.center)


class ZigZagProjectile(Projectile):
    def __init__(self, game, pos=(0, 0), team="en", speed=0.4, color=(200, 0, 0), angle=0, size=[16, 14], htradius=6, marginxy=[5, 55], dist_to_reflect=100):
        super().__init__(game, pos, team, speed, color, angle, size, htradius, marginxy)
        self.start_pos = self.pos
        self.dist_to_reflect = dist_to_reflect
        self.start_angle = self.angle
        self.reflected = False
    
    def logic(self):
        self.pos[0] += self.dx
        self.pos[1] += self.dy
        if dist(self.pos, self.start_pos) >= self.dist_to_reflect:
            if self.reflected:
                self.angle = radians(self.start_angle)
                self.start_pos = self.pos
                self.reflected = False
            else:
                self.angle = radians(360 - self.start_angle)
                self.start_pos = self.pos
                self.reflected = True

class AcceleratingProjectile(Projectile):
    def __init__(self, game, pos=(0, 0), team="en", speed=0.4, color=(200, 0, 0), angle=0, size=[16, 14], htradius=6, marginxy=[5, 55], startspeed=-0.4,acceleration=0.1):
        super().__init__(game, pos, team, speed, color, angle, size, htradius, marginxy)
        self.start_pos = self.pos
        self.end_speed = self.speed
        self.speed = startspeed
        self.acceleration = acceleration
        self.start_angle = self.angle
        self.reflected = False
    
    def logic(self):
        self.change_speed(self.speed)
        if self.speed != self.end_speed:
            self.speed += self.acceleration
        self.pos[0] += self.dx
        self.pos[1] += self.dy

class ReflectingProjectile(Projectile):
    def __init__(self, game, pos=(0, 0), team="en", speed=0.4, color=(200, 0, 0), angle=0, size=[16, 14], htradius=6, marginxy=[5, 55], reflection_count=1):
        super().__init__(game, pos, team, speed, color, angle, size, htradius, marginxy)
        self.reflect_count = reflection_count
    
    def logic(self):
        if self.pos[0] <= self.game.left_fight_area_border and self.reflect_count > 0:
            self.change_angle(-degrees(self.angle))
            self.reflect_count -= 1
        if self.pos[0] >= self.game.right_fight_area_border and self.reflect_count > 0:
            self.change_angle(-degrees(self.angle))
            self.reflect_count -= 1
        if self.pos[1] <= self.game.top_fight_area_border and self.reflect_count > 0:
            self.change_angle(-degrees(self.angle))
            self.reflect_count -= 1
        if self.pos[1] >= self.game.bottom_fight_area_border and self.reflect_count > 0:
            self.change_angle(-degrees(self.angle))
            self.reflect_count -= 1
        self.pos[0] += self.dx
        self.pos[1] += self.dy