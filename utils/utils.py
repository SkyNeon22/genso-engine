import math


# distance 2d
def dist_2d(a, b):
    return math.dist(a, b)

# direction and speed compensation
def get_direction(a: list, b: list):
    return [(a[0] - b[0]) / 384, (a[1] - b[1]) / 448]

def is_negative(num: int):
    return True if num % -1 else False

# don't even try to understand this func
def speed_compensation(direction: list, speed: float): 
    return speed / (1 - (direction[0] % 1 + direction[1] % 1))
# don't care for now
def direction_to_angle(direction=[0, 0]):
    return direction[0] * 180 + direction[1] * 180