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
        self.shoot_time = 1
        self.counter = 0
        self.alloc_hp = 3000
        self.timeout = 2400
        self.in_game_display_name = None # dont touch its fixes a crash
        self.old_time = self.timeout
        self.cooldown = 0
        self.difficulty = difficulty
        self.inflictor = inflictor
        
        self.font = pg.font.SysFont('notosansjp', 14)
    
    def draw_name(self):
        timeout_surface = self.font.render(str((self.timeout // 60)), True, (255, 255, 255))
        self.game.screen.blit(timeout_surface, [30, 0])
    
    def shoot(self,group=0, proj_id: str= "ball_white", position: list= (0, 0), angle: float=0, speed: float=1):
        '''Shoots a projectile from the game's projectile registry,
           proj_id: internal registry id,
           position: position,
           angle: an angle, at what the projectile would go (in degrees),
           speed: projectile speed'''
        self.game.projregistry.shoot(group, proj_id, position, angle, speed)

    def do(self):
        self.counter += 1
        if self.counter % 25 == 0:
            self.game.projregistry.shoot(1, "ball_blue", self.inflictor.hitbox.position, random.randint(0, 360), 0.5)
        if self.counter % 10 == 0:
            self.game.projregistry.shoot(0, "ball_red", self.inflictor.hitbox.position, get_angle(self.game.player.hitbox.position ,self.inflictor.hitbox.position), 3)
        if self.counter % 60 == 0:
            modified_projs = list(filter(lambda pr: pr.bulletgroup == 1, self.game.proj_list))
            for proj in modified_projs:
                proj.change_angle(get_angle(self.game.player.hitbox.position ,self.inflictor.hitbox.position))
                proj.change_speed(5)
                modified_projs.remove(proj)

    def update(self):
        if not self.active:
            self.start_hp = int(self.inflictor.hp)
            self.active = True
            self.timeout = self.old_time
        elif self.active:
            self.draw_name()
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
                