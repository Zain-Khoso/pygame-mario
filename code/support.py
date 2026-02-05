# Imports
from os import walk
from csv import reader
import pygame

from settings import tile_size
from game_data import cut_graphics


# Use to import animation frames
def import_folder(path):
    surfaces = []

    for _, __, files in walk(path):
        for filename in files:
            surfaces.append(pygame.image.load(path + "/" + filename).convert_alpha())

    return surfaces


# Use to import tailed csv data.
def import_csv_data(path):
    terrain_map = []

    with open(path) as map:
        level = reader(map, delimiter=",")

        for row in level:
            terrain_map.append(list(row))

    return terrain_map


# Use to get graphics in a single png file.
def import_cut_graphics(type):
    cut_tiles = []

    try:
        graphic = cut_graphics[type]
    except KeyError:
        return []

    surf = pygame.image.load(graphic).convert_alpha()
    tile_num_x = int(surf.get_width() // tile_size)
    tile_num_y = int(surf.get_height() // tile_size)

    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size

            new_surf = pygame.Surface((tile_size, tile_size))
            new_surf.blit(surf, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles
