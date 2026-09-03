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
        '''Works Like Intented'''
        # the commented code taken from my own c# projects(i dont use unity btw)
        # float testX = circle.X;
        # float testY = circle.Y;

        # if (circle.X < rect.X)
        # {
        #     testX = rect.X;
        # } else if (circle.X > rect.X + rect.Width)
        # {
        #     testX = rect.X + rect.Width;
        # }

        # if (circle.Y < rect.Y)
        # {
        #     testY = rect.Y;
        # }
        # else if (circle.Y > rect.Y + rect.Heigth)
        # {
        #     testY = rect.Y + rect.Heigth;
        # }

        # float distX = circle.X - testX;
        # float distY = circle.Y - testY;
        # float distance = (float)Math.Sqrt((distX * distX) + (distY*distY));
        # if (distance <= circle.Radius)
        # {
        #     return true;
        # } else
        # {
        #     return false;
        # }

        testX = self.x
        testY = self.y
        
        if self.x < rect.left:
            testX = rect.left
        elif self.x > rect.right:
            testX = rect.right

        if self.y < rect.top:
            testY = rect.top
        elif self.y > rect.bottom:
            testY = rect.bottom

        distX = self.x - testX
        distY = self.y - testY
        distance = math.sqrt((distX * distX) + (distY * distY))
        if distance <= self.radius:
            return True
        else:
            return False

    def collidecircle(self, circle):
        if dist(self.position, circle.position) < (self.radius + circle.radius) - 1:
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
    