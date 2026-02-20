import pygame as pg
import numpy as np
import sys
from core.visuals.ui import *


class MenuSystem: 
    def __init__(self, game):
        self.game = game
        self.menus = {}
        self.current_menu_item = "mainmenu" # a name of the menu in the dictionary
        self.menu_ui_selected = 0
        self.previous_menu_ui_select = self.menu_ui_selected
    
    def update(self):
        try:
            self.menus[self.current_menu_item].update()
        except:
            self.current_menu_item = None
    
    def change_menu_ui_selected_down(self):
        if len(self.menus[self.current_menu_item].selectable_elements) != 0:
            if self.menu_ui_selected != len(self.menus[self.current_menu_item].selectable_elements):
                self.previous_menu_ui_select = self.menu_ui_selected
                self.menu_ui_selected += 1
    
    def change_menu_ui_selected_up(self):
        if len(self.menus[self.current_menu_item].selectable_elements) != 0:
            if self.menu_ui_selected != 0:
                self.previous_menu_ui_select = self.menu_ui_selected
                self.menu_ui_selected -= 1


    def add_menu_itm(self, name: str, item: str=None):
        self.menus[name] = item

    def remove_menu_itm(self, name: str):
        del self.menus[name]

    def change_menu_itm(self, name: str, value: any): ...

    def change_current_menu(self, name: str):
        self.menu_ui_selected = 0
        self.current_menu_item = name

class Menu:
    def __init__(self, game, menumanager):
        self.game = game
        self.menumanager = menumanager
        self.elements = []
        self.selectable_elements = []

    def add_element(self, element, args: list = []):
        self.elements.append(element(self.game, *args))
    
    def add_element_kwargs(self, element, kwargs: dict):
        self.elements.append(element(self.game, **kwargs))
    
    def add_selectable_element(self, element, args: list = []):
        self.selectable_elements.append(element(self.game, *args))

    def add_selectable_element_test(self, element, args: list = []):
        self.selectable_elements.append(element(self.game, *args))

    def update(self):
        for elem in self.elements:
            elem.update()

        if len(self.selectable_elements) != 0:
            for elem in self.selectable_elements:
                elem.update()
                self.selectable_elements[self.menumanager.previous_menu_ui_select].is_selected = False
                self.selectable_elements[self.menumanager.menu_ui_selected].is_selected = True

class MenuBar:
    def __init__(self, game, pos:list = [0, 0], text = None, textcolor = None, barcolor = None, textsize = None, size = None):
        pass
    
class MenuText:
    def __init__(self, game, pos: list = [0, 0], text: str = "", color=(255, 255, 255), size=30):
        self.game = game
        self.pos = pos
        self.text_str = text
        self.color = color
        self.size = size
        self.text = Text(self.game, pos=self.pos, text=self.text_str, size=self.size, color=self.color)
    
    def change_size(self, size: int):
        self.text.size = size
    
    def change_color(self, color: tuple):
        self.text.color = color
    
    def change_text(self, text):
        self.text_str = text

    def update_text(self):
        self.text.text = self.text_str

    def draw(self):
        self.text.draw()
    
    def update(self):
        self.draw()
        self.update_text()
    
class MenuSelectableText: 
    def __init__(self, game, pos: list = [0, 0], text: str = "", execute=None, args=None, color=(160, 160, 160), select_color=(255,255,255), size=30):
        self.game = game
        self.pos = pos
        self.text_str = text
        self.color = color
        self.def_color = color
        self.select_color = select_color
        self.size = size
        self.execute = execute
        self.args = args
        self.text = Selectable_Text(self.game, 
                                    pos=self.pos, 
                                    text=self.text_str, 
                                    on_use=self.execute, 
                                    args=self.args, 
                                    size=self.size, 
                                    color=self.color, 
                                    select_color=self.select_color)
        self.is_selected = False
        self.is_selectable = True

    def change_select_color(self, color:tuple):
        self.select_color = color
        self.text.select_color = self.select_color

    def change_def_color(self, color:tuple):
        self.def_color = color 
        self.text.def_color = self.def_color
    
    def change_on_use(self, func):
        self.text.on_use = func

    def change_func_args(self, args: list):
        self.args = args
        self.text.args = self.args
    
    def change_size(self, size: int):
        self.text.size = size
    
    def change_color(self, color: tuple):
        self.text.color = color
    
    def change_text(self, text):
        self.text_str = text

    def update_text(self):
        self.text.text = self.text_str

    def swap_selectable(self):
        self.is_selectable = not self.is_selectable
        self.text.is_selectable = self.is_selectable
    
    def on_use(self):
        try:
            if self.args == None:
                self.text.on_use()
            else:
                self.text.on_use(*self.args)
        except Exception:
            self.game.soundregistry.rglist["cancel"].play()
        self.game.soundregistry.rglist["cancel"].reload()

    def update_status(self):
        self.text.is_selected = self.is_selected
    
    def draw(self):
        self.text.draw()
    
    def update_text_object(self):
        self.text.update()
        self.update_text()
        self.update_status()
    
    def update(self):
        #self.draw()
        self.update_text_object()
    

class MenuLabel: 
    def __init__(self, game, pos: list = [0, 0], img_path: pg.Surface = None):
        self.game = game
        self.pos = pos
        try:
            if img_path is not str or img_path is not None:
                self.img = pg.image.load(img_path).convert_alpha()
            else:
                self.img = pg.image.load("assets/img/guesswhatismissing.png")
        except FileNotFoundError:
            self.img = pg.image.load("assets/img/guesswhatismissing.png")
            
    def no(self): ... # reserved
    def no(self): ... # reserved
    def no(self): ... # reserved
    def no(self): ... # reserved
    def no(self): ... # reserved
    def no(self): ... # reserved
    def no(self): ... # reserved
    def no(self): ... # reserved
    def no(self): ... # reserved
    def update(self):
        self.game.screen.blit(self.img, self.pos)
    def change_img(self, img_path):
        try:
            if img_path is not str or img_path is not None:
                self.img = pg.image.load(img_path).convert_alpha() 
            else:
                self.img = pg.image.load("assets/img/guesswhatismissing.png")
        except FileNotFoundError:
            self.img = pg.image.load("assets/img/guesswhatismissing.png")
        

    def update(self):
        self.draw()
    
    def draw(self):
        self.game.screen.blit(self.img, self.pos)

class MenuRect:
    '''optional args: \n
        color: Tuple or List (default:(255, 255, 255))\n
        size: Tuple or List (default:(40, 60)) \n
        pos: Tuple or List (default:(0, 0))'''
    default_values = {"color": (255, 255, 255), "size": (40, 60), "pos": (0, 0)}
    def __init__(self, game, **kwargs):
        self.game = game
        self.color = (255, 255, 255)
        self.pos = (0, 0)
        self.size = (40, 60)
        for key, value in kwargs.items():
            setattr(self, key, value) 
        self.rect = pg.Rect(self.pos, self.size)

    def update(self):
        pg.draw.rect(self.game.screen, self.color, self.rect)
    

# unused for now
class MenuMouseButton: 
    def __init__(self, game, pos: list = [0, 0], onclick=None, args=[], size=(40, 80), color=(255, 255, 255), outline=(150, 150, 150), border_radius=5, text: str="", textcolor=(255,255,255)):
        self.game = game
        self.pos = pos
        self.cl_cool = 5
        self.cl: int
        self.size = size
        self.text = MenuText(self.game, pos=self.pos, text=text, size=int(self.size[0] + self.size[1] / 4), color=textcolor)
        self.rect = pg.rect.Rect(self.pos, self.size)
        self.onclick = onclick
        self.args = args
        self.color = color
        self.outline = outline
        self.border_radius = border_radius
    
    def update(self):
        if self.cl >= 0:
            self.cl -= 1

        if self.rect.collidepoint(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]):
            self.onclick(self.game, *self.args)

        self.text.update()
        
        self.draw()
    
    def draw(self):
        pg.draw.rect(self.game.screen, self.color, self.rect)
        pg.draw.rect(self.game.screen, self.outline, self.rect, border_radius=self.border_radius)
