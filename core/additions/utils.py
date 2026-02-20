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
    return math.degrees(math.atan2(target_pos[1] - object_pos[1], target_pos[0] - object_pos[0]))
