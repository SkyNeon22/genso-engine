from core.visuals.opengl.model import *
from core.visuals.opengl.light import Light


class Scene:
    def __init__(self, app, scenemanager=None):
        self.app = app
        self.scenemanager = scenemanager
        self.objects = []
        self.lights = []
        self.add = self.add_object
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def add_light(self, obj):
        self.lights.append(obj)

    def load(self):
        app = self.app

        self.add(Tower(self.app, scenemanager=self.scenemanager, rot=(0, 0, 0), scale=(0.5, 0.5, 0.5)))
        #self.add(Cat(self.app, scenemanager=self.scenemanager))

    def render(self):
        for obj in self.objects:
            obj.render()

class sc(Scene):
    def __init__(self, app, scenemanager=None):
        super().__init__(app, scenemanager)
    
    def load(self):
        app = self.app

        self.add(Tower(self.app, scenemanager=self.scenemanager, rot=(0, 0, 0), scale=(0.5, 0.5, 0.5)))
