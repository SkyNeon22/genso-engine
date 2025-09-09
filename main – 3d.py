import pygame as pg 
import moderngl as mgl 
import sys
from model import *
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene


class GraphicsEngine:
    def __init__(self, win_size = (800, 600)):
        pg.init()
        self.WIN_SIZE = win_size
        self.screen = pg.display.set_mode(self.WIN_SIZE, pg.DOUBLEBUF|pg.OPENGL)
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_CORE, pg.GL_CONTEXT_PROFILE_MASK)

        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.CULL_FACE | mgl.DEPTH_TEST | mgl.BLEND)
        self.ctx.gc_mode = 'auto'

        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
 
        #self.light = Light(position=(0, 3, -10), color=(0, 0.8, 0))
        self.light = Light(position=(0, 10, 0), color=(0.8, 0.8, 0))

        self.camera = Camera(self, position=(0, 2, 6))
        
        self.mesh = Mesh(self)

        self.scene = Scene(self)

    def check_events(self):
        pg.display.set_caption(f'{self.clock.get_fps(): .0f}')

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.mesh.destroy()
                pg.quit()
                sys.exit()
    
    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001
    
    def render(self):
        self.ctx.clear(0.08, 0.16, 0.20)

        self.scene.render()

        pg.display.flip()

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)

if __name__ == '__main__':
    game = GraphicsEngine()
    game.run()
