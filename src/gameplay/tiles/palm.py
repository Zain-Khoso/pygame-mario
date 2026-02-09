# Local Imports
from .animated_tile import AnimatedTile


class Palm(AnimatedTile):
    def __init__(self, x, y, paths, type):
        # Setup
        if type == "bg":
            path_frames = paths["terrain"]["animation"]["palm_bg"]
            y = y - 32
        elif type == "large":
            path_frames = paths["terrain"]["animation"]["palm_large"]
            y = y - 32
        else:
            path_frames = paths["terrain"]["animation"]["palm_small"]
            y = y - 24

        super().__init__(x, y, path_frames)

        self.rect = self.image.get_rect(topleft=(x, y))
