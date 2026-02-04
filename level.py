# Imports
import pygame
from settings import *
from tile import Tile
from player import Player


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.world_shift = 0

        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        self.setup(level_data)

    def setup(self, layout):
        for row_index, row in enumerate(layout):
            for column_index, column in enumerate(row):
                x_pos = tile_size * column_index
                y_pos = tile_size * row_index

                if column == "P":
                    self.player.add(Player((x_pos, y_pos)))

                elif column == "X":
                    self.tiles.add(Tile((x_pos, y_pos), tile_size))
                else:
                    continue

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        left_border = (screen_width // 100) * 20
        right_border = (screen_width // 100) * 80

        if player_x < left_border and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > right_border and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite

        player.rect.x += int(player.direction.x) * player.speed

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = tile.rect.right
                elif player.direction.x > 0:
                    player.rect.right = tile.rect.left

    def draw(self):
        # Tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # Player
        self.player.update()
        self.horizontal_movement_collision()
        self.player.draw(self.display_surface)
