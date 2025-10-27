from core.opengl.scene import *
from core.visuals.opengl.mesh import Mesh


# The SceneManager object
class SceneManager:
    def __init__(self, ctx, game):
        self.ctx = ctx
        self.game = game
        self.mesh = Mesh(self.game)
        self.scenes = {"test": Scene(self.game, self),
                       "test2": sc(self.game, self),}
        self.current_scene = self.scenes["test"]
        self.current_scene.load()
    
    # reserved
    def update(self): ...
    
    def change_scene(self, scene: str):
        self.current_scene = self.scenes.get(scene)
    
    def clean_up(self):
        self.mesh.destroy()

    def get_current_scene(self):
        return self.current_scene

    def add_scene(self, name: str, scene):
        self.scenes.update(name, scene)

    def render_current_scene(self):
        self.current_scene.render()

    def del_scene(self, name: str):
        self.scenes.popitem(name)

    def get_all_scenes(self):
        return self.scenes

    def find_scene(self, name: str):
        if self.scenes.get(name) != None:
            return True
        else: 
            print("did not found the scene with name id: " + str(name))
            return False

    def return_scene(self, name: str):
        if self.scenes.get(name) != None:
            return self.scenes.get(name)
        else: 
            print("can't return: " + str(name))
            return False