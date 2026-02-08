# Lib Imports
import pygame

# Local Imports
from ..game_data import levels
from ..decoration import Sky
from .level_platform import Platform
from .player_hat import Hat


class Overworld:
    def __init__(self, start_level, max_level, screen, create_level):
        # Setup
        self.display_surface = screen
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

        # Icon movement
        self.icon_vecter = pygame.Vector2(0, 0)
        self.icon_speed = 8
        self.icon_moving = False

        # Sprites
        self.nodes = self.create_nodes()
        self.icon = self.create_icon()
        self.sky = Sky(8, "overworld")

        # Input timer
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_length = 300

    def create_nodes(self):
        group = pygame.sprite.Group()

        for index, level_data in enumerate(levels.values()):
            pos = level_data["node_pos"]
            graphics = level_data["node_graphics"]
            locked = index > self.max_level

            group.add(Platform(pos, locked, self.icon_speed, graphics))

        return group

    def draw_paths(self):
        if self.max_level == 0:
            return

        points = [
            level_data["node_pos"]
            for index, level_data in enumerate(levels.values())
            if index <= self.max_level
        ]
        pygame.draw.lines(self.display_surface, "#a04f45", False, points, 6)

    def create_icon(self):
        group = pygame.sprite.GroupSingle()

        icon = Hat(self.nodes.sprites()[self.current_level].rect.center)
        group.add(icon)

        return group

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if self.icon_moving or not self.allow_input:
            return

        if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
            self.get_icon_vector(1)
            self.current_level += 1
            self.icon_moving = True

        elif keys[pygame.K_LEFT] and self.current_level > 0:
            self.get_icon_vector(-1)
            self.current_level -= 1
            self.icon_moving = True

        elif keys[pygame.K_SPACE]:
            self.create_level(self.current_level)

    def get_icon_vector(self, next):
        current_level_pos = self.nodes.sprites()[self.current_level].rect.center
        next_level_pos = self.nodes.sprites()[self.current_level + next].rect.center

        start_vector = pygame.math.Vector2(current_level_pos)
        end_vector = pygame.math.Vector2(next_level_pos)

        self.icon_vecter = (end_vector - start_vector).normalize()

    def update_icon_pos(self):
        if self.icon_moving and self.icon_vecter:
            self.icon.sprite.pos += self.icon_vecter * self.icon_speed
            target_node = self.nodes.sprites()[self.current_level]

            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.icon_moving = False
                self.icon_vecter = pygame.Vector2(0, 0)

    def input_timer(self):
        if self.allow_input:
            return

        current_time = pygame.time.get_ticks()

        if current_time <= (self.start_time + self.timer_length):
            return

        self.allow_input = True

    def run(self):
        self.sky.draw(self.display_surface)
        self.input_timer()
        self.handle_input()
        self.draw_paths()
        self.nodes.update()
        self.nodes.draw(self.display_surface)
        self.icon.update()
        self.icon.draw(self.display_surface)
        self.update_icon_pos()
