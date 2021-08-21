import pygame
import random
from pygame.constants import RLEACCEL #buttons used in game
from constants import COLOR_BLACK

class Sprites(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, center):
        super(Sprites, self).__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center = center

    def get_center(self):
        return self.center

    def out_of_bounds(self):
        if self.rect.right > self.screen_width:
            self.rect.move_ip(-self.screen_width, 0)
        if self.rect.left < 0:
            self.rect.move_ip(self.screen_width, 0)
        if self.rect.top < 0:
            self.rect.move_ip(0, self.screen_height)
        if self.rect.bottom > self.screen_height:
            self.rect.move_ip(0, -self.screen_height) 

class Player(Sprites):
    def __init__(self, screen_width, screen_height):
        Sprites.__init__(self, screen_width, screen_height, [screen_width/2,screen_height/2])
        self.surf1 = pygame.image.load("player_sprite1.png").convert()
        self.surf1.set_colorkey(COLOR_BLACK, RLEACCEL)
        self.mask = pygame.mask.from_surface(self.surf1)
        self.rect = self.surf1.get_rect(center = (self.screen_width/2,self.screen_height/2))
        self.front = 1
        self.front_last = 0
        self.position = pygame.mouse.get_pos()
        self.player_size = 50

    def get_front(self):
        return self.front
    
    def get_size(self):
        return self.player_size

    def rotate(self):
        if self.front == 1:
            self.surf1 = pygame.image.load("player_sprite1.png").convert()
            self.surf1.set_colorkey(COLOR_BLACK, RLEACCEL)
            self.mask = pygame.mask.from_surface(self.surf1)
        elif self.front == 2:
            self.surf1 = pygame.image.load("player_sprite2.png").convert()
            self.surf1.set_colorkey(COLOR_BLACK, RLEACCEL)
            self.mask = pygame.mask.from_surface(self.surf1)
        elif self.front == 3:
            self.surf1 = pygame.image.load("player_sprite3.png").convert()
            self.surf1.set_colorkey(COLOR_BLACK, RLEACCEL)
            self.mask = pygame.mask.from_surface(self.surf1)
        elif self.front == 4:
            self.surf1 = pygame.image.load("player_sprite4.png").convert()
            self.surf1.set_colorkey(COLOR_BLACK, RLEACCEL)
            self.mask = pygame.mask.from_surface(self.surf1) 

    def change_position_mouse(self):
        #updates the position of player sprite based off of mouse cursor location
        self.position = pygame.mouse.get_pos()
        if self.position[0] > self.player_size-25 and self.position[0] < 475 and self.position[1] < 475 and self.position[1] > 22: #only update mouse postion if inside window
            self.rect.center = pygame.mouse.get_pos() 
        self.center = [self.rect.centerx, self.rect.centery] #update position after moving

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

class Projectile(Sprites):
    def __init__(self, center, player_front, screen_width, screen_height, player_size):
        Sprites.__init__(self, screen_width, screen_height, center)
        self.surf1 = pygame.Surface((10, 10))
        self.surf1.fill(COLOR_BLACK)
        self.center = center
        self.front = player_front
        self.orientation_flag = 0
        self.p_speed = 15
        self.player_size = player_size
        self.x = center[0]
        self.y = center[1]
        #change firing position based off player orientation
        if self.front == 1:
            self.rect = self.surf1.get_rect(center = (self.x, self.y-25)) 
        elif self.front == 2:
            self.rect = self.surf1.get_rect(center = (self.x+25, self.y+3)) 
        elif self.front == 3:
            self.rect = self.surf1.get_rect(center = (self.x, self.y+25)) 
        else:
            self.rect = self.surf1.get_rect(center = (self.x-25, self.y+3))

    def update(self):
        #keep updating position until out of bounds
        if self.front == 1:
            if self.rect.top > 1:
                self.rect.move_ip(0, -self.p_speed)
            else:
                self.kill() 
        elif self.front == 2:
            if self.rect.right < self.screen_width:
                self.rect.move_ip(self.p_speed, 0)
            else:
                self.kill()
        elif self.front == 3:
            if self.rect.bottom < self.screen_height:
                self.rect.move_ip(0, self.p_speed)
            else:
                self.kill()
        else:
            if self.rect.left > 1:
                self.rect.move_ip(-self.p_speed, 0)
            else:
                self.kill()
                
class Enemy(Sprites):
    def __init__(self, screen_width, screen_height, creation_flag, creation_type, center):
        Sprites.__init__(self, screen_width, screen_height, center)
        self.surf1 = pygame.Surface((10, 10))
        #self.surf1.fill(COLOR_BLACK)
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

    def update(self): 
        #change position on wall bounces
        #commented portions could be added to increase speed on every wall bounce
        #change position on wall bounces
        #commented portions could be added to increase speed on every wall bounce
        if self.rect.right < self.screen_width and self.flag1 == 0:
            self.rect.move_ip(self.random_speed , 0)
            if self.rect.right >= self.screen_width :
                self.flag1 = 1
                #self.random_speed  += .5
        elif self.rect.left > 0 and self.flag1 == 1:
            self.rect.move_ip(-self.random_speed , 0)
            if self.rect.left <= 0:
                self.flag1 = 0
                #self.random_speed  += .5
        if self.rect.bottom < (self.screen_height) and self.flag2 == 0:
            self.rect.move_ip(0, self.random_speed )
            if self.rect.bottom >= self.screen_height :
                self.flag2 = 1 
                #self.random_speed  += .5
        elif self.rect.top > 0 and self.flag2 == 1:
            self.rect.move_ip(0, -self.random_speed )
            if self.rect.top <= 0:
                self.flag2 = 0
                #self.random_speed  += .5