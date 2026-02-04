# Imports
import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface((32, 64))
        self.image.fill("cyan")
        self.rect = self.image.get_rect(topleft=pos)

        # Movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_power = -16

        # Animation.
        self.assets_dir = "graphics/character/"
        self.animations = {"idle": [], "run": [], "jump": [], "fall": []}

        self.import_character_assets()

    def import_character_assets(self):
        for animation in self.animations.keys():
            full_path = self.assets_dir + animation

            self.animations[animation] = import_folder(full_path)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += int(self.direction.y)

    def jump(self):
        self.direction.y = self.jump_power

    def update(self):
        self.get_input()
