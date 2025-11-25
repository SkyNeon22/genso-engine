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

    def render(self):
        for obj in self.objects:
            obj.render()
