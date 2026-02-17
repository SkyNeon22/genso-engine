import pygame as pg
from core.game.colliders import CircleCollider
from math import cos, sin, radians
from core.additions.utils import get_angle


class Power_pickup:
    def __init__(self, game, pos=(10, 300), vel=-0.2):
        self.game = game
        self.size = [20, 20]
        self.pos = list(pos)
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))

        self.type = "pwr"

        self.points = 10
        if self.game.player.legacy_shots:
            self.power = 1
        else:
            self.power = 0.01
        
        self.vel = vel

        self.kill = False
        self.follow = False

        self.hitbox = CircleCollider(5, self.center)

        self.angle = radians(get_angle(self.game.player.graze_hitbox.position, self.pos))
        self.launch()
    
    def start_follow(self):
        self.follow = True
    
    def launch(self):
        self.dx, self.dy = cos(self.angle) * 5, sin(self.angle) * 5
    
    def draw(self):
        pg.draw.rect(self.game.fight_area, (255, 255, 255), pg.Rect(self.pos[0] - 2, self.pos[1] - 2, self.size[0] + 4, self.size[1] + 4))
        pg.draw.rect(self.game.fight_area, (255, 0, 0), pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))
    
    def update(self):
        if self.follow:
            self.angle = radians(get_angle(self.game.player.graze_hitbox.position, self.pos))
            self.launch()
            self.pos[0] += self.dx
            self.pos[1] += self.dy
        else:
            self.pos[1] += self.vel
            self.vel += 0.0062
        if self.pos[0] >= 800:
            self.kill = True
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))
        self.hitbox.update(self.center)
        self.draw()

class Full_Power_pickup(Power_pickup):
    def __init__(self, game, pos=(10, 300), vel=-0.2):
        self.game = game
        self.size = [20, 20]
        self.pos = list(pos)
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))

        self.type = "pwr"

        self.points = 10
        if self.game.player.legacy_shots:
            self.power = 128
        else:
            self.power = 4.00
        
        self.vel = vel

        self.kill = False

        self.hitbox = CircleCollider(5, self.center)
    
    def draw(self):
        pg.draw.rect(self.game.fight_area, (255, 255, 255), pg.Rect(self.pos[0] - 2, self.pos[1] - 2, self.size[0] + 4, self.size[1] + 4))
        pg.draw.rect(self.game.fight_area, (200, 80, 0), pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))
    
    def update(self):
        self.pos[1] += self.vel
        self.vel += 0.0062
        if self.pos[0] >= 800:
            self.kill = True
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))
        self.hitbox.update(self.center)
        self.draw()

class Big_Power_pickup(Power_pickup):
    def __init__(self, game, pos=(10, 300), vel=-0.2):
        super().__init__(game, pos, vel)
        self.type = "pwr"
        self.size = [30, 30]
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))
        self.points = 50
        if self.game.player.legacy_shots:
            self.power = 8
        else:
            self.power = 0.50

class Point_pickup(Power_pickup):
    def __init__(self, game, pos=(10, 300), vel=-0.2):
        super().__init__(game, pos, vel)
        self.game = game
        self.size = [20, 20]
        self.pos = list(pos)
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))

        self.type = "col"

        self.points = 50000
        self.power = 1
        
        self.vel = vel

        self.kill = False

        self.hitbox = CircleCollider(5, self.center)
    
    def draw(self):
        pg.draw.rect(self.game.fight_area, (255, 255, 255), pg.Rect(self.pos[0] - 2, self.pos[1] - 2, self.size[0] + 4, self.size[1] + 4))
        pg.draw.rect(self.game.fight_area, (0, 0, 255), pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))

class Score_Pickup(Point_pickup):
    def __init__(self, game, pos=(10, 300), vel=-0.2):
        super().__init__(game, pos, vel)
        self.size = [10, 10]
        self.points = 100
    
    def draw(self):
        pg.draw.rect(self.game.fight_area, (255, 255, 255), pg.Rect(self.pos[0] - 2, self.pos[1] - 2, self.size[0] + 4, self.size[1] + 4))
        pg.draw.rect(self.game.fight_area, (0, 150, 0), pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))
    
    def update(self):
        self.follow = True
        if self.pos[1] >= 800:
            self.kill = True
        if self.follow:
            self.launch()
            self.pos[0] += self.dx
            self.pos[1] += self.dy
        else:
            self.pos[1] += self.vel
            self.vel += 0.0062
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))
        self.hitbox.update(self.center)
        self.draw()

class Life_pickup(Power_pickup):
    def __init__(self, game, pos=(10, 300), vel=-0.2):
        super().__init__(game, pos, vel)
        self.points = 100
        self.type = "life"
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))
    

    def draw(self):
        pg.draw.rect(self.game.fight_area, (255, 255, 255), pg.Rect(self.pos[0] - 2, self.pos[1] - 2, self.size[0] + 4, self.size[1] + 4))
        pg.draw.rect(self.game.fight_area, (255, 0, 255), pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))

class Bomb_pickup(Power_pickup):
    def __init__(self, game, pos=(10, 300), vel=-0.2):
        super().__init__(game, pos, vel)
        self.points = 100
        self.type = "bom"
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))
    

    def draw(self):
        pg.draw.rect(self.game.fight_area, (255, 255, 255), pg.Rect(self.pos[0] - 2, self.pos[1] - 2, self.size[0] + 4, self.size[1] + 4))
        pg.draw.rect(self.game.fight_area, (0, 255, 0), pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))

class Life_piece_pickup(Power_pickup):
    def __init__(self, game, pos=(10, 300), vel=-0.2):
        super().__init__(game, pos, vel)
        self.size = [16, 16]
        self.points = 20
        self.type = "lifepiece"
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))
    

    def draw(self):
        pg.draw.rect(self.game.fight_area, (255, 255, 255), pg.Rect(self.pos[0] - 2, self.pos[1] - 2, self.size[0] + 4, self.size[1] + 4))
        pg.draw.rect(self.game.fight_area, (255, 0, 255), pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]))