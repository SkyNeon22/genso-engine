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

    def do(self):
        self.game.projregistry.testshoot("ball_red", self.inflictor.hitbox.center, get_angle(self.game.player.hitbox.center ,self.inflictor.hitbox.center), 3)

        
        
        
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


class Nonspell01(Nonspell):
    def __init__(self, game, inflictor=None, difficulty=None):
        super().__init__(game, inflictor, difficulty)
        self.shoot_time = 120
        self.alloc_hp = 3000
        self.timeout = 2400
    
    def do(self):
        self.game.projregistry.shoot("opaque_ball_green", [0, self.game.player.hitbox.y], [1, 0], 0.6, directional=True)
        self.game.projregistry.shoot("opaque_ball_green", [384, self.game.player.hitbox.y], [-1, 0], 0.6, directional=True)
        self.game.projregistry.shoot("opaque_ball_green", [self.game.player.hitbox.x, 0], [0, 1], 0.6, directional=True)
        self.game.projregistry.shoot("opaque_ball_green", [self.game.player.hitbox.x, 448], [0, -1], 0.6, directional=True)
        self.game.projregistry.shoot("opaque_ball_green", [0, self.game.player.hitbox.y], [1, 0], 0.2, directional=True)
        self.game.projregistry.shoot("opaque_ball_green", [384, self.game.player.hitbox.y], [-1, 0], 0.2, directional=True)
        self.game.projregistry.shoot("opaque_ball_green", [self.game.player.hitbox.x, 0], [0, 1], 0.2, directional=True)
        self.game.projregistry.shoot("opaque_ball_green", [self.game.player.hitbox.x, 448], [0, -1], 0.2, directional=True)
                
