# Lib Imports
import pygame
from random import choice, randint

# Local Imports
from ..settings import vertical_tile_number, tile_size, screen_width
from ..support import import_folder


class Background:
    def __init__(self, paths):
        # Setup
        self.display_surface = pygame.display.get_surface()
        self.horizon = 8

        # Loading assets
        path_sky_top = paths["decorations"]["image"]["sky_top"]
        path_sky_middle = paths["decorations"]["image"]["sky_middle"]
        path_sky_bottom = paths["decorations"]["image"]["sky_bottom"]
        path_palms = paths["menu"]["animation"]["palms"]
        path_clouds = paths["menu"]["animation"]["clouds"]

        self.top = pygame.image.load(path_sky_top).convert()
        self.middle = pygame.image.load(path_sky_middle).convert()
        self.bottom = pygame.image.load(path_sky_bottom).convert()
        palm_surfaces = [choice(import_folder(path_palms)) for _ in range(10)]
        cloud_surfaces = [choice(import_folder(path_clouds)) for _ in range(10)]
        self.decorations = []

        # Asset editing
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))

        for palm in palm_surfaces:
            x = randint(0, screen_width)
            y = (self.horizon * tile_size) - randint(0, 50)
            rect = palm.get_rect(topleft=(x, y))
            self.decorations.append((palm, rect))

        for cloud in cloud_surfaces:
            x = randint(0, screen_width)
            y = randint(0, (self.horizon * tile_size) - 100)
            rect = cloud.get_rect(midbottom=(x, y))
            self.decorations.append((cloud, rect))

    def draw(self):
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horizon:
                self.display_surface.blit(self.top, (0, y))
            elif row == self.horizon:
                self.display_surface.blit(self.middle, (0, y))
            else:
                self.display_surface.blit(self.bottom, (0, y))

        for surface in self.decorations:
            self.display_surface.blit(surface[0], surface[1])
