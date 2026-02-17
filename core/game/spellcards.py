import pygame as pg
from core.game.projectile import *
from core.game.pickups import *
from core.additions import get_angle
import random
import math

# 60 ticks = 1 second
class Spellcard:
    def __init__(self, game, rank, difficulty=None, inflictor=None):
        self.game = game
        self.start_hp = int(inflictor.hp)
        self.shoot_time = 40
        self.active = False
        self.alloc_hp = 1000
        self.timeout = 1980
        self.old_time = self.timeout
        self.cooldown = 0
        self.rank = rank
        self.in_game_display_name = """Test: "?" """
        self.difficulty = difficulty
        self.inflictor = inflictor
        self.done = False

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
            if self.cooldown <= 0:
                self.do()
                self.cooldown = self.shoot_time
            if self.timeout <= 0 or self.inflictor.hp < self.start_hp - self.alloc_hp:
                self.game.score += 100000 + (self.timeout * 100)
                self.inflictor.hp = self.start_hp - self.alloc_hp
                self.inflictor.active_attack += 1
                self.game.proj_list.clear()
                self.active = False
