# Lib Imports
import sys, pygame

# Local Imports
from ..state import State
from ..settings import platforms

from .background import Background
from .platform import Platform
from .player_hat import Hat
from .stats import Stats


class Menu:
    def __init__(self, state: State, paths, show_gameplay):
        # Setup
        pygame.display.set_caption("Mario - Menu")
        self.display_surface = pygame.display.get_surface()
        self.state = state
        self.paths = paths
        self.show_gameplay = show_gameplay

        self.platforms = self.create_plateforms()
        self.background = Background(self.paths)
        self.hat = self.create_hat()
        self.stats = Stats(self.state, self.paths)

        # Input timer
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_length = 300

    def create_plateforms(self):
        group = pygame.sprite.Group()

        for index, position in enumerate(platforms):
            group.add(Platform(position, self.state, index, self.paths))

        return group

    def create_hat(self):
        group = pygame.sprite.GroupSingle()
        pos = self.platforms.sprites()[self.state.current_level].rect.center

        group.add(Hat(pos, self.state, self.paths, self.platforms))
        return group

    def draw_paths(self):
        if self.state.unlocked_levels == 0:
            return

        points = [
            position
            for index, position in enumerate(platforms)
            if index <= self.state.unlocked_levels
        ]
        pygame.draw.lines(self.display_surface, "#a04f45", False, points, 6)

    def handle_events(self, event):
        if not self.allow_input:
            if pygame.time.get_ticks() > (self.start_time + self.timer_length):
                self.allow_input = True

        if self.hat.sprite.moving or not self.allow_input:
            return

        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()
        elif (
            event.key == pygame.K_RIGHT
            and self.state.current_level < self.state.unlocked_levels
        ):
            self.hat.sprite.update_vector(1)
            self.state.change_level(1)
            self.hat.sprite.moving = True

        elif event.key == pygame.K_LEFT and self.state.current_level > 0:
            self.hat.sprite.update_vector(-1)
            self.state.change_level(-1)
            self.hat.sprite.moving = True

        elif event.key == pygame.K_SPACE:
            self.show_gameplay()

    def run(self):
        # Background
        self.background.draw()

        # Platform paths
        self.draw_paths()

        # Platforms
        self.platforms.update()
        self.platforms.draw(self.display_surface)

        # Hat: player indicator
        self.hat.update()
        self.hat.sprite.move()
        self.hat.draw(self.display_surface)

        # Stats
        self.stats.draw()
