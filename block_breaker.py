#block shooting game
#simple game to learn pygame and practice using classes in python
#need to clean up with functions some parts
#mouse to move, right click to shoot, and scroll wheel to rotate
#press enter to try again
#each round player player ammo and block count are the same
#gain 1 ammo for each block shot
#game is over if player runs out of ammo or hits block
import pygame
from game_classes import Game
from pygame.constants import K_RETURN, MOUSEBUTTONDOWN, RLEACCEL, K_ESCAPE, KEYDOWN #buttons used in game
from constants import *

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT)) #creates a game window with given size 

def main():
    running = True
    pygame.mouse.set_visible(False)
    game = Game(30, COLOR_WHITE, win, WIDTH, HEIGHT)
    game.start()
    while running:
        for event in pygame.event.get():
            ammo = game.text.get_ammo()
            if event.type == KEYDOWN: #exit game if esc key pressed
                if event.key == K_ESCAPE: 
                    running = False
                if event.key == K_RETURN and game.get_status() == 1:
                        game.restart()
            elif event.type == MOUSEBUTTONDOWN and game.get_status() == 0: #update orientation or fire projectile
                button_pressed = event.button
                game.player1.change_front(button_pressed)
                if event.button == 1:
                    if ammo > 0:
                        game.add_projectile()
                        ammo -= 1
                        game.text.set_ammo(ammo)
            elif event.type == pygame.QUIT:
                running = False
        #set up next level
        game.update()  
    pygame.quit()

if __name__ == "__main__":
    main()