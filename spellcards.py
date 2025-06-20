import pygame as pg
from projectile import *
import random
import math


class Spellcard:
    def __init__(self, game, rank, difficulty=None, inflictor=None):
        self.game = game
        self.shoot_time = 40
        self.timeout = 60
        self.cooldown = 0
        self.rank = rank
        self.in_game_display_name = """Test: "?" """
        self.difficulty = difficulty
        self.inflictor = inflictor

    def do(self):
        if self.difficulty == "Easy" or self.difficulty == "Normal":
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(0, -1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(1, 0), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(-1, 0), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(1, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(1, -1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(-1, -1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(-1, 1), speed=4))
        if self.difficulty == "Hard" or self.difficulty == "Lunatic":
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(0, -1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(1, 0), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(-1, 0), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(1, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(1, -1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(-1, -1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(-1, 1), speed=4))

            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=2))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(0, -1), speed=2))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(1, 0), speed=2))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(-1, 0), speed=2))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(1, 1), speed=2))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(1, -1), speed=2))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(-1, -1), speed=2))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(-1, 1), speed=2))

    def update(self):
        pass

class Rage(Spellcard):
    def __init__(self, game, rank, difficulty=None, inflictor=None):
        self.game = game
        self.in_game_display_name = """Rage Sign: "Tearing Scream" """
        self.shoot_time = 40
        self.timeout = 60
        self.cooldown = 0
        self.rank = rank
        self.difficulty = difficulty
        self.inflictor = inflictor

    def do(self):
        if self.difficulty == "Easy" or self.difficulty == "Normal":
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] + 10, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] - 10, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] + 40, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] - 40, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] + 60, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] - 80, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] - 100, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] - 60, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] + 80, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] + 100, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] + 160, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] - 160, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] + 300, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] - 300, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))

            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] - 300, self.inflictor.pos[1] + 25), team="en", direction=(1, -1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] - 300, self.inflictor.pos[1] + 25), team="en", direction=(1, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] - 300, self.inflictor.pos[1] + 25), team="en", direction=(-1, 1), speed=4))

        if self.difficulty == "Hard" or self.difficulty == "Lunatic":
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] + 10, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] - 10, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] + 40, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] - 40, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] + 60, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] - 80, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] - 100, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] - 60, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] + 80, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] + 100, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] + 160, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] - 160, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] + 300, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0] - 300, self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=4))

            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(random.random(), random.random()), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(random.random(), random.random()), speed=8))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(random.random(), -random.random()), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(-random.random(), random.random()), speed=8))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(random.random(), -random.random()), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(-random.random(), -random.random()), speed=8))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(random.random(), -random.random()), speed=4))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(-random.random(), random.random()), speed=8))



    def update(self):
        pass

class SideShot(Spellcard):
    def __init__(self, game, rank, difficulty=None, inflictor=None):
        self.game = game
        self.shoot_time = 40
        self.timeout = 60
        self.cooldown = 0
        self.in_game_display_name = """Portal : "Bullets From Sides" """
        self.rank = rank
        self.difficulty = difficulty
        self.inflictor = inflictor

    def do(self):
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (1, random.randint(1, 650)), team="en", direction=(1, 0), speed=4))

        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
        self.game.proj_list.append(Projectile(self.game, (399, random.randint(1, 650)), team="en", direction=(-1, 0), speed=4))
            
    def update(self):
        pass