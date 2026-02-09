# Lib Imports
import pygame

# Local Imports
from ...settings import screen_width, tile_size, vertical_tile_number, horizon_point


class Sky:
    def __init__(self, paths):
        # Setup
        self.display_suface = pygame.display.get_surface()
        self.horizon = horizon_point

        # Loading assets
        path_top = paths["decorations"]["image"]["sky_top"]
        path_middle = paths["decorations"]["image"]["sky_middle"]
        path_bottom = paths["decorations"]["image"]["sky_bottom"]

        self.top = pygame.image.load(path_top).convert()
        self.middle = pygame.image.load(path_middle).convert()
        self.bottom = pygame.image.load(path_bottom).convert()

        # Editing assets
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))

    def draw(self):
        for row in range(vertical_tile_number):
            y = row * tile_size

            if row < self.horizon:
                self.display_suface.blit(self.top, (0, y))
            elif row == self.horizon:
                self.display_suface.blit(self.middle, (0, y))
            else:
                self.display_suface.blit(self.bottom, (0, y))
