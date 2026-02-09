# Imports
import pygame

# Local Imports
from ..settings import text_color
from ..state import State


class UI:
    def __init__(self, state: State, paths):
        # Setup
        self.display_surface = pygame.display.get_surface()
        self.state = state
        self.paths = paths

        self.health_bar = pygame.image.load(
            self.paths["ui"]["image"]["health_bar"]
        ).convert_alpha()
        self.health_bar_top_left = (54, 39)
        self.health_max_width = 152
        self.health_bar_height = 4

        self.coin = pygame.image.load(
            self.paths["coins"]["image"]["silver"]
        ).convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft=(50, 61))

        self.font = pygame.font.Font(self.paths["ui"]["font"]["arcade_pi"], 30)

    def show_health(self):
        health_ratio = self.state.current_health / self.state.max_health
        current_bar_width = self.health_max_width * health_ratio
        bar_rect = pygame.Rect(
            self.health_bar_top_left, (current_bar_width, self.health_bar_height)
        )

        self.display_surface.blit(self.health_bar, (20, 10))
        pygame.draw.rect(self.display_surface, "#dc4949", bar_rect)

    def show_coins(self):
        amount = str(self.state.current_coins)
        text = self.font.render(amount, False, text_color)
        text_rect = text.get_rect(
            midleft=(self.coin_rect.centerx + 20, self.coin_rect.centery)
        )

        self.display_surface.blit(self.coin, self.coin_rect)
        self.display_surface.blit(text, text_rect)
