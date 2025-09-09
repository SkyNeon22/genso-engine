import pygame as pg
import moderngl as mgl
import encodings
import encodings.hex_codec
import numpy as np
import time

def mergebuffers(a, b, insert: int = 3):
    a = pg.BufferProxy()
    b = pg.BufferProxy()
    print(a.raw()) 

def get_view(surf):
    temp = []
    for x in range(0, surf.get_height(), 1):
            for y in range(0, surf.get_width(), 1):
                temp.append(surf.get_at((y, x)))
    flat = [byte_val for tpl in temp for byte_val in tpl]
    return bytes(flat)

if __name__ == '__main__':
    time.perf_counter()
    pg.init()
    scr = pg.display.set_mode((640, 480), flags=pg.SRCALPHA, depth=32)
    s = pg.Surface((100, 100))

    while True:
        scr.fill((255, 255, 255, 100))
        s.fill((20, 100, 20, 100))
        s.set_at((0, 0), (100, 100, 100))
        scr.blit(s, dest=(0, 0))
        pg.display.update()
        #print(scr.get_view('2').raw)
        with open("test.txt", "w") as file:
            file.write(str(get_view(scr)))
        #print(scr.get_view('2').raw)
        break
    #print()