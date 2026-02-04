# Imports
import pygame
from tile import Tile
from settings import *


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.world_shift = 0

        self.setup(level_data)

    def setup(self, layout):
        self.tiles = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for column_index, column in enumerate(row):
                if column == " ":
                    continue

                elif column == "X":
                    x_pos = tile_size * column_index
                    y_pos = tile_size * row_index

                    self.tiles.add(Tile((x_pos, y_pos), tile_size))
                else:
                    continue

    def draw(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
