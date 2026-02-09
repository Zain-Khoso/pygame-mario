# Lib Imports
import pygame

# Local Imports
from ...settings import tile_size


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, x_shift):
        self.rect.x += x_shift
