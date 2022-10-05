import pygame, time, random, os, sys
from obstacle import Obstacle
from player import Player
from scrolling_image import ScrollingImage
from util import load_sprites
from load_sidescroll_textures import load_bg_pieces
import game_manager
pygame.init()

SCR_WIDTH = 600
SCR_HEIGHT = 400
GROUND_Y = SCR_HEIGHT/4*3
FPS_CAP = 60
#TODO: audio and sfx

def update_play(player, screen, gameManager):
    to_remove = [] #delete obtacles after reaching end of screen
    for x in gameManager.obstacles:
        player.detect_collision(x.hitbox)
        x.draw()
        x.move()
        if x.x < -200:
            to_remove.append(x)
     
    for y in to_remove: #delete obstacle
        gameManager.obstacles.remove(y)


def play(player, gameManager, screen, bg_pieces):
    if gameManager.game_state is not game_manager.Gamestate.PLAY:
        for x in bg_pieces:
            x.draw()

    if gameManager.game_state is game_manager.Gamestate.PLAY:
        for x in bg_pieces:
            x.draw()
            x.update()  
        update_play(player, screen, gameManager)
        player.jump()
        player.animate()

    gameManager.update(player, Player, Obstacle, bg_pieces)

    player.draw()
    pygame.display.update()


def get_input(event, player, gameManager):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        player.falling = False
        Player.jump_key_held = True
    else: 
        player.falling = True
        Player.jump_key_held = False

    if event.type == pygame.KEYDOWN:
        if keys[pygame.K_h]:
            Player.show_hitbox *= -1
            Obstacle.show_hitbox *= -1
        if keys[pygame.K_ESCAPE]:
            gameManager.paused *= -1
            if gameManager.paused == 1:
                gameManager.pause_time += (time.time()-gameManager.pause_time_start)
                gameManager.game_state = game_manager.Gamestate.PLAY
            elif gameManager.paused == -1:
                gameManager.pause_time_start = time.time()
                gameManager.game_state = game_manager.Gamestate.PAUSED



def main():
    screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
    gameManager = game_manager.GameManager(screen, GROUND_Y)
    player = Player(GROUND_Y, screen, gameManager)
    bg_pieces = load_bg_pieces(screen)
    
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill((150,150,150)) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            get_input(event, player, gameManager)

        play(player, gameManager, screen, bg_pieces)
        clock.tick(FPS_CAP)
        pygame.display.update()
        

if __name__ == "__main__":
    main()