# Lib Imports
import pygame
from random import choice, randint

# Local Imports
from ...settings import (
    screen_width,
    screen_height,
    tile_size,
    horizon_point,
    clouds_num,
)
from ...support import import_folder
from ..tiles import StaticTile


class Clouds:
    def __init__(self, paths, world_width):
        # Setup
        self.display_surface = pygame.display.get_surface()
        self.clouds = import_folder(paths["decorations"]["animation"]["clouds"])

        self.far_left = -screen_width
        self.far_right = world_width + screen_width
        self.far_up = -screen_height
        self.far_down = horizon_point * tile_size

        # Loading assets
        self.cloud_sprites = self.create_tiles()

    def create_tiles(self):
        group = pygame.sprite.Group()

        for cloud in range(clouds_num):
            cloud = choice(self.clouds)

            x = randint(self.far_left, self.far_right)
            y = randint(self.far_up, self.far_down)

            sprite = StaticTile(x, y, cloud)
            group.add(sprite)

        return group

    def draw(self, shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(self.display_surface)
