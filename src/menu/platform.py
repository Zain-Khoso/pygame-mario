# Lib Imports
import pygame

# Local Imports
from ..settings import player_hat_speed
from ..support import import_folder
from ..state import State


class Platform(pygame.sprite.Sprite):
    def __init__(self, pos, state: State, index: int, paths):
        super().__init__()

        # Setup
        self.position = pos
        self.state = state
        self.locked = index > self.state.unlocked_levels
        path = paths["menu"]["animation"][("level_%s" % str(index + 1))]

        # Animation
        self.frame = 0
        self.frame_speed = 0.15
        self.frames = import_folder(path)

        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect(center=pos)

        # Collision detection
        detection_zone_x_pos = self.rect.centerx - (player_hat_speed / 2)
        detection_zone_y_pos = self.rect.centery - (player_hat_speed / 2)
        self.detection_zone = pygame.Rect(
            detection_zone_x_pos,
            detection_zone_y_pos,
            player_hat_speed,
            player_hat_speed,
        )

    def animate(self):
        self.frame += self.frame_speed

        if self.frame >= len(self.frames):
            self.frame = 0

        self.image = self.frames[int(self.frame)]

    def update(self):
        if self.locked:
            tint_surf = self.image.copy()
            tint_surf.fill("black", None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surf, (0, 0))
        else:
            self.animate()
