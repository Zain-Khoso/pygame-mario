# Imports.
import pygame, sys
from src.settings import *

from src.overworld import Overworld
from src.level import Level
from src.ui import UI


class Game:
    def __init__(self):
        self.max_level = 0
        self.max_health = 100
        self.current_health = 100
        self.coins = 0

        self.overworld_music = pygame.mixer.Sound("./assets/audio/overworld_music.wav")
        self.overworld_music.set_volume(0.1)
        self.level_music = pygame.mixer.Sound("./assets/audio/level_music.wav")
        self.level_music.set_volume(0.1)

        self.create_overworld(0, self.max_level)

        self.ui = UI(screen)

    def create_overworld(self, next_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level

        self.overworld = Overworld(
            next_level, self.max_level, screen, self.create_level
        )
        self.status = "overworld"
        self.level_music.stop()
        self.overworld_music.play(-1)

    def create_level(self, current_level):
        self.level = Level(
            current_level,
            screen,
            self.create_overworld,
            self.add_coins,
            self.change_health,
        )
        self.status = "level"
        self.overworld_music.stop()
        self.level_music.play(-1)

    def add_coins(self, amount):
        self.coins += amount

    def change_health(self, amount):
        self.current_health += amount

    def check_game_over(self):
        if self.current_health > 0:
            return

        self.max_level = 0
        self.current_health = 100
        self.coins = 0
        self.create_overworld(0, self.max_level)

    def run(self):
        if self.status == "overworld":
            self.overworld.run()

        else:
            self.level.draw()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()


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

    screen.fill("gray")
    game.run()

    pygame.display.update()
    clock.tick(60)
