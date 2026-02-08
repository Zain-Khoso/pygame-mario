# Imports
import pygame


class UI:
    def __init__(self, surface):
        self.display_surface = surface

        self.health_bar = pygame.image.load(
            "./assets/graphics/ui/health_bar.png"
        ).convert_alpha()
        self.health_bar_top_left = (54, 39)
        self.health_max_width = 152
        self.health_bar_height = 4

        self.coin = pygame.image.load("./assets/graphics/ui/coin.png").convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft=(50, 61))

        self.font = pygame.font.Font("./assets/graphics/ui/ARCADEPI.TTF", 30)

    def show_health(self, current_health, full):
        health_ratio = current_health / full
        current_bar_width = self.health_max_width * health_ratio
        bar_rect = pygame.Rect(
            self.health_bar_top_left, (current_bar_width, self.health_bar_height)
        )

        self.display_surface.blit(self.health_bar, (20, 10))
        pygame.draw.rect(self.display_surface, "#dc4949", bar_rect)

    def show_coins(self, amount):
        text = self.font.render(str(amount), False, "#33323d")
        text_rect = text.get_rect(
            midleft=(self.coin_rect.centerx + 20, self.coin_rect.centery)
        )

        self.display_surface.blit(self.coin, self.coin_rect)
        self.display_surface.blit(text, text_rect)
