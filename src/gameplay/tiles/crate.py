# Lib Imports
import pygame

# Local Imports
from ...settings import tile_size

from .static_tile import StaticTile


class Crate(StaticTile):
    def __init__(self, x, y, paths):

        # Setup
        path_graphic = paths["terrain"]["image"]["crate"]
        graphic = pygame.image.load(path_graphic).convert_alpha()

        super().__init__(x, y, graphic)

        # Position.
        offset_y = y + tile_size
        offset_x = x + (tile_size // 2)
        self.rect = self.image.get_rect(midbottom=(offset_x, offset_y))
