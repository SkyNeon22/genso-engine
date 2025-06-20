import pygame as pg
from projectile import *
from pickups import *
from spellcards import *
from nonspells import *
import random


class Enemy:
    def __init__(self, game, pos=(190, 400), time=0, behavior=None):
        self.game = game
        self.col_dmg = False
        self.time = time
        self.speed = 0.04
        self.dmg_resist = 1
        self.damage = 20
        self.behavior = behavior
        self.hp = 20
        self.is_boss = False

        self.shot_cooldown = 3.04
        self.cooldown = 0.0

        self.kill = False

        self.pos = list(pos)
        self.size = (30, 45)

        self.can_die = True
        self.iframes = 0

        self.invurnelable = False

        self.hitbox = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def check_bullet(self):
        for bul in self.game.player_proj:
            if self.hitbox.colliderect(bul.hitbox):
                if not self.invurnelable:
                    self.hp -= bul.damage * self.dmg_resist
                    self.game.score += 10
                    bul.kill = True

    def draw(self):
        pg.draw.rect(self.game.fight_area, (200, 0, 0), self.hitbox)

    def update(self):
        if self.cooldown <= 0:
            self.game.proj_list.append(Projectile(self.game, (self.pos[0], self.pos[1] + 25), team="en", direction=(0, 1), speed=0.4))
            self.cooldown = self.shot_cooldown
        self.cooldown -= 0.01
        self.pos[1] += self.speed
        if self.hp <= 0:
            self.kill = True
            drop = random.randint(1, 100)
            if drop >= 60 and drop <= 84:
                self.game.pickup_list.append(Point_pickup(self.game, pos=self.pos))
            if drop >= 85 and drop <= 99:
                self.game.pickup_list.append(Power_pickup(self.game, pos=self.pos))
            elif drop >= 100:
                self.game.pickup_list.append(Big_Power_pickup(self.game, pos=self.pos))
        self.hitbox = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.check_bullet()
        self.draw()

class WhiteFlame(Enemy):
    def __init__(self, game, pos=(190, 400), time=0, behavior=None):
        super().__init__(game, pos, time, behavior)
        self.speed = 0.34
        self.damage = 0
        self.hp = 40
        self.is_boss = False
        self.behavior = behavior

        self.shot_cooldown = 1000.0
        self.cooldown = 1000.0
    
    def draw(self):
        pg.draw.rect(self.game.fight_area, (255, 255, 255), self.hitbox)

class Testboss(Enemy):
    def __init__(self, game, pos=(190, 400), time=0, behavior=None):
        self.game = game
        self.col_dmg = True
        self.dmg_resist = 1
        self.behavior = behavior
        self.speed = 0.04
        self.damage = 20
        self.time = time
        self.is_boss = True
        self.hp = 8000

        self.shot_cooldown = 3.0
        self.cooldown = 0.0
        self.img = pg.image.load("sprites/enemies/bosses/rumia/Rumia.png")

        self.kill = False

        self.pos = list(pos)
        self.size = (50, 50)

        self.can_die = True
        self.iframes = 0

        self.invurnelable = False

        self.hitbox = pg.Rect(self.pos[0] - 10, self.pos[1] - 10, self.size[0], self.size[1])
        self.nonspells = [Nonspell(self.game, self, self.game.diff)] 
        self.spellcards = [Spellcard(self.game, 5, self.game.diff, self), Rage(self.game, 5, self.game.diff, self), SideShot(self.game, 5, self.game.diff, self)]
    
    def draw(self):
        self.game.fight_area.blit(self.img, (self.pos[0] - 10, self.pos[1]))
    
    def update(self):
        self.spellcards[0].update()
        if self.hp >= 7000:
                self.nonspells[0].update()
        if self.cooldown <= 0:
            if self.hp >= 3500 and self.hp <= 7000:
                self.spellcards[1].do()
                self.cooldown = self.spellcards[1].shoot_time
            elif self.hp <= 3500:
                self.spellcards[2].do()
                self.cooldown = self.spellcards[2].shoot_time
        self.cooldown -= 1
        #self.pos[1] += self.speed
        if self.hp <= 0:
            self.kill = True
            drop = random.randint(1, 100)
            if drop >= 60 and drop <= 84:
                self.game.pickup_list.append(Point_pickup(self.game, pos=self.pos))
            if drop >= 85 and drop <= 99:
                self.game.pickup_list.append(Power_pickup(self.game, pos=self.pos))
            elif drop >= 100:
                self.game.pickup_list.append(Big_Power_pickup(self.game, pos=self.pos))
        self.hitbox = pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.check_bullet()
        self.draw()
