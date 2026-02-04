# Imports
from os import walk
import pygame


def import_folder(path):
    surfaces = []

    for _, __, files in walk(path):
        for filename in files:
            surfaces.append(pygame.image.load(path + "/" + filename).convert_alpha())

    return surfaces
