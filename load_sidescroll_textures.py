import pygame
from util.util import load_sprites
from scrolling_image import ScrollingImage
pygame.init()

def load_bg_pieces(screen, ground_y) -> list:
    bg_pieces = []
    
    bg_image = load_sprites("Assets\\Images\\Background\\", "sky", None, ".png")
    bg_pieces.append(ScrollingImage(bg_image, (600, 200), 0.2, screen, 3, 0))

    bg_image = load_sprites("Assets\\Images\\Background\\", "cloud", None, ".png")
    bg_pieces.append(ScrollingImage(bg_image, (600, 200), 0.5, screen, 3, 0))

    bg_image = load_sprites("Assets\\Images\\Background\\", "mountain2", None, ".png")
    bg_pieces.append(ScrollingImage(bg_image, (600, 200), 1, screen, 3, 120, darkness=30))

    bg_image = load_sprites("Assets\\Images\\Background\\", "pine1", None, ".png")
    bg_pieces.append(ScrollingImage(bg_image, (600, 200), 2, screen, 3, 150))

    bg_image = load_sprites("Assets\\Images\\Background\\", "pine2", None, ".png")
    bg_pieces.append(ScrollingImage(bg_image, (600, 200), 3, screen, 3, 200))

    bg_image = load_sprites("Assets\\Images\\Ground\\", "ground_2", None, ".png")
    bg_pieces.append(ScrollingImage(bg_image, (48,48), 6, screen, 15, ground_y))

    bg_image = load_sprites("Assets\\Images\\Ground\\", "ground_11", None, ".png") 
    bg_pieces.append(ScrollingImage(bg_image, (64,64), 6, screen, 15, ground_y+48))

    bg_image = load_sprites("Assets\\Images\\Ground\\", "grass_1", None, ".png") 
    bg_pieces.append(ScrollingImage(bg_image, (48, 48), 6, screen, 15, ground_y))
    
    return bg_pieces