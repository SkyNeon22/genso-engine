import pygame as pg


class Particle:
    def __init__(self, game, time=60, pos=(69, 911)):
        self.game = game
        self.pos=list(pos)
        self.time = time
        self.timer = 0
        self.kill = False
        self.img = pg.image.load("sprites/other/explosionfromtemu.png")

    def draw(self):
        self.game.fight_area.blit(self.img, self.pos)

    def update(self):
        self.draw()
        self.timer += 1
        if self.timer == self.time:
            self.kill = True

class MiracleWave:
    def __init__(self, game, time=20, pos=(69, 911)):
        self.game = game
        self.pos=list(pos)
        self.time = time
        self.timer = 0
        self.kill = False
        self.img = pg.image.load("sprites/bullets/g_s.png")

    def draw(self):
        self.game.fight_area.blit(self.img, self.pos)

    def update(self):
        self.draw()
        self.timer += 1
        if self.timer == self.time:
            self.kill = True