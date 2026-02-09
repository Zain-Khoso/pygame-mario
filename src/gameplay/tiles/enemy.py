# Imports
import pygame
from random import randint

# Local Imports
from ...settings import tile_size

from .animated_tile import AnimatedTile


class Enemy(AnimatedTile):
    def __init__(self, x, y, paths):
        # Setup
        path_graphics = paths["enemy"]["animation"]["run"]
        super().__init__(x, y, path_graphics)

        self.reward = 1

        # Offset
        offset_x = x + (tile_size // 2)
        offset_y = y + tile_size
        self.rect = self.image.get_rect(midbottom=(offset_x, offset_y))

        # Attributes
        self.speed = randint(3, 5)

    def movement(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse_movement(self):
        self.speed *= -1

    def update(self, x_shift):
        super().update(x_shift)

        self.movement()
        self.reverse_image()
