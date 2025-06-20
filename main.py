# Core
import pygame as pg
import sys

# From
from character import *
from enemy import Enemy, WhiteFlame, Testboss
from pickups import *
from ui import *
from settings import *
from spellcards import *

# Mics
import random


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((RES))
        pg.display.set_caption("TH 69")
        self.clock = pg.time.Clock()

        self.enemy_cooldown = 1000.0
        self.cooldown = 1000.0

        self.time = 0
        self.bossfight = False

        self.difficulties = ("Easy","Normal","Hard","Lunatic","Extra")
        self.diff = self.difficulties[1]
        self.min_rank = 5
        self.rank = 5
        self.max_rank = 34

        self.Character = None

        self.in_menu = True
        self.in_select_menu = False

        self.is_paused = False

        self.score = 0

        self.fight_area = pg.Surface((400, 650))

        self.proj_list = []
        self.player_proj = []
        self.enemy_list = []
        self.pickup_list = []
        self.particles = []

        self.Menu()
    
    def exit(self):
        pg.quit()
        sys.exit()

    def goback(self):
        self.in_menu = True
        self.in_select_menu = False
        self.Menu()
    
    def select_character(self, character):
        self.Character = character
        self.new_game()
    
    def select_character_menu(self):
        self.in_select_menu = True
        self.in_menu = False
        self.reimuA = Selectable_Text(self, (70, 300), text="Reimu: Fantasy Seal", on_use=self.select_character, args=ReimuA)
        self.reimuB = Selectable_Text(self, (70, 330), text="Reimu: Percusion Needle", on_use=self.select_character, args=ReimuB)
        self.marisaA = Selectable_Text(self, (70, 360), text="Marisa: Starlight Reverie", on_use=self.select_character, args=MarisaA)
        self.marisaB = Selectable_Text(self, (70, 390), text="Marisa: MASTER SPAAAAAAAAAAAAAAARK!!!", on_use=self.select_character, args=MarisaB)
        self.sanaeA = Selectable_Text(self, (70, 420), text="Sanae: Miracle Waves or smth", on_use=self.select_character, args=SanaeA)
        self.gobacktomenu = Selectable_Text(self, (70, 450), text="Go Back", on_use=self.goback)
        self.menu_list = [self.reimuA, self.reimuB, self.marisaA, self.marisaB, self.sanaeA, self.gobacktomenu]
        self.menu_ui_selected = 0
        self.selected_button = self.menu_list[self.menu_ui_selected]
        self.selected_button.is_selected = True
    
    def Menu(self):
        self.start_the_game = Selectable_Text(self, (70, 300), text="Game Start", on_use=self.select_character_menu)
        self.extra = Selectable_Text(self, (50, 330), text="Extra Start", is_selectable=False, on_use=self.select_character_menu)
        self.practice = Selectable_Text(self, (30, 360), text="Practice Start", is_selectable=False, on_use=self.select_character_menu)
        self.settings = Selectable_Text(self, (50, 390), text="Settings")
        self.exitt = Selectable_Text(self, (70, 420), text="Exit", on_use=self.exit)
        self.menu_list = [self.start_the_game, self.extra, self.practice, self.settings, self.exitt]
        self.menu_ui_selected = 0
        self.selected_button = self.menu_list[self.menu_ui_selected]

    def new_game(self):
        self.in_select_menu = False
        self.in_menu = False
        self.player = self.Character(self)
        self.enemy_list.append(Testboss(self, pos=(190, 200)))
        self.pickup_list.append(Big_Power_pickup(self, pos=(10, 100)))
        self.pickup_list.append(Big_Power_pickup(self, pos=(10, 150)))
        self.pickup_list.append(Big_Power_pickup(self, pos=(10, 200)))
        self.pickup_list.append(Big_Power_pickup(self, pos=(10, 300)))
        self.pickup_list.append(Live_pickup(self, pos=(10, 10)))
        self.pickup_list.append(Bomb_pickup(self, pos=(10, 15)))



        #ui
        self.lives_text = Text(self, (660, 150), text=f"Lives {self.player.lives}")
        self.bombs_text = Text(self, (660, 200), text=f"Bombs {self.player.bombs}")
        self.pause_text = Text(self, (0, 0), color=(255, 255, 255), text="Paused. Press Esc to continue")
        self.power_bar = Bar(self, (660, 250), text=f"{self.player.power}")
        self.score_text = Text(self, (660, 100), text=f"Score {self.score}")
        self.graze_text = Text(self, (660, 300), text=f"Graze {self.player.grazes}")
        self.boss_hp = Bar(self, (3, 5),size=5, text=f"{self.enemy_list[0].hp}")
        self.boss_hp.drawsurf = self.fight_area

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
                        if self.menu_ui_selected != 0:
                            self.selected_button.is_selected = False
                            self.menu_ui_selected -= 1
                    if ev.key == pg.K_DOWN:
                        if self.menu_ui_selected != len(self.menu_list) - 1:
                            self.selected_button.is_selected = False
                            self.menu_ui_selected += 1
                if self.is_paused:
                    if ev.key == pg.K_1:
                        self.Character = ReimuA
                    if ev.key == pg.K_2:
                        self.Character = ReimuB
                    if ev.key == pg.K_3:
                        self.Character = ReimuC
                    if ev.key == pg.K_4:
                        self.Character = MarisaA
                    if ev.key == pg.K_5:
                        self.Character = MarisaB
                    if ev.key == pg.K_6:
                        self.Character = SanaeA
                    if ev.key == pg.K_r:
                        self.enemy_list = []
                        self.pickup_list = []
                        self.proj_list = []
                        self.player_proj = []
                        self.new_game()
                        self.is_paused = False
        self.screen.fill((0, 0, 0))

        pg.display.set_caption(f"{self.clock.get_fps()}")

        if not self.in_menu and not self.in_select_menu:
                self.screen.fill((0, 80, 10))

                self.screen.blit(pg.transform.scale(self.fight_area, (570, 730)), (50, 25))
                self.fight_area.fill((0, 0, 0))

                if self.is_paused:
                    self.pause_text.update()
                    for proj in self.proj_list:
                        proj.draw()
                    
                    for proj in self.player_proj:
                        proj.draw()

                    for pickup in self.pickup_list:
                        pickup.draw()

                    for enemy in self.enemy_list:
                        enemy.draw()

                    for particle in self.particles:
                        particle.draw()
                
                self.score_text.update() 
                self.bombs_text.update()
                self.lives_text.update()
                self.power_bar.update()
                self.graze_text.update()
                if self.bossfight:
                    self.boss_hp.update()
                    self.boss_hp.bar_len = self.enemy_list[0].hp / 38
                    self.boss_hp.text = f"{self.enemy_list[0].hp}"


                self.player.draw()

                if not self.is_paused:
                    for proj in self.player_proj:
                        proj.update()
                        if proj.kill:
                            if proj.can_die:
                                self.player_proj.remove(proj)
                    self.player.update()
                    self.score_text.text = f"Score {000000000 + self.score}"
                    self.lives_text.text = f"Lives {self.player.lives}"
                    self.bombs_text.text = f"Bombs {self.player.bombs}"
                    self.graze_text.text = f"Graze {self.player.grazes}"
                    self.power_bar.bar_len = self.player.power
                    self.power_bar.text = f"{self.player.power}"
                
                    if self.cooldown <= 0:
                        for x in range(15):
                            self.enemy_list.append(WhiteFlame(self, (random.randint(0, 350), -40)))
                            self.cooldown = self.enemy_cooldown
                            if random.randint(1, 1000) >= 920:
                                self.enemy_list.append(Enemy(self, (random.randint(0, 350), -40)))
                    
                    for proj in self.proj_list:
                        proj.update()
                        if proj.kill:
                            if proj.can_die:
                                self.proj_list.remove(proj)

                    for pickup in self.pickup_list:
                        pickup.update()
                        if self.player.focus == True:
                            pickup.vel = self.player.item_slow_rate
                        if pickup.pos[1] >= 800:
                            self.pickup_list.remove(pickup)
                        if pickup.kill:
                            self.pickup_list.remove(pickup)
                        if self.player.pos[1] <= 100:
                            pickup.pos = self.player.pos
                    
                    for particle in self.particles:
                        particle.update()
                        if particle.kill:
                            self.particles.remove(particle)

                    try:
                        for enemy in self.enemy_list:
                            if enemy.is_boss == True:
                                self.bossfight = True
                            enemy.update()
                            if enemy.can_die:
                                if enemy.kill:
                                    self.bossfight = False
                                    self.enemy_list.remove(enemy)
                    except:
                        for enemy in self.enemy_list:
                            if enemy.is_boss == True:
                                self.bossfight = True
                            enemy.update()
                            if enemy.kill:
                                self.bossfight = False
                                self.enemy_list.remove(enemy) 
                    
                    if self.player.focus == True:
                        self.fight_area.blit(self.player.hitbox_img, (self.player.hitbox.x, self.player.hitbox.y))
                    
                    self.cooldown -= 0.01
        else:
            if self.in_menu:
                self.selected_button = self.menu_list[self.menu_ui_selected]
                self.start_the_game.update()
                self.practice.update()
                self.exitt.update()
                self.extra.update()
                self.settings.update()
                self.selected_button.is_selected = True
            else:
                self.selected_button = self.menu_list[self.menu_ui_selected]
                self.sanaeA.update()
                self.reimuA.update()
                self.reimuB.update()
                self.marisaA.update()
                self.marisaB.update()
                self.gobacktomenu.update()
                self.selected_button.is_selected = True
        pg.display.update()

        self.clock.tick(60)
    
    def run(self):
        while True:
            self.update()

if __name__ == "__main__":
    game = Game()
    game.run()