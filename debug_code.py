import pygame
pygame.init()

def draw_hitboxes(screen, hitbox):
    pygame.draw.line(screen, (255,0,0), (hitbox[0], hitbox[1]), 
                                            (hitbox[0]+hitbox[2], hitbox[1]))
    pygame.draw.line(screen, (255,0,0), (hitbox[0], hitbox[1]), 
                                            (hitbox[0], hitbox[1]-hitbox[3]))
    pygame.draw.line(screen, (255,0,0), (hitbox[0]+hitbox[2], hitbox[1]), 
                                            (hitbox[0]+hitbox[2], hitbox[1]-hitbox[3]))
    pygame.draw.line(screen, (255,0,0), (hitbox[0], hitbox[1]-hitbox[3]), 
                                            (hitbox[0]+hitbox[2], hitbox[1]-hitbox[3]))