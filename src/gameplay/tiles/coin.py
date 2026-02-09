# Local Imports
from .animated_tile import AnimatedTile

from ...settings import tile_size


class Coin(AnimatedTile):
    def __init__(self, x, y, paths, type):
        # Setup
        if type == "gold":
            value = 5
            path_frames = paths["coins"]["animation"]["gold"]
        else:
            value = 1
            path_frames = paths["coins"]["animation"]["silver"]

        super().__init__(x, y, path_frames)

        # Offset
        offset_x = x + (tile_size // 2)
        offset_y = y + (tile_size // 2)
        self.rect = self.image.get_rect(center=(offset_x, offset_y))

        self.value = value
