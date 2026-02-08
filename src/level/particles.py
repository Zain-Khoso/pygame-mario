# Imports
import pygame

# Local Imports
from ..support import import_folder


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__()

        self.frame = 0
        self.animation_speed = 0.5

        if type == "jump":
            self.frames = import_folder(
                "./assets/graphics/character/dust_particles/jump/"
            )

        if type == "land":
            self.frames = import_folder(
                "./assets/graphics/character/dust_particles/land/"
            )

        if type == "explosion":
            self.frames = import_folder("./assets/graphics/enemy/explosion/")

        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame += self.animation_speed

        if self.frame >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame)]

    def update(self, x_shift):
        self.animate()
        self.rect.x += x_shift
