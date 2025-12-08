# Core
import pygame as pg
import sys
import moderngl
import array 
import pyperclip

# From
from core import *
from configs.config import *

# Mics
import random
from core.game_skele import *

def test_stg_file(stg_name="1.stg"):
    try:
        with open(f"assets\stages\{stg_name}") as file:
            return True
    except FileNotFoundError:
        return False

def create_stg_file(stg_name=None):
    with open(f"assets\stages\{stg_name}", "w") as file:
        file.write("""{"enemies":{}, "triggers":{}}""")

# The New(TM) Editor for Genso Engine v0.1.0
# No comments of explaining are not provided (maybe someday will be)
class EDITOR(AdvancedGameClass):
    def __init__(self, window_caption="Genso Engine v0.1.0 Prototype Game (Advanced Template)", stg_path="assets/stages/1.stg", win_size=(1440, 900)):
        super().__init__(window_caption, win_size=win_size)
        self.helptext = Text(self, pos=(0, 460), size=16, text="Help:F1,Inspector:F2,Editor:F3,Save/Load:F9/F10,Disable Mousepos/Camera:F11/F12")

        self.frametime_text = Text(self, size=20)

        self.disable_mouseposshow = False

        self.camera_editor = False

        self.dialoguenum = 0

        self.mousepostext = Text(self, pos=(0, 0), size=20, text=str(pg.mouse.get_pos()))

        self.args = []
        self.trigger_args = {}

        self.stage = stg_path
        self.stagesystem.mapfile = self.stage

        self.scene_manager.add_scene("test", Scene(self, self.scene_manager))
        self.scene_manager.current_scene = "test"
        self.scene_manager.scenes[f"{self.scene_manager.current_scene}"].add_object(Tower(self, scenemanager=self.scene_manager, rot=(0, 0, 0)))


        self.inspectorinit()
        self.editorinit()
        self.helpinit()
        self.enemymenuinit()
        self.triggermenuinit()
        self.triggereditmenuinit()
        self.init_enemy_registry()
        self.init_behavior_registry()

        self.enemies = ["enemy", "testboss"]
        self.behaviors = ["none", "movebypoints"]
        self.triggers = ["dialoguestart"]
        self.selected_enemy = 0
        self.selected_behavior = 0

    def all_clear(self):
        self.enemy_list = []
        self.frametime = 0
    
    def init_enemy_registry(self):
        self.enemyregistry = REGISTRY(self)

        self.enemyregistry.register("enemy", Enemy)
        self.enemyregistry.register("testboss", Testboss)
    
    def init_behavior_registry(self):
        self.behavioregistry = REGISTRY(self)

        self.behavioregistry.register('none', None)
        self.behavioregistry.register('movebypoints', MoveByPoints)

    def load(self):
        self.all_clear()
        self.stagesystem.load(self.stage)
    
    def enemy_editor_open(self):
        self.menu.change_current_menu("enemy_editor")
        self.helptext.text = "Help:F1,Inspector:F2,Editor:F3,Right Click: Set Marker"
    
    def trigger_editor_open(self):
        self.menu.change_current_menu("trigger_editor")
        self.helptext.text = "Help:F1,Inspector:F2,Editor:F3,Disable Mousepos/Camera Editor:F11/F12"
    
    def open_camera_editor(self):
        self.helptext.text = "Set3DPositionArg/CameraRotationArg:End/Insert,SetSetTriggerStart/TriggerEnd:K/L,SetMoveTrigger/RotateTrigger:M/N"
        self.args = []
        self.camera.disabled_movement = False
        self.camera_editor = True
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
    
    def close_camera_editor(self):
        self.args = []
        self.camera.disabled_movement = True
        self.camera_editor = False
        pg.mouse.set_visible(True)
        pg.event.set_grab(False)

    def clear_args(self):
        self.soundregistry.rglist["cancel"].play()
        self.args = []
        self.soundregistry.rglist["cancel"].reload()
    
    def open_trigger_add_editor(self):
        self.menu.change_current_menu("trigger_editor_menu")
    
    def helpinit(self):
        self.menu.menus['help'] = Menu(self, self.menu)

        self.menu.menus['help'].elements.append(MenuRect(self, color=(50, 50, 50, 255), pos=(420, 5), size=(216, 440)))
        self.menu.menus['help'].elements.append(MenuRect(self, color=(40, 40, 40, 255), pos=(420, 5), size=(216, 30)))
        self.menu.menus['help'].elements.append(MenuText(self, pos=(420, 5), size=20, text="Help Menu"))

    def inspectorinit(self):
        # init
        self.menu.menus["inspector"] = Menu(self, self.menu)
        self.menu.current_menu_item = "inspector"


        # append
        self.menu.menus['inspector'].elements.append(MenuRect(self, color=(50, 50, 50, 255), pos=(420, 5), size=(216, 440)))
        self.menu.menus['inspector'].elements.append(MenuRect(self, color=(40, 40, 40, 255), pos=(420, 5), size=(216, 30)))
        self.menu.menus['inspector'].elements.append(MenuText(self, pos=(420, 5), size=20, text="Inspector"))
        self.menu.menus['inspector'].elements.append(MenuText(self, pos=(420, 420), size=20, text=f"Total Enemies: 0"))
    
    def editorinit(self):
        # init
        self.menu.menus["editor"] = Menu(self, self.menu)


        # append
        self.menu.menus['editor'].elements.append(MenuRect(self, color=(50, 50, 50, 255), pos=(420, 5), size=(216, 440)))
        self.menu.menus['editor'].elements.append(MenuRect(self, color=(40, 40, 40, 255), pos=(420, 5), size=(216, 30)))
        self.menu.menus['editor'].elements.append(MenuText(self, pos=(420, 5), size=20, text="Editor"))
        self.menu.menus['editor'].selectable_elements.append(MenuSelectableText(self, pos=(450, 50), size=20, text="Enemy Editor", execute=self.enemy_editor_open))
        self.menu.menus['editor'].selectable_elements.append(MenuSelectableText(self, pos=(450, 100), size=20, text="Trigger Editor", execute=self.trigger_editor_open))
        self.menu.menus['editor'].selectable_elements.append(MenuSelectableText(self, pos=(450, 150), size=20, text="Mics"))
    
    def enemymenuinit(self):
        # init
        self.menu.menus["enemy_editor"] = Menu(self, self.menu)


        # append
        self.menu.menus['enemy_editor'].elements.append(MenuRect(self, color=(50, 50, 50, 255), pos=(420, 5), size=(216, 440)))
        self.menu.menus['enemy_editor'].elements.append(MenuRect(self, color=(40, 40, 40, 255), pos=(420, 5), size=(216, 30)))
        self.menu.menus['enemy_editor'].elements.append(MenuText(self, pos=(420, 5), size=20, text="Enemy Editor"))
        self.menu.menus['enemy_editor'].selectable_elements.append(MenuSelectableText(self, pos=(450, 50), size=20, text="Selected Enemy:"))
        self.menu.menus['enemy_editor'].elements.append(MenuText(self, pos=(450, 75), size=20, text=""))
        self.menu.menus['enemy_editor'].selectable_elements.append(MenuSelectableText(self, pos=(450, 100), size=20, text="Selected Behavior:"))
        self.menu.menus['enemy_editor'].elements.append(MenuText(self, pos=(450, 125), size=20, text=""))
        self.menu.menus['enemy_editor'].selectable_elements.append(MenuSelectableText(self, pos=(450, 150), size=20, text="Args:", execute=self.clear_args))
        self.menu.menus['enemy_editor'].elements.append(MenuText(self, pos=(450, 175), size=20, text=""))
    
    def triggermenuinit(self):
        # init
        self.menu.menus["trigger_editor"] = Menu(self, self.menu)


        # append
        self.menu.menus['trigger_editor'].elements.append(MenuRect(self, color=(50, 50, 50, 255), pos=(420, 5), size=(216, 440)))
        self.menu.menus['trigger_editor'].elements.append(MenuRect(self, color=(40, 40, 40, 255), pos=(420, 5), size=(216, 30)))
        self.menu.menus['trigger_editor'].elements.append(MenuText(self, pos=(420, 5), size=20, text="Trigger Editor"))
        self.menu.menus['trigger_editor'].selectable_elements.append(MenuSelectableText(self, pos=(450, 50), size=20, text="Camera Editor", execute=self.open_camera_editor))
        self.menu.menus['trigger_editor'].selectable_elements.append(MenuSelectableText(self, pos=(450, 100), size=20, text="Trigger Editor", execute=self.open_trigger_add_editor))
    
    def triggereditmenuinit(self):
        # init
        self.menu.menus["trigger_editor_menu"] = Menu(self, self.menu)


        # append
        self.menu.menus['trigger_editor_menu'].elements.append(MenuRect(self, color=(50, 50, 50, 255), pos=(420, 5), size=(216, 440)))
        self.menu.menus['trigger_editor_menu'].elements.append(MenuRect(self, color=(40, 40, 40, 255), pos=(420, 5), size=(216, 30)))
        self.menu.menus['trigger_editor_menu'].elements.append(MenuText(self, pos=(420, 5), size=20, text="Trigger Add Editor"))
        self.menu.menus['trigger_editor_menu'].selectable_elements.append(MenuSelectableText(self, pos=(450, 50), size=20, text="Selected Trigger:"))
        self.menu.menus['trigger_editor_menu'].elements.append(MenuText(self, pos=(450, 75), size=20, text=""))
        self.menu.menus['trigger_editor_menu'].selectable_elements.append(MenuSelectableText(self, pos=(450, 100), size=20, text="Num Arg:"))
        self.menu.menus['trigger_editor_menu'].elements.append(MenuText(self, pos=(450, 125), size=20, text=""))
    
    def render_args(self):
        if len(self.args) >= 1:
            for pos in self.args:
                pg.draw.rect(self.screen, (0, 255, 0), pg.Rect(pos[0], pos[1], 20, 20), width=2)
                if len(self.args) >= 2:
                    pg.draw.aalines(self.screen, (0, 255, 0), False, self.args)

    def update(self):
        for ev in pg.event.get():
            self.event_handler(ev)
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_z:
                    try:
                        self.menu.menus[self.menu.current_menu_item].selectable_elements[self.menu.menu_ui_selected].on_use()
                    except IndexError:
                        self.soundregistry.rglist["cancel"].play()
                        self.soundregistry.rglist["cancel"].reload()
                if ev.key == pg.K_UP and self.menu.menu_ui_selected != 0:
                    self.menu.change_menu_ui_selected_up()
                if ev.key == pg.K_DOWN and self.menu.menu_ui_selected != len(self.menu.menus[self.menu.current_menu_item].selectable_elements) - 1:
                    self.menu.change_menu_ui_selected_down()

                # The Function Keys Binds
                if ev.key == pg.K_F1:
                    self.helptext.text = "Help:F1,Inspector:F2,Editor:F3,Save/Load:F9/F10,Disable Mousepos/Camera:F11/F12"
                    self.menu.change_current_menu('help')
                if ev.key == pg.K_F2:
                    self.helptext.text = "Help:F1,Inspector:F2,Editor:F3,Save/Load:F9/F10,Disable Mousepos/Camera:F11/F12"
                    self.menu.change_current_menu("inspector")
                if ev.key == pg.K_F3:
                    self.helptext.text = "Help:F1,Inspector:F2,Editor:F3,Save/Load:F9/F10,Disable Mousepos/Camera:F11/F12"
                    self.menu.change_current_menu("editor")
                if ev.key == pg.K_F9:
                    self.stagesystem.enemies = self.enemy_list
                    self.stagesystem.triggers = self.trigger_list
                    self.stagesystem.save()
                if ev.key == pg.K_F10:
                    self.load()
                if ev.key == pg.K_F11:
                    self.disable_mouseposshow = not self.disable_mouseposshow
                if ev.key == pg.K_F12:
                    self.helptext.text = "Help:F1,Inspector:F2,Editor:F3,Save/Load:F9/F10,Disable Mousepos/Camera:F11/F12"
                    if self.camera_editor:
                        self.close_camera_editor()
                
                if self.camera_editor == True:
                    if ev.key == pg.K_END:
                        self.trigger_args["destpos"] = self.camera.position
                    if ev.key == pg.K_INSERT:
                        self.trigger_args["yaw"] = self.camera.yaw
                        self.trigger_args["pitch"] = self.camera.pitch
                    if ev.key == pg.K_k:
                        self.trigger_args["startframetime"] = self.frametime
                    if ev.key == pg.K_l:
                        self.trigger_args["endframetime"] = self.frametime
                    if ev.key == pg.K_m:
                        try:
                            self.trigger_list.append(MoveCameraToDestPos(self.camera, destinatedpos=self.trigger_args["destpos"], startframetime=self.trigger_args["startframetime"], endframetime=self.trigger_args["endframetime"]))
                            self.trigger_args = {}
                        except:
                            print("KeyError: one key is not provided")
                    if ev.key == pg.K_n:
                        try:
                            self.trigger_list.append(RotateCamera(self.camera, yaw=self.trigger_args["yaw"], pitch=self.trigger_args["pitch"], startframetime=self.trigger_args["startframetime"], endframetime=self.trigger_args["endframetime"]))
                            self.trigger_args = {}
                        except:
                            print("KeyError: one key is not provided")

                if ev.key == pg.K_LCTRL:
                    self.frametime -= 1
                if ev.key == pg.K_RCTRL:
                    self.frametime += 1
                if ev.key == pg.K_LALT:
                    self.frametime -= 10
                if ev.key == pg.K_RALT:
                    self.frametime += 10

                if ev.key == pg.K_LEFT:
                    if self.menu.menus['enemy_editor'].selectable_elements[0].is_selected:
                        if self.selected_enemy != 0:
                            self.selected_enemy -= 1
                    else:
                        if self.selected_behavior != 0:
                            self.selected_behavior -= 1
                    if self.menu.menus['trigger_editor_menu'].selectable_elements[1].is_selected:
                        self.dialoguenum -= 1
                if ev.key == pg.K_RIGHT:
                    if self.menu.menus['enemy_editor'].selectable_elements[0].is_selected:
                        if self.selected_enemy < len(self.enemyregistry.rglist) - 1:
                            self.selected_enemy += 1
                    else:
                        if self.selected_behavior < len(self.behavioregistry.rglist) - 1:
                            self.selected_behavior += 1
                    if self.menu.menus['trigger_editor_menu'].selectable_elements[1].is_selected:
                        self.dialoguenum += 1

            if ev.type == pg.MOUSEBUTTONDOWN:
                if ev.button == 3:
                    self.args.append(pg.mouse.get_pos())
                    pyperclip.copy(str(pg.mouse.get_pos()))
                if ev.button == 1:
                    if self.menu.current_menu_item == "trigger_editor_menu":
                        self.trigger_list.append(DialogueActivate(self))
                    else:
                        self.enemy_list.append(self.enemyregistry.rglist[self.enemies[self.selected_enemy]](self, pos=self.mousepos, time=self.frametime, behavior=self.behaviors[self.selected_behavior], behavior_args=(self.args)))

        self.menu.menus['inspector'].elements[3].text_str = f"Total Enemies: {len(self.enemy_list)}"
        self.frametime_text.text = f"Frametime: {self.frametime}"


        self.menu.menus['enemy_editor'].elements[3].text_str = self.enemies[self.selected_enemy]
        self.menu.menus['enemy_editor'].elements[4].text_str = self.behaviors[self.selected_behavior]
        self.menu.menus['trigger_editor_menu'].elements[4].text_str = f"{self.dialoguenum}"

        self.mousepos = list(pg.mouse.get_pos())
        self.mousepostext.pos = (self.mousepos[0] + 7, self.mousepos[1] + 7)
        self.mousepostext.text = str(pg.mouse.get_pos())

        self.menu.menus['enemy_editor'].elements[5].text_str = f"{self.args}"

        self.render_args()

        if not self.is_paused:
            if not self.camera_editor:
                self.screen.blit(self.gamebg, (0, 0))
            else:
                pg.draw.rect(self.screen, (200, 200, 200), rect=(32, 16, 384, 448), width=3)

            self.screen.blit(self.fight_area, (32, 16))
            
            self.menu.update()
            self.helptext.update()
                    
        self.frametime_text.update()

        for particle in self.particles:
            particle.update()
        for enemy in self.enemy_list:
            enemy.draw()

        if not self.disable_mouseposshow:
            self.mousepostext.update()
    
if __name__ == '__main__':
    stg_path = input("StagePath (EX:1.stg):")
    if stg_path == '':
        editor = EDITOR()
    else:
        if test_stg_file(stg_path) == True:
            editor = EDITOR(stg_path=f"{stg_path}")
        else:
            editor = EDITOR(stg_path=f"{stg_path}")
    editor.run()