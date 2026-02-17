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
        self.dialogue_collection_dict = {0 : DialogueCollection(self.game, self, [Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="???:\nWho is here?"), 
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="???:\nAh... A Familiar face"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nOh it's you again..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Yuuka:\nYes it's me again."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nWhat are doing at this place"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Yuuka:\nAh... Just wanderin' around."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nStrange..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Yuuka:\nSo it's gonna be a friendly duel I suppose."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nNo."),
                                                                                  Dialogue(self.game, self, maxshowtime=120, is_skippable=True, text="Yuuka:\nDid I ask?"),
                                                                                  ]),
                                         1 : DialogueCollection(self.game, self, [Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="???:\nWho is here?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="???:\nAh... You seem familiar..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nYou are that one..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Yuuka:\nThat one?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nWe fought once few years ago..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Yuuka:\nSo you did remember it!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Yuuka:\n...So it's gonna be a friendly duel\n again I suppose..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nYeah!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Yuuka:\n..."),
                                                                                   ]),
                                         2 : DialogueCollection(self.game, self, [Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="???:\nWho is here?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="Alice:\n!?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="???:\nSomeone new it seems..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Yuuka:\nMy name is Yuuka Kazami.\n What's your name?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nAlice."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Yuuka:\nSo, how did you get in Gensokyo?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nI dont know."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Yuuka:\nYou are really new here..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Yuuka:\nSo it's gonna be a welcoming duel\n I suppose."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nIs it required?"),
                                                                                #   Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Yuuka:\nNo. But we are gonna fight anyway."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\n!!!"),
                                                                                   ]),
                                         
                                         3 : DialogueCollection(self.game, self, [Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="???:\nDon't move!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="Reimu:\nAh..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="???:\nStop right there criminal scum!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nWho are you?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marie:\nMarie, the Grand Guard Doll."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nFor Who do You work?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marie:\nWhy do You need to know?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nJust curious..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marie:\nI work for Alice Margatroid."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nAh... Someone familiar... So where\nis she?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marie:\nSomewhere far from you scum!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\n..."),
                                                                                  ]),
                                        4 : DialogueCollection(self.game, self, [Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="???:\nDon't move!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="Marisa:\nAAAAAAAAAAAAA!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="???:\nStop right there criminal scum!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\n(Did I get exposed?)"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="???:\nSpeak NOW! Who are YOU!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nFujiwara no Iyozane.A humble boater\nat the Gloomy Straits.\n(NO WAY, A LEN'EN REFERENCE?)"),
                                                                                  Dialogue(self.game, self, maxshowtime=90, is_skippable=True, text="???:\nWhere is your paddle?"),
                                                                                  Dialogue(self.game, self, maxshowtime=90, is_skippable=True, text="???:\nAnd why you are here now?"),
                                                                                  Dialogue(self.game, self, maxshowtime=90, is_skippable=True, text="???:\nAnd there is no Gloomy Straits \nin Gensokyo!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nI'm joking, ma name is Marisa!\nWhat is yours!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="???:\n!!!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marie:\nMarie, the Grand Guard Doll, \nYou LIAR!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nOk, after the indroduction can i go?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marie:\nNOO!!!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\n..."),
                                                                                  ]),
                                        5 : DialogueCollection(self.game, self, [Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="???:\nDon't move!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="Alice:\n!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="???:\nStop right there you black and white!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nEveryone in Gensokyo is so rude!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="???:\nWhy do you think that?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nEveryone so aggresive, trying to attack..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="???:\nWell, not everyone is a fighter."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nSo who are you?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marie:\nMarie, the Grand Guard Doll. Whats Your Name?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nAlice..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marie:\nAlice... That's the name of\nmy master..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nReally?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marie:\nYeah..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nWell... Can I go now?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marie:\nNo...You Shall not Pass!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nI will fight my way thought then!"),
                                                                                  ]),
                                         
                                         6 : DialogueCollection(self.game, self, [Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="???:\nHow did you get here."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="Reimu:\n..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nWho are you!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nAlice Margatroid... You didn't\nchange, same as always!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nI don't remember seeing you even once..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nMy name is Reimu Hakurei."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nWha... Really?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nYes."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nYou changed so much..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nYeah."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nWell, I learned some new spells...\nSo Let's fight like the previous time!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nWhy not!"),
                                                                                    ]),
                                         7 : DialogueCollection(self.game, self, [Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="???:\nHow did you get here."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="Marisa:\n..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nYou seem familiar... Just black"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nAlice Margatroid YOU ARE SO SMALL HAHAAH!!!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nHEY, I'm NOT. But who are you..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nMy name is Reimu Hakurei."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nWha... Really?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nlol no"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nSo.."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nI am Marisa Kirisame!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nOh... Yeah... I now remember...\nSo Let's fight like the previous time!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nTHAT'S THE SPIRIT!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nCan you stop screaming."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nOk."),
                                                                                    ]),
                                         8 : DialogueCollection(self.game, self, [Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="???:\nWho are you"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="Shangai Alice:\n?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice Margatroid:\nBlack and White, what a bold choice...\nFor clothes..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Shangai:\nWhy is that..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Margatroid:\nThere was someone who had the same\ncolors in Makai."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Shangai:\n...Tf is makai?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Margatroid:\nIt's destroyed now...\nBut, who are you?"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Shangai:\nShangai Alice. What is your name!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Margatroid:\nMy name is Alice Margatroid."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Shangai:\nOh... The same name."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Margatroid:\nWell... Why not do a duel, as a celebration."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Shangai:\nWell..."),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Margatroid:\nWhat? Don't be shy!"),
                                                                                  Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Shangai:\n..."),
                                                                                    ]),
                                        9 : DialogueCollection(self.game, self, [Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="???:\nReimu?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nRin?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Rin Satsuki:\nYeah it's me!"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nAren't you always at the shrine?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Rin:\nThat's only partialy true."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nWhy is that."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Rin:\nI sometimes go on a walk."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nWhen I'm at the shrine,\nyou do nothing."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Rin:\nYou just fail to notice."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nMaybe."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Rin:\nNot maybe, it's just the truth."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nDon't make me angry."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Rin:\nIt's just the truth."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\n!!!"),
                                                                                 ]), 
                                        10 : DialogueCollection(self.game, self, [Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="???:\nWho are you?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\n?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nAh you are the nurse at the shrine."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Rin Satsuki:\nYou know me?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nyes"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Rin:\nWell,then tell me who you are."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nMarisa Kirisame, a Magician"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Rin:\nOh, understood."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Rin:\n..."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nEh?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Rin:\nI don't remember seeing you at the shrine."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nHow did you not notice me once?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Rin:\nI don't know.It's just the truth."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nOh. SO LET'S FIGHT!"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Rin:\n!?"),]),
                                        11 : DialogueCollection(self.game, self, [Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="???:\nWho are you?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\n?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="???:\nWho are you black-white?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nSo rude."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="???:\nWhat's wrong?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nEveryone calls me like that."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="???:\nAnd what's wrong.And also who you are?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nAlice."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Rin Satsuki:\nOh. Ok. And my name is Rin."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\n..."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Rin:\nSo why are you heading to the shrine."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nDon't you see?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Rin:\nWhat?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nThe Energy"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Rin:\nUr weird."),]),
                                    
                                        12 : DialogueCollection(self.game, self, [Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="???:\nThere is no hope?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="Reimu:\n?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="???:\nAre you the shrine maiden?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nYeah... I've seen you."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Shangai Alice:\nMy name is Alice, and I know you seen me."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nFor what did you come here?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\n..."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nAlice."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\n..."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nALICE!"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nAh..."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nNow I understood."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nWhat?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nI'll seal you for good."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\n!?"),]),
                                        13 : DialogueCollection(self.game, self, [Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="???:\nMarisa?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="Marisa:\n?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nIt's you."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nYEAH>:)."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nWhat's wrong?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nNOTHIN'>:)"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nWhat's with your '>:)' intent."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nJust came to pay a little visit."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nOh. Ok."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\n..."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nSo what are you waiting for."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nDon't you understand?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\n?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Marisa:\nLET'S FIGHT >:D"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nIf you wish... Why not!"),]),
                                        14 : DialogueCollection(self.game, self, [Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="???:\nWho are you?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=False, text="Alice:\nAlice."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nWhy are you here?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nYou know why."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\n?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\n..."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nAnd?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\nReimu!"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nI DON'T UNDERSTAND!"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\n..."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nI WOULD SEAL YOU FOR GOOD."),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\n!?"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nWHATEVER IT TAKES"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Alice:\n!!!"),
                                                                                 Dialogue(self.game, self, maxshowtime=200, is_skippable=True, text="Reimu:\nUR DONE.\nAlice:\n?????"),]),
                                            }
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
            else:
                for dialog in self.dialogue_collection_dict[self.active_collection].dialogue:
                    dialog.on_scr_time = 0
                self.dialogue_collection_dict[self.active_collection].dialog_index = 0
                self.active = False
            for enemy in self.game.enemy_list:
                if enemy.is_boss != True:
                    enemy.kill = True
    
    def skip(self):
        if len(self.dialogue_collection_dict) >= 1 and self.dialogue_collection_dict[self.active_collection].active == True and self.dialogue_collection_dict[self.active_collection].dialogue[self.dialogue_collection_dict[self.active_collection].dialog_index].is_skippable != False:
            self.dialogue_collection_dict[self.active_collection].dialogue[self.dialogue_collection_dict[self.active_collection].dialog_index].skip()