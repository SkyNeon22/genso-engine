import pygame as pg
import numpy as np
from math import radians
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
                self.menus[self.current_menu_item].selectable_elements[self.previous_menu_ui_select].is_selected = False
                self.menu_ui_selected += 1
    
    def change_menu_ui_selected_up(self):
        if len(self.menus[self.current_menu_item].selectable_elements) != 0:
            if self.menu_ui_selected != 0:
                self.previous_menu_ui_select = self.menu_ui_selected
                self.menus[self.current_menu_item].selectable_elements[self.previous_menu_ui_select].is_selected = False
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

        for elem in self.selectable_elements:
            elem.update()
            #self.selectable_elements[self.menumanager.previous_menu_ui_select].is_selected = False
            self.selectable_elements[self.menumanager.menu_ui_selected].is_selected = True

class ShotTypeSelectMenu(Menu):
    def __init__(self, game, menumanager):
        super().__init__(game, menumanager)
        self.ssc_angle = 0
        self.selected_shottype_circle = MenuLabel(self.game, (480, 320), "assets\\img\\sprites\\ui\\test.png", sprite_size=[300, 300])
        self.elements = [MenuText(self.game, [50, 50], size=40), MenuText(self.game, [50, 90], size=25), MenuText(self.game, [50, 120], size=25)]
        self.elements[0].text = JapaneseFontText(self.game, self.elements[0].pos, self.elements[0].size, text="博麗　霊夢")
        self.elements[1].text = JapaneseFontText(self.game, self.elements[1].pos, self.elements[1].size, text="広範囲をカバーショットタイプ")
        self.elements[2].text = JapaneseFontText(self.game, self.elements[2].pos, self.elements[2].size, text="速度: 中")
        self.selectable_elements = [
            MenuSelectableText(self.game, execute=self.game.new_game_reimu),            
            MenuSelectableText(self.game, execute=self.game.new_game_marisa),            
            MenuSelectableText(self.game, execute=self.game.new_game_alice),            
            MenuSelectableText(self.game, execute=self.menumanager.change_current_menu, args=["mainmenu"]),
        ]
    
    def rotate_clockwise(self):
        self.ssc_angle -= 3
    def rotate_counterclockwise(self):
        self.ssc_angle += 3
    
    def _update(self):
        self.selected_shottype_circle.draw_with_rot(self.ssc_angle)
        if self.menumanager.menu_ui_selected == 0 and self.ssc_angle != 0:
            self.elements[0].text_str = "博麗　霊夢"
            self.elements[1].text_str = "広範囲をカバーショットタイプ"
            self.elements[2].text_str = "速度: 中"
            if self.ssc_angle >= 0:
                self.rotate_clockwise()
            else:
                self.rotate_counterclockwise()
        if self.menumanager.menu_ui_selected == 1 and self.ssc_angle != 90:
            self.elements[0].text_str = "霧雨　魔理沙"
            self.elements[1].text_str = "前方中心のショットタイプ"
            self.elements[2].text_str = "速度: 速い"
            if self.ssc_angle >= 90:
                self.rotate_clockwise()
            else:
                self.rotate_counterclockwise()
        if self.menumanager.menu_ui_selected == 2 and self.ssc_angle != 180:
            self.elements[0].text_str = "上海アリス幻樂団"
            self.elements[1].text_str = "ハイブリッドショットタイプ"
            self.elements[2].text_str = "速度: 中"
            if self.ssc_angle >= 180:
                self.rotate_clockwise()
            else:
                self.rotate_counterclockwise()
        if self.menumanager.menu_ui_selected == 3 and self.ssc_angle != 270:
            self.elements[0].text_str = "ＥＸＩＴ"
            self.elements[1].text_str = ""
            self.elements[2].text_str = ""
            if self.ssc_angle >= 270:
                self.rotate_clockwise()
            else:
                self.rotate_counterclockwise()
            
    
    def update(self):
        self._update()
        return super().update()

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
            self.game.soundregistry.rglist["cancel"].play(self.game.soundvolume)
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
    def __init__(self, game, pos: list = [0, 0], img_path: str = "", sprite_size=[]):
        self.game = game
        self.pos = pos
        try:
            if img_path:
                self.img = pg.image.load(img_path)#.convert_alpha()
            else:
                self.img = pg.image.load("assets/img/guesswhatismissing.png")
        except FileNotFoundError:
            self.img = pg.image.load("assets/img/guesswhatismissing.png")
        if sprite_size == []:
            self.sprite_size = list(self.img.get_size())
        else:
            self.sprite_size = sprite_size
            
    def no(self): ... # reserved
    def no(self): ... # reserved
    def no(self): ... # reserved
    def no(self): ... # reserved
    def no(self): ... # reserved
    def no(self): ... # reserved
    def no(self): ... # reserved
    def no(self): ... # reserved
    def no(self): ... # reserved
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
        self.game.screen.blit(pg.transform.scale(self.img, self.sprite_size), self.pos)
    
    def draw_with_rot(self, angle):
       self.game.screen.blit(pg.transform.rotate(pg.transform.scale(self.img, self.sprite_size), angle), self.pos)

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
