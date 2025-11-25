import pygame as pg
import glm


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
    def __init__(self, game, **kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.dialoguenum = 0
        self.armed = True
        self.type = "dialogueactivate"
    
    def todict(self):
        return {"startframetime": self.startframetime,
                "endframetime": self.endframetime,
                "type": self.type,
                }

    @classmethod
    def fromdict(cls, asset, game):
        return cls(game, startframetime=asset['startframetime'], endframetime=asset['endframetime'])
    
    def update(self):
        if self.game.frametime >= self.startframetime and self.armed:
            self.game.dialogsys.active = True
            self.game.dialogsys.active_collection = self.dialoguenum
            self.armed = False

class MoveCameraByAxis(Trigger):
    '''Values:
        startframetime: int
        endframetime: int
        axis: str (x, y or z)
        destinatedpos: int (position on the axis)
        
        Errors:
            Valuerror: if axis != 'x' or 'y' or 'z', also if startframe time > endframetime
        '''
    default_values = {
        'startframetime': 0, 'endframetime': 10, 'axis': 'x', 'destinatedpos': 0
    }
    def __init__(self, camera, **kwargs):
        self.axis = 'x'
        self.destinatedpos = 0
        super().__init__(**kwargs)
        self.type = "movecamerabyaxis"
        self.camera = camera
        self.activetime = self.endframetime - self.startframetime
        try:
            self.dist = self.destinatedpos - getattr(self.camera, 'position').__getattribute__(self.axis)
        except:
            self.dist = self.destinatedpos
        self.speed = self.dist / self.activetime

    def update(self):
        if self.camera.app.frametime >= self.startframetime and self.camera.app.frametime <= self.endframetime:
            self.camera.position += self.speed
    
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
        self.type = "movecameratodestpos"
        self.activetime = self.endframetime - self.startframetime
        try:
            self.dist = self.destinatedpos - getattr(self.camera, 'position')
        except:
            self.dist = self.destinatedpos
        self.speed = glm.vec3() 
        try:
            self.speed.x = self.dist.x / self.activetime
            self.speed.y = self.dist.y / self.activetime
            self.speed.z = self.dist.z / self.activetime
        except ZeroDivisionError:
            self.speed.x = 0
            self.speed.y = 0
            self.speed.z = 0
    
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
            self.camera.position += self.speed
    
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
        self.activetime = self.endframetime - self.startframetime
        self.distpitch = 0
        self.distyaw = 0

        try:
            self.distyaw = self.yaw - getattr(self.camera, 'yaw')
        except:
            self.distyaw = self.yaw
        try:
            self.distpitch = self.pitch - getattr(self.camera, 'pitch')
        except:
            self.distpitch = self.pitch

        self.speedyaw = 0
        self.speedpitch = 0

        try:
            self.speedyaw = self.distyaw / self.activetime
        except ZeroDivisionError:
            self.speedyaw = 0

        try:
            self.speedpitch = self.distpitch / self.activetime
        except ZeroDivisionError:
            self.speedpitch = 0
    
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
            self.camera.yaw += self.speedyaw
            self.camera.pitch += self.speedpitch
