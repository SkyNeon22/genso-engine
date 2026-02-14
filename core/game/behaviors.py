import pygame as pg 

# A basic skeleton
class Behavior:
    def __init__(self, game, target):
        self.game = game
        self.target = target
        self.stop = False

    def tick(self):
        pass

    def update(self):
        if not self.stop:
            self.tick()

class MoveInDirection(Behavior):
    def __init__(self, game, target, args=[[0, 0]]):
        super().__init__(game, target)
        self.direction = [args[0], args[1]] 
        self.vel = [args[0], args[1]]
    
    def tick(self):
        self.target.pos[0] += self.vel[0]
        self.target.pos[1] += self.vel[1]

class MoveByPoints(Behavior):
    def __init__(self, game, target, args=()):
        super().__init__(game, target)
        self.waypoints = args
        self.curwaypoint = 0

    def tick(self):
        try:
            if self.target.pos != self.waypoints[self.curwaypoint]:
                if self.target.pos[0] < self.waypoints[self.curwaypoint][0]:
                    self.target.pos[0] += self.target.speed
                elif self.target.pos[0] > self.waypoints[self.curwaypoint][0]:
                    self.target.pos[0] -= self.target.speed
                else:
                    self.target.pos[0] += 0
                if self.target.pos[1] < self.waypoints[self.curwaypoint][1]:
                    self.target.pos[1] += self.target.speed
                elif self.target.pos[1] > self.waypoints[self.curwaypoint][1]:
                    self.target.pos[1] -= self.target.speed
                else:
                    self.target.pos[0] += 0
            else:
                self.curwaypoint += 1
        except IndexError:
            self.stop = True
            
    