import pygame as pg


# tileset class only used for bullets for now
class Tileset:
    def __init__(self, file):
        self.file = file
        self.image = pg.image.load(file)
        self.rect = self.image.get_rect()
    
    def draw_sprite_from_tile(self ,surf ,tilepos=[0, 0] ,pos=[0, 0] ,marginxy=[5, 7], size=[10, 10], angle=0, scale=[1.2, 1.2]):
        mx, my = marginxy
        tilepos = [tilepos[0] + mx, tilepos[1] + my]
        size = size
        tile = pg.Surface(size, pg.SRCALPHA)
        tile.fill((0, 0, 0, 0))
        tile.blit(self.image, (0, 0), (tilepos[0], tilepos[1], tilepos[0]*size[0], tilepos[1]*size[1]))
        surf.blit(pg.transform.rotate(tile, angle), pos)

    def load(self):

        self.tiles = []
        x0 = y0 = self.margin
        w, h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing
        
        for x in range(x0, w, dx):
            for y in range(y0, h, dy):
                tile = pg.Surface(self.size)
                tile.blit(self.image, (0, 0), (x, y, *self.size))
                self.tiles.append(tile)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'