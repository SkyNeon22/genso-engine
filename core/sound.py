import pygame as pg


#class SoundHandler:
#    def __init__(self, game):
#        pg.mixer.init()
#        self.game = game
#        self.volume = 1
#        self.musicvolume = 1
#        self.soundchannel_1 = pg.mixer.Sound()
#        self.soundchannel_2 = pg.mixer.Sound()
#        self.soundchannel_3 = pg.mixer.Sound()
#        self.soundchannel_4 = pg.mixer.Sound()
#        self.soundchannel_5 = pg.mixer.Sound()
#        self.musicchannel_1 = pg.mixer.Sound() 
#    
#    def play(self, sound, channel):
#        channel.append(Sound(self.game, sound, channel))

#doesn't work
#class SoundHandler:
#    def __init__(self, game):
#        pg.mixer.init()
#        self.game = game
#        self.volume = 1
#        self.musicvolume = 1
#        self.soundchannel_1 = []
#        self.soundchannel_2 = []
#        self.soundchannel_3 = []
#        self.soundchannel_4 = []
#        self.soundchannel_5 = []
#        self.musicchannel_1 = [] 
#    
#    def update(self):
#        if len(self.soundchannel_1) != 0:
#            self.soundchannel_1[0].update(self.volume)
#        if len(self.soundchannel_2) != 0:
#            print(len(self.soundchannel_2))
#            self.soundchannel_2[0].update(self.volume)
#        if len(self.soundchannel_3) != 0:
#            self.soundchannel_3[0].update(self.volume)
#        if len(self.soundchannel_4) != 0:
#            self.soundchannel_4[0].update(self.volume)
#        if len(self.soundchannel_5) != 0:
#            self.soundchannel_5[0].update(self.volume)
#        if len(self.musicchannel_1) != 0:
#            self.musicchannel_1[0].update(self.musicvolume)
#    
#    def play(self, sound, channel):
#        channel.append(Sound(self.game, sound, channel))
#
class Sound:
    def __init__(self, game, sound: str):
        '''game: required\n
           sound: path to the file (ex:"sfx/sounds/se_ok00.wav")\n'''
        self.game = game
        self.sound = sound
        self.isplaying = False
        self.lnght = 0
        self.player = pg.mixer.Sound(self.sound)
    
    def play(self, volume: float = 1.00):
        if not self.isplaying:
            self.player.set_volume(volume)
            self.player.play()
            self.isplaying = True
            for i in range(0, (int(self.player.get_length()) * 100), 16):
                self.lnght += 0.016 
    
    def reload(self):
        self.isplaying = False

if __name__ == "__main__":
    pg.init()
    pg.mixer.init()
    s = Sound(None, "sfx/sounds/se_cat01.wav")
    sg = pg.mixer.Sound("sfx/sounds/se_cat01.wav")
    sg.play(10)
    #print(s.player.get_length())
    #s.play()