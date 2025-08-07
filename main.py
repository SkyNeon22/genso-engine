# Core
import pygame as pg
import sys
import moderngl
import array

# From
from character import *
from pickups import *
from ui import *
from configs.settings import *
from spellcards import *
from stage import *
from utils.registries import *
from components.sound import *

# Mics
import random

 
class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.window = pg.display.set_mode((RES), pg.OPENGL | pygame.DOUBLEBUF)
        self.screen = pg.surface.Surface((RES))
        pg.display.set_caption("TH 69")
        self.clock = pg.time.Clock()
        self.ctx = moderngl.create_context()

        self.frametime = 0
        self.bossfight = False

        self.difficulties = ("Easy","Normal","Hard","Lunatic","Extra")
        self.diff = self.difficulties[2]
        self.min_rank = 5
        self.rank = 5
        self.max_rank = 34

        self.Character = None
        self.active_spell = None

        self.in_menu = True
        self.in_select_menu = False

        self.is_paused = False

        self.score = 0

        self.fight_area = pg.Surface((384, 448),pg.SRCALPHA)

        self.proj_list = []
        self.player_proj = []
        self.enemy_list = []
        self.pickup_list = []
        self.particles = []

        self.pentabuff = self.ctx.buffer(data=array.array('f', [
            # pos (x, y, z), uv coords (x, y)
            -1.0, 1.0, 0.0,   0.0, 0.0,  #topleft
            1.0, 1.0, 0.0,   1.0, 0.0,   #topright
            -1.0, -1.0, 0.0,   0.0, 1.0, #botleft
            1.0, -1.0, 0.0,   1.0, 1.0,  #botright
        ]))

        with open("shaders\\frag.glsl") as file:
            frag = file.read()
        with open("shaders\\vert.glsl") as file:
            vert = file.read()

        self.program = self.ctx.program(vertex_shader=vert, fragment_shader=frag)
        self.renderobject = self.ctx.vertex_array(self.program, [(self.pentabuff, '3f 2f', 'vert', 'texcoord')])

        self.stage = "1.stg"
        self.stagesystem = StageSystem(game=self, mapfile=self.stage)
        self.projregistry = PROJECTILE_REGISTRY(self) # a projectile registry  
        self.soundregistry = SOUND_REGISTRY(self)

        self.Menu()
    
    def surt_to_tex(self, surf):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = "BGRA"
        tex.write(surf.get_view('1'))
        return tex
    
    def exit(self):
        self.program.release()
        self.renderobject.release()
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
        self.reimuA = Selectable_Text(self, (70, 200), text="Reimu: Fantasy Seal", on_use=self.select_character, args=ReimuA)
        self.reimuB = Selectable_Text(self, (70, 230), text="Reimu: Persuasion Needle", on_use=self.select_character, args=ReimuB)
        self.marisaA = Selectable_Text(self, (70, 260), text="Marisa: Starlight Reverie", on_use=self.select_character, args=MarisaA)
        self.marisaB = Selectable_Text(self, (70, 290), text="Marisa: Illusion lazer", on_use=self.select_character, args=MarisaB)
        self.sanaeA = Selectable_Text(self, (70, 320), text="Sanae: Miracle winds", on_use=self.select_character, args=SanaeA)
        self.gobacktomenu = Selectable_Text(self, (70, 350), text="Go Back", on_use=self.goback)
        self.menu_list = [self.reimuA, self.reimuB, self.marisaA, self.marisaB, self.sanaeA, self.gobacktomenu]
        self.menu_ui_selected = 0
        self.selected_button = self.menu_list[self.menu_ui_selected]
        self.selected_button.is_selected = True
    
    def Menu(self):
        self.start_the_game = Selectable_Text(self, (70, 200), text="Game Start", on_use=self.select_character_menu)
        self.extra = Selectable_Text(self, (50, 230), text="Extra Start", is_selectable=False, on_use=self.select_character_menu)
        self.practice = Selectable_Text(self, (30, 260), text="Practice Start", is_selectable=False, on_use=self.select_character_menu)
        self.settings = Selectable_Text(self, (50, 290), text="Settings")
        self.exitt = Selectable_Text(self, (70, 320), text="Exit", on_use=self.exit)
        self.menu_list = [self.start_the_game, self.extra, self.practice, self.settings, self.exitt]
        self.menu_ui_selected = 0
        self.selected_button = self.menu_list[self.menu_ui_selected]

    def new_game(self):
        self.in_select_menu = False
        self.in_menu = False
        self.player = self.Character(self, pos=(194, 350),start_power=4.0)
        self.enemy_list = self.stagesystem.init_map()

        #ui
        self.lives_text = Text(self, (420, 80), text=f"Lives {self.player.lives}", size=25)
        self.pieces_text = Text(self, (420, 110), text=f"Pieces {self.player.life_pieces}", size=18)
        self.bombs_text = Text(self, (420, 130), text=f"Bombs {self.player.bombs}", size=25)
        self.pause_text = Text(self, (0, 0), color=(255, 255, 255), text="Paused. Press Esc to continue")
        self.power_text = Text(self, (420, 180), text=f"{round(self.player.power, 3)}", size=25)
        self.score_text = Text(self, (420, 30), text=f"Score {self.score}", size=25)
        self.graze_text = Text(self, (420, 230), text=f"Graze {self.player.grazes}", size=25)
        self.spell_text = Text(self, (200, 20), text=f"", size=15)
        #self.spell_text = Text(self, (200, 30))
        #self.spell_text.drawsurf = self.fight_area
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
                    if self.is_paused:
                        self.soundregistry.get("pause").play()
                        self.soundregistry.get("pause").reload()
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
                        self.score = 0
                        self.enemy_list = []
                        self.pickup_list = []
                        self.proj_list = []
                        self.player_proj = []
                        self.frametime = 0
                        self.new_game()
                        self.is_paused = False

        frametex = self.surt_to_tex(self.screen)
        frametex.use(0)
        self.program['tex'] = 0
        self.renderobject.render(mode=moderngl.TRIANGLE_STRIP)
        
        self.screen.fill((0, 0, 0))

        pg.display.set_caption(f"{self.clock.get_fps()}")

        if not self.in_menu and not self.in_select_menu:
                self.screen.fill((0, 80, 10))

                self.screen.blit(self.fight_area, (32, 16))
                self.fight_area.fill((0, 0, 0, 255))

                if self.active_spell != None:
                    self.spell_text.text = self.active_spell
                    self.spell_text.update()

                if self.is_paused:
                    self.pause_text.update()
                    for proj in self.proj_list:
                        proj.draw()
                    
                    for proj in self.player_proj:
                        proj.draw()

                    for pickup in self.pickup_list:
                        pickup.draw()

                    for enemy in self.enemy_list:
                        if self.frametime >= enemy.time:
                            enemy.draw() 

                    for particle in self.particles:
                        particle.draw()
                
                self.score_text.update() 
                self.bombs_text.update()
                self.lives_text.update()
                self.pieces_text.update()
                self.power_text.update()
                self.graze_text.update()
                if self.bossfight:
                    self.boss_hp.update()

                self.player.draw()

                if not self.is_paused:
                    for proj in self.player_proj:
                        proj.update()
                        if proj.kill:
                            if proj.can_die:
                                self.player_proj.remove(proj)
                    self.player.update()
                    self.score_text.text = f"Score: {000000000 + self.score}"
                    self.lives_text.text = f"Lives: {self.player.lives}"
                    self.pieces_text.text = f"Pieces: {self.player.life_pieces}/{self.player.piecesforlife}"
                    self.bombs_text.text = f"Bombs: {self.player.bombs}"
                    self.graze_text.text = f"Graze: {self.player.grazes}"
                    self.power_text.text = f"Power: {round(self.player.power, 3)}"
                
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
                            if enemy.is_boss == True and self.frametime >= enemy.time:
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
                    self.frametime += 1
                    
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
        pg.display.flip()

        frametex.release()

        self.clock.tick(60)
    
    def run(self):
        while True:
            self.update()

if __name__ == "__main__":
    game = Game()
    game.run()