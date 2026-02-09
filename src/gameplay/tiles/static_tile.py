# Local Import
from .tile import Tile


class StaticTile(Tile):
    def __init__(self, x, y, graphic):
        super().__init__(x, y)
        self.image = graphic
