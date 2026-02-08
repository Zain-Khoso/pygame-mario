# Lib Imports
import pygame


class Hat(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.pos = pos
        self.image = pygame.image.load(
            "./assets/graphics/overworld/hat.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.rect.center = self.pos
