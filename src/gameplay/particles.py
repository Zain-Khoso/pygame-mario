# Imports
import pygame

# Local Imports
from ..support import import_folder


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, paths, type):
        super().__init__()

        # Setup
        if type == "jump":
            path_frames = paths["character"]["animation"]["dust_jump"]
        elif type == "land":
            path_frames = paths["character"]["animation"]["dust_land"]
        elif type == "explosion":
            path_frames = paths["enemy"]["animation"]["explosion"]
        else:
            return self.kill()

        # Animation
        self.frame = 0
        self.animation_speed = 0.5
        self.frames = import_folder(path_frames)

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
