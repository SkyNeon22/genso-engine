import pygame as pg
from projectile import *


class Nonspell:
    def __init__(self, game, inflictor=None, difficulty=None):
        self.game = game
        self.shoot_time = 400
        self.cooldown = 0
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
        if self.difficulty == "Hard":
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
        if self.difficulty == "Lunatic":
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

            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(0, 1), speed=6))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(0, -1), speed=6))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(1, 0), speed=6))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(-1, 0), speed=6))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(1, 1), speed=6))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(1, -1), speed=6))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(-1, -1), speed=6))
            self.game.proj_list.append(Projectile(self.game, (self.inflictor.pos[0], self.inflictor.pos[1] + 25), team="en", direction=(-1, 1), speed=6))
        
    def update(self):
        self.cooldown -= 1

        if self.cooldown <= 0:
            self.do()
            self.cooldown = self.shoot_time
