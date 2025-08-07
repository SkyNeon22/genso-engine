import pygame as pg


class Power_pickup:
    def __init__(self, game, pos=(10, 300), vel=-0.2):
        self.game = game
        self.size = [20, 20]
        self.pos = list(pos)

        self.type = "pwr"

        self.points = 10
        if self.game.player.legacy_shots:
            self.power = 1
        else:
            self.power = 0.01
        
        self.vel = vel

        self.kill = False

        self.hitbox = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def draw(self):
        pg.draw.rect(self.game.fight_area, (255, 255, 255), pg.Rect(self.pos[0] - 2, self.pos[1] - 2, self.size[0] + 4, self.size[1] + 4))
        pg.draw.rect(self.game.fight_area, (255, 0, 0), self.hitbox)
    
    def update(self):
        self.pos[1] += self.vel
        self.vel += 0.0062
        self.hitbox = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.draw()

class Full_Power_pickup(Power_pickup):
    def __init__(self, game, pos=(10, 300), vel=-0.2):
        self.game = game
        self.size = [20, 20]
        self.pos = list(pos)

        self.type = "pwr"

        self.points = 10
        if self.game.player.legacy_shots:
            self.power = 128
        else:
            self.power = 4.00
        
        self.vel = vel

        self.kill = False

        self.hitbox = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def draw(self):
        pg.draw.rect(self.game.fight_area, (255, 255, 255), pg.Rect(self.pos[0] - 2, self.pos[1] - 2, self.size[0] + 4, self.size[1] + 4))
        pg.draw.rect(self.game.fight_area, (200, 80, 0), self.hitbox)
    
    def update(self):
        self.pos[1] += self.vel
        self.vel += 0.0062
        self.hitbox = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.draw()

class Big_Power_pickup(Power_pickup):
    def __init__(self, game, pos=(10, 300), vel=-0.2):
        super().__init__(game, pos, vel)
        self.type = "pwr"
        self.size = [30, 30]
        self.points = 50
        if self.game.player.legacy_shots:
            self.power = 8
        else:
            self.power = 0.50

class Point_pickup(Power_pickup):
    def __init__(self, game, pos=(10, 300), vel=-0.2):
        self.game = game
        self.size = [20, 20]
        self.pos = list(pos)

        self.type = "col"

        self.points = 56550
        self.power = 1
        
        self.vel = vel

        self.kill = False

        self.hitbox = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def draw(self):
        pg.draw.rect(self.game.fight_area, (255, 255, 255), pg.Rect(self.pos[0] - 2, self.pos[1] - 2, self.size[0] + 4, self.size[1] + 4))
        pg.draw.rect(self.game.fight_area, (0, 0, 255), self.hitbox)
    
    def update(self):
        if self.pos[1] >= 1000:
            self.kill = True
        self.pos[1] += self.vel
        self.vel += 0.0062
        self.hitbox = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.draw()

class Life_pickup(Power_pickup):
    def __init__(self, game, pos=(10, 300), vel=-0.2):
        super().__init__(game, pos, vel)
        self.points = 100
        self.type = "life"
    

    def draw(self):
        pg.draw.rect(self.game.fight_area, (255, 255, 255), pg.Rect(self.pos[0] - 2, self.pos[1] - 2, self.size[0] + 4, self.size[1] + 4))
        pg.draw.rect(self.game.fight_area, (255, 0, 255), self.hitbox)

class Bomb_pickup(Power_pickup):
    def __init__(self, game, pos=(10, 300), vel=-0.2):
        super().__init__(game, pos, vel)
        self.points = 100
        self.type = "bom"
    

    def draw(self):
        pg.draw.rect(self.game.fight_area, (255, 255, 255), pg.Rect(self.pos[0] - 2, self.pos[1] - 2, self.size[0] + 4, self.size[1] + 4))
        pg.draw.rect(self.game.fight_area, (0, 255, 0), self.hitbox)

class Life_piece_pickup(Power_pickup):
    def __init__(self, game, pos=(10, 300), vel=-0.2):
        super().__init__(game, pos, vel)
        self.size = [16, 16]
        self.points = 20
        self.type = "lifepiece"
    

    def draw(self):
        pg.draw.rect(self.game.fight_area, (255, 255, 255), pg.Rect(self.pos[0] - 2, self.pos[1] - 2, self.size[0] + 4, self.size[1] + 4))
        pg.draw.rect(self.game.fight_area, (255, 0, 255), self.hitbox)