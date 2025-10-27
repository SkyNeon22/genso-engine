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

    def do(self):
        self.game.projregistry.shoot("ball_red", self.inflictor.hitbox.center, get_angle(self.game.player.hitbox.center ,self.inflictor.hitbox.center), 3)
        self.game.projregistry.shoot("big_ball_green", (random.randint(0, 400), 0), random.randint(-30, 30), random.randint(1, 4))
        self.game.projregistry.shoot("big_ball_yellow", (random.randint(0, 400), 0), random.randint(-30, 30), random.randint(1, 4))
        self.game.projregistry.shoot("big_ball_pink", (random.randint(0, 400), 0), random.randint(-30, 30), random.randint(1, 4))
        self.game.projregistry.shoot("big_ball_blue", (random.randint(0, 400), 0), random.randint(-30, 30), random.randint(1, 4))

    def update(self):
        if not self.active:
            self.start_hp = int(self.inflictor.hp)
            self.active = True
            self.timeout = self.old_time
        elif self.active:
            self.timeout -= 1
            self.cooldown -= 1
            self.inflictor.dmg_resist = 0.6
            if self.cooldown <= 0:
                self.do()
                self.cooldown = self.shoot_time
            if self.timeout <= 0 or self.inflictor.hp < self.start_hp - self.alloc_hp:
                self.inflictor.hp = self.start_hp - self.alloc_hp
                self.inflictor.active_attack += 1
                self.game.proj_list.clear()
                self.active = False
