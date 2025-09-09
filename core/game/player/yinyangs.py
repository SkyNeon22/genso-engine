import pygame as pg
from core.game.projectile import *

class YingYang:
    def __init__(self, game, player, pos=(0, 0)):
          
        self.game = game
        self.player = player
        
        self.img = pg.image.load("assets/img/sprites/other/ying_reimu.png")

        self.pos = list(pos)
        self.homing_shot_cooldown = 0.9
        self.homing_cooldown = 0.0
        self.shot = Homing_Projectile
    
    def shoot(self):
        self.game.player_proj.append(self.shot(self.game, self.pos))

    def update(self):
        self.game.fight_area.blit(pg.transform.scale(self.img, (15, 18)), self.pos)

class YingYangReimuA(YingYang):
    def __init__(self, game, player, pos=(0, 0)):
        super().__init__(game, player, pos)

        self.img = pg.image.load("assets/img/sprites/other/ying_reimu.png")

        self.homing_shot_cooldown = 0.9
        self.homing_cooldown = 0.0
        self.shot = ReimuHomingNormal

class YingYangReimuB(YingYang):
    def __init__(self, game, player, pos=(0, 0)):
        super().__init__(game, player, pos)
        
        
        self.img = pg.image.load("assets/img/sprites/other/ying_reimu.png")

        self.homing_shot_cooldown = 0.9
        self.homing_cooldown = 0.0
        self.shot = ReimuNeedleNormal
    
    def shoot(self):
        self.game.player_proj.append(self.shot(self.game, (self.pos[0] + 11, self.pos[1])))
        self.game.player_proj.append(self.shot(self.game, (self.pos[0] - 11, self.pos[1])))

class YingYangReimuC(YingYang):
    def __init__(self, game, player, pos=(0, 0)):
        super().__init__(game, player, pos)
        
        
        self.img = pg.image.load("assets/img/sprites/other/ying_reimu.png")

        self.homing_shot_cooldown = 0.1
        self.homing_cooldown = 0.0
        self.shot = ReimuHomingNormal
        self.shott = ReimuNeedleNormal
    
    def shoot(self):
        if not self.player.focus:
            self.game.player_proj.append(self.shot(self.game, self.pos))
        else:
            self.game.player_proj.append(self.shott(self.game, (self.pos[0] + 11, self.pos[1])))
            self.game.player_proj.append(self.shott(self.game, (self.pos[0] - 11, self.pos[1])))

class YingYangMarisaA(YingYang):
    def __init__(self, game, player, pos=(0, 0)):
        super().__init__(game, player, pos)
        
        self.img = pg.image.load("assets/img/sprites/other/ying_marisa.png")

        self.homing_shot_cooldown = 1.4
        self.homing_cooldown = 0.0
        self.shot = MarisaRocketNormal

class YingYangMarisaB(YingYang):
   def __init__(self, game, player, pos=(0, 0)):
        super().__init__(game, player, pos)
        
        
        self.img = pg.image.load("assets/img/sprites/other/ying_marisa.png")

        self.homing_shot_cooldown = 0.1
        self.homing_cooldown = 0.0
        self.shot = MarisaLaserNormal

class YingYangSanaeA(YingYang):
    def __init__(self, game, player, pos=(0, 0)):
        super().__init__(game, player, pos)
        
        
        self.img = pg.image.load("assets/img/sprites/other/ying_sanae.png")

        self.homing_shot_cooldown = 0.21
        self.homing_cooldown = 0.0
        self.shot = SanaeWaveNormal
    
    def shoot(self):
        self.game.player_proj.append(self.shot(self.game, self.pos))
