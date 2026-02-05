# Imports.
import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()

        self.image = pygame.Surface((size, size))
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
        offet_y = y + size
        offet_x = x + (size // 2)
        self.rect = self.image.get_rect(midbottom=(offet_x, offet_y))
