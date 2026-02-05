# Imports.
import pygame

from game_data import animation_frames
from support import import_folder


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()

        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, x_shift):
        self.rect.x += x_shift


class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface


class Crate(StaticTile):
    def __init__(self, size, x, y):

        image = pygame.image.load("./graphics/terrain/crate.png").convert_alpha()
        super().__init__(size, x, y, image)

        # Position.
        offset_y = y + size
        offset_x = x + (size // 2)
        self.rect = self.image.get_rect(midbottom=(offset_x, offset_y))


class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)

        # Animation
        self.frame = 0
        self.frame_speed = 0.15
        self.frames = import_folder(path)

        self.image = self.frames[self.frame]

    def animate(self):
        self.frame += self.frame_speed

        if self.frame >= len(self.frames):
            self.frame = 0

        self.image = self.frames[int(self.frame)]

    def update(self, x_shift):
        super().update(x_shift)

        self.animate()


class Coin(AnimatedTile):
    def __init__(self, size, x, y, type):
        frames_path = animation_frames["coins"][type]
        super().__init__(size, x, y, frames_path)

        # Offset
        offset_x = x + (size // 2)
        offset_y = y + (size // 2)
        self.rect = self.image.get_rect(center=(offset_x, offset_y))


class Palm(AnimatedTile):
    def __init__(self, size, x, y, type):
        frames_path = animation_frames["palms"][type]
        super().__init__(size, x, y, frames_path)

        # Offset
        offset_y = y - (32 if type == "small" else 24)
        self.rect = self.image.get_rect(topleft=(x, offset_y))
