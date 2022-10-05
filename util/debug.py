import pygame
pygame.init()

draw_fps_b: int = -1
def draw_fps(screen, clock, scr_w):
    font = pygame.font.Font(None, 50)
    text = font.render(str(round(clock.get_fps())), True, (255,0,0))
    screen.blit(text, (scr_w-50, 10))


def draw_hitboxes(screen, hitbox):
    pygame.draw.line(screen, (255,0,0), (hitbox[0], hitbox[1]), 
                                            (hitbox[0]+hitbox[2], hitbox[1]))
    pygame.draw.line(screen, (255,0,0), (hitbox[0], hitbox[1]), 
                                            (hitbox[0], hitbox[1]-hitbox[3]))
    pygame.draw.line(screen, (255,0,0), (hitbox[0]+hitbox[2], hitbox[1]), 
                                            (hitbox[0]+hitbox[2], hitbox[1]-hitbox[3]))
    pygame.draw.line(screen, (255,0,0), (hitbox[0], hitbox[1]-hitbox[3]), 
                                            (hitbox[0]+hitbox[2], hitbox[1]-hitbox[3]))