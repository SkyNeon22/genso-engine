import pygame as pg

class Sound:
    def __init__(self, game, sound: str):
        '''game: required\n
           sound: path to the file (ex:"sfx/sounds/se_ok00.wav")\n'''
        self.game = game
        self.sound = sound
        self.isplaying = False
        self.lnght = 0
        self.player = pg.mixer.Sound(self.sound)
    
    def play(self, volume: float = 0.10):
        '''Plays the sound at given volume'''
        if not self.isplaying:
            self.player.set_volume(volume)
            self.player.play()
            self.isplaying = True
            for i in range(0, (int(self.player.get_length()) * 100), 16):
                self.lnght += 0.016 
    
    def reload(self):
        self.isplaying = False

class Music:
    def __init__(self, game, sound: str):
        '''game: required\n
           sound: path to the file (ex:"sfx/sounds/se_ok00.wav")\n'''
        self.game = game
        self.sound = sound
    
    def play(self, volume: float = 1.00):
        '''Plays the song at given volume'''
        pg.mixer_music.load(self.sound)
        pg.mixer_music.set_volume(volume)
        pg.mixer_music.play(fade_ms=40)
    
    def pause(self):
        pg.mixer_music.pause()

    def resume(self):
        pos = pg.mixer_music.get_pos()
        pg.mixer_music.play(start=pos)
    
    def immediate_stop(self):
        pg.mixer_music.stop()
    
    def stop(self):
        pg.mixer_music.fadeout(40)

if __name__ == "__main__":
    pg.init()
    pg.mixer.init()
    s = Sound(None, "sfx/sounds/se_cat01.wav")
    sg = pg.mixer.Sound("sfx/sounds/se_cat01.wav")
    sg.play(10)