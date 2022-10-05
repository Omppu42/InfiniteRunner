import pygame, random
pygame.init()

class ScrollingImage:
    def __init__(self, bg_image: pygame.image, size: tuple, scroll_speed: float, screen, image_count: int, y: int, alpha=255, darkness=0):
        self.bg_array_bool: bool = False
        if (isinstance(bg_image, list)):
            self.bg_array_bool = True
            self.bg_image = self.process_image_arr(bg_image, size, alpha, darkness)
        else:
            self.process_image(bg_image, size, alpha, darkness)

        self.x_pos = 0
        self.y = y
        self.size_w = size[0]
        self.size_h = size[1]
        self.scroll_speed = scroll_speed
        self.screen = screen
        self.image_count = image_count
        self.images = []
        self.to_remove = [] #images to remove

        for i in range(image_count):
            self.append_bgpiece((self.size_w)*i, self.y)

    def process_image_arr(self, image_arr, size, alpha, darkness):
        output = []
        for x in image_arr:
            x = pygame.transform.scale(x, size).convert_alpha()
            x.set_alpha(alpha)
            x.fill((darkness,darkness,darkness), special_flags=pygame.BLEND_RGB_SUB)
            output.append(x)
        
        return output

    def process_image(self, image, size, alpha, darkness):
        self.bg_image = pygame.transform.scale(image, size).convert_alpha()
        self.bg_image.set_alpha(alpha)
        self.bg_image.fill((darkness,darkness,darkness), special_flags=pygame.BLEND_RGB_SUB)

    def restart(self):
        for i, x in enumerate(self.images):
            x.x = self.size_w*i

    def append_bgpiece(self, x, y):
        self.images.append(BGPiece(self.bg_image, self.scroll_speed, x, y, self.bg_array_bool))

    def draw(self):
        for x in self.images:
            self.screen.blit(x.image, (x.x, x.y))

    def update(self):
        for x in self.images:
            if x.x < -(self.size_w+50):
                self.to_remove.append(x)
    
            x.move()

        for x in self.to_remove:
            self.images.remove(x)
            self.to_remove.remove(x)
            self.append_bgpiece(self.images[len(self.images)-1].x+self.size_w, self.y) #append new one behind last


class BGPiece:
    def __init__(self, image, speed, start_x, y, randomize):
        if randomize:
            self.image = image[random.randint(0, len(image)-1)]
        else:
            self.image = image
        self.speed = speed
        self.x = start_x
        self.y = y
    
    def move(self):
        self.x -= self.speed