# Lib Imports
import sys, csv, pygame

# Local Imports
from .settings import screen_width, screen_height, csv_audio
from .overworld import Overworld
from .level import Level
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
        self.audio_paths = self.load_file_paths(csv_audio)

        # Background music setup
        self.overworld_music = pygame.mixer.Sound(
            self.audio_paths["music"]["overworld"]
        )
        self.overworld_music.set_volume(0.1)
        self.level_music = pygame.mixer.Sound(self.audio_paths["music"]["level"])
        self.level_music.set_volume(0.1)

        # Game state
        self.game_state = State()
        self.game_state.load()

        # Game initialization
        self.create_overworld()
        self.ui = UI(self.game_state)

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

    def create_overworld(self):
        self.overworld = Overworld(self.game_state, self.create_level)
        self.game_state.set_in_game(False)

        self.level_music.stop()
        self.overworld_music.play(-1)

    def create_level(self):
        self.level = Level(self.game_state, self.audio_paths, self.create_overworld)
        self.game_state.set_in_game(True)

        self.overworld_music.stop()
        self.level_music.play(-1)

    def check_game_over(self):
        if self.game_state.current_health > 0:
            return

        self.game_state.reset()
        self.create_overworld()

    def load_screen(self):
        if self.game_state.in_game:
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
