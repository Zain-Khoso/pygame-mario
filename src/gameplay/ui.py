# Imports
import pygame

# Local Imports
from ..settings import (
    text_color,
    text_size,
    healthbar_color,
    healthbar_width,
    healthbar_height,
)
from ..state import State


class UI:
    def __init__(self, state: State, paths):
        # Setup
        self.display_surface = pygame.display.get_surface()
        self.state = state
        self.paths = paths

        # Loading assets
        path_healthbar = self.paths["ui"]["image"]["health_bar"]
        path_coin = self.paths["coins"]["image"]["silver"]
        path_font = self.paths["ui"]["font"]["arcade_pi"]
        path_star = self.paths["ui"]["image"]["star"]

        self.health_bar = pygame.image.load(path_healthbar).convert_alpha()
        self.coin = pygame.image.load(path_coin).convert_alpha()
        self.star = pygame.image.load(path_star).convert_alpha()
        self.font = pygame.font.Font(path_font, text_size)

        self.health_bar = pygame.transform.scale(
            self.health_bar, (healthbar_width, healthbar_height)
        )
        self.star = pygame.transform.scale(self.star, (32, 32))
        self.coin = pygame.transform.scale(self.coin, (32, 32))

        self.healthbar_rect = self.health_bar.get_rect(topleft=(32, 16))
        self.star_rect = self.star.get_rect(topleft=(64, 72))
        self.coin_rect = self.coin.get_rect(topleft=(64, 118))

    def show_health(self):
        bar_pos = (self.healthbar_rect.left + 34, self.healthbar_rect.left + 14)
        bar_width = self.healthbar_rect.width - 40
        bar_height = 3

        health_ratio = self.state.current_health / self.state.max_health
        bar_width = bar_width * health_ratio

        bar_rect = pygame.Rect(bar_pos, (bar_width, bar_height))

        self.display_surface.blit(self.health_bar, self.healthbar_rect)
        pygame.draw.rect(self.display_surface, healthbar_color, bar_rect)

    def show_points(self):
        amount = str(10)
        text_pos = (self.star_rect.right + 8, self.star_rect.centery + 4)

        text = self.font.render(amount, False, text_color)
        text_rect = text.get_rect(midleft=text_pos)

        self.display_surface.blit(self.star, self.star_rect)
        self.display_surface.blit(text, text_rect)

    def show_coins(self):
        amount = str(self.state.current_coins)
        text_pos = (self.coin_rect.right + 8, self.coin_rect.centery + 4)

        text = self.font.render(amount, False, text_color)
        text_rect = text.get_rect(midleft=text_pos)

        self.display_surface.blit(self.coin, self.coin_rect)
        self.display_surface.blit(text, text_rect)

    def draw(self):
        self.show_health()
        self.show_points()
        self.show_coins()
