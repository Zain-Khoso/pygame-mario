# Lib Imports
import pygame

# Local Imports
from ...settings import tile_size, screen_width, screen_height
from ..tiles import AnimatedTile


class Ocean:
    def __init__(self, paths, world_width):
        # Setup
        self.display_surface = pygame.display.get_surface()
        self.path = paths["decorations"]["animation"]["ocean"]

        # Asset loading
        far_left = -screen_width
        far_right = world_width + screen_width
        self.water_tile_num = ((far_left * -1) + far_right) // tile_size

        self.water_sprites = self.create_tiles()

    def create_tiles(self):
        group = pygame.sprite.Group()

        for tile in range(self.water_tile_num):
            x = (tile * tile_size) - screen_width
            y = screen_height - tile_size

            tile = AnimatedTile(x, y, self.path)
            group.add(tile)

        return group

    def draw(self, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(self.display_surface)
