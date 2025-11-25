import math

def dist(a, b):
    return math.dist(a, b)

class Collider:
    def __init__(self):
        pass

class CircleCollider:
    def __init__(self, radius=4 , pos=(0, 0)):
        self.radius = radius
        self.x = pos[0]
        self.y = pos[1]
        self.position = pos
    
    def colliderect(self, rect):
        '''DISCLAIMER:\n
        DO NOT USE IF NOT REQUIRED TO,\n
        BECAUSE IT ONLY CHECKS FOR THE RECT'S CENTER'''

        if dist(rect.center, self.position) <= self.radius:
            return True
        else:
            return False

    def collidecircle(self, circle):
        if dist(self.position, circle.position) <= self.radius and dist(self.position, circle.position) <= circle.radius:
            return True
        else:
            return False

    def collidepoint(self, point):
        if dist(self.position, point) <= self.radius:
            return True
        else:
            return False
    
    def update(self, pos=(0, 0)):
        setattr(self, "position", pos)
        setattr(self, "x", pos[0])
        setattr(self, "y", pos[1])
    