import pygame as pg
from core.game.projectile import *
from core.game.player.yinyangs import *
from core.game.colliders import CircleCollider


class Player:
    def __init__(self, game, pos=(194, 300), start_power=0.0):
        self.game = game
        self.unfocus_speed = 0.73
        self.focus_speed = 0.4
        self.speed = self.unfocus_speed

        self.lives = 2
        self.life_pieces = 0
        self.piecesforlife = 3
        self.max_lives = 8
        self.bombs = 3
        self.max_bombs = 8

        self.yinyang = YingYang
        self.yinyangs = []

        self.yin_offset_p_1 = [-1 , -50]
        self.yin_offset_p_2 = [20, -30, -20, -30]
        self.yin_offset_p_3 = [28, -30, -35, -30, -2, 30]
        self.yin_offset_p_4 = [28, -30, -35, -30, 28, 30, -35, 30]

        self.focus_yin_offset_p_1 = [-1 , -30]
        self.focus_yin_offset_p_2 = [20, -30, -20, -30]
        self.focus_yin_offset_p_3 = [28, -30, -35, -30, -2, 30]
        self.focus_yin_offset_p_4 = [28, -30, -35, -30, 28, 30, -35, 30]

        self.grazes = 0
        self.deathbomb = 8
        self.deathbombc = 0
        self.bomb_used = False

        self.shooting = False
        self.legacy_shots = False

        if self.legacy_shots:
            self.power = 0
            self.max_power = 128
        else:
            self.power = start_power
            self.max_power = 4.0

        self.item_slow_rate = 0.11

        self.shot_type = Projectile
        self.secondary = Projectile

        self.focus = False

        self.shot_cooldown = 0.04
        self.cooldown = 0.0

        self.homing_shot_cooldown = 0.9
        self.homing_cooldown = 0.0

        self.bomb_cooldown = 0.0

        self.animstate = "I"

        self.right = pg.image.load("assets/img/sprites/characters/Reimu/ReimuRight.png")
        self.left = pg.transform.flip(self.right, 1, 0)
        self.other = pg.image.load("assets/img/sprites/characters/Reimu/Reimu.png")
        self.hitbox_img = pg.image.load("assets/img/sprites/other/hitbox.png")
        self.graze_hitbox_img = pg.image.load("assets/img/sprites/other/graze_hitbox.png")
        self.graze_angle = 0
        self.img = self.other

        self.pos = list(pos)
        self.start_pos = pos
        self.size = (39, 43)
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))

        self.hitboxradius = 3
        self.grazeradius = 40
        self.hitbox = CircleCollider(self.hitboxradius, self.center)
        self.graze_hitbox = CircleCollider(self.hitboxradius, self.center)
        self.iframes = 0
        self.ifmax = 200
        self.angle_x = 0
        self.angle_y = 0
    
    def bomb(self):
        self.bombs -= 1
        self.iframes = 180 
        self.game.player_proj.append(Bomb(self.game, (self.hitbox.x - self.hitbox.x / 2, self.hitbox.y)))
    
    def calculate_dir(self):
        self.dx, self.dy = sin(self.angle_x) * self.speed, sin(self.angle_y) * self.speed
    
    def move_x(self):
        self.calculate_dir()
        self.pos[0] += self.dx

    def move_y(self):
        self.calculate_dir()
        self.pos[1] += self.dy
    
    def movement(self):
        keys = pg.key.get_pressed()
        if self.deathbombc <= -1:
            if keys[pg.K_UP] and self.pos[1] >= -10:
                    self.angle_y = -90
                    self.move_y()
                    self.animstate = "I"
            if keys[pg.K_DOWN] and self.pos[1] <= 416:
                    self.angle_y = 90
                    self.move_y()
                    self.animstate = "I"
            if keys[pg.K_LEFT] and self.pos[0] >= -10:
                    self.angle_x = -90
                    self.move_x()
                    self.animstate = "L"
            if keys[pg.K_RIGHT] and self.pos[0] <= 358:
                    self.angle_x = 90
                    self.move_x()
                    self.animstate = "R"
            if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
                self.focus = True
            if keys[pg.K_z]:
                self.shooting = True
                if self.shooting:
                    if self.cooldown <= 0:
                        self.game.player_proj.append(self.shot_type(self.game, (self.hitbox.x + 10, self.hitbox.y - 25), angle=-90))
                        self.game.player_proj.append(self.shot_type(self.game, (self.hitbox.x - 12, self.hitbox.y - 25), angle=-90))
                        if len(self.yinyangs) > 0:
                            if self.homing_cooldown <= 0:
                                
                                for yin in self.yinyangs:
                                    yin.shoot()
                                self.homing_cooldown = self.homing_shot_cooldown
                        self.cooldown = self.shot_cooldown
        if keys[pg.K_x]:
            if self.bomb_cooldown <= 0 and self.bombs >= 1: 
                self.bomb()
                self.bomb_used = True
                self.bomb_cooldown = 2.0

    def draw(self):
        self.game.fight_area.blit(pg.transform.scale(self.img, self.size), self.pos)

    def if_hit(self):
        self.lives -= 1
        if self.power >= 0.50:
            self.power -= 0.50
        self.bombs = 3
        self.pos = list(self.start_pos)
        self.game.proj_list = []
        self.iframes = self.ifmax
    
    def check_hit(self):
        if self.deathbombc <= -10:
            for enemy in self.game.enemy_list:
                if self.hitbox.collidecircle(enemy.hitbox) and enemy.col_dmg and self.game.frametime >= enemy.time:
                    if self.iframes <= 0:
                        self.deathbombc = self.deathbomb
                        return True
            for bul in self.game.proj_list:
                if self.hitbox.collidecircle(bul.hitbox):
                    if self.iframes <= 0:
                        if bul.team == "en":
                            self.deathbombc = self.deathbomb
                            return True

    def check_colliders(self):
        is_hit = self.check_hit()
        if is_hit or self.deathbombc >= 0:
            if self.iframes <= 0:
                self.game.soundregistry.get("pl_death").play()
                self.bomb_used = False
                if self.deathbombc == 0 and not self.bomb_used:
                    self.if_hit()
                    self.game.soundregistry.get("pl_death").reload()
                elif self.bomb_used and self.deathbombc == 0:
                    self.iframes = 100
                    self.game.soundregistry.get("pl_death").reload()
        for pickup in self.game.pickup_list:
            if self.graze_hitbox.collidecircle(pickup.hitbox):
                if pickup.type == "pwr":
                    if self.power < self.max_power:
                        self.power += pickup.power
                    self.game.score += pickup.points
                    pickup.kill = True
                if pickup.type == "col":
                    self.game.score += pickup.points
                    pickup.kill = True
                if pickup.type == "life":
                    self.game.score += pickup.points
                    self.lives += 1
                    pickup.kill = True
                if pickup.type == "lifepiece":
                    self.game.score += pickup.points
                    if self.life_pieces > self.piecesforlife - 1 and self.lives < self.max_lives: # - 1 required to register the extend when life piece count gets to the count for giving a life
                        self.lives += 1
                        self.life_pieces = 0
                        self.game.soundregistry.get("extend").play()
                    else:
                        self.life_pieces += 1
                    pickup.kill = True
                if pickup.type == "bom":
                    self.bombs += 1
                    self.game.score += pickup.points
                    pickup.kill = True
        for bul in self.game.proj_list:
            if bul.team == "en":
                if self.graze_hitbox.collidecircle(bul.hitbox):
                    self.grazes += 1

    def update(self):
        #self.graze_angle += 1
        #if self.legacy_shots == False:
        self.draw()
        if len(self.yinyangs) > 0:
            for yin in self.yinyangs:
                yin.update()
        self.shooting = False
        if self.bomb_cooldown <= 0:
            self.bomb_used = False
        self.deathbombc -= 1
        self.iframes -= 1
        if self.power <= 0.99:
            self.yinyangs = []
        if self.focus == True:
            self.speed = self.focus_speed
            if self.power >= 1.0 and self.power <= 1.99:
                self.yinyangs = [self.yinyang(self.game, self, pos=(self.hitbox.x + self.focus_yin_offset_p_1[0], self.hitbox.y + self.focus_yin_offset_p_1[1]))]
            if self.power >= 2.0 and self.power <= 2.99:
                self.yinyangs = [self.yinyang(self.game, self, pos=(self.hitbox.x + self.focus_yin_offset_p_2[0], self.hitbox.y + self.focus_yin_offset_p_2[1])), self.yinyang(self.game, self, pos=(self.hitbox.x + self.focus_yin_offset_p_2[2], self.hitbox.y + self.focus_yin_offset_p_2[3]))]
            if self.power >= 3.0 and self.power <= 3.99:
                self.yinyangs = [self.yinyang(self.game, self, pos=(self.hitbox.x + self.focus_yin_offset_p_3[0], self.hitbox.y + self.focus_yin_offset_p_3[1])), self.yinyang(self.game, self, pos=(self.hitbox.x + self.focus_yin_offset_p_3[2], self.hitbox.y + self.focus_yin_offset_p_3[3])), self.yinyang(self.game, self, pos=(self.hitbox.x + self.focus_yin_offset_p_3[4], self.hitbox.y + self.focus_yin_offset_p_3[5]))]
            if self.power >= 4.0:
                self.power = 4.0
                self.yinyangs = [self.yinyang(self.game, self, pos=(self.hitbox.x + self.focus_yin_offset_p_4[0], self.hitbox.y + self.focus_yin_offset_p_4[1])), self.yinyang(self.game, self, pos=(self.hitbox.x + self.focus_yin_offset_p_4[2], self.hitbox.y + self.focus_yin_offset_p_4[3])), self.yinyang(self.game, self, pos=(self.hitbox.x + self.focus_yin_offset_p_4[4], self.hitbox.y + self.focus_yin_offset_p_4[5])),self.yinyang(self.game, self, pos=(self.hitbox.x + self.focus_yin_offset_p_4[6], self.hitbox.y + self.focus_yin_offset_p_4[7]))]
        else:
            self.speed = self.unfocus_speed
            if self.power >= 1.0 and self.power <= 1.99:
                self.yinyangs = [self.yinyang(self.game, self, pos=(self.hitbox.x + self.yin_offset_p_1[0], self.hitbox.y + self.yin_offset_p_1[1]))]
            if self.power >= 2.0 and self.power <= 2.99:
                self.yinyangs = [self.yinyang(self.game, self, pos=(self.hitbox.x + self.yin_offset_p_2[0], self.hitbox.y + self.yin_offset_p_2[1])), self.yinyang(self.game, self, pos=(self.hitbox.x + self.yin_offset_p_2[2], self.hitbox.y + self.yin_offset_p_2[3]))]
            if self.power >= 3.0 and self.power <= 3.99:
                self.yinyangs = [self.yinyang(self.game, self, pos=(self.hitbox.x + self.yin_offset_p_3[0], self.hitbox.y + self.yin_offset_p_3[1])), self.yinyang(self.game, self, pos=(self.hitbox.x + self.yin_offset_p_3[2], self.hitbox.y + self.yin_offset_p_3[3])), self.yinyang(self.game, self, pos=(self.hitbox.x + self.yin_offset_p_3[4], self.hitbox.y + self.yin_offset_p_3[5]))]
            if self.power >= 4.0:
                self.yinyangs = [self.yinyang(self.game, self, pos=(self.hitbox.x + self.yin_offset_p_4[0], self.hitbox.y + self.yin_offset_p_4[1])), self.yinyang(self.game, self, pos=(self.hitbox.x + self.yin_offset_p_4[2], self.hitbox.y + self.yin_offset_p_4[3])), self.yinyang(self.game, self, pos=(self.hitbox.x + self.yin_offset_p_4[4], self.hitbox.y + self.yin_offset_p_4[5])),self.yinyang(self.game, self, pos=(self.hitbox.x + self.yin_offset_p_4[6], self.hitbox.y + self.yin_offset_p_4[7]))]

        if self.animstate == "I":
            self.img = self.other
        elif self.animstate == "R":
            self.img = self.right
        elif self.animstate == "L":
            self.img = self.left
        self.animstate = "I"
        self.focus = False
        self.homing_cooldown -= 0.01
        self.cooldown -= 0.01
        self.bomb_cooldown -= 0.01
        self.center = (self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2))
        self.graze_hitbox.update(self.center)
        self.hitbox.update(self.center)
        self.check_colliders()
        self.movement()
