import pygame as pg
from core.game.projectile import *
from core.game.pickups import *
from core.game.spellcards import *
from core.game.nonspells import *
from core.game.registries import REGISTRY
from core.game.colliders import CircleCollider
import random

behavioregistry = REGISTRY(None)

behavioregistry.register('none', None)
behavioregistry.register('movebypoints', MoveByPoints)
# the enemy classs
# 1 second = 60 ticks
class Enemy:
    def __init__(self, game, pos=(190, 400), time=0, behavior=None, behavior_args=[]):
        self.game = game
        self.type = "enemy" # enemy's class name (so stage loader can understand what class to append(manually add for every enemy class in stage.py) if not using registries)
        self.col_dmg = False # check if you want for the enemy to deal contact damage
        self.time = time # timings in ticks 
        self.speed = 1 # speed
        self.dmg_resist = 1 # dmg taken percens (set 100%)
        self.damage = 20 # ? does nothing
        self.behavior = behavior # behavior of the enemy (see behaviors.py)
        self.args = behavior_args  # behavior arguments
        self.hp = 20 # enemy health
        self.is_boss = False # self explanatonary

        self.shot_cooldown = 3.04 # cooldown for shots (from prototype versions when there was no fps cap cuz I just forgot to add it)
        self.cooldown = 0.0 # cooldown for shots

        self.kill = False # kill flag 

        # self explanatonary
        self.pos = list(pos)
        self.size = (30, 45)
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))
        self.bh_enabled = True

        self.can_die = True # break the rules (makes the enemy ignore kill flag)
        self.iframes = -1 # stop registering damage for a short time

        self.invurnelable = False # the same for iframes

        self.hitbox = CircleCollider(10, self.center) # hitbox
        try:
            self.behavior = self.behavior(self.game, self, self.args)
        except Exception:
            self.behavior = behavior
            self.bh_enabled = False
    
    def todict(self): # method for saving an enemy object to a stage file
        return {"game": None,
                "type": self.type,
                "time": self.time,
                "dmg_resist": self.dmg_resist,
                "behavior": self.behavior,
                "behavior_args": self.args,
                "pos": self.pos,
        }

    @classmethod
    def fromdict(cls, asset, game=None): # method for loading an enemy object from a stage file
        return cls(asset["game"] or game,asset["pos"], asset["time"], behavioregistry.rglist.get(asset["behavior"]), asset["behavior_args"])

    def check_despawn(self): # despawn when outside of the fight area (you can change the values for more outside room of despawn)
        if self.pos[0] < -80 or self.pos[0] > 400 or self.pos[1] < -80 or self.pos[1] > 498:
            self.kill = True

    def check_bullet(self): # check for player projectiles
        for bul in self.game.player_proj:
            if self.hitbox.collidecircle(bul.hitbox):
                if not self.invurnelable and self.iframes <= 0:
                    self.hp -= bul.damage * self.dmg_resist
                    self.game.score += 10
                    bul.kill = True 
    
    def shoot(self):
        self.game.proj_list.append(Projectile(self.game, (self.pos[0], self.pos[1] + 25), team="en", direction=(0, 1), speed=0.4))

    def draw(self): # draw function
        pg.draw.rect(self.game.fight_area, (200, 0, 0), pg.Rect(self.pos, self.size))

    def drop(self):
        drop = random.randint(1, 100)
        if drop >= 60 and drop <= 84:
            self.game.pickup_list.append(Point_pickup(self.game, pos=self.pos))
        if drop >= 85 and drop <= 99:
            self.game.pickup_list.append(Power_pickup(self.game, pos=self.pos))
        elif drop >= 100:
            self.game.pickup_list.append(Big_Power_pickup(self.game, pos=self.pos))

    def update(self): # update the enemy
        if self.game.frametime >= self.time:
            if self.cooldown <= 0:
                self.shoot()
                self.cooldown = self.shot_cooldown
            self.cooldown -= 0.01
            if self.bh_enabled:
                self.behavior.update()
            if self.hp <= 0:
                self.kill = True
                self.drop()
            self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))
            self.hitbox.update(self.center)
            self.check_bullet()
            self.check_despawn()
            self.draw()

class Testboss(Enemy): # fork of the enemy class to make a boss (if you want to make a boss fork this class)
    # commenting this shit another time
    def __init__(self, game, pos=(190, 400), time=0, behavior=None, behavior_args=[]):
        super().__init__(game, pos, time, behavior, behavior_args)
        self.game = game 
        self.type = "testboss"
        self.col_dmg = False
        self.dmg_resist = 1
        self.behavior = behavior
        self.args = behavior_args
        self.theme_id = 1
        self.speed = 0.04
        self.damage = 20
        self.time = time
        self.active_spell = None # ignore
        self.is_boss = True # needed for showing the bossbar and timeout timer
        self.hp = 8000
        self.active_attack = 0 # for determing what attack should be active 
        self.shot_cooldown = 3.0
        self.cooldown = 0.0
        self.img = pg.image.load("assets/img/sprites/enemies/bosses/rumia/Rumia.png")

        self.kill = False

        self.pos = list(pos)
        self.size = (50, 50)
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))
        self.music_done = False

        self.can_die = True
        self.iframes = 0

        self.invurnelable = False

        self.hitbox = CircleCollider(40, self.center)
        self.nonspells = [Nonspell(self.game, self, self.game.diff)] # non lists (if no registies used)
        self.spellcards = [Spellcard(self.game, 5, self.game.diff, self)] # spell lists (if no registies used)
        self.attorder = [self.nonspells[0], self.spellcards[0], self.nonspells[0], self.spellcards[0]] # attack order

    def check_bullet(self): # check for player projectiles
        for bul in self.game.player_proj:
            if self.hitbox.collidecircle(bul.hitbox):
                if not self.invurnelable:
                    self.game.soundregistry.rglist["damage00"].play()
                    self.hp -= bul.damage * self.dmg_resist
                    self.game.score += 10
                    bul.kill = True
                    #if not self.game.soundregistry.get("damage00").get_busy():
                    #    self.game.soundregistry.get("damage00").play()
    
    def draw(self):
        self.game.fight_area.blit(self.img, (self.pos[0], self.pos[1]))#(self.pos[0] -10, self.pos[1])) why'd I even put -10 to the  x position 💀💀
    
    def update(self):
        if self.game.frametime >= self.time:
            if not self.music_done:
                self.game.current_song = 1
                self.game.musicregistry.rglist[self.game.current_song].stop()
                self.game.musicregistry.rglist[self.theme_id].play(self.game.musicvolume)
                self.music_done = True
            self.game.soundregistry.rglist["damage00"].reload()
            if self.attorder[self.active_attack] !=  None:
                self.game.active_spell = self.attorder[self.active_attack].in_game_display_name
            else:
                self.game.active_spell = None
            try:
                if self.active_attack <= len(self.attorder):
                    self.attorder[self.active_attack].update()
                else:
                    self.kill = True
                    self.game.active_spell = None
            except IndexError:
                self.kill = True
                self.game.active_spell = None
            #if self.hp != 0:
            #   self.non_attack(self.nonspells[0], 8000)
            self.cooldown -= 1
            #self.pos[1] += self.speed
            if self.hp <= 0:
                for proj in self.game.proj_list:
                    proj.destroy()
                self.kill = True
                self.game.active_spell = None
                self.drop()
            self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))
            self.hitbox.update(self.center)
            self.check_bullet()
            self.check_despawn()
            self.draw()
