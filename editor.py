# Core
import pygame as pg
import sys

# From
from character import *
from enemy import Enemy, WhiteFlame, Testboss
from pickups import *
from ui import *
from settings import *
from stage import *
from behaviors import *

# Mics
import random


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((RES))
        pg.display.set_caption("TH 69")
        self.clock = pg.time.Clock()

        #self.enemy_cooldown = 1000.0
        #self.cooldown = 1000.0

        self.time = 0
        self.allenemies = [Enemy, WhiteFlame, Testboss]
        self.allbehaviors = [MoveByPoints]

        self.sel_b = 0
        self.sel_e = 0

        self.selected_behavior = self.allbehaviors[self.sel_b]
        self.selected_enemy = self.allenemies[self.sel_e]

        #self.difficulties = ("Easy","Normal","Hard","Lunatic","Extra")
        #self.diff = self.difficulties[3]
        #self.min_rank = 5
        #self.rank = 5
        #self.max_rank = 34

        self.stagename = None

        self.in_menu = True
        self.in_select_menu = False

        self.fight_area = pg.Surface((400, 650))

        self.enemy_list = []

        self.mousepos = list(pg.mouse.get_pos())
        self.mouse_pos = [self.mousepos[0] - 50, self.mousepos[1] - 25]

        self.Menu()
    
    def exit(self):
        pg.quit()
        sys.exit()

    def goback(self):
        self.in_menu = True
        self.in_select_menu = False
        self.Menu()
    
    def create_a_stage(self, character):
        self.Character = character
        self.new_game()
    
    def select_character_menu(self):
        self.in_select_menu = True
        self.in_menu = False
        self.createastage = Selectable_Text(self, (70, 300), text="Create a stage", on_use=self.create_a_stage, args=self.stagename)
        self.gobacktomenu = Selectable_Text(self, (70, 330), text="Go Back", on_use=self.goback)
        self.menu_list = [self.createastage, self.gobacktomenu]
        self.menu_ui_selected = 0
        self.selected_button = self.menu_list[self.menu_ui_selected]
        self.selected_button.is_selected = True
    
    def Menu(self):
        self.start_the_game = Selectable_Text(self, (70, 300), text="Game Start", on_use=self.select_character_menu)
        self.settings = Selectable_Text(self, (50, 330), text="Settings")
        self.exitt = Selectable_Text(self, (70, 360), text="Exit", on_use=self.exit)
        self.menu_list = [self.start_the_game, self.settings, self.exitt]
        self.menu_ui_selected = 0
        self.selected_button = self.menu_list[self.menu_ui_selected]

    def new_game(self):
        self.in_select_menu = False
        self.in_menu = False

        #ui
        self.enemy_count_text = Text(self, (500, 80), text=f"Enemies in the stage: {len(self.enemy_list)}")
        self.sb_mm_text = Text(self, (500, 100), text=f"Selected Behavior: {self.selected_behavior}")
        self.se_mm_text = Text(self, (500, 120), text=f"Selected Enemy: {self.selected_enemy}")
        self.st_mm_text = Text(self, (500, 140), text=f"Time: {self.time}")

    def update(self):
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                self.exit()
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_F5:
                    pg.display.toggle_fullscreen()
                if ev.key == pg.K_ESCAPE:
                    self.is_paused = not self.is_paused
                if self.in_menu or self.in_select_menu:
                    if ev.key == pg.K_z:
                        if self.selected_button.args == None:
                            self.selected_button.on_use()
                        else:
                            self.selected_button.on_use(self.selected_button.args)
                    if ev.key == pg.K_UP:
                        self.selected_button.is_selected = False
                        self.menu_ui_selected -= 1
                    if ev.key == pg.K_DOWN:
                        self.selected_button.is_selected = False
                        self.menu_ui_selected += 1
                if not self.in_menu and not self.in_select_menu:
                    if ev.key == pg.K_UP:
                        self.sel_b -= 1
                    if ev.key == pg.K_DOWN:
                        self.sel_b += 1
                    if ev.key == pg.K_LEFT:
                        self.sel_e -= 1
                    if ev.key == pg.K_RIGHT:
                        self.sel_e += 1
                    if ev.key == pg.K_LALT:
                        self.time -= 1
                    if ev.key == pg.K_RALT:
                        self.time += 1
            if ev.type == pg.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    self.enemy_list.append(self.selected_enemy(self, self.mouse_pos, self.time))

        self.mousepos = pg.mouse.get_pos()
        self.mouse_pos =[self.mousepos[0] - 50, self.mousepos[1] - 25]

        self.screen.fill((0, 0, 0))
        if not self.in_menu and not self.in_select_menu:
            self.screen.fill((0, 80, 10))

            self.screen.blit(self.fight_area, (50, 25))
            self.fight_area.fill((0, 0, 0))

            for enemy in self.enemy_list:
                enemy.draw()
            
            self.enemy_count_text.text = f"Enemies in the stage: {len(self.enemy_list)}"
            self.sb_mm_text.text = f"Selected Behavior: {self.selected_behavior}"
            self.se_mm_text.text = f"Selected Enemy: {self.selected_enemy}"
            self.st_mm_text.text = f"Time: {self.time}"
            self.se_mm_text.update()
            self.sb_mm_text.update()
            self.st_mm_text.update()
            self.enemy_count_text.update()
        
        else:
            if self.in_menu:
                self.selected_button = self.menu_list[self.menu_ui_selected]
                self.start_the_game.update()
                self.exitt.update()
                self.settings.update()
                self.selected_button.is_selected = True
            else:
                self.selected_button = self.menu_list[self.menu_ui_selected]
                self.createastage.update()
                self.gobacktomenu.update()
                self.selected_button.is_selected = True
        pg.display.update()

        try:
            self.selected_behavior = self.allbehaviors[self.sel_b]
            self.selected_enemy = self.allenemies[self.sel_e]
        except:
            self.selected_behavior = self.allbehaviors[0]
            self.selected_enemy = self.allenemies[0]
    
    def run(self):
        while True:
            self.update()

if __name__ == "__main__":
    game = Game()
    game.stagename = input("Input a stage name(if you modifying a game stage, write a number between 1-7): ")
    game.run()