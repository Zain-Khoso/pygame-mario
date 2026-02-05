# Imports
from os import walk
from csv import reader
import pygame


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
