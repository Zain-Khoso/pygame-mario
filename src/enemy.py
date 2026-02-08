# Imports
import pygame
from random import randint

from .game_data import animation_frames
from .tiles import AnimatedTile


class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        assets_path = animation_frames["enemies"]
        super().__init__(size, x, y, assets_path)

        # Offset
        offset_x = x + (size // 2)
        offset_y = y + size
        self.rect = self.image.get_rect(midbottom=(offset_x, offset_y))

        # Attributes
        self.speed = randint(2, 6)

    def movement(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, x_shift):
        super().update(x_shift)

        self.movement()
        self.reverse_image()
