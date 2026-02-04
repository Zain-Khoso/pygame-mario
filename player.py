# Imports
import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        # Loading assets.
        self.assets_dir = "graphics/character/"
        self.animations = {"idle": [], "run": [], "jump": [], "fall": []}
        self.import_character_assets()

        # Sprite
        self.frame = 0
        self.animation_speed = 0.15
        self.image = self.animations["idle"][self.frame]
        self.rect = self.image.get_rect(topleft=pos)

        # Movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_power = -16
        self.status = "idle"
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False

    def import_character_assets(self):
        for animation in self.animations.keys():
            full_path = self.assets_dir + animation

            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]
        self.frame += self.animation_speed

        if self.frame >= len(animation):
            self.frame = 0

        image = animation[int(self.frame)]
        self.image = (
            image if self.facing_right else pygame.transform.flip(image, True, False)
        )

        if self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center=self.rect.center)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > 1:
            self.status = "fall"
        else:
            if self.direction.x != 0:
                self.status = "run"
            else:
                self.status = "idle"

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += int(self.direction.y)

    def jump(self):
        self.direction.y = self.jump_power

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
