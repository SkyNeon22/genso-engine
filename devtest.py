from core import *
from core.game_skele import *


class DevTest(AdvancedGameClass):
    def __init__(self, window_caption="Genso Engine v0.1.4 Game (CHANGE ME)", win_size=[640, 480]):
        super().__init__(window_caption, win_size)
        self.scene_manager.add_scene("test", Scene(self, self.scene_manager))
        self.scene_manager.change_scene("test")

        self.new_game()

    
    def new_game(self):
        super().new_game()  

        self.enemy_list.append(Boss(self, pos=(190, 150)))
        self.player = Player(self, start_power=4)
    
    def update(self):
        for ev in pg.event.get():
            self.event_handler(ev)
        
        if not self.is_paused:
            self.screen.blit(self.gamebg, (0, 0))

            self.screen.blit(self.fight_area, (32, 16))

            self.fight_area.fill((0, 0, 0, 0))

            self.player.update()
            self.update_entities()
        

if __name__ == "__main__":
    devtest = DevTest()
    devtest.run()