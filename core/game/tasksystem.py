import pygame as pg
import random
import math
from core.game.projectile import *
from core.game.pickups import *
from core.additions import get_angle



class Task:
    def __init__(self, object, function=None, args=[], time=1, interval=0, wait=True):
        self.object = object
        self.wait = wait
        self.func = function
        self.args = args
        self.stop = False
        self.timer = 0
        self.time = time
        self.interval = interval

    def update(self):
        if not self.func == None:
            if self.timer < self.time:
                self.timer += 1
                self.object.waitforend = self.wait
                if len(self.args) == 0:
                    if self.timer % self.interval == 0:
                        self.func()
                else:
                    if self.timer % self.interval == 0:
                        self.func(*self.args)
            else:
                self.stop = True
                self.object.waitforend = False
        else:
            self.stop = True
            self.object.waitforend = False