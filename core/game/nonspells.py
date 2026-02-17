import pygame as pg
from core.game.projectile import *
from core.additions.utils import get_angle
import random
import math

# 60 ticks = 1 second
class Nonspell:
    def __init__(self, game, inflictor=None, difficulty=None):
        self.game = game
        self.start_hp = int(inflictor.hp)
        self.active = False
        self.shoot_time = 5
        self.counter = 0
        self.alloc_hp = 3000
        self.timeout = 2400
        self.in_game_display_name = None # dont touch its fixes a crash
        self.old_time = self.timeout
        self.cooldown = 0
        self.difficulty = difficulty
        self.inflictor = inflictor
    
    def shoot(self, name="ball_white", pos=(0, 0), angle=0, speed=10):
        self.game.projregistry.shoot(name, pos, angle, speed)
    
    def shoottest(self, name="ball_white", pos=(0, 0), angle=0, speed=[10, 10]):
        self.game.projregistry.shoottest(name, pos, angle, speed)
        
    def do(self):
        pass

    def update(self):
        if not self.active:
            self.start_hp = int(self.inflictor.hp)
            self.active = True
            self.timeout = self.old_time
        elif self.active:
            self.timeout -= 1
            self.cooldown -= 1
            self.inflictor.dmg_resist = 1.0
            if self.cooldown <= 0:
                self.do()
                self.cooldown = self.shoot_time
            if self.timeout <= 0 or self.inflictor.hp < self.start_hp - self.alloc_hp:
                self.inflictor.hp = self.start_hp - self.alloc_hp
                self.inflictor.active_attack += 1
                self.game.proj_list.clear()
                self.active = False 
                