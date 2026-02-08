# Lib Imports
import pygame

# Local Imports
from ..state import State
from ..settings import platforms
from ..decoration import Sky

from .platform import Platform
from .player_hat import Hat


class Menu:
    def __init__(self, state: State, paths, show_gameplay):
        # Setup
        pygame.display.set_caption("Mario - Menu")
        self.display_surface = pygame.display.get_surface()
        self.state = state
        self.paths = paths
        self.show_gameplay = show_gameplay

        self.platforms = self.create_plateforms()
        # self.sky = Sky(8, "overworld")
        self.hat = self.create_hat()

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

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if self.hat.sprite.moving or not self.allow_input:
            return

        if (
            keys[pygame.K_RIGHT]
            and self.state.current_level < self.state.unlocked_levels
        ):
            self.hat.sprite.update_vector(1)
            self.state.change_level(1)
            self.hat.sprite.moving = True

        elif keys[pygame.K_LEFT] and self.state.current_level > 0:
            self.hat.sprite.update_vector(-1)
            self.state.change_level(-1)
            self.hat.sprite.moving = True

        elif keys[pygame.K_SPACE]:
            self.show_gameplay()

    def input_timer(self):
        if self.allow_input:
            return

        current_time = pygame.time.get_ticks()

        if current_time <= (self.start_time + self.timer_length):
            return

        self.allow_input = True

    def run(self):
        # self.sky.draw(self.display_surface)
        self.input_timer()
        self.handle_input()
        self.draw_paths()
        self.platforms.update()
        self.platforms.draw(self.display_surface)
        self.hat.update()
        self.hat.draw(self.display_surface)
        self.hat.sprite.move()
