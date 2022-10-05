import pygame, random, time
from util.util import load_sprites, Gravity
from game_manager import Gamestate
from util.debug import draw_hitboxes
pygame.init()

player_gravity = Gravity(6, 6)

class Player:
    jump_height = 45
    jump_speed = 6

    jump_sprites = load_sprites("Assets\\Images\\Jump\\", "adventurer-jump-0", 2, ".png")
    run_sprites = load_sprites("Assets\\Images\\Run\\", "adventurer-run-0", 6, ".png")

    run_sound = pygame.mixer.Sound("Assets\\Sounds\\run.wav")
    run_sound.set_volume(0.4)
    jump_sound = pygame.mixer.Sound("Assets\\Sounds\\jump.wav")
    jump_sound.set_volume(1)
    death_sound = pygame.mixer.Sound("Assets\\Sounds\\death.wav")

    show_hitbox = -1 #1:on, -1:off
    jump_key_held = False

    def __init__(self, ground_y, screen, gameManager):
        self.image = Player.run_sprites[0]
        self.gameManager = gameManager
        self.x = 50
        self.y = ground_y
        self.dy = 0
        self.ground_y = ground_y
        self.w = Player.run_sprites[0].get_size()[0]*2
        self.h = Player.run_sprites[0].get_size()[1]*2
        self.hitbox = []
        self.animation_frame = 0
        self.animation_image = 0
        self.screen = screen
        self.falling = False
        self.run_channel = pygame.mixer.Channel(0)
        self.jump_channel = pygame.mixer.Channel(1)
        self.death_channel = pygame.mixer.Channel(2)


    def restart(self):
        self.y = self.ground_y-1
        self.image = Player.run_sprites[0]
        self.animation_frame = 0
        self.animation_image = 0
        self.jump_key_held = False
        self.falling = True
        self.dy = 0

    def detect_collision(self, obs_hitbox):
        player_rect = pygame.Rect(self.hitbox[0],self.hitbox[1],self.hitbox[2],self.hitbox[3])
        player_rect.bottomleft = (self.hitbox[0],self.hitbox[1])

        obs_rect = pygame.Rect(obs_hitbox[0],obs_hitbox[1],obs_hitbox[2],obs_hitbox[3])
        obs_rect.bottomleft = (obs_hitbox[0], obs_hitbox[1])

        collide = player_rect.colliderect(obs_rect)
        
        if collide:
            if not self.death_channel.get_busy():
                self.death_channel.play(Player.death_sound)
            self.gameManager.game_state = Gamestate.DED


    def animate(self): 
        self.animation_frame += 1
        if not player_gravity.reached_top and not self.on_ground():
            self.image = Player.jump_sprites[0]
        if player_gravity.reached_top and not self.on_ground():
            self.image = Player.jump_sprites[1]

        if self.animation_frame < 6 or not self.on_ground(): return
        
        if self.animation_image >= 5:
            self.animation_image = 0
        else:
            self.animation_image += 1

        self.animation_frame = 0
        self.image = Player.run_sprites[self.animation_image]


    def draw(self):
        self.hitbox = [self.x+45, self.y-15, self.w-80, self.h-40]
        self.image = pygame.transform.scale(self.image, (self.w, self.h))

        player_rect = self.image.get_rect(bottomleft = (self.x, self.y))

        self.screen.blit(self.image, player_rect)
        
        if Player.show_hitbox == 1:
            draw_hitboxes(self.screen, self.hitbox)


    def on_ground(self) -> bool:
        return self.y >= self.ground_y


    def player_on_ground(self):
        if not self.on_ground(): 
            self.run_channel.stop()
            return

        if not self.run_channel.get_busy(): #run sounds
            self.run_channel.play(Player.run_sound)

        self.falling = False
        player_gravity.reset_gravity()
        self.dy = 0

        if Player.jump_key_held:
            self.played_land_sound = False
            if not self.jump_channel.get_busy(): #jump sounds
                self.jump_channel.play(Player.jump_sound)

            self.dy = Player.jump_speed
            player_gravity.start_dy = Player.jump_speed


    def jump(self):
        self.player_on_ground()

        if self.y < self.ground_y - Player.jump_height: #reached max haight
            self.falling = True 

        if self.falling:
            player_gravity.apply_gravity(self)
            self.falling = True 

        if self.y-self.dy > self.ground_y: # inside ground next frame
            self.dy = 0
            self.y = self.ground_y

        self.y-=self.dy