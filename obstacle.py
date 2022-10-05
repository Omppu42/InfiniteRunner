import pygame, random, math, json
from debug_code import draw_hitboxes
from util import load_sprites
pygame.init()


def load_obstacles() -> list:
    data_lst = []
    data = json.load(open("obstacles.json", "r"))
    for x in data:
        data_lst.append(data[x])
    return data_lst

class Obstacle:
    obstacle_data = load_obstacles()
    total_obstacles = 0
    show_hitbox = -1 #1:on, -1:off
    start_spawn_time_min = 60
    start_spawn_time_max = 81
    spawn_time_min = start_spawn_time_min
    spawn_time_max = start_spawn_time_max
    min_spawn_time_b = 40 #spawm_time_min decreases until this value
    min_spawn_time_t = 41 #spawm_time_max decreases until this value
    difficluty_multiplier: float = 0.8 #how many frames faster obstacles spawn each cycle times total obstacles, can be float

    def __init__(self, x_off, y, screen, ground_y, scr_w, obstacle_type):
        self.obstacle_type = obstacle_type #take random obstacle
        self.x = scr_w+x_off
        self.y = ground_y-y
        self.w = self.obstacle_type["size"]["w"]*self.obstacle_type["scale_multiplier"]
        self.h = self.obstacle_type["size"]["h"]*self.obstacle_type["scale_multiplier"]
        self.hitbox = [self.obstacle_type["hitbox"]["x"], self.obstacle_type["hitbox"]["y"], 
                        self.obstacle_type["hitbox"]["w"], self.obstacle_type["hitbox"]["h"]]
        self.screen = screen
        self.speed = 6
        self.image = pygame.image.load(self.obstacle_type["path"])
        self.image = pygame.transform.scale(self.image, (self.w,self.h))
        Obstacle.total_obstacles += 1
    
    def draw(self):
        self.hitbox = [self.x+(self.obstacle_type["hitbox"]["x"]*self.obstacle_type["scale_multiplier"]), 
                        self.y-(self.obstacle_type["hitbox"]["y"]*self.obstacle_type["scale_multiplier"]), 
                        self.w-(self.obstacle_type["hitbox"]["w"]*self.obstacle_type["scale_multiplier"]), 
                        self.h-(self.obstacle_type["hitbox"]["h"]*self.obstacle_type["scale_multiplier"])]
        surface = pygame.Surface((self.w, self.h))
        obst_rect = surface.get_rect(bottomleft=(self.x, self.y))
        #pygame.draw.rect(self.screen, (0,0,0), (obst_rect))
        self.screen.blit(self.image, obst_rect)

        if Obstacle.show_hitbox == 1:
           draw_hitboxes(self.screen, self.hitbox)

    def move(self):
        self.x -= self.speed

    def set_new_spwn_times():
        Obstacle.spawn_time_min -= Obstacle.difficluty_multiplier
        if Obstacle.spawn_time_min <= Obstacle.min_spawn_time_b: 
            Obstacle.spawn_time_min = Obstacle.min_spawn_time_b
        
        Obstacle.spawn_time_max -= Obstacle.difficluty_multiplier
        if Obstacle.spawn_time_max <= Obstacle.min_spawn_time_t: 
            Obstacle.spawn_time_max = Obstacle.min_spawn_time_t
        
        #print(Obstacle.spawn_time_min, Obstacle.spawn_time_max)

    def spawn_obstacles(obstacle_list, screen, ground_y, scr_w) -> list:
        obst_count = random.randint(1,2)
        
        obst_type_lst = []
        for i in range(obst_count):
            obst_type = random.choice(Obstacle.obstacle_data)
            if i == 1:
                x_offset = obst_type_lst[0]["size"]["w"]+obst_type_lst[0]["hitbox"]["x"]-obst_type_lst[0]["hitbox"]["w"] + 50
            else:
                x_offset = 0

            obst_type_lst.append(obst_type)
            obstacle_list.append(Obstacle(x_offset, 0, screen, ground_y, scr_w, obst_type))

        return obstacle_list

    def new_spwn_delay() -> int:
        Obstacle.set_new_spwn_times() #set new spawn times
        
        obst_spwn_delay = random.uniform(Obstacle.spawn_time_min, Obstacle.spawn_time_max)
        obst_spwn_delay = round(obst_spwn_delay, 0)
        return obst_spwn_delay

    
    def reset_obst():
        Obstacle.spawn_time_min = Obstacle.start_spawn_time_min
        Obstacle.spawn_time_max = Obstacle.start_spawn_time_max