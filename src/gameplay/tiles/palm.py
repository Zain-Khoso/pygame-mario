# Local Imports
from ...settings import tile_size

from .animated_tile import AnimatedTile


class Palm(AnimatedTile):
    def __init__(self, x, y, paths, type):
        # Setup
        if type == "bg":
            path_frames = paths["terrain"]["animation"]["palm_bg"]
            y = y - (tile_size * 1.2)
        elif type == "large":
            path_frames = paths["terrain"]["animation"]["palm_large"]
            y = y - (tile_size * 1.2)
        else:
            path_frames = paths["terrain"]["animation"]["palm_small"]
            y = y - (tile_size * 0.5)

        super().__init__(x, y, path_frames)

        self.rect = self.image.get_rect(topleft=(x, y))
