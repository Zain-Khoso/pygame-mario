# Local Imports
from ...support import import_folder

from .tile import Tile


class AnimatedTile(Tile):
    def __init__(self, x, y, path):
        super().__init__(x, y)

        # Animation
        self.frame = 0
        self.frame_speed = 0.15
        self.frames = import_folder(path)

        self.image = self.frames[self.frame]

    def animate(self):
        self.frame += self.frame_speed

        if self.frame >= len(self.frames):
            self.frame = 0

        self.image = self.frames[int(self.frame)]

    def update(self, x_shift):
        super().update(x_shift)

        self.animate()
