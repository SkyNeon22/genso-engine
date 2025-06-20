import pygame as pg

class Text:
    def __init__(self, game, pos=(0, 0), size=30, color=(255, 255, 255), text=""):
        pg.font.init()
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.color = color
        self.text = text
        self.font = pg.font.SysFont('Comic Sans MS', self.size)

    def draw(self):
        text_surface = self.font.render(self.text, False, self.color)
        self.game.screen.blit(text_surface, self.pos)

    def update(self):
        self.draw()

class Bar:
    def __init__(self, game, pos=(0, 0), size=10, color=(255, 255, 255), text=""):
        pg.font.init()
        self.font = pg.font.SysFont('Comic Sans MS', 30)
        self.game = game
        self.pos = list(pos)
        self.drawsurf = self.game.screen
        self.size = size
        self.color = color
        self.text = text
        self.bar_len = 0
        self.bar_color = (200, 200, 200)
        self.bar_size_mul = 3.5

    def draw(self):
        pg.draw.rect(self.drawsurf, self.bar_color, [self.pos[0], self.pos[1], self.bar_len, self.size * self.bar_size_mul])
        text_surface = self.font.render(self.text, False, self.color)
        self.drawsurf.blit(text_surface, self.pos)

    def update(self):
        self.draw()
    
class PopUpText(Text):
    def __init__(self, game, pos=(0, 0), size=10, color=(255, 255, 255), text="", speed=-2, maxlifetime=50):
        super().__init__(game, pos, size, color, text)
        self.lifetime = 0
        self.maxlifetime = maxlifetime
        self.speed = speed
        self.kill = False
    
    def draw(self):
        return super().draw()

    def update(self):
        self.pos[1] += self.speed
        self.speed += 0.2
        self.lifetime += 1
        if self.lifetime >= self.maxlifetime:
            self.kill = True
        return super().update()
    
def test():
    print("it works💀💀💀💀💀💀💀💀💀💀")
    
class Button:
    def __init__(self, game, text="Button", pos=(400, 200), size=(80, 60), color=(200, 200, 200), outline=(255, 255, 255)):
        self.game = game
        self.text = text
        self.size = size
        self.pos = list(pos)
        self.color = color
        self.outline = outline
        self.on_click = test
        self.textobj = Text(self.game, self.pos, 10, text=self.text)
        self.hitbox = pg.Rect(self.pos[0] * 1.1, self.pos[1] * 1.1, self.size[0], self.size[1])
        self.disable = False
    
    def __on__click__(self):
        self.on_click()
    
    def draw(self):
        pg.draw.rect(self.game.screen, self.outline, pg.Rect(self.pos[0], self.pos[1], self.size[0] * 1.2, self.size[1] * 1.2 ))
        pg.draw.rect(self.game.screen, self.color, self.hitbox)

    def update(self):
        if not self.disable:
            if self.hitbox.collidepoint(self.game.mouse_pos) and pg.MOUSEBUTTONDOWN:
                self.__on__click__()
            self.draw()

class Selectable_Text:
    def __init__(self, game, pos=(0, 0), size=10, color=(160, 160, 160), text="", on_use=None, is_selectable=True, args=None):
        pg.font.init()
        self.font = pg.font.SysFont('Comic Sans MS', 30)
        self.game = game
        self.is_selectable = is_selectable
        self.is_selected = False
        self.on_use = on_use
        self.args = args
        self.pos = list(pos)
        self.normal_pos = self.pos
        self.size = size
        self.color = color
        self.text = text

    def draw(self):
        text_surface = self.font.render(self.text, False, self.color)
        self.game.screen.blit(text_surface, self.pos)

    def update(self):
        self.draw()
        if self.is_selected:
            self.color = (255, 255, 255, 255)
        else:
            self.color = (160, 160, 160, 200)
