from core.game import *
import pygame as pg


# 60 ticks = 1 second
class Spellcard:
    def __init__(self, game, inflictor=None):
        self.game = game

        self.start_hp = int(inflictor.hp)
        self.alloc_hp = 1000


        self.time = 0
        self.timeout = 1980
        self.old_time = self.timeout
        self.do_start = False
        
        self.in_game_display_name = """Test: "?" """
        self.bg = pg.image.load("assets/img/guesswhatismissing.png")
        self.blit_portrait = pg.image.load("assets/img/guesswhatismissing.png")
        self.inflictor = inflictor
        self.dmg_res = 0.3

        self.start_pos = [(self.game.fight_area.get_width() / 2) - (self.inflictor.center[0] / 2), self.game.fight_area.get_height() / 4]

        self.pos_x = -200
        self.pos_y = 0
        self.font = pg.font.SysFont('notosansjp', 14)
    
    def spell_open_animation(self):
        self.pos_x += 5
        self.pos_y += 2
        if self.pos_x >= 700:
                self.do_start = True
    
    def draw_name(self):
        text_surface = self.font.render(self.in_game_display_name, True, (255, 255, 255))
        self.game.screen.blit(text_surface, [60, 0])
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
        pass

    def update(self):
        self.game.fight_area.blit(self.bg, (0, 0))
        self.draw_name()
        if self.do_start:
            self.timeout -= 1
            self.time += 1
            self.inflictor.dmg_resist = self.dmg_res
            self.do()
            if self.timeout <= 0 or self.inflictor.hp < self.start_hp - self.alloc_hp:
                self.inflictor.hp = self.start_hp - self.alloc_hp
                self.inflictor.active_attack += 1
                self.game.proj_list.clear()
        else:
            self.start_hp = int(self.inflictor.hp)
            self.timeout = self.old_time
            self.inflictor.dmg_resist = 0
            self.inflictor.pos = self.start_pos
            self.game.fight_area.blit(self.blit_portrait, (self.pos_x, self.pos_y))
            self.spell_open_animation()

