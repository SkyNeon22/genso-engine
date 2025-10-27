from core.game_skele import *


class Game(BasicGameClass):
    def __init__(self, window_caption="Genso Engine v0.1.0 Prototype Game"):
        super().__init__(window_caption)
        self.musicregistry.rglist[self.current_song].play(0.20)
        
if __name__ == "__main__":
    game = Game()
    game.run()