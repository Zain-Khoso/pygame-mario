# Lib Imports
import sys, csv, pygame

# Local Imports
from .settings import *
from .menu import Menu
from .gameplay import Gameplay
from .state import State
from .ui import UI


class Game:
    def __init__(self):
        # Setup
        pygame.init()
        pygame.display.set_caption("Mario")
        self.display_surface = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()

        # Loading asset paths
        self.paths_audio = self.load_file_paths(csv_audio)
        self.paths_character = self.load_file_paths(csv_character)
        self.paths_coins = self.load_file_paths(csv_coins)
        self.paths_decorations = self.load_file_paths(csv_decorations)
        self.paths_enemy = self.load_file_paths(csv_enemy)
        self.paths_levels = self.load_file_paths(csv_levels)
        self.paths_menu = self.load_file_paths(csv_menu)
        self.paths_terrain = self.load_file_paths(csv_terrain)
        self.paths_ui = self.load_file_paths(csv_ui)

        # Background music setup
        self.music_menu = pygame.mixer.Sound(self.paths_audio["music"]["overworld"])
        self.music_menu.set_volume(0.1)
        self.music_gameplay = pygame.mixer.Sound(self.paths_audio["music"]["level"])
        self.music_gameplay.set_volume(0.1)

        # Game state
        self.state = State()
        self.state.load()

        # Game initialization
        self.show_menu()
        self.ui = UI(self.state)

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
        self.overworld = Menu(self.state, self.show_gameplay)
        self.state.set_in_game(False)

        self.music_gameplay.stop()
        self.music_menu.play(-1)

    def show_gameplay(self):
        self.level = Gameplay(self.state, self.paths_audio, self.show_menu)
        self.state.set_in_game(True)

        self.music_menu.stop()
        self.music_gameplay.play(-1)

    def check_game_over(self):
        if self.state.current_health > 0:
            return

        self.state.reset()
        self.show_menu()

    def load_screen(self):
        if self.state.in_game:
            self.level.draw()
            self.ui.show_health()
            self.ui.show_coins()
            self.check_game_over()
        else:
            self.overworld.run()

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
