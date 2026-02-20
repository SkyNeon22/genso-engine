import pygame as pg
import math
import random

def circlepattern(game, speed=1, pos=(0, 0), proj_type="big_ball_white", bullet_count=10):
    for i in range(bullet_count):
        game.projregistry.shoot(proj_type, pos, 360 - (360 / i), speed)
