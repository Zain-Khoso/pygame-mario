# Imports
from os import walk
from csv import reader
import pygame

from .settings import tile_size


# Use to import animation frames
def import_folder(path):
    surfaces = []

    for _, __, files in walk(path):
        for filename in files:
            surfaces.append(pygame.image.load(path + filename).convert_alpha())

    return surfaces


# Use to import tailed csv data.
def import_layout_csv(dir_path, filename):
    layout = []

    with open(dir_path + filename + ".csv") as map:
        file = reader(map, delimiter=",")

        for row in file:
            layout.append(list(row))

    return layout


# Use to get graphics in a single png file.
def import_cut_graphics(path):
    tiles = []

    surf = pygame.image.load(path).convert_alpha()
    tile_num_x = surf.get_width() // tile_size
    tile_num_y = surf.get_height() // tile_size

    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size

            new_surf = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
            new_surf.blit(surf, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            tiles.append(new_surf)

    return tiles
