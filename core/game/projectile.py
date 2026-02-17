import pygame as pg
from math import *
from core.visuals.particles import *
from core.game.behaviors import *
from core.additions.utils import is_negative
from core.visuals.tileset import Tileset
from core.game.colliders import CircleCollider

tileset = Tileset("assets/img/sprites/bullets/bullets.png")


class Projectile:
    def __init__(self, game, pos=(0, 0), team="pl", speed=0.4, direction=(0, 0), color=(200, 0, 0), behavior=MoveInDirection, angle=0):
        self.game = game
        self.damage = 10
        self.size = [20, 20]
        self.radius = 12
        self.speed = speed
        self.pos = list(pos)
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))
        self.previous = [0, 0]
        self.imgsize = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.hitbox = CircleCollider(self.radius, self.center)
        self.team = team

        self.color = color
        self.angle = angle

        self.vel = list(direction)
        self.behavior = behavior(self.game, self, self.vel)

        self.kill = False
        self.can_die = True
    
    def draw(self):
        tileset.draw_sprite_from_tile(self.game.fight_area, size=[16, 14], pos=self.pos, marginxy=[5, 55], angle=self.angle)
    
    def update(self):
        self.behavior.update()
        self.draw()
        if self.pos[1] <= -10 or self.pos[1] >= 494:
            self.kill = True
        if self.pos[0] <= -10 or self.pos[0] >= 478:
            self.kill = True
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))
        self.imgsize = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.hitbox.update(self.center)

class NewFormatProjectile:
    def __init__(self, game, pos=(0, 0), team="en", speed=0.4, targpos=(0, 0), behavior=MoveInDirection, bh_args=[], angle=0, size=[16,14], htradius=6, marginxy=[5, 55], directional=True):
        self.game = game
        self.speed = speed
        self.pos = list(pos)
        self.trgt = targpos
        self.size = size
        self.ref = pg.transform.rotate(pg.Surface(self.size), angle)
        self.center = (self.pos[0] + (self.ref.get_width() / 2), self.pos[1] + (self.ref.get_height() / 2))
        self.directional = directional
        self.marginxy = marginxy
        self.hitbox = CircleCollider(htradius, self.center)
        self.team = team

        self.angle = radians(angle)
        self.grazed = False

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
        tileset.draw_sprite_from_tile(self.game.fight_area, size=self.size, pos=self.pos, marginxy=self.marginxy, angle=degrees(self.angle) + 90)
        # pg.draw.circle(self.game.fight_area, (0, 0, 0), self.center, self.hitbox.radius)
    
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

class AcceleratingProjectile(NewFormatProjectile):
    def __init__(self, game, pos=(0, 0), team="en", speed=0.4, targpos=(0, 0), behavior=MoveInDirection, bh_args=[], angle=0, size=[16,14], htradius=6, marginxy=[5, 55], directional=True):
        super().__init__(game, pos, team, speed, targpos, behavior, bh_args, angle, size, htradius, marginxy, directional)
        self.max_speed = self.speed
        self.speed = -2
        self.time = 0.7
    
    def update(self):
        if self.speed < self.max_speed:
            self.speed += 0.5
            self.launch()
        else:
            self.speed = self.max_speed
            self.launch()
        return super().update()


class Homing_Projectile(Projectile):
    def __init__(self, game, pos=(0, 0), team="pl", speed=4, direction=(0, 0), color=(200, 0, 0), behavior=MoveInDirection):
        super().__init__(game, pos, team, speed, direction, color, behavior)
        self.game = game
        self.damage = 5
        self.size = [20, 20]
        self.pos = list(pos) 
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))
        self.hitbox = CircleCollider(self.radius, self.center)
    
    def draw(self):
        pg.draw.rect(self.game.fight_area, (230, 230, 230), self.hitbox)
    
    def update(self):
        if len(self.game.enemy_list) > 0:
            for enemy in self.game.enemy_list:
                if self.game.frametime >= enemy.time: self.previous = enemy.hitbox.center
                if self.pos[0] < enemy.pos[0]:
                    self.pos[0] += self.speed
                elif self.pos[0] > enemy.pos[0]:
                    self.pos[0] -= self.speed
                else:
                    self.pos[0] += 0
                if self.pos[1] < enemy.pos[1]:
                    self.pos[1] += self.speed
                elif self.pos[1] > enemy.pos[1]:
                    self.pos[1] -= self.speed
                else:
                    self.pos[1] -= self.speed 
        else:
            self.pos[1] -= 2
        self.draw()
        if self.pos[1] <= 0:
            self.kill = True
        self.hitbox.update(self.center)

class Bomb(Projectile):
    def __init__(self, game, pos=(0, 0), team="pl", speed=0.4, direction=(0, 0), color=(200, 0, 0, 120 ), behavior=MoveInDirection):
        super().__init__(game, pos, team, speed, direction, color, behavior)
        self.game = game
        self.damage = 20
        self.radius = 100
        self.size = [200, 200]
        self.speed = 0.4
        self.pos = list(pos)
        self.hitbox = CircleCollider(self.radius, self.center)
        self.team = team

        self.timer = 0

        self.can_die = False
        self.kill = False
    
    def update(self):
        self.timer += 1
        #if len(self.game.enemy_list) > 0:
        #    for enemy in self.game.enemy_list:
        #        previous = enemy.pos
        #        if utils.dist_2d(self.game.player.pos, enemy.pos) <= previous[0] and self.pos[0] < enemy.pos[0]:
        #            self.pos[0] += self.speed
        #        elif utils.dist_2d(self.game.player.pos, enemy.pos) <= previous[0] and self.pos[0] > enemy.pos[0]:
        #            self.pos[0] -= self.speed
        for proj in self.game.proj_list:
            if self.hitbox.colliderect(proj.hitbox):
                self.game.proj_list.remove(proj)
        self.pos[1] -= self.speed
        if self.timer >= 180:
            self.kill = True
            self.can_die = True
        self.hitbox.update(self.center)
