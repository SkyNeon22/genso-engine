import pygame as pg
import utils
from particles import *
from behaviors import *


class Projectile:
    def __init__(self, game, pos=(0, 0), team="pl", speed=0.4, direction=(0, 0), color=(200, 0, 0), behavior=MoveInDirection):
        self.game = game
        self.damage = 10
        self.size = [20, 20]
        self.speed = speed
        self.pos = list(pos)
        self.imgsize = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.hitbox = pg.Rect(self.pos[0], self.pos[1], self.size[0] * 0.3, self.size[1] * 0.3)
        self.team = team

        self.color = color

        self.vel = list(direction)
        self.behavior = behavior(self.game, self, self.vel)

        self.kill = False
        self.can_die = True
    
    def draw(self):
        pg.draw.rect(self.game.fight_area, self.color, self.imgsize)
        #pg.draw.rect(self.game.fight_area, (100, 100, 150), self.hitbox)
    
    def update(self):
        self.behavior.update()
        self.draw()
        if self.pos[1] <= -10 or self.pos[1] >= 660:
            self.kill = True
        if self.pos[0] <= -10 or self.pos[0] >= 410:
            self.kill = True
        self.imgsize = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.hitbox = pg.Rect(self.pos[0] + 6, self.pos[1] + 6, self.size[0] * 0.5, self.size[1] * 0.5)

class Homing_Projectile(Projectile):
    def __init__(self, game, pos=(0, 0), team="pl", speed=4, direction=(0, 0), color=(200, 0, 0), behavior=MoveInDirection):
        super().__init__(game, pos, team, speed, direction, color, behavior)
        self.game = game
        self.damage = 5
        self.size = [20, 20]
        self.pos = list(pos) 
    
    def draw(self):
        pg.draw.rect(self.game.fight_area, (230, 230, 230), self.hitbox)
    
    def update(self):
        if len(self.game.enemy_list) > 0:
            for enemy in self.game.enemy_list:
                previous = enemy.pos
                if utils.dist_2d(self.pos, enemy.pos) <= previous[0] and self.pos[0] < enemy.pos[0]:
                    self.pos[0] += self.speed
                elif utils.dist_2d(self.pos, enemy.pos) <= previous[0] and self.pos[0] > enemy.pos[0]:
                    self.pos[0] -= self.speed
        self.pos[1] -= self.speed
        self.draw()
        if self.pos[1] <= 0:
            self.kill = True
        self.hitbox = pg.Rect(self.pos, self.size)

class Bomb(Projectile):
    def __init__(self, game, pos=(0, 0), team="pl", speed=0.4, direction=(0, 0), color=(200, 0, 0), behavior=MoveInDirection):
        super().__init__(game, pos, team, speed, direction, color, behavior)
        self.game = game
        self.damage = 20
        self.size = [200, 200]
        self.speed = 0.2
        self.pos = list(pos)
        self.hitbox = pg.Rect(self.pos, self.size)
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
        self.pos[1] -= self.speed
        self.size = [self.size[0] / 1.0004, self.size[1] / 1.0004]
        pg.draw.rect(self.game.fight_area, (200, 0, 0,120), self.hitbox)
        if self.timer == 1000:
            self.kill = True
            self.can_die = True
        self.hitbox = pg.Rect(self.pos, self.size)

class ReimuShotNormal(Projectile):
    def __init__(self, game, pos=(0, 0), team="pl", speed=18, direction=(0, 0), color=(200, 0, 50), behavior=MoveInDirection):
        super().__init__(game, pos, team, speed, direction, color, behavior)
        self.damage = 1
        self.img = pg.image.load("sprites/bullets/bullet_reimu.png")
        self.img.map_rgb(self.color)
        self.hitbox = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def draw(self):
        self.game.fight_area.blit(self.img, self.pos)
    
    def update(self):
        self.pos[0] += self.vel[0] * self.speed
        self.pos[1] += self.vel[1] * self.speed
        self.draw()
        if self.pos[1] <= 0:
            self.kill = True
        self.hitbox = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

class MarisaShotNormal(Projectile):
    def __init__(self, game, pos=(0, 0), team="pl", speed=18, direction=(0, 0), color=(200, 0, 50), behavior=MoveInDirection):
        super().__init__(game, pos, team, speed, direction, color, behavior)
        self.damage = 1
        self.img = pg.image.load("sprites/bullets/bullet_marisa.png")
        self.img.map_rgb(self.color)
    
    def draw(self):
        self.game.fight_area.blit(self.img, self.pos)
    
    def update(self):
        self.pos[0] += self.vel[0] * self.speed
        self.pos[1] += self.vel[1] * self.speed
        self.draw()
        if self.pos[1] <= 0:
            self.kill = True
        self.hitbox = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])


