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
        Note: this is a "game" object\n
        and you need to supply this object to classes\n
        like this: Sound(game=self(AdvancedGameClass), ...)'''
    def __init__(self, window_caption="Genso Engine v0.2.0 Game (CHANGE ME)", win_size=RES):
        pg.init()
        self.window = pg.display.set_mode((RES), pg.OPENGL | pygame.DOUBLEBUF | pg.SRCALPHA | pg.BLEND_ADD)
        self.WIN_SIZE = win_size
        self.proj_cap = 1000
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
        self.left_fight_area_border = 0
        self.right_fight_area_border = self.fight_area.get_width()
        self.top_fight_area_border = 0
        self.bottom_fight_area_border = self.fight_area.get_height()
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
            -1.0, 1.0, 0.0,   0.0, 0.0, 1.0,
            1.0, 1.0, 0.0,   1.0, 0.0, 1.0,
            -1.0, -1.0, 0.0,   0.0, 1.0, 1.0,
            1.0, -1.0, 0.0,   1.0, 1.0, 1.0,
        ]))

        self.renderobject = self.ctx.vertex_array(self.program.programs["2dsurf"], [(self.pentabuff, '3f 3f', 'vert', 'texcoord')])

        self.musicvolume = 0.20
        self.soundvolume = 0.20

        self.opengl_blit_color = [0.1, 0.2, 0.2]

        self.lazer_list = []

        self.stage = "1.stg"
        self.current_song = None
        self.item_pickup_border_y = 100

        self.stagesystem = StageSystem(game=self, mapfile=self.stage)
        self.projregistry = PROJECTILE_REGISTRY(self) 
        self.soundregistry = SOUND_REGISTRY(self)
        self.musicregistry = MUSIC_REGISTRY(self)
        self.menu = MenuSystem(self)
        self.dialogsys = DialogueSystem(self)

        self.proj_registry_fill()
        self.sound_registry_fill()
        self.music_registry_fill()
    
    def proj_registry_fill(self):
        self.projregistry.rglist = {"ball_gray": (self, [5, 55], [16, 16], projectile.MoveInDirection, [], 4),
                             "ball_red": (self, [37, 55], [16, 16], projectile.MoveInDirection, [], 4),
                             "ball_green": (self,(181, 55), [16, 16], projectile.MoveInDirection, [], 4),
                             "ball_blue": (self, (101, 55), [16, 16], projectile.MoveInDirection, [], 4),
                             "ball_pink": (self, (69, 55), [16, 16], projectile.MoveInDirection, [], 4),
                             "ball_yellow": (self,(214, 55), [16, 16], projectile.MoveInDirection, [], 4),
                             "ball_light_blue": (self,(117, 55), [16, 16], projectile.MoveInDirection, [], 4),
                             "ball_white": (self,(245, 55), [16, 16], projectile.MoveInDirection, [], 4),

                             "opaque_ball_gray": (self, [5, 38], [16, 16], projectile.MoveInDirection, [], 6),
                             "opaque_ball_red": (self, [37, 38], [16, 16], projectile.MoveInDirection, [], 6),
                             "opaque_ball_green": (self,(181, 38), [16, 16], projectile.MoveInDirection, [], 6),
                             "opaque_ball_blue": (self, (101, 38), [16, 16], projectile.MoveInDirection, [], 6),
                             "opaque_ball_pink": (self, (69, 38), [16, 16], projectile.MoveInDirection, [], 6),
                             "opaque_ball_yellow": (self,(214, 38), [16, 16], projectile.MoveInDirection, [], 6),
                             "opaque_ball_light_blue": (self,(117, 38), [16, 16], projectile.MoveInDirection, [], 6),

                             "big_ball_gray": (self,(8, 308), [28, 28], projectile.MoveInDirection, [], 8),
                             "big_ball_red": (self,(39, 308), [28, 28], projectile.MoveInDirection, [], 8),
                             "big_ball_blue": (self,(103, 308), [28, 28], projectile.MoveInDirection, [], 8),
                             "big_ball_yellow": (self,(199, 308), [28, 28], projectile.MoveInDirection, [], 8),
                             "big_ball_green": (self,(167, 308), [28, 28], projectile.MoveInDirection, [], 8),
                             "big_ball_pink": (self,(71, 308), [28, 28], projectile.MoveInDirection, [], 8),
                             "big_ball_light_blue": (self,(135, 308), [28, 28], projectile.MoveInDirection, [], 8),
                             "big_ball_white": (self,(231, 308), [28, 28], projectile.MoveInDirection, [], 8),}
    
    def sound_registry_fill(self):
        self.soundregistry.rglist = {"pause": sfx.Sound(self, "assets/sfx/sounds/se_pause.wav"),
                             "damage00": sfx.Sound(self, "assets/sfx/sounds/se_damage00.wav"),
                             "damage01": sfx.Sound(self, "assets/sfx/sounds/se_damage01.wav"),
                             "power01": sfx.Sound(self, "assets/sfx/sounds/se_power1.wav"),
                             "plst": sfx.Sound(self, "assets/sfx/sounds/se_plst00.wav"),
                             "powerup": sfx.Sound(self, "assets/sfx/sounds/se_powerup.wav"),
                             "select00": sfx.Sound(self, "assets/sfx/sounds/se_select00.wav"),
                             "nice": sfx.Sound(self, "assets/sfx/sounds/se_nice.wav"),
                             "ok": sfx.Sound(self, "assets/sfx/sounds/se_ok00.wav"),
                             "timeout": sfx.Sound(self, "assets/sfx/sounds/se_timeout.wav"),
                             "nep00": sfx.Sound(self, "assets/sfx/sounds/se_nep00.wav"),
                             "kira00": sfx.Sound(self, "assets/sfx/sounds/se_kira00.wav"),
                             "lazer01": sfx.Sound(self, "assets/sfx/sounds/se_lazer00.wav"),
                             "pl_death": sfx.Sound(self, "assets/sfx\sounds\se_pldead00.wav"),
                             "cancel": sfx.Sound(self, "assets/sfx\sounds\se_cancel00.wav"),
                             "extend": sfx.Sound(self, "assets/sfx\sounds\se_extend.wav"), }
    
    def music_registry_fill(self):
        self.musicregistry.rglist = {-1: sfx.Music(self, "assets/sfx/music/Heart-Stirring Urban Legends.mp3"),
                             0: sfx.Music(self, "assets/sfx/music/Electric Heritage.mp3"),
                             1: sfx.Music(self, "assets/sfx/music/The Lost Emotion.mp3")}

    
    def change_gl_blit_color(self, r: float, g: float, b:float):
        '''r: red color (0 to 1)
           g: green color (0 to 1)
           b: blue color (0 to 1)'''
        self.opengl_blit_color = [r, g, b]


    def set_caption(caption: str = "Genso Engine v0.2.0 Game (CHANGE ME)"):
        pg.display.set_caption(caption)

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def surt_to_tex(self, surf):
        tex = self.ctx.texture(surf.get_size(), 4, dtype="f1")
        tex.filter = (mgl.NEAREST, mgl.NEAREST)
        tex.swizzle = "BGRA"
        b = np.array(surf.get_view('1'))
        tex.write(b.tobytes())
        return tex
    
    def exit(self):
        self.program.destroy()
        self.renderobject.release()
        self.scene_manager.clean_up()
        pg.quit()
        sys.exit()

    def reload(self):
        self.camera.position = glm.vec3(0, 3, 0)
        self.camera.pitch = 0
        self.camera.yaw = -90
        self.trigger_list.clear()
        self.enemy_list.clear()
        self.pickup_list.clear()
        self.proj_list.clear()
        self.player_proj.clear()

    def new_game(self):
        self.in_menu = False
        
        self.reload()

    def event_handler(self, ev):
        if ev.type == pg.QUIT:
            self.exit()
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_F5:  
                pg.display.toggle_fullscreen()
            if ev.key == pg.K_BACKSPACE: 
                self.exit()



    
    def update_projectiles(self):
        for proj in self.proj_list:
                proj.update()
                if proj.kill and proj.can_die:
                    self.proj_list.remove(proj)
    
    def update_player_projectiles(self):
            for proj in self.player_proj:
                proj.update()
                if proj.kill and proj.can_die:
                        self.player_proj.remove(proj)
    
    def update_enemies(self):
        for enemy in self.enemy_list:
            if enemy.is_boss == True and self.frametime >= enemy.time:
                self.bossfight = True
            enemy.update()
            if enemy.can_die:
                if enemy.kill:
                    self.bossfight = False
                    self.enemy_list.remove(enemy)
    
    def update_pickups(self):
        for pickup in self.pickup_list:
                pickup.update()
                if pickup.pos[1] >= 800:
                    self.pickup_list.remove(pickup)
                if pickup.kill: 
                    self.pickup_list.remove(pickup)
                if self.player.pos[1] <= self.item_pickup_border_y:
                    pickup.pos = self.player.pos

    def update_particles(self):   
        for particle in self.particles:
            particle.update()
            if particle.kill:
                self.particles.remove(particle)

    def update_lazers(self):   
        for lazer in self.lazer_list:
            lazer.update()
            if lazer.kill:
                self.lazer_list.remove(lazer)



    # the update method that you can override
    def update(self):
        for ev in pg.event.get():
            self.event_handler(ev)
        
        if not self.is_paused:
            self.screen.blit(self.gamebg, (0, 0))

            self.screen.blit(self.fight_area, (32, 16))

            self.update_player_projectiles()
            self.update_enemies()
            self.update_pickups()
            self.update_particles()
            self.update_lazers()
            self.update_projectiles()
    
    # don't override
    def _update(self):
        self.ctx.clear(*self.opengl_blit_color)

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