# Imports
import pygame
from settings import tile_size, screen_height
from support import import_csv_data, import_cut_graphics

from tiles import Tile, StaticTile, Crate, Coin, Palm
from enemy import Enemy
from decoration import Sky, Water, Clouds

from player import Player
from particles import ParticleEffect


class Level:
    def __init__(self, data_path, surface):
        # World
        self.display_surface = surface
        self.world_shift = -2
        self.data_path = data_path
        self.level_width = 0

        # Level
        self.terrain = self.create_tile_group("terrain")
        self.grass = self.create_tile_group("grass")
        self.coins = self.create_tile_group("coins")
        self.crates = self.create_tile_group("crates")
        self.fg_palms = self.create_tile_group("fg palms")
        self.bg_palms = self.create_tile_group("bg palms")
        self.enemies = self.create_tile_group("enemies")
        self.constraints = self.create_tile_group("constraints")

        # Player
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.create_player()

        # Decorations
        self.sky = Sky(8)
        self.water = Water(screen_height - 48, self.level_width)
        self.clouds = Clouds(400, self.level_width, 20)

        self.current_player_x = 0
        self.player_on_ground = False

        # Particles
        self.dust_sprite = pygame.sprite.GroupSingle()

    def create_tile_group(self, type):
        group = pygame.sprite.Group()
        data = import_csv_data(self.data_path[type])
        cut_graphics = import_cut_graphics(type)

        for row_index, row in enumerate(data):
            for col_index, col in enumerate(row):
                if col == "-1":
                    continue

                x_pos = tile_size * col_index
                y_pos = tile_size * row_index

                if type == "terrain" or type == "grass":
                    surf = cut_graphics[int(col)]
                    tile = StaticTile(tile_size, x_pos, y_pos, surf)

                elif type == "crates":
                    tile = Crate(tile_size, x_pos, y_pos)

                elif type == "coins":
                    coin_type = "silver" if col == "1" else "gold"
                    tile = Coin(tile_size, x_pos, y_pos, coin_type)

                elif type == "fg palms":
                    palm_type = "small" if col == "0" else "large"
                    tile = Palm(tile_size, x_pos, y_pos, palm_type)

                elif type == "bg palms":
                    tile = Palm(tile_size, x_pos, y_pos, "bg")

                elif type == "enemies":
                    tile = Enemy(tile_size, x_pos, y_pos)

                elif type == "constraints":
                    tile = Tile(tile_size, x_pos, y_pos)

                else:
                    continue

                group.add(tile)

        self.level_width = len(data[0]) * tile_size
        return group

    def enemy_collisions(self):
        for enemy in self.enemies.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraints, False):
                enemy.reverse()

    def create_player(self):
        data = import_csv_data(self.data_path["player"])

        for row_index, row in enumerate(data):
            for col_index, col in enumerate(row):
                x_pos = tile_size * col_index
                y_pos = tile_size * row_index

                if col == "0":
                    print("player", x_pos, y_pos)
                    continue

                if col == "1":
                    hat_surface = pygame.image.load(
                        "./graphics/character/hat.png"
                    ).convert_alpha()

                    tile = StaticTile(tile_size, x_pos, y_pos, hat_surface)

                    self.goal.add(tile)

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
        # Decorations
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)
        self.water.draw(self.display_surface, self.world_shift)

        # Bg Palms
        self.bg_palms.update(self.world_shift)
        self.bg_palms.draw(self.display_surface)

        # Terrain
        self.terrain.update(self.world_shift)
        self.terrain.draw(self.display_surface)

        # Enemies
        self.enemies.update(self.world_shift)
        self.enemies.draw(self.display_surface)
        self.enemy_collisions()

        # Constraints
        self.constraints.update(self.world_shift)
        self.constraints.draw(self.display_surface)

        # Crates
        self.crates.update(self.world_shift)
        self.crates.draw(self.display_surface)

        # Grass
        self.grass.update(self.world_shift)
        self.grass.draw(self.display_surface)

        # Coins
        self.coins.update(self.world_shift)
        self.coins.draw(self.display_surface)

        # Fg Palms
        self.fg_palms.update(self.world_shift)
        self.fg_palms.draw(self.display_surface)

        # Goal
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # self.scroll_x()

        # # Player
        # self.player.update()
        # self.get_player_on_ground()
        # self.horizontal_movement_collision()
        # self.vertical_movement_collision()
        # self.create_landing_dust()
        # self.player.draw(self.display_surface)
        pass
