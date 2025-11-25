import pygame as pg
import math
import random

class BulletPattern:
    def __init__(self, game):
        self.game = game

    def shoot(self):
        pass

class CirclePattern(BulletPattern):
    def __init__(self, game, speed=1, pos=(0, 0), proj_type="big_ball_white", bullet_count=10):
        super().__init__(game)
        self.speed = speed
        self.pos = pos
        self.proj_type = proj_type
        self.bullet_count = bullet_count
    
    def shoot(self):
        for i in range(self.bullet_count):
            self.game.projregistry.shoot(self.proj_type, self.pos, 360 - (360 / i), self.speed)