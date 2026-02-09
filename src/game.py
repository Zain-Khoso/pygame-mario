# Lib Imports
import sys, csv, pygame

# Local Imports
from .settings import *
from .menu import Menu
from .gameplay import Gameplay
from .state import State


class Game:
    def __init__(self):
        # Setup
        pygame.init()
        pygame.display.set_caption("Mario")
        self.display_surface = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        # Loading asset paths
        self.paths = {
            "audio": self.load_file_paths(csv_audio),
            "character": self.load_file_paths(csv_character),
            "coins": self.load_file_paths(csv_coins),
            "decorations": self.load_file_paths(csv_decorations),
            "enemy": self.load_file_paths(csv_enemy),
            "levels": self.load_file_paths(csv_levels),
            "menu": self.load_file_paths(csv_menu),
            "terrain": self.load_file_paths(csv_terrain),
            "ui": self.load_file_paths(csv_ui),
        }

        # Background music setup
        self.music_menu = pygame.mixer.Sound(self.paths["audio"]["music"]["menu"])
        self.music_menu.set_volume(0.1)
        self.music_gameplay = pygame.mixer.Sound(
            self.paths["audio"]["music"]["gameplay"]
        )
        self.music_gameplay.set_volume(0.1)

        # Game state
        self.state = State()
        self.state.load()

        # Game initialization
        self.show_menu()

    def load_file_paths(self, file_path):
        paths = {}

        with open(file_path, "r") as raw:
            file = csv.DictReader(raw)

            for line in file:
                path_type = line["type"]
                path_name = line["name"]

                try:
                    paths[path_type][path_name] = line["path"]
                except KeyError:
                    paths[path_type] = {}
                    paths[path_type][path_name] = line["path"]

        return paths

    def show_menu(self):
        self.menu = Menu(self.state, self.paths, self.show_gameplay)
        self.state.set_in_game(False)

        self.music_gameplay.stop()
        self.music_menu.play(-1)

    def show_gameplay(self):
        self.gameplay = Gameplay(self.state, self.paths, self.show_menu)
        self.state.set_in_game(True)

        self.music_menu.stop()
        self.music_gameplay.play(-1)

    def check_game_over(self):
        if self.state.current_health > 0:
            return

        print("run")
        self.state.reset()
        self.show_menu()

    def load_screen(self):
        if self.state.in_game:
            self.check_game_over()
            self.gameplay.draw()
        else:
            self.menu.run()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                try:
                    if self.state.in_game:
                        self.gameplay.handle_events(event)
                    else:
                        self.menu.handle_events(event)
                except AttributeError:
                    pass

    def run(self):
        while True:

            self.load_screen()
            self.handle_events()

            pygame.display.update()
            self.clock.tick(60)
