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



class MoveInDirection(Behavior):
    def __init__(self, game, target, direction=(0, 0)):
        super().__init__(game, target)
        self.direction = direction
    
    def tick(self):
        self.target.pos[0] += self.direction[0] * self.target.speed
        self.target.pos[1] += self.direction[1] * self.target.speed


class MoveToPos(Behavior):
    def __init__(self, game, target, pos=(0, 0)):
        super().__init__(game, target)
        self.pos = pos
    
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
    def __init__(self, game, target, waypoints=[(0, 0), (250, 250)]):
        super().__init__(game, target)
        self.waypoints = waypoints
        self.curwaypoint = 0

    
    def tick(self):
        if self.target.pos != self.waypoints[self.curwaypoint]:
            self.target.pos += self.waypoints[0] * self.target.speed
        else:
            self.curwaypoint += 1