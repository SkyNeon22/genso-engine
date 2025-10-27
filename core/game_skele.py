# SUM STUFF
import sys
import moderngl as mgl
import numpy as np
import array

# Core
from core import *
from core.game.stage import *
from core.additions import *
from configs.config import *
from core.game.registries import *
from core.opengl.scenemanager import *

# 3D
from core.visuals.opengl.model import *
from core.visuals.opengl.light import Light
from core.visuals.opengl.mesh import Mesh

# Mics
import random


# Time to comment
class BasicGameClass:
    '''For now it's not a skeleton\n
        but an example game.\n
        Note: this is a game object\n
        and you need to supply this object to classes\n
        like this: Sound(game=self(BasicGameClass), ...)'''
    def __init__(self, window_caption="Genso Engine v0.1.0 Prototype Game"):
        # init pygame
        pg.init()
        # The basic initialization of a pygame window
        self.window = pg.display.set_mode((RES), pg.OPENGL | pygame.DOUBLEBUF | pg.SRCALPHA | pg.BLEND_ADD)
        self.WIN_SIZE = RES # required for camera
        self.screen = pg.surface.Surface((RES), pg.SRCALPHA, depth=32)
        pg.display.set_caption(window_caption) 
        # moderngl context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.BLEND | mgl.DEPTH_TEST)
        self.ctx.blend_func = self.ctx.DEFAULT_BLENDING
        self.ctx.gc_mode = 'auto'   
        # shader program collection
        self.program = ShaderProgram(self.ctx)
        # pygame clock
        self.clock = pg.time.Clock()
        # game background for ui
        self.gamebg = pg.image.load("assets/img/gamebg.png")
        # mouse not visible and movable
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        # delete and opengl explodes
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_CORE, pg.GL_CONTEXT_PROFILE_MASK)
        # stage stuff
        self.frametime = 0
        self.bossfight = False
        self.difficulties = ("Easy","Normal","Hard","Lunatic","Extra")     
        self.diff = self.difficulties[2]
        self.selected_button = 0
        # rank (unused)
        self.min_rank = 5 # unused
        self.rank = 5 # unused
        self.max_rank = 34 # unused

        # Shottype selection
        self.Character = None
        # unused (damn I should delete some of unused stuff sometime)
        self.active_spell = None

        # no more exploding menus (menu flag)
        self.in_menu = True
        # pause check
        self.is_paused = False
        # just try to guess (camera movement)
        self.delta_time = None
        # score
        self.score = 0
        # Touhou STG without a game area is not Touhou STG
        self.fight_area = pg.Surface((384, 448),pg.SRCALPHA)
        # sum lists
        self.proj_list = []
        self.player_proj = []
        self.enemy_list = []
        self.pickup_list = []
        self.particles = []
        self.trigger_list = []
        # 3D Stuff
        self.light = Light(position=(0, 10, 0), color=(1, 1, 1))
        # camera
        self.camera = Camera(self, position=(0, 2, 6))

        self.scene_manager = SceneManager(self.ctx, self)
        # 2d pygame surface to 3d object&texture
        self.pentabuff = self.ctx.buffer(data=array.array('f', [
            # pos (x, y, z), uv coords (x, y)
            -1.0, 1.0, 0.0,   0.0, 0.0, 1.0,   #topleft
            1.0, 1.0, 0.0,   1.0, 0.0, 1.0,    #topright
            -1.0, -1.0, 0.0,   0.0, 1.0, 1.0,  #botleft
            1.0, -1.0, 0.0,   1.0, 1.0, 1.0,   #botright
        ]))

        self.renderobject = self.ctx.vertex_array(self.program.programs["2dsurf"], [(self.pentabuff, '3f 3f', 'vert', 'texcoord')])

        # some more game system init
        self.stage = "1.stg"
        self.current_song = -1
        self.stagesystem = StageSystem(game=self, mapfile=self.stage)
        self.projregistry = PROJECTILE_REGISTRY(self) # a projectile registry  
        self.soundregistry = SOUND_REGISTRY(self)
        self.musicregistry = MUSIC_REGISTRY(self)
        self.menu = MenuSystem(self)
        self.dialogsys = DialogueSystem(self)
        self.menu.menus["mainmenu"] = Menu(self, self.menu)
        self.menu.menus["characterselect"] = Menu(self, self.menu)
        # init game
        self.mainmenuinit()
        self.characterselectinit()
    
    def mainmenuinit(self):
        self.menu.menu_ui_selected = self.selected_button
        self.menu.menus["mainmenu"].add_selectable_element(MenuSelectableText, [(70, 200), "Game Start", self.menu.change_current_menu, ["characterselect"]])
        self.menu.menus["mainmenu"].add_selectable_element(MenuSelectableText, [(50, 230), "Extra Start", self.menu.change_current_menu, ["characterselect"]])
        self.menu.menus["mainmenu"].add_selectable_element(MenuSelectableText, [(30, 260), "Practice Start", self.menu.change_current_menu, ["characterselect"]])
        self.menu.menus["mainmenu"].add_selectable_element(MenuSelectableText, [(50, 290), "Settings"])
        self.menu.menus["mainmenu"].add_selectable_element(MenuSelectableText, [(70, 320), "Exit", self.exit])
    
    def characterselectinit(self):
        self.menu.menus["characterselect"].add_selectable_element(MenuSelectableText, [(70, 200), "Reimu: Fantasy Seal", self.select_character, [ReimuA]])
        self.menu.menus["characterselect"].add_selectable_element(MenuSelectableText, [(70, 230), "Reimu: Persuasion Needle", self.select_character, [ReimuB]])
        self.menu.menus["characterselect"].add_selectable_element(MenuSelectableText, [(70, 260), "Marisa: Starlight Reverie", self.select_character, [MarisaA]])
        self.menu.menus["characterselect"].add_selectable_element(MenuSelectableText, [(70, 290), "Marisa: Illusion lazer", self.select_character, [MarisaB]])
        self.menu.menus["characterselect"].add_selectable_element(MenuSelectableText, [(70, 320), "Sanae: Miracle winds", self.select_character, [SanaeA]])
        self.menu.menus["characterselect"].add_selectable_element(MenuSelectableText, [(70, 350), "Go Back", self.goback])
    
    #def charactermenuinit(self):
    #    self.reimuA = Selectable_Text(self, (70, 200), text="Reimu: Fantasy Seal", on_use=self.select_character, args=ReimuA)
    #    self.reimuB = Selectable_Text(self, (70, 230), text="Reimu: Persuasion Needle", on_use=self.select_character, args=ReimuB)
    #    self.marisaA = Selectable_Text(self, (70, 260), text="Marisa: Starlight Reverie", on_use=self.select_character, args=MarisaA)
    #    self.marisaB = Selectable_Text(self, (70, 290), text="Marisa: Illusion lazer", on_use=self.select_character, args=MarisaB)
    #    self.sanaeA = Selectable_Text(self, (70, 320), text="Sanae: Miracle winds", on_use=self.select_character, args=SanaeA)
    #    self.gobacktomenu = Selectable_Text(self, (70, 350), text="Go Back", on_use=self.goback)
    
    def get_time(self):
        # deltatime
        self.time = pg.time.get_ticks() * 0.001
    # the 2d surface to texture function
    def surt_to_tex(self, surf):
        tex = self.ctx.texture(surf.get_size(), 4, dtype="f1")
        tex.filter = (mgl.NEAREST, mgl.NEAREST)
        tex.swizzle = "BGRA"
        b = np.array(surf.get_view('1'))
        tex.write(b.tobytes())
        return tex
    
    # garbage collection and exiting
    def exit(self):
        self.program.destroy()
        self.renderobject.release()
        self.scene_manager.clean_up()
        pg.quit()
        sys.exit()
    #-------menu stuff------
    def goback(self):
        self.in_menu = True
        self.in_select_menu = False
    
    def select_character(self, character):
        self.Character = character
        self.new_game()

    def new_game(self):
        self.musicregistry.rglist[self.current_song].stop()
        self.current_song = 0
        self.musicregistry.rglist[0].play(0.20)
        self.frametime = 0
        self.player = self.Character(self, pos=(194, 350),start_power=4.0)
        self.enemy_list = self.stagesystem.init_enemies(self.stage)
        
        self.camera.position = glm.vec3(0, 0, 0)
        self.camera.yaw = -90
        self.camera.pitch = 0

        self.trigger_list = self.stagesystem.init_triggers(self.stage)
        self.scene_manager.change_scene("test2")

        #ui
        self.lives_text = Text(self, (420, 80), text=f"Lives {self.player.lives}", size=25)
        self.pieces_text = Text(self, (420, 110), text=f"Pieces {self.player.life_pieces}", size=18)
        self.bombs_text = Text(self, (420, 130), text=f"Bombs {self.player.bombs}", size=25)
        self.pause_text = Text(self, (0, 0), color=(255, 255, 255), text="Paused. Press Esc to continue")
        self.power_text = Text(self, (420, 180), text=f"{round(self.player.power, 3)}", size=25)
        self.score_text = Text(self, (420, 30), text=f"Score {self.score}", size=25)
        self.graze_text = Text(self, (420, 230), text=f"Graze {self.player.grazes}", size=25)
        self.spell_text = Text(self, (100, 60), text=f"", size=15)
        self.timeout_text = Text(self, (200, 60), text=f"", size=15)
        #self.spell_text = Text(self, (200, 30))
        #self.spell_text.drawsurf = self.fight_area
        #self.boss_hp = Bar(self, (3, 5),size=5, text=f"{self.enemy_list[0].hp}" if len(self.enemy_list) else "")
        self.boss_hp = Bar(self, (3, 5),size=5, text=f"Rumia" if len(self.enemy_list) else "")
        self.boss_hp.drawsurf = self.fight_area 
        
        self.in_menu = False
        self.in_select_menu = False
    #--------no more menu stuff-------
    # teh update so game is working and responding
    def update(self):
        # Commenting Laziness ~ No More Commenting, Just Read and Try To Understand
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
                if ev.key == pg.K_BACKSPACE: 
                    self.exit()
                if self.in_menu or self.in_select_menu:
                    if ev.key == pg.K_z:
                        self.menu.menus[self.menu.current_menu_item].selectable_elements[self.menu.menu_ui_selected].on_use()
                    if ev.key == pg.K_UP:
                        self.menu.change_menu_ui_selected_up()
                    if ev.key == pg.K_DOWN:
                        self.menu.change_menu_ui_selected_down()
                if not self.in_menu and not self.in_select_menu:
                    if ev.key == pg.K_LCTRL:
                        if self.dialogsys.active:
                            self.dialogsys.skip()
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
                        self.new_game()
                        self.is_paused = False

        self.ctx.clear(0.1, 0.2, 0.2)
        self.menu.menus[self.menu.current_menu_item].selected_button = self.selected_button

        self.scene_manager.render_current_scene()

        frametex = self.surt_to_tex(self.screen)
        frametex.use(0)
        self.program.programs["2dsurf"]['tex'] = 0
        self.renderobject.render(mode=mgl.TRIANGLE_STRIP)
        
        self.screen.fill((0, 0, 0, 0))

        if not self.in_menu:
                self.screen.fill((0, 0, 0, 0))

                self.screen.blit(self.gamebg, (0, 0))

                self.screen.blit(self.fight_area, (32, 16))
                self.fight_area.fill((0, 0, 0, 0))

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
                    self.timeout_text.update()
                    self.boss_hp.update()

                self.player.draw()

                if not self.is_paused:
                    for proj in self.player_proj:
                        proj.update()
                        if proj.kill:
                            if proj.can_die:
                                self.player_proj.remove(proj)
                    self.dialogsys.update()
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
                    
                    for trigger in self.trigger_list:
                        trigger.update()

                    try:
                        for enemy in self.enemy_list:
                            if enemy.is_boss == True and self.frametime >= enemy.time:
                                self.timeout_text.text = f"{enemy.attorder[enemy.active_attack].timeout // 60}"
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
                        self.fight_area.blit(pg.transform.scale(self.player.hitbox_img, self.player.hitboxsize), (self.player.hitbox.x, self.player.hitbox.y))
                    self.frametime += 1
                    
        else:
            self.menu.menus[self.menu.current_menu_item].update()
        # I'm back to commenting
        # flipping the buffers (look Line 30 at the flags=... and you will see the pg.DOUBLEBUF flag)
        pg.display.flip()
        # garbage collecting the generated texture
        frametex.release()
        # capping the fps to 60 and setting dt
        self.delta_time = self.clock.tick(60)
    
    # while loop
    def run(self):
        while True:
            self.get_time()
            self.update()
            self.camera.update()








