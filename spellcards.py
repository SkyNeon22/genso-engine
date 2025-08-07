import pygame as pg
from projectile import *
from pickups import *
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
            self.game.projregistry.shoot("ball_red", self.inflictor.hitbox.center, utils.get_direction(self.game.player.hitbox.center, self.inflictor.hitbox.center), 2.2)
            self.game.projregistry.shoot("ball_green", self.inflictor.hitbox.center, utils.get_direction(self.game.player.hitbox.center, self.inflictor.hitbox.center), 2.4) 
            self.game.projregistry.shoot("ball_blue", self.inflictor.hitbox.center, utils.get_direction(self.game.player.hitbox.center, self.inflictor.hitbox.center), 2.6)
            self.game.projregistry.shoot("ball_yellow", self.inflictor.hitbox.center, utils.get_direction(self.game.player.hitbox.center, self.inflictor.hitbox.center), 2.8)

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



class Spellcard01(Spellcard):
    def __init__(self, game, rank, difficulty=None, inflictor=None):
        super().__init__(game, rank, difficulty, inflictor) 
        self.shoot_time = 30
        self.counter = 0
        self.alloc_hp = 1000
        self.timeout = 1980
        self.old_time = self.timeout
        self.in_game_display_name = """Falling Sign: "Falling Particles -Easy-" """
            
    def do(self):
        self.game.projregistry.shoot("big_ball_light_blue", [random.randint(0, 384), 0], [0, 1], random.randint(20, 200) / 100)
        self.game.projregistry.shoot("big_ball_blue", [random.randint(0, 384), 0], [0, 1], random.randint(20, 200) / 100)
        self.counter += 1
        if self.counter % 10:
            self.game.projregistry.shoot("ball_green", self.inflictor.hitbox.center, utils.get_direction(self.game.player.hitbox.center, self.inflictor.hitbox.center), 2)

class Spellcard02(Spellcard):
    def __init__(self, game, rank, difficulty=None, inflictor=None):
        super().__init__(game, rank, difficulty, inflictor) 
        self.shoot_time = 25
        self.counter = 0
        self.alloc_hp = 1000
        self.timeout = 1980
        self.old_time = self.timeout
        self.in_game_display_name = """Falling Sign: "Falling Particles -Normal-" """
            
    def do(self):
        self.game.projregistry.shoot("big_ball_light_blue", [random.randint(0, 384), 0], [0, 1], random.randint(20, 200) / 100)
        self.game.projregistry.shoot("big_ball_blue", [random.randint(0, 384), 0], [0, 1], random.randint(20, 200) / 100)
        self.counter += 1
        if self.counter % 10:
            self.game.projregistry.shoot("ball_green", self.inflictor.hitbox.center, utils.get_direction(self.game.player.hitbox.center, self.inflictor.hitbox.center), 4)

class Spellcard03(Spellcard):
    def __init__(self, game, rank, difficulty=None, inflictor=None):
        super().__init__(game, rank, difficulty, inflictor) 
        self.shoot_time = 20
        self.counter = 0
        self.alloc_hp = 1000
        self.timeout = 1980 
        self.old_time = self.timeout
        self.in_game_display_name = """Falling Sign: "Falling Particles -Hard-" """
            
    def do(self):
        self.game.projregistry.shoot("big_ball_light_blue", [random.randint(0, 384), 0], [0, 1], random.randint(20, 200) / 100)
        self.game.projregistry.shoot("big_ball_blue", [random.randint(0, 384), 0], [0, 1], random.randint(20, 200) / 100)
        self.counter += 1
        if self.counter % 10:
            self.game.projregistry.shoot("ball_green", self.inflictor.hitbox.center, utils.get_direction(self.game.player.hitbox.center, self.inflictor.hitbox.center), 3)
            self.game.projregistry.shoot("ball_green", self.inflictor.hitbox.center, utils.get_direction(self.game.player.hitbox.center, self.inflictor.hitbox.center), 3)

class Spellcard01(Spellcard):
    def __init__(self, game, rank, difficulty=None, inflictor=None):
        super().__init__(game, rank, difficulty, inflictor) 
        self.shoot_time = 10
        self.counter = 0
        self.alloc_hp = 1000
        self.timeout = 1980
        self.old_time = self.timeout
        self.in_game_display_name = """Falling Sign: "Falling Particles -Lunatic-" """
            
    def do(self):
        self.game.projregistry.shoot("big_ball_light_blue", [random.randint(0, 384), 0], [0, 1], random.randint(20, 200) / 100)
        self.game.projregistry.shoot("big_ball_blue", [random.randint(0, 384), 0], [0, 1], random.randint(20, 200) / 100)
        self.counter += 1
        if self.counter % 5:
            self.game.projregistry.shoot("ball_green", self.inflictor.hitbox.center, utils.get_direction(self.game.player.hitbox.center, self.inflictor.hitbox.center), 2)
            self.game.projregistry.shoot("ball_green", self.inflictor.hitbox.center, utils.get_direction(self.game.player.hitbox.center, self.inflictor.hitbox.center), 2)
            self.game.projregistry.shoot("ball_green", self.inflictor.hitbox.center, utils.get_direction(self.game.player.hitbox.center, self.inflictor.hitbox.center), 2)