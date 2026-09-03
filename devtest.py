from core import *
from core.game.enemy import Boss
from core.game_skele import *


class DevTest(AdvancedGameClass):
    def __init__(self, window_caption="Genso Engine v0.1.4 Game (CHANGE ME)", win_size=[640, 480]):
        super().__init__(window_caption, win_size)
        self.scene_manager.add_scene("test", Scene(self, self.scene_manager))
        self.scene_manager.scenes["test"].add_object(Tower(self, scenemanager=self.scene_manager))
        self.scene_manager.change_scene("test")

        self.new_game()

        self.pos_x = 380

        self.test_ui()

    def test_ui(self):
        self.playerprojtext = Text(self, pos=[self.pos_x,200] ,size=20)
        self.projtext = Text(self, pos=[self.pos_x,220] ,size=20)
        self.lazertext = Text(self, pos=[self.pos_x,240] ,size=20)
        self.enemytext = Text(self, pos=[self.pos_x,260] ,size=20)
        self.pickuptext = Text(self, pos=[self.pos_x,280] ,size=20)
        self.fpstext = Text(self, pos=[self.pos_x,300] ,size=20)

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
            self.update_player_projectiles()
            self.update_enemies()
            self.update_pickups()
            self.update_particles()
            self.update_lazers()
            self.update_projectiles()

            for trigger in self.trigger_list:
                    trigger.update()
            self.frametime += 1

            self.playerprojtext.text = f"player_projs:{len(self.player_proj)}"
            self.projtext.text = f"projs:{len(self.proj_list)}"
            self.lazertext.text = f"lazer:{len(self.lazer_list)}"
            self.enemytext.text = f"enemy:{len(self.enemy_list)}"
            self.pickuptext.text = f"pickup:{len(self.pickup_list)}"
            self.fpstext.text = f"fps:{self.clock.get_fps()}"
            self.projtext.update()
            self.playerprojtext.update()
            self.lazertext.update()
            self.enemytext.update()
            self.pickuptext.update()
            self.fpstext.update()
        

if __name__ == "__main__":
    devtest = DevTest()
    devtest.run()