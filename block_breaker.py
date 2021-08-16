#block shooting game
#simple game to learn pygame and practice using classes in python
#need to clean up with functions some parts
#mouse to move, right click to shoot, and scroll wheel to rotate
#press enter to try again
#each round player player ammo and block count are the same
#gain 1 ammo for each block shot
#game is over if player runs out of ammo or hits block

import pygame
import random

from pygame.constants import K_RETURN, MOUSEBUTTONDOWN, RLEACCEL, K_ESCAPE, KEYDOWN #buttons used in game

pygame.init()
player_s1_size = 50
width, height = 500, 500
color_black = (0, 0, 0)
win = pygame.display.set_mode((width, height)) #creates a game window with given size 
font = pygame.font.Font('freesansbold.ttf', 32) #font used for all text

class player(pygame.sprite.Sprite):
    def __init__(self):
        super(player, self).__init__()
        self.surf1 = pygame.image.load("player_sprite1.png").convert()
        self.surf1.set_colorkey((color_black), RLEACCEL)
        self.mask = pygame.mask.from_surface(self.surf1)
        self.rect = self.surf1.get_rect(center = (width/2,height/2))
        self.front = 1
        self.front_last = 0
        self.position = pygame.mouse.get_pos()

    def change_position_mouse(self):
        #updates the position of player sprite based off of mouse cursor location
        self.position = pygame.mouse.get_pos()
        if self.position[0] > player_s1_size-25 and self.position[0] < 475 and self.position[1] < 440 and self.position[1] > 22: #only update mouse postion if inside window
            self.rect.center = pygame.mouse.get_pos() 
    
    def change_front(self, button_pressed):
        #if scroll wheel is moved rotate player
        #scroll up rotates right
        #scroll left rotates left
        if button_pressed == 5:
            if self.front < 4:
                self.front += 1
            else:
                self.front = 1
        if button_pressed == 4:
            if self.front > 1:
                self.front -= 1
            else:
                self.front = 4

    def change_orientation(self):
        #update player image and mask (hitbox)
        if self.front == 1:
            self.surf1 = pygame.image.load("player_sprite1.png").convert()
            self.surf1.set_colorkey(color_black, RLEACCEL)
            self.mask = pygame.mask.from_surface(self.surf1)
        elif self.front == 2:
            self.surf1 = pygame.image.load("player_sprite2.png").convert()
            self.surf1.set_colorkey(color_black, RLEACCEL)
            self.mask = pygame.mask.from_surface(self.surf1)
        elif self.front == 3:
            self.surf1 = pygame.image.load("player_sprite3.png").convert()
            self.surf1.set_colorkey(color_black, RLEACCEL)
            self.mask = pygame.mask.from_surface(self.surf1)
        elif self.front == 4:
            self.surf1 = pygame.image.load("player_sprite4.png").convert()
            self.surf1.set_colorkey(color_black, RLEACCEL)
            self.mask = pygame.mask.from_surface(self.surf1)    

class projectile(pygame.sprite.Sprite):
    def __init__(self, position, player_front):
        super(projectile, self).__init__()
        self.surf1 = pygame.Surface((10, 10))
        self.surf1.fill(color_black)
        self.rect = position
        self.front = player_front
        self.orientation_flag = 0
        self.p_speed = 15
        
    def update(self):
        #change firing position based off player orientation
        #keep updating position until out of bounds
        if self.front == 1:
            if self.orientation_flag == 0: #fixes projectile firing position
                self.rect.move_ip(0, -player_s1_size/2)
                self.orientation_flag = 1
            if self.rect.top > 1:
                self.rect.move_ip(0, -self.p_speed)
            else:
                self.kill()
        elif self.front == 2:

            if self.rect.right < width:
                self.rect.move_ip(self.p_speed, 0)
            else:
                self.kill()
        elif self.front == 3:
            if self.orientation_flag == 0:
                self.rect.move_ip(0, player_s1_size/2)
                self.orientation_flag = 1
            if self.rect.bottom < (height-40):
                self.rect.move_ip(0, self.p_speed)
            else:
                self.kill()
        elif self.front == 4:
            if self.orientation_flag == 0:
                self.rect.move_ip(-player_s1_size/2, 0)
                self.orientation_flag = 1
            if self.rect.left > 1:
                self.rect.move_ip(-self.p_speed, 0)
            else:
                self.kill()       
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf1 = pygame.Surface((10, 10))
        #self.surf1.fill(color_black)
        self.surf1.fill((random.randint(0, 225), random.randint(0, 225), random.randint(0, 225)))
        self.mask = pygame.mask.from_surface(self.surf1)
        self.flag1 = 0
        self.flag2 = 0
        self.random_speed = random.randint(1, 3) 
        random_place = random.randint(1, 4)  #random starting place on outskirts of play area
        if random_place == 1:
            self.rect = self.surf1.get_rect(center = (random.randint(0, 494), random.randint(1, 5)))
        elif random_place == 2:
            self.rect = self.surf1.get_rect(center = (random.randint(1, 5), random.randint(0, 440)))
        elif random_place == 3:
            self.rect = self.surf1.get_rect(center = (random.randint(0, 499), random.randint(435, 440)))
        elif random_place == 4:
            self.rect = self.surf1.get_rect(center = (random.randint(439, 494), random.randint(0, 440)))

    def change_position(self): 
        #change position on wall bounces
        #commented portions could be added to increase speed on every wall bounce
        if self.rect.right < width and self.flag1 == 0:
            self.rect.move_ip(self.random_speed , 0)
            if self.rect.right >= width :
                self.flag1 = 1
                #self.random_speed  += .5
        elif self.rect.left > 0 and self.flag1 == 1:
            self.rect.move_ip(-self.random_speed , 0)
            if self.rect.left <= 0:
                self.flag1 = 0
                #self.random_speed  += .5
        if self.rect.bottom < (height-50) and self.flag2 == 0:
            self.rect.move_ip(0, self.random_speed )
            if self.rect.bottom >= height-50 :
                self.flag2 = 1 
                #self.random_speed  += .5
        elif self.rect.top > 0 and self.flag2 == 1:
            self.rect.move_ip(0, -self.random_speed )
            if self.rect.top <= 0:
                self.flag2 = 0
                #self.random_speed  += .5

def update_pos(player_sprite, enemies_sprite, projectiles):
    #update all current sprties
    player_sprite.change_position_mouse()
    player_sprite.change_orientation()
    for en in enemies_sprite:
            en.change_position()
    projectiles.update()

def draw_surfaces(surfaces):
    for s in surfaces:
            win.blit(s.surf1, s.rect)

def create_text():
    text1 = font.render('Score:', False, color_black)
    text2 = font.render('Ammo:', False, color_black)
    text3 = font.render('Game Over', False, color_black)
    text4 = font.render('High Score:', False, color_black)
    text_list = [text1, text2, text3, text4, text1, text1, text1]
    return text_list

def update_text(text_list_, flag_value):
    if flag_value == 0:
        win.blit(text_list_[0], (5, height-40))
        win.blit(text_list_[1], (250, height-40))
        win.blit(text_list_[4], (125, height-40))
        win.blit(text_list_[5], (370, height-40))
    else:
        win.blit(text_list_[0], (5, height-40))
        win.blit(text_list_[2], (170, height-300))
        win.blit(text_list_[3], (150, height-250))
        win.blit(text_list_[4], (125, height-40))
        win.blit(text_list_[6], (350, height-250))

def remove_sprites(player_sprite, enemies_sprite, flag):
    #clean up sprites on game over
    if flag == 0:
        player_sprite.kill()
    for en in enemies_sprite:
        en.kill()

def en_pro_collisions(projects, enemies, all_s):
    #check for projectile and enemy collision
    for en in enemies:
        if pygame.sprite.spritecollideany(en, projects):
            en.kill()
            return 1
    return 0

def en_plr_collisions(s1, enemies):
    #check for player collisions
    for en in enemies:
        if pygame.sprite.spritecollideany(s1, enemies, collided=pygame.sprite.collide_mask):
            en.kill()
            return 1
    return 0

def add_sprites(enemies, all_s ,enemies_list, s1):
    all_s.add(s1)
    for en in enemies_list:
        en = Enemy()
        enemies.add(en)
        all_s.add(en)

def make_enemie_list(num_enemies):
    list1 = []
    for i in range(num_enemies):
        en = Enemy()
        list1.append(en)
    return list1

def main():
    count = 0 #current game score
    ammo_start = 1 #starting ammo for each round, ammo = enemie count for each round
    ammo = ammo_start #current ammo
    count_string = str(count) #needed for text
    ammo_string = str(ammo)
    high_score_string = str(0)
    high_score = 0
    text_list = create_text()
    clock = pygame.time.Clock()
    running = True
    game_status = 0 #0 main game, 1 game over
    ammo_status = 0 #0 have ammo, 1 no ammo
    button_pressed = 0
    s1 = player()
    enemy_start_count = 1
    enemie_list = make_enemie_list(enemy_start_count)
    enemies = pygame.sprite.Group()
    projects = pygame.sprite.Group()
    all_s = pygame.sprite.Group()
    add_sprites(enemies, all_s, enemie_list, s1)
    pygame.mouse.set_visible(False)
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN: #exit game if esc key pressed
                if event.key == K_ESCAPE: 
                    running = False
            elif event.type == MOUSEBUTTONDOWN and game_status == 0 and ammo_status == 0: #update orientation or fire projectile
                button_pressed = event.button
                s1.change_front(button_pressed)
                if event.button == 1:
                    if ammo > 0:
                        x_spread = 1 #change spread, would have to remove projectiles at end
                        for i in range(1):#change this for more projectiles
                            p1 = projectile((s1.rect.copy()).inflate(-40, -35), s1.front)
                            p1.rect.move_ip(0,-i*x_spread)#need to change for diffferent or orientations
                            all_s.add(p1)
                            projects.add(p1)
                        ammo -= 1
                        ammo_string = str(ammo)
            elif event.type == pygame.QUIT:
                running = False
        #set up next level
        if len(enemies) == 0:
            remove_sprites(s1, enemies, 1)
            en = Enemy()
            enemie_list.append(en)
            add_sprites(enemies, all_s, enemie_list, s1) 
            ammo_start += 1
            ammo = ammo_start
            ammo_string = str(ammo)
            text_list[5] = font.render(ammo_string, False, color_black)
            update_text(text_list, 0)
            pygame.display.flip()

        #main game    
        if game_status == 0:
            win.fill((255, 255, 255))
            update_pos(s1, enemies, projects)
            draw_surfaces(all_s)
            if en_pro_collisions(projects, enemies, all_s) == 1:
                count += 1
                ammo += 1
                ammo_status = 0
                count_string = str(count)
                ammo_string = str(ammo)
            if en_plr_collisions(s1, enemies) == 1:
                game_status = 1
            text_list[4] = font.render(count_string, False, color_black)
            text_list[5] = font.render(ammo_string, False, color_black)
            update_text(text_list, 0)
            pygame.display.flip()
            if ammo < 1:
                ammo_status = 1
                if(len(projects) == 0):
                    game_status = 1
        #game over
        else:
            remove_sprites(s1, enemies, 0)
            s1 = player()
            enemie_list = make_enemie_list(enemy_start_count)
            add_sprites(enemies, all_s, enemie_list, s1)
            if count > high_score:
                high_score = count
            high_score_string = str(high_score)
            text_list[6] = font.render(high_score_string, False, color_black)
            win.fill((255, 255, 255))
            update_text(text_list, 1)
            pygame.display.flip()
            pressed_key = pygame.key.get_pressed()
            if pressed_key[K_RETURN]: #restart main game
                count = 0
                ammo_start = 1
                ammo = ammo_start
                count_string = str(count)
                ammo_string = str(ammo)
                game_status = 0
                ammo_status = 0
        clock.tick(60)     
    pygame.quit()

if __name__ == "__main__":
    main()