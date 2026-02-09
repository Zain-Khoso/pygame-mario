# Lib Imports
import pygame

# Local Imports
from ..settings import player_hat_speed
from ..state import State


class Hat(pygame.sprite.Sprite):
    def __init__(self, pos, state: State, paths, platforms):
        super().__init__()
        # Setup
        self.position = pos
        self.state = state
        self.platforms = platforms
        image_path = paths["character"]["image"]["hat"]

        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=self.position)

        # Movement
        self.vector = pygame.Vector2(0, 0)
        self.moving = False
        self.speed = player_hat_speed

    def update_vector(self, next):
        current_pos = self.platforms.sprites()[self.state.current_level].rect.center
        next_pos = self.platforms.sprites()[self.state.current_level + next].rect.center

        start_vector = pygame.math.Vector2(current_pos)
        end_vector = pygame.math.Vector2(next_pos)

        self.vector = (end_vector - start_vector).normalize()

    def move(self):
        if not self.moving or not self.vector:
            return

        self.position += self.vector * self.speed
        target_node = self.platforms.sprites()[self.state.current_level]

        if target_node.detection_zone.collidepoint(self.position):
            self.moving = False
            self.vector = pygame.Vector2(0, 0)

    def update(self):
        self.rect.center = self.position