class AdvancedGameClass:
    '''The skeleton of the game class\n
        Note: this is a game object\n
        and you need to supply this object to classes\n
        like this: Sound(game=self(BasicGameClass), ...)'''
    def __init__(self, window_caption="Genso Engine v0.1.0 Prototype Game (Advanced Template)"):
        # init pygame
        pg.init()
        # The basic initialization of a pygame window
        self.window = pg.display.set_mode((RES), pg.OPENGL | pygame.DOUBLEBUF | pg.SRCALPHA | pg.BLEND_ADD)
        self.WIN_SIZE = RES # required for camera
        self.screen = pg.surface.Surface((RES), pg.SRCALPHA, depth=32)
        pg.display.set_caption(window_caption) 
        # moderngl context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.BLEND | mgl.DEPTH_TEST)
        self.ctx.blend_func = self.ctx.DEFAULT_BLENDING
        self.ctx.gc_mode = 'auto'   
        # shader program collection
        self.program = ShaderProgram(self.ctx)
        # pygame clock
        self.clock = pg.time.Clock()
        # game background for ui
        self.gamebg = pg.image.load("assets/img/gamebg.png")
        # delete and opengl explodes
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_CORE, pg.GL_CONTEXT_PROFILE_MASK)
        # stage stuff
        self.frametime = 0
        self.bossfight = False
        self.difficulties = ("Easy","Normal","Hard","Lunatic","Extra")     
        self.diff = self.difficulties[2]
        self.selected_button = 0
        # rank (unused)
        self.min_rank = 5 # unused
        self.rank = 5 # unused
        self.max_rank = 34 # unused

        # Shottype selection
        self.Character = None
        # unused (damn I should delete some of unused stuff sometime)
        self.active_spell = None

        # no more exploding menus (menu flag)
        self.in_menu = False
        # pause check
        self.is_paused = False
        # just try to guess (camera movement)
        self.delta_time = None
        # score
        self.score = 0
        # Touhou STG without a game area is not Touhou STG
        self.fight_area = pg.Surface((384, 448),pg.SRCALPHA)
        # sum lists
        self.proj_list = []
        self.player_proj = []
        self.enemy_list = []
        self.pickup_list = []
        self.particles = []
        self.trigger_list = []
        # 3D Stuff
        self.light = Light(position=(0, 10, 0), color=(1, 1, 1))
        # camera
        self.camera = Camera(self, position=(0, 2, 6))

        self.scene_manager = SceneManager(self.ctx, self)
        # 2d pygame surface to 3d object&texture
        self.pentabuff = self.ctx.buffer(data=array.array('f', [
            # pos (x, y, z), uv coords (x, y)
            -1.0, 1.0, 0.0,   0.0, 0.0, 1.0,   #topleft
            1.0, 1.0, 0.0,   1.0, 0.0, 1.0,    #topright
            -1.0, -1.0, 0.0,   0.0, 1.0, 1.0,  #botleft
            1.0, -1.0, 0.0,   1.0, 1.0, 1.0,   #botright
        ]))

        self.renderobject = self.ctx.vertex_array(self.program.programs["2dsurf"], [(self.pentabuff, '3f 3f', 'vert', 'texcoord')])

        # some more game system init
        self.stage = "1.stg"
        self.current_song = None
        self.stagesystem = StageSystem(game=self, mapfile=self.stage)
        self.projregistry = PROJECTILE_REGISTRY(self) # a projectile registry  
        self.soundregistry = SOUND_REGISTRY(self)
        self.musicregistry = MUSIC_REGISTRY(self)
        self.menu = MenuSystem(self)
        self.dialogsys = DialogueSystem(self)
        # init game

    def get_time(self):
        # deltatime
        self.time = pg.time.get_ticks() * 0.001
    # the 2d surface to texture function
    def surt_to_tex(self, surf):
        tex = self.ctx.texture(surf.get_size(), 4, dtype="f1")
        tex.filter = (mgl.NEAREST, mgl.NEAREST)
        tex.swizzle = "BGRA"
        b = np.array(surf.get_view('1'))
        tex.write(b.tobytes())
        return tex
    
    # garbage collection and exiting
    def exit(self):
        self.program.destroy()
        self.renderobject.release()
        self.scene_manager.clean_up()
        pg.quit()
        sys.exit()
    #-------menu stuff------

    def new_game(self):
        self.in_select_menu = False
        self.in_menu = False

    def event_handler(self, ev):
        if ev.type == pg.QUIT:
            self.exit()
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_F5:  
                pg.display.toggle_fullscreen()
            if ev.key == pg.K_BACKSPACE: 
                self.exit()

    def update_entities(self):
            for proj in self.player_proj:
                proj.update()
                if proj.kill:
                    if proj.can_die:
                        self.player_proj.remove(proj)
                
            for proj in self.proj_list:
                proj.update()
                if proj.kill:
                    if proj.can_die:
                        self.proj_list.remove(proj)

            for pickup in self.pickup_list:
                pickup.update()
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
    # the update method that you can override
    def update(self):
        for ev in pg.event.get():
            self.event_handler(ev)
        
        if not self.is_paused:
            self.screen.blit(self.gamebg, (0, 0))

            self.screen.blit(self.fight_area, (32, 16))

            self.update_entities()
    
    def _update(self):
        self.ctx.clear(0.1, 0.2, 0.2)

        self.scene_manager.render_current_scene()

        frametex = self.surt_to_tex(self.screen)
        frametex.use(0)
        self.program.programs["2dsurf"]['tex'] = 0
        self.renderobject.render(mode=mgl.TRIANGLE_STRIP)
        
        self.screen.fill((0, 0, 0, 0))
    
        self.update()

        pg.display.flip()

        frametex.release()

        self.delta_time = self.clock.tick(60)
    
    def run(self):
        while True:
            self.get_time()
            self._update()
            self.camera.update()

# only runs when running this file
if __name__ == "__main__":
    game = BasicGameClass()
    game.run()