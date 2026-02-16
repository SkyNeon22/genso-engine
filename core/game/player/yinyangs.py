import pygame as pg
from core.game.projectile import *

class YingYang:
    def __init__(self, game, player, pos=(0, 0)):
          
        self.game = game
        self.player = player
        
        self.img = pg.image.load("assets/img/sprites/other/ying_reimu.png")

        self.pos = list(pos)
        self.homing_shot_cooldown = 0.9
        self.homing_cooldown = 0.0
        self.shot = Projectile
    
    def shoot(self):
        self.game.player_proj.append(self.shot(self.game, self.pos , speed=10))

    def update(self):
        self.game.fight_area.blit(pg.transform.scale(self.img, (15, 18)), self.pos)
