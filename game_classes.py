import pygame
import sprite_classes
from constants import *

class Game_Text():
    def __init__(self, win, width, height):
        self.width = width
        self.height = height
        self.text_list = []
        self.font = pygame.font.Font('freesansbold.ttf', 32) #font used for all text
        self.win = win
        self.score = 0
        self.high_score = 0
        self.game_over_width = (self.width/2) - 100
        self.game_over_height = (self.height/2) - 32
        self.score_padding = 125 
        self.high_score_padding = 200
        self.ammo_padding = 125
        self.score_pad_num = 10
        self.high_score_pad_num = 10
        self.ammo_pad_num = 10
        self.ammo = 1
    
    def get_ammo(self):
        return self.ammo
    
    def set_ammo(self, ammo):
        self.ammo = ammo

    def get_score(self):
        return self.score

    def get_high_score(self):
        return self.high_score

    def set_score(self, score):
        self.score = score

    def set_high_score(self, high_score):
        self.high_score = high_score

    def padding(self):
        if self.score / self.score_pad_num == 1:
            self.score_padding += 10
            self.score_pad_num *= 10

        if self.high_score / self.high_score_pad_num == 1:
            self.high_score_padding += 10
            self.high_score_pad_num *= 10

        if self.ammo / self.ammo_pad_num == 1:
            self.ammo_padding += 10
            self.ammo_pad_num *= 10

    def update_score(self):
        self.padding()
        if self.score > self.high_score:
            self.high_score = self.score
        self.text_list[3] = self.font.render(str(self.score), False, COLOR_BLACK)
        self.text_list[4] = self.font.render(str(self.high_score), False, COLOR_BLACK)
        self.text_list[6] = self.font.render(str(self.ammo), False, COLOR_BLACK)
        
    def create_text(self):
        text_score = self.font.render('Score:', False, COLOR_BLACK)
        text_game_over = self.font.render('Game Over', False, COLOR_BLACK)
        text_high_score = self.font.render('High Score:', False, COLOR_BLACK)
        text_ammo = self.font.render('Ammo:', False, COLOR_BLACK)
        score = self.font.render(str(self.score), False, COLOR_BLACK)
        high_score = self.font.render(str(self.high_score), False, COLOR_BLACK)
        ammo = self.font.render(str(self.ammo), False, COLOR_BLACK)
        self.text_list = [text_score, text_game_over, text_high_score, score, high_score, text_ammo, ammo]  

    def update_text(self, game_status):
        if game_status == 0:
            self.update_score()
            self.win.blit(self.text_list[0], (5, 10)) #text_score
            self.win.blit(self.text_list[3], (self.score_padding, 10))  #score
            self.win.blit(self.text_list[5], (0, self.height - 40))  #text_ammo
            self.win.blit(self.text_list[6], (self.ammo_padding, self.height - 40))  #ammo

        else:
            self.win.blit(self.text_list[0], (5, 10)) #text_score
            self.win.blit(self.text_list[3], (self.score_padding, 10))  #score
            self.win.blit(self.text_list[1], (self.game_over_width, self.game_over_height)) #text_game_over
            self.win.blit(self.text_list[2], (5, self.height - 40)) #text_high_score
            self.win.blit(self.text_list[4], (self.high_score_padding, self.height - 40))  #high_score

class Game():
    def __init__(self, clock_speed, rgb_tuple, win, width, height):
        self.width = width
        self.height = height
        self.win = win
        self.text = Game_Text(win, width, height)
        self.game_status = 0
        self.player1 = sprite_classes.Player(WIDTH, HEIGHT)
        self.projects = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.surfaces = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.clock_speed = clock_speed
        self.win_rgb = rgb_tuple
        self.enemie_count = 1

    def get_status(self):
        return self.game_status

    #functions for game progression
    def start(self):
        self.read_high_score()
        self.text.create_text()
        self.add_sprites()

    def next_level(self):
        self.surfaces = pygame.sprite.Group()
        self.add_sprites()
        self.text.set_ammo(self.enemie_count)

    def restart(self):
        self.player1 = sprite_classes.Player(self.width, self.height)
        self.text.set_ammo(1)
        self.text.set_score(0)
        self.enemie_count = 1
        self.add_sprites()
        self.game_status = 0

    #draw all surfaces on screen
    def draw_surfaces(self):
        for s in self.surfaces:
            self.win.blit(s.surf1, s.rect)
    
    #update all sprite positions if 
    def update_sprite_pos(self):
        #pressed_key = pygame.key.get_pressed()
        #self.player1.update(pressed_key)
        self.player1.change_position_mouse()
        self.player1.rotate()
        self.projects.update()
        self.enemies.update()

    def check_ammo(self):
        if self.text.get_ammo() == 0 and len(self.projects) == 0:
            self.game_status = 1

    #main game function
    def update(self):
        self.win.fill(self.win_rgb)
        self.text.update_text(self.game_status)
        self.check_ammo()
        if self.game_status == 0:
            self.draw_surfaces()
            self.update_sprite_pos()
            self.check_for_collisions()
        else:
            self.remove_sprites()
        pygame.display.flip()
        self.clock.tick(60) 
    
    #functions for creating sprites
    def add_projectile(self):
        p1 = sprite_classes.Projectile(self.player1.get_center(), self.player1.get_front(), self.width, self.height, self.player1.get_size())
        self.surfaces.add(p1)
        self.projects.add(p1)
    
    def add_enemies(self, creation_flag, creation_type, center, num_enemies):
        for i in range(num_enemies):
            en = sprite_classes.Enemy(self.width, self.height, creation_flag, creation_type, center)
            self.enemies.add(en)
            self.surfaces.add(en)

    def add_sprites(self):
        self.surfaces.add(self.player1)
        num_enemies = self.enemie_count
        self.add_enemies(0, 0, [0,0], num_enemies)

    #check if there are no more enemies left
    def check_enemies(self):
        if len(self.enemies) == 0:
            self.enemie_count += 1
            self.next_level()

    #functions for collisions between sprites       
    def en_plr_collisions(self):
        for en in self.enemies:
            if pygame.sprite.spritecollideany(self.player1, self.enemies, collided=pygame.sprite.collide_mask):
                self.game_status = 1
                
            
    def en_pro_collisions(self):
        for en in self.enemies:
            x = pygame.sprite.spritecollideany(en, self.projects)
            if x != None:
                en.kill()
                self.text.set_score(self.text.get_score() + 1)
                self.text.set_ammo(self.text.get_ammo() + 1)
        if self.game_status == 0: #don't wnat game to go to next level on game over screen
            self.check_enemies()

    def check_for_collisions(self):
        self.en_plr_collisions()
        self.en_pro_collisions()

    #functions for cleaning up sprites
    def remove_enemies(self):
        for en in self.enemies:
            en.kill()

    def remove_projectiles(self):
        for proj in self.projects:
            proj.kill()
    
    def remove_sprites(self):
        self.player1.kill()
        self.remove_enemies()
        self.remove_projectiles()
        self.surfaces = pygame.sprite.Group()

    #functions for high score
    def read_high_score(self):
        high_score_file = open('high_score.txt', "r")
        self.text.set_high_score(int(high_score_file.read()))
        high_score_file.close()

    def write_high_score(self):
        high_score_file = open('high_score.txt', "w")
        high_score_file.write(str(self.text.get_high_score()))
        high_score_file.close()
