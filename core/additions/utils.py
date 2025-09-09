import math
import pygame as pg

# distance 2d
def dist_2d(a, b):
    return math.dist(a, b)

# direction and speed compensation
def get_direction(a: list, b: list):
    return [(a[0] - b[0]) / 384, (a[1] - b[1]) / 448]

def is_negative(num: int):
    return True if num % -1 else False

def get_angle(target_pos, object_pos):
    pos1 = pg.math.Vector2(target_pos)
    pos2 = pg.math.Vector2(object_pos)
    return math.atan2(pos1.y - pos2.y, pos1.x - pos2.x)

# don't even try to understand this func (it's useless)
def speed_compensation(direction: list, speed: float): 
    return speed / (1 - (direction[0] % 1 + direction[1] % 1))
# don't care for now
def direction_to_angle(direction=[0, 0]):
    return direction[0] * 180 + direction[1] * 180