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

class AdvancedGameClass:
    '''The skeleton of the game class\n
        Note: this is a game object\n
        and you need to supply this object to classes\n
        like this: Sound(game=self(BasicGameClass), ...)'''
    def __init__(self, window_caption="Genso Engine v0.1.0.1 Game (CHANGE ME)"):
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
        self.musicvolume = 0.20 # set between 0 and 1 
        self.soundvolume = 0.20 # set between 0 and 1 
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

if __name__ == "__main__":
    game = AdvancedGameClass()
    game.run()