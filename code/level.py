# Imports
import pygame
from settings import *
from tile import Tile
from player import Player
from particles import ParticleEffect


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.world_shift = 0

        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        self.setup(level_data)

        self.current_player_x = 0
        self.player_on_ground = False

        self.dust_sprite = pygame.sprite.GroupSingle()

    def setup(self, layout):
        for row_index, row in enumerate(layout):
            for column_index, column in enumerate(row):
                x_pos = tile_size * column_index
                y_pos = tile_size * row_index

                if column == "P":
                    self.player.add(
                        Player(
                            (x_pos, y_pos),
                            self.display_surface,
                            self.create_jump_particles,
                        )
                    )

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
                    player.on_left = True
                    self.current_player_x = player.rect.left

                elif player.direction.x > 0:
                    player.rect.right = tile.rect.left
                    player.on_right = True
                    self.current_player_x = player.rect.right

        if player.on_left and (
            player.rect.left < self.current_player_x or player.direction.x >= 0
        ):
            player.on_left = False

        if player.on_right and (
            player.rect.right > self.current_player_x or player.direction.x <= 0
        ):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for tile in self.tiles.sprites():
            if tile.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = tile.rect.top
                    player.direction.y = 0
                    player.on_ground = True

                elif player.direction.y < 0:
                    player.rect.top = tile.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)

        self.dust_sprite.add(ParticleEffect(pos, "jump"))

    def get_player_on_ground(self):
        self.player_on_ground = self.player.sprite.on_ground

    def create_landing_dust(self):
        if (
            self.player_on_ground
            or not self.player.sprite.on_ground
            or self.dust_sprite.sprites()
        ):
            return

        if self.player.sprite.facing_right:
            offset = pygame.math.Vector2(10, 15)
        else:
            offset = pygame.math.Vector2(10, -15)

        particles = ParticleEffect(self.player.sprite.rect.midbottom - offset, "land")
        self.dust_sprite.add(particles)

    def draw(self):
        # Particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # Tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # Player
        self.player.update()
        self.get_player_on_ground()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.player.draw(self.display_surface)
