# Imports
import pygame

# Local Imports
from ..settings import text_color, text_size
from ..state import State


class Stats:
    def __init__(self, state: State, paths):
        # Setup
        self.display_surface = pygame.display.get_surface()
        self.state = state
        self.paths = paths

        # Asset loading
        path_coin = self.paths["coins"]["image"]["silver"]
        path_font = self.paths["ui"]["font"]["arcade_pi"]
        path_star = self.paths["ui"]["image"]["star"]

        self.coin = pygame.image.load(path_coin).convert_alpha()
        self.star = pygame.image.load(path_star).convert_alpha()
        self.font = pygame.font.Font(path_font, text_size)

        self.coin = pygame.transform.scale(self.coin, (32, 32))
        self.star = pygame.transform.scale(self.star, (32, 32))

        self.coin_rect = self.coin.get_rect(topleft=(16, 16))
        self.star_rect = self.star.get_rect(topleft=(16, 64))

    def show_coins(self):
        amount = str(self.state.total_coins)
        x = self.coin_rect.centerx + 32
        y = self.coin_rect.centery + 4

        text = self.font.render(amount, False, text_color)
        text_rect = text.get_rect(midleft=(x, y))

        self.display_surface.blit(self.coin, self.coin_rect)
        self.display_surface.blit(text, text_rect)

    def show_points(self):
        amount = str(self.state.total_xp)
        x = self.star_rect.centerx + 32
        y = self.star_rect.centery + 4

        text = self.font.render(amount, False, text_color)
        text_rect = text.get_rect(midleft=(x, y))

        self.display_surface.blit(self.star, self.star_rect)
        self.display_surface.blit(text, text_rect)

    def draw(self):
        self.show_coins()
        self.show_points()
