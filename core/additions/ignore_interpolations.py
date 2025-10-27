import math
import numpy


# a linear interp
def linear(x1, y1, x2, y2):
    x = (x1 + x2) / 2
    y = y1+ (x-x1) * (y2-y1)/ (x2-x1)
    return y