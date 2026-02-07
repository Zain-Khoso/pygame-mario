# Imports.
import pygame, sys
from settings import *

from overworld import Overworld
from level import Level


class Game:
    def __init__(self):
        self.max_level = 2

        self.create_overworld(0, self.max_level)

    def create_overworld(self, next_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level

        self.overworld = Overworld(
            next_level, self.max_level, screen, self.create_level
        )
        self.status = "overworld"

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld)
        self.status = "level"

    def run(self):
        self.overworld.run() if self.status == "overworld" else self.level.draw()


# Pygame setup.
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()

# Game loop.
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("black")
    game.run()

    pygame.display.update()
    clock.tick(60)
