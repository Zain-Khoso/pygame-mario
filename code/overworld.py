# Imports
import pygame
from game_data import levels


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, is_locked):
        super().__init__()

        self.image = pygame.Surface((100, 80))
        self.image.fill("gray" if is_locked else "red")
        self.rect = self.image.get_rect(center=pos)


class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface((20, 20))
        self.image.fill("blue")
        self.rect = self.image.get_rect(center=pos)


class Overworld:
    def __init__(self, start_level, max_level, screen):
        # Setup
        self.display_surface = screen
        self.max_level = max_level
        self.current_level = start_level

        # Sprites
        self.nodes = self.create_nodes()
        self.icon = self.create_icon()

    def create_nodes(self):
        group = pygame.sprite.Group()

        for index, level_data in enumerate(levels.values()):
            group.add(Node(level_data["node_pos"], index > self.max_level))

        return group

    def draw_paths(self):
        points = [
            level_data["node_pos"]
            for index, level_data in enumerate(levels.values())
            if index <= self.max_level
        ]
        pygame.draw.lines(self.display_surface, "red", False, points, 6)

    def create_icon(self):
        group = pygame.sprite.GroupSingle()

        icon = Icon(self.nodes.sprites()[self.current_level].rect.center)
        group.add(icon)

        return group

    def run(self):
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
