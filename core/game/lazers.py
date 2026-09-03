from core import *


class Lazer:
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        self.game = game
        self.pos = start_pos
        self.angle = radians(angle)
        self.segments = segments
        self.speed = speed
        self.lazer_margin = [5, 7]
        self.lazer_size = [15, 13]
        self.launch()
        self.kill = False
        self.projs = [Projectile(self.game, [self.pos[0] + (self.dx * (self.lazer_size[0] * (self.segments - segment))), self.pos[1] + (self.dy * (self.lazer_size[1] * (self.segments - segment)))], speed=self.speed, angle=degrees(self.angle), size=self.lazer_size, htradius=4, marginxy=self.lazer_margin) for segment in range(self.segments)]
    
    def update(self):
        for proj in self.projs:
            proj.update()
            if proj.kill:
                self.projs.remove(proj)
        if len(self.projs) <= 0:
            self.kill
    
    def launch(self):
        self.dx, self.dy = cos(self.angle), sin(self.angle)

class Red_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [22, 7]


class Bright_Red_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [37, 7]


class Purple_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [53, 7]


class Bright_Purple_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [68, 7]


class Red_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [22, 7]


class Bright_Red_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [37, 7]


class Purple_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [53, 7]


class Bright_Purple_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [68, 7]


class Blue_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [85, 7]


class Bright_Blue_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [101, 7]


class LightBlue_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [117, 7]


class Bright_LightBlue_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [133, 7]


class Green_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [149, 7]


class Bright_Green_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [165, 7]


class Lime_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [181, 7]


class Yellow_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [197, 7]


class Bright_Yellow_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [213, 7]


class Gold_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [229, 7]


class White_Lazer(Lazer):
    def __init__(self, game, start_pos=[0, 0], angle=0, segments=5, speed=1):
        super().__init__(game, start_pos, angle, segments, speed)
        self.lazer_margin = [245, 7]
