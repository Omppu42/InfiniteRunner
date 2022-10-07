import pygame, time, sys
from enum import Enum
from util.util import get_highscore
pygame.init()

class Gamestate(Enum):
    START=0
    PLAY=1
    DED=2
    PAUSED=3

class GameManager:
    start_obs_spawn_delay = 60
    obs_spawn_delay = start_obs_spawn_delay

    def __init__(self, screen, GROUND_Y):
        self.screen = screen
        self.font = pygame.font.Font(None, 50)
        self.big_font = pygame.font.Font(None, 75)
        self.game_state = Gamestate.PLAY
        self.start_time = time.time()
        self.pause_time = 0
        self.pause_time_start = 0
        self.score = 0
        self.ground_y = GROUND_Y
        self.scr_w = screen.get_width()
        self.scr_h = screen.get_height()
        self.obstacles = []
        self.obs_loop_count = 0
        self.paused = 1

    def update(self, player, PlayerCls, Obstacle, bg_pieces):
        if self.game_state is Gamestate.PLAY:
            self.update_obstacles(Obstacle)
            self.score = int((time.time() - self.start_time)-self.pause_time)

        text = self.font.render(str(self.score), True, (255,0,0)) #score
        self.screen.blit(text, (10,10))
        for x in self.obstacles:
            x.draw()
        
        if self.game_state is Gamestate.PAUSED:
            text_str = "PAUSED"
            text = self.font.render(text_str, True, (200,0,0))
            text_size = self.font.size(text_str)
            self.screen.blit(text, (self.scr_w//2-text_size[0]//2, self.scr_h//2-text_size[1]//2))

        if self.game_state is Gamestate.DED: # when ded
            self.dead_func(player)
            self.restart_game(player, PlayerCls, bg_pieces, Obstacle)
            


    def dead_func(self, player):
        hihgscore = get_highscore(self.score)

        text_str = "YOU DIED"
        text = self.big_font.render(text_str, True, (200,0,0))
        text_size = self.big_font.size(text_str)
        self.screen.blit(text, (self.scr_w//2-text_size[0]//2, self.scr_h//2-text_size[1]//2-25))

        text_str = "Press 'R' to restart"
        text = self.font.render(text_str, True, (200,0,0))
        text_size = self.font.size(text_str)
        self.screen.blit(text, (self.scr_w//2-text_size[0]//2, self.scr_h//2+20))

        small_font = pygame.font.Font(None, 30)
        if hihgscore[1]: #new highscore
            text_str = "NEW HIGHSCORE: {}".format(hihgscore[0])
            text = self.font.render(text_str, True, (255,50,50))
            text_size = self.font.size(text_str)
            self.screen.blit(text, (self.scr_w//2-text_size[0]//2, self.scr_h//2+60))
        else: #no new highscore
            text_str = "Highscore: {}".format(hihgscore[0])
            text = small_font.render(text_str, True, (200,0,0))
            text_size = small_font.size(text_str)
            self.screen.blit(text, (self.scr_w//2-text_size[0]//2, self.scr_h//2+60))

        player.draw()
        pygame.display.update()

        pygame.event.clear()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    break
        

    def restart_game(self, player, PlayerCls, bg_pieces, ObstacleCls):
        GameManager.obs_spawn_delay = GameManager.start_obs_spawn_delay
        self.game_state = Gamestate.PLAY
        self.obstacles = []
        self.obs_loop_count = 0
        self.obs_spwn_delay = GameManager.obs_spawn_delay
        self.start_time = time.time()
        self.pause_time = 0

        ObstacleCls.reset_obst()
        player.restart()

        for x in bg_pieces:
            x.restart()


    def update_obstacles(self, obstacleCls):
        self.obs_loop_count += 1
        if self.obs_loop_count >= GameManager.obs_spawn_delay:
            GameManager.obs_spawn_delay = obstacleCls.new_spwn_delay()
            self.obstacles = obstacleCls.spawn_obstacles(self.obstacles, self.screen, self.ground_y, self.scr_w)
            self.obs_loop_count = 0