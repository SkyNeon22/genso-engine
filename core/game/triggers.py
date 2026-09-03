import pygame as pg
import glm
import math


class Trigger:
    default_values = {
        'startframetime': 0, 'endframetime': 10}
    def __init__(self, **kwargs):
        self.startframetime = 0
        self.endframetime = 0
        self.type = "base"
        for key, value in kwargs.items():
            setattr(self, key, value) 
    def todict(self):
        return {"startframetime": self.startframetime,
                "endframetime": self.endframetime
        }
    @classmethod
    def fromdict(cls, asset):
        return cls(startframetime=asset['startframetime'], endframetime=asset['endframetime'])
    def update(self): ...
    def reserved(self): ...







class DialogueActivate(Trigger):
    def __init__(self, game, dialoguenum=0, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.dialoguenum = dialoguenum
        self.armed = True
        self.type = "dialogueactivate"
    def todict(self):
        return {"startframetime": self.startframetime,
                "endframetime": self.endframetime,
                "type": self.type,
                "dialoguenum": self.dialoguenum,
        }
    @classmethod
    def fromdict(cls, asset, game):
        return cls(game, startframetime=asset['startframetime'], endframetime=asset['endframetime'], dialoguenum=asset["dialoguenum"])
    def update(self):
        if self.game.frametime >= self.startframetime and self.armed:
            self.game.dialogsys.active = True
            self.game.dialogsys.active_collection = self.dialoguenum
            self.armed = False







class MoveCameraToDestPos(Trigger):
    '''Values:
        startframetime: int
        endframetime: int
        destinatedpos: glm.vec3()
        
        Errors:
            Valuerror: if startframe time > endframetime
        '''
    default_values = {
        'startframetime': 0, 'endframetime': 10, 'destinatedpos': glm.vec3(0, 0, 0)
    }
    def __init__(self, camera, **kwargs):
        self.destinatedpos = glm.vec3(0, 0, 0)
        super().__init__(**kwargs)
        self.camera = camera
        self.startposition = camera.position
        self.type = "movecameratodestpos"

    def todict(self):
        return {"destpos": self.destinatedpos.to_list(),
                "startframetime": self.startframetime,
                "endframetime": self.endframetime,
                "type": self.type,
        }

    @classmethod
    def fromdict(cls, asset, camera):
        return cls(camera,startframetime=asset['startframetime'], endframetime=asset['endframetime'], destinatedpos=glm.vec3(asset['destpos']))
    
    def update(self):
        if self.camera.app.frametime >= self.startframetime and self.camera.app.frametime <= self.endframetime:
            x_interpolation = ((self.camera.app.frametime - self.startframetime) / (self.endframetime - self.startframetime))
            y_interpolation = ((self.camera.app.frametime - self.startframetime) / (self.endframetime - self.startframetime))
            z_interpolation = ((self.camera.app.frametime - self.startframetime) / (self.endframetime - self.startframetime))
            self.camera.position.x = self.startposition.x + x_interpolation * (self.destinatedpos.x - self.startposition.x)
            self.camera.position.y = self.startposition.y + y_interpolation * (self.destinatedpos.y - self.startposition.y)
            self.camera.position.z = self.startposition.z + z_interpolation * (self.destinatedpos.z - self.startposition.z)
    





    
class RotateCamera(Trigger):
    '''Values:
        startframetime: int
        endframetime: int
        yaw: int
        pitch: int
        
        Errors:
            Valuerror: if startframe time > endframetime
        '''
    default_values = {
        'startframetime': 0, 'endframetime': 10, 'yaw': -90, 'pitch': 0
    }
    def __init__(self, camera, **kwargs):
        self.yaw = -90
        self.pitch = 0
        super().__init__(**kwargs)
        self.type = "rotatecamera"
        self.camera = camera
        self.startyaw = camera.yaw
        self.startpitch = camera.pitch

    def todict(self):
        return {"yaw": self.yaw ,
                "pitch": self.pitch,
                "startframetime": self.startframetime,
                "endframetime": self.endframetime,
                "type": self.type,
        }

    @classmethod
    def fromdict(cls, asset, camera):
        return cls(camera,startframetime=asset['startframetime'], endframetime=asset['endframetime'], pitch=asset['pitch'], yaw=asset['yaw'])
    
    def update(self):
        if self.camera.app.frametime >= self.startframetime and self.camera.app.frametime <= self.endframetime:
            pitch_interpolation = ((self.camera.app.frametime - self.startframetime) / (self.endframetime - self.startframetime))
            yaw_interpolation = ((self.camera.app.frametime - self.startframetime) / (self.endframetime - self.startframetime))
            self.camera.yaw = self.startyaw + yaw_interpolation * (self.yaw - self.startyaw)
            self.camera.pitch = self.startpitcch + pitch_interpolation * (self.pitch - self.startpitch)

