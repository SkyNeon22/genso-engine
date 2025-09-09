import pygame as pg 

# A basic skeleton
class Behavior:
    def __init__(self, game, target):
        self.game = game
        self.target = target

    def tick(self):
        pass

    def update(self):
        self.tick()

class MoveAtAnAngle(Behavior):
    def __init__(self, game, target):
        super().__init__(game, target)

class MoveInDirection(Behavior):
    def __init__(self, game, target, args=[[0, 0]]):
        super().__init__(game, target)
        self.direction = [args[0], args[1]] 
        self.vel = [args[0], args[1]]
    
    def tick(self):
        self.target.pos[0] += self.vel[0]
        self.target.pos[1] += self.vel[1]

class MoveToPos(Behavior):
    def __init__(self, game, target, args=[[0, 0]]):
        super().__init__(game, target)
        self.pos = args[0]
    
    def tick(self):
        if self.target.pos[0] < self.pos[0]:
            self.target.pos[0] += self.target.speed
        elif self.target.pos[0] > self.pos[0]:
            self.target.pos[0] -= self.target.speed
        else:
            self.target.pos[0] += 0
        if self.target.pos[1] < self.pos[1]:
            self.target.pos[1] += self.target.speed
        elif self.target.pos[1] > self.pos[1]:
            self.target.pos[1] -= self.target.speed
        else:
            self.target.pos[1] -= self.target.speed 


class MoveByPoints(Behavior):
    def __init__(self, game, target, args=([(0, 0), (250, 250)])):
        super().__init__(game, target)
        self.waypoints = args[0]
        self.curwaypoint = 0

    
    def tick(self):
        if self.target.pos != self.waypoints[self.curwaypoint]:
            self.target.pos += self.waypoints[0] * self.target.speed
        else:
            self.curwaypoint += 1