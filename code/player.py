# Imports
import pygame
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles):
        super().__init__()
        self.display_surface = surface

        # Loading assets.
        self.animations_dir = "graphics/character/"
        self.dust_particles_dir = "graphics/character/dust_particles/run/"

        self.animations = {"idle": [], "run": [], "jump": [], "fall": []}
        self.dust_particles = import_folder(self.dust_particles_dir)

        self.import_character_assets()

        # Sprite
        self.frame = 0
        self.dust_frame = 0
        self.animation_speed = 0.15
        self.dust_animation_speed = 0.15
        self.image = self.animations["idle"][self.frame]
        self.rect = self.image.get_rect(topleft=pos)
        self.create_jump_particles = create_jump_particles

        # Movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_power = -16
        self.status = "idle"
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_right = False
        self.on_left = False

    def import_character_assets(self):
        for animation in self.animations.keys():
            full_path = self.animations_dir + animation

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

        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center=self.rect.center)

    def animate_particles(self):
        if not self.on_ground or self.status != "run":
            return

        self.dust_frame += self.dust_animation_speed

        if self.dust_frame >= len(self.dust_particles):
            self.dust_frame = 0

        particle = self.dust_particles[int(self.dust_frame)]

        if self.facing_right:
            pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
            self.display_surface.blit(particle, pos)
        else:
            pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
            self.display_surface.blit(pygame.transform.flip(particle, True, False), pos)

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
            self.create_jump_particles(self.rect.midbottom)

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
        self.animate_particles()
