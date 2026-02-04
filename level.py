# Imports
import pygame
from settings import *
from tile import Tile
from player import Player


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.world_shift = 0

        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        self.setup(level_data)

    def setup(self, layout):
        for row_index, row in enumerate(layout):
            for column_index, column in enumerate(row):
                x_pos = tile_size * column_index
                y_pos = tile_size * row_index

                if column == "P":
                    self.player.add(Player((x_pos, y_pos)))

                elif column == "X":
                    self.tiles.add(Tile((x_pos, y_pos), tile_size))
                else:
                    continue

    def draw(self):
        # Tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

        # Player
        self.player.draw(self.display_surface)