class MarisaLaserNormal(Projectile):
    def __init__(self, game, pos=(0, 0), team="pl", speed=10, direction=(0, -1), color=(200, 0, 0), behavior=MoveInDirection):
        super().__init__(game, pos, team, speed, direction, color, behavior)
        self.damage = 1
        self.size = (10, 60)
        self.img = pg.image.load("sprites\\bullets\\laser_marisa.png")
        self.speed = 15
        self.timer = 0
    
    def draw(self):
        self.game.fight_area.blit(pg.transform.scale(self.img, self.size), self.pos)
    
    def update(self):
        self.pos[0] += self.vel[0] * self.speed
        self.pos[1] += self.vel[1] * self.speed
        self.draw()
        if self.pos[1] <= 0:
            self.kill = True
        self.hitbox = pg.Rect(self.pos, self.size)

class MarisaRocketNormal(Projectile):
    def __init__(self, game, pos=(0, 0), team="pl", speed=2, direction=(0, -1), color=(200, 0, 50), behavior=MoveInDirection):
        super().__init__(game, pos, team, speed, direction, color, behavior)
        self.img = pg.image.load("sprites/bullets/rocket_marisa.png")
        self.size = (10, 20)
        self.damage = 5
        self.explode = False
    
    def draw(self):
        self.game.fight_area.blit(self.img, self.pos)
    
    def update(self):
        self.speed += 0.09
        self.pos[0] += self.vel[0] * self.speed
        self.pos[1] += self.vel[1] * self.speed
        self.draw()
        if self.pos[1] <= 0:
            self.kill = True
        if self.kill == True:
            self.game.player_proj.append(RocketExplosion(self.game, self.pos))
        self.hitbox = pg.Rect(self.pos, self.size)

class RocketExplosion(Projectile):
    def __init__(self, game, pos=(0, 0), team="pl", speed=10, direction=(0, 0), color=(200, 0, 0), behavior=MoveInDirection):
        super().__init__(game, pos, team, speed, direction, color, behavior)
        self.size = (51, 51)
        self.timer = 0
        self.damage = 20
    
    def draw(self):
        pass
        #pg.draw.rect(self.game.fight_area, (255, 40, 0), self.hitbox)
    
    def update(self):
        self.timer += 2
        #self.pos[0] += self.vel[0] * self.speed
        #self.pos[1] += self.vel[1] * self.speed
        self.draw()
        if self.kill == True:
            self.game.particles.append(Particle(self.game, 100, self.pos))
        if self.timer == 200:
            self.kill = True
        self.hitbox = pg.Rect(self.pos, self.size)



class ReimuHomingNormal(Homing_Projectile):
    def __init__(self, game, pos=(0, 0), team="pl"):
        super().__init__(game, pos, team)
        self.damage = 7
        self.img = pg.image.load("sprites/bullets/bullet_homing_reimu.png")

    def draw(self):
        self.game.fight_area.blit(pg.transform.rotate(self.img, 45.0), self.pos)
    
class ReimuNeedleNormal(Projectile):
    def __init__(self, game, pos=(0, 0), team="pl", speed=12, direction=(0, -1), color=(200, 0, 50), behavior=MoveInDirection):
        super().__init__(game, pos, team, speed, direction, color, behavior)
        self.img = pg.image.load("sprites/bullets/needle_reimu.png")
        self.size = (9, 35)
        self.damage = 3
    
    def draw(self):
        self.game.fight_area.blit(self.img, self.pos)

class SanaeShotNormal(Projectile):
    def __init__(self, game, pos=(0, 0), team="pl", speed=18, direction=(0, 0), color=(200, 0, 50), behavior=MoveInDirection):
        super().__init__(game, pos, team, speed, direction, color, behavior)
        self.damage = 1
        self.img = pg.image.load("sprites/bullets/bullet_sanae.png")
        self.img.map_rgb(self.color)
        self.hitbox = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def draw(self):
        self.game.fight_area.blit(self.img, self.pos)
    
    def update(self):
        self.pos[0] += self.vel[0] * self.speed
        self.pos[1] += self.vel[1] * self.speed
        self.draw()
        if self.pos[1] <= 0:
            self.kill = True
        self.hitbox = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

class SanaeWaveNormal(Projectile):
    def __init__(self, game, pos=(0, 0), team="pl", speed=10, direction=(-0.2, -1), color=(200, 0, 50), behavior=MoveInDirection):
        super().__init__(game, pos, team, speed, direction, color, behavior)
        self.img = pg.image.load("sprites/bullets/green_wave_sanae.png")
        self.damage = 14
        self.size = [40, 20]
        self.img.map_rgb(self.color)
        self.hitbox = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def draw(self):
        self.game.fight_area.blit(pg.transform.scale(self.img, (self.size[0], self.size[1])), self.pos)
    
    def update(self):
        self.size[0] += 5
        self.pos[0] += self.vel[0] * self.speed
        self.pos[1] += self.vel[1] * self.speed
        self.draw()
        if self.pos[1] <= 0:
            self.kill = True
        self.hitbox = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])