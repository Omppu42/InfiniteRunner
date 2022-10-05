import pygame
from util import load_sprites
from scrolling_image import ScrollingImage
pygame.init()

def load_bg_pieces(screen) -> list:
    bg_pieces = []
    
    bg_image = load_sprites("Sprites\\Background\\", "sky", None, ".png")
    bg_pieces.append(ScrollingImage(bg_image, (600, 200), 0.2, screen, 3, 0))

    bg_image = load_sprites("Sprites\\Background\\", "cloud", None, ".png")
    bg_pieces.append(ScrollingImage(bg_image, (600, 200), 0.5, screen, 3, 0))

    bg_image = load_sprites("Sprites\\Background\\", "mountain2", None, ".png")
    bg_pieces.append(ScrollingImage(bg_image, (600, 200), 1, screen, 3, 120, darkness=30))

    bg_image = load_sprites("Sprites\\Background\\", "pine1", None, ".png")
    bg_pieces.append(ScrollingImage(bg_image, (600, 200), 2, screen, 3, 150))

    bg_image = load_sprites("Sprites\\Background\\", "pine2", None, ".png")
    bg_pieces.append(ScrollingImage(bg_image, (600, 200), 3, screen, 3, 200))

    bg_image = load_sprites("Sprites\\Ground\\", "ground_2", None, ".png")
    bg_pieces.append(ScrollingImage(bg_image, (48,48), 6, screen, 15, 300))

    bg_image = load_sprites("Sprites\\Ground\\", "ground_11", None, ".png") 
    bg_pieces.append(ScrollingImage(bg_image, (64, 64), 6, screen, 15, 348))

    bg_image = load_sprites("Sprites\\Ground\\", "grass_1", None, ".png") 
    bg_pieces.append(ScrollingImage(bg_image, (48, 48), 6, screen, 15, 300))
    
    return bg_pieces