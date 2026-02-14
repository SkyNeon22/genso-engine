import pygame as pg
from core.visuals.ui import *
from ursina import Entity

class Dialogue:
    '''Values:
        is_skippable: bool
        maxtime: int
        text: str

        Errors:
            ...
        '''
    default_values = {
        'maxshowtime': 400, 'is_skippable': True, 'text': "Test"
    }
    def __init__(self, game, dialoguemanager, **kwargs):
        self.game = game
        self.dialogmanage = dialoguemanager
        self.text = "Test\nMultiline"
        self.is_skippable = True
        self.on_scr_time = 0
        self.maxtime = 400
        for key, value in kwargs.items():
            setattr(self, key, value) 
    
    def todict(self): # method for saving an enemy object to a stage file
        return {"game": None,
                "text": self.text,
                "is_skippable": self.is_skippable,
                "maxshowtime": self.maxtime
        }

    @classmethod
    def fromdict(cls, asset, game=None, dialogmanager=None): # method for loading an enemy object from a stage file
        return cls(game, dialogmanager, text=asset["text"], is_skippable=asset["is_skippable"], maxtime=asset["maxshowtime"])
    
    def update(self):
        self.on_scr_time += 1
        if self.on_scr_time >= self.maxtime:
            return True
        else:
            return False
    
    def skip(self):
        self.on_scr_time = self.maxtime
    
class DialogueCollection:
    def __init__(self, game, dialoguemanager, dialogue=[]):
        self.game = game
        self.active = True
        self.dialog_index = 0
        self.dialogmanager = dialoguemanager
        self.dialogue = dialogue
    
    def todict(self): # method for saving an enemy object to a stage file
        return {"game": None,
                "dialogue": self.dialogue
        }

    @classmethod
    def fromdict(cls, asset, game=None, dialogmanager=None): # method for loading an enemy object from a stage file
        return cls(game, dialogmanager, dialogue=asset["dialogue"])

    def update(self):
        if len(self.dialogue) >= 1:
            try:
                line_height = self.dialogmanager.font.get_linesize()
                lines = self.dialogue[self.dialog_index].text.split('\n')
                if self.dialogue[self.dialog_index].update() == True:
                    self.dialog_index += 1
                for line in lines: 
                    text_surface = self.dialogmanager.font.render(line, True, (255, 255, 255))
                    self.game.fight_area.blit(text_surface, (self.dialogmanager.dialoguerect.left, self.dialogmanager.dialoguerect.top + self.dialogmanager.y_offset))
                    self.dialogmanager.y_offset += line_height
                self.dialogmanager.y_offset = self.dialogmanager.default_offset
            except IndexError:
                self.active = False

class DialogueSystem:
    def __init__(self, game):
        self.game = game
        self.active = False
        self.active_collection = 0
        self.dialogue_collection_dict = {0 : DialogueCollection(self.game, self, [Dialogue(self.game, self, maxshowtime=400, is_skippable=True, text="Test\nMultiline"), Dialogue(self.game, self, maxshowtime=400, is_skippable=True, text="Test NAH")])}
        self.skip_dialogue = False
        self.dialoguerect = pg.Rect(16, 300, 354, 130)
        self.font = pg.font.SysFont('Comic Sans MS', 18)

        self.default_offset = 0
        self.y_offset = 0
    
    def update(self):
        if self.active:
            if len(self.dialogue_collection_dict) >= 1 and self.dialogue_collection_dict[self.active_collection].active == True:
                pg.draw.rect(self.game.fight_area, (40, 40, 40, 150), self.dialoguerect)
                self.dialogue_collection_dict[self.active_collection].update()
    
    def skip(self):
        if len(self.dialogue_collection_dict) >= 1 and self.dialogue_collection_dict[self.active_collection].active == True:
            self.dialogue_collection_dict[self.active_collection].dialogue[self.dialogue_collection_dict[self.active_collection].dialog_index].skip()