import pygame

pygame.init()

class Gravity:
    def __init__(self, strength: float, terminal_vel: float):
        self.strength = strength / 100
        self.terminal_vel = terminal_vel
        self.total_grav = 0
        self.start_dy = 0
        self.reached_top = False

    def apply_gravity(self, other_object): 
        self.total_grav += self.strength
        
        if other_object.dy < -self.terminal_vel: #termianl vel
            other_object.dy = -self.terminal_vel

        other_object.dy -= self.total_grav

        if (abs(other_object.dy) <= 0.5 and not other_object.on_ground() and not self.reached_top):
            self.total_grav = 0
            self.reached_top = True
    
    def reset_gravity(self):
        self.total_grav = 0
        self.reached_top = False


def load_sprites(folder, sprite_name, sprite_count, image_extension) -> list:
    sprites = []
    sprite_path = folder+sprite_name
    if sprite_count is None: return pygame.image.load(sprite_path+image_extension)

    for i in range(sprite_count):
        sprites.append(pygame.image.load(sprite_path+str(i)+image_extension))
    return sprites


def get_highscore(score) -> tuple: #returns score and bool was new highscore or not
    highscore = 0
    with open("data\\highscore.txt", "r") as f:
        highscore = f.readline()

        if highscore != "":
            highscore = int(highscore)
        else: 
            print("no previous highscore")
            highscore = 0   

    if score > highscore:
        set_new_highscore(score)
        return (score, True) #new highscore

    return (highscore, False)


def set_new_highscore(score):
    with open("data\\highscore.txt", "w") as f:
        f.write(str(score))