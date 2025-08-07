# Core
import pygame as pg
import sys
import moderngl
import array

# From
from character import *
from enemy import Enemy, WhiteFlame, Testboss
from pickups import *
from ui import *
from configs.settings import *
from stage import *
from behaviors import *
from utils.registries import *
from components.sound import *

# Mics
import random


# dont forget 1 second = 60 ticks
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((RES_EDITOR), pg.OPENGL | pygame.DOUBLEBUF)
        pg.display.set_caption("TH 69")
        self.clock = pg.time.Clock()

        self.ctx = moderngl.create_context()

        #self.enemy_cooldown = 1000.0
        #self.cooldown = 1000.0

        self.frametime = 0 # in ticks
        # enemies and behaviors
        self.allenemies = [Enemy, WhiteFlame, Testboss]
        self.allbehaviors = [MoveByPoints, MoveInDirection]

        self.sel_b = 0
        self.sel_e = 0

        self.selected_behavior = self.allbehaviors[self.sel_b]
        self.selected_enemy = self.allenemies[self.sel_e]

        # if you want to make different stages for different diffs
        self.difficulties = ("Easy","Normal","Hard","Lunatic","Extra")
        self.diff = self.difficulties[3]
        #self.min_rank = 5
        #self.rank = 5
        #self.max_rank = 34

        # self explanatory
        self.stagename = None

        self.stgsystem = StageSystem(self)

        # menu
        self.in_menu = True
        self.in_select_menu = False

        # area visible to the player(for preview, not scaled for easier enemy placement)
        self.fight_area = pg.Surface((400, 650))

        # also self explanatory
        self.enemy_list = []

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

        # mouse track for editing a stage
        self.mousepos = list(pg.mouse.get_pos())
        self.mouse_pos = [self.mousepos[0] - 50, self.mousepos[1] - 25]
        self.projregistry = PROJECTILE_REGISTRY(self) # a projectile registry  
        self.soundregistry = SOUND_REGISTRY(self)


        # menu init
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
    
    def create_a_stage(self, character):
        self.Character = character
        self.new_game()
     
    # creating a stage menu
    def select_character_menu(self):
        self.in_select_menu = True
        self.in_menu = False
        self.createastage = Selectable_Text(self, (70, 300), text="Create a stage", on_use=self.create_a_stage, args=self.stagename)
        self.gobacktomenu = Selectable_Text(self, (70, 330), text="Go Back", on_use=self.goback)
        self.menu_list = [self.createastage, self.gobacktomenu]
        self.menu_ui_selected = 0
        self.selected_button = self.menu_list[self.menu_ui_selected]
        self.selected_button.is_selected = True
    
    # menu init
    def Menu(self):
        self.start_the_game = Selectable_Text(self, (70, 300), text="Game Start", on_use=self.select_character_menu)
        self.settings = Selectable_Text(self, (50, 330), text="Settings")
        self.exitt = Selectable_Text(self, (70, 360), text="Exit", on_use=self.exit)
        self.menu_list = [self.start_the_game, self.settings, self.exitt]
        self.menu_ui_selected = 0
        self.selected_button = self.menu_list[self.menu_ui_selected]

    # ignore the func names cuz they are not changed
    def new_game(self):
        self.in_select_menu = False
        self.in_menu = False
        try:
            self.enemy_list = self.stgsystem.init_map()
        except TypeError:
            self.enemy_list = [] 
            

        #ui
        self.enemy_count_text = Text(self, (500, 80), text=f"Enemies in the stage: {len(self.enemy_list)}")
        self.sb_mm_text = Text(self, (500, 100), text=f"Selected Behavior: {self.selected_behavior}")
        self.se_mm_text = Text(self, (500, 120), text=f"Selected Enemy: {self.selected_enemy}")
        self.st_mm_text = Text(self, (500, 140), text=f"Time(in ticks): {self.frametime}")

    # update
    def update(self):
        # input checks
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                self.stgsystem.enemies = self.enemy_list
                self.stgsystem.save()
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
                    if ev.type == pg.KEYDOWN:
                        if ev.key == pg.K_LSHIFT:
                            self.frametime -= 60
                        if ev.key == pg.K_RSHIFT:
                            self.frametime += 60
                        if ev.key == pg.K_LALT:
                            self.frametime -= 1
                        if ev.key == pg.K_RALT:
                            self.frametime += 1
            if ev.type == pg.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    self.enemy_list.append(self.selected_enemy(self, self.mouse_pos, self.frametime))
            
        frametex = self.surt_to_tex(self.screen)
        frametex.use(0)
        self.program['tex'] = 0
        self.renderobject.render(mode=moderngl.TRIANGLE_STRIP)

        self.mousepos = pg.mouse.get_pos()
        self.mouse_pos = [self.mousepos[0] - 50, self.mousepos[1] - 25]

        self.screen.fill((0, 0, 0))
        if not self.in_menu and not self.in_select_menu:
            self.screen.fill((0, 80, 10))

            #self.screen.blit(pg.transform.scale(self.fight_area, (570, 730)), (50, 25))
            self.screen.blit(self.fight_area, (50, 25))
            self.fight_area.fill((0, 0, 0))

            for enemy in self.enemy_list:
                enemy.draw()
            
            self.enemy_count_text.text = f"Enemies in the stage: {len(self.enemy_list)}"
            self.sb_mm_text.text = f"Selected Behavior: {self.selected_behavior}"
            self.se_mm_text.text = f"Selected Enemy: {self.selected_enemy}"
            self.st_mm_text.text = f"Time(in ticks): {self.frametime}"
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
        pg.display.flip()

        frametex.release()

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
    game.stgsystem.mapfile =  f"{game.stagename}.stg"
    game.run()