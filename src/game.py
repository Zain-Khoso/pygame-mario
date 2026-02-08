# Lib Imports
import pygame, sys

# Local Imports
from .settings import *
from .overworld import Overworld
from .level import Level
from .ui import UI


class Game:
    def __init__(self):
        # Pygame setup
        pygame.init()
        pygame.display.set_caption("Mario")
        self.display_surface = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        # Loading assets
        self.overworld_music = pygame.mixer.Sound("./assets/audio/overworld_music.wav")
        self.overworld_music.set_volume(0.1)
        self.level_music = pygame.mixer.Sound("./assets/audio/level_music.wav")
        self.level_music.set_volume(0.1)

        # Game state
        self.max_level = 0
        self.max_health = 100
        self.current_health = 100
        self.coins = 0

        # Game initialization
        self.create_overworld(0, self.max_level)
        self.ui = UI(self.display_surface)

    def create_overworld(self, next_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level

        self.overworld = Overworld(
            next_level, self.max_level, self.display_surface, self.create_level
        )
        self.status = "overworld"
        self.level_music.stop()
        self.overworld_music.play(-1)

    def create_level(self, current_level):
        self.level = Level(
            current_level,
            self.display_surface,
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

    def load_screen(self):
        if self.status == "overworld":
            self.overworld.run()

        else:
            self.level.draw()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        while True:

            self.load_screen()
            self.handle_events()

            pygame.display.update()
            self.clock.tick(60)
