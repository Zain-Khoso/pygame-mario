# Lib Imports
import pygame

# Local Imports
from ..state import State
from ..support import import_layout_csv, import_cut_graphics
from ..settings import tile_size, screen_width, screen_height

from .tiles import Tile, StaticTile, Crate, Coin, Palm
from .decorations import Sky, Ocean, Clouds
from .particles import ParticleEffect
from .player import Player
from .tiles.enemy import Enemy
from .ui import UI


class Gameplay:
    def __init__(self, state: State, paths, show_menu):
        # Setup
        pygame.display.set_caption("Mario - Game")
        self.display_surface = pygame.display.get_surface()
        self.state = state
        self.paths = paths
        self.show_menu = show_menu

        self.world_layout = self.paths["levels"]["level"][str(self.state.current_level)]
        self.world_shift = 0
        self.world_width = 0

        # Level loading
        self.terrain = self.create_tile_group("terrain")
        self.grass = self.create_tile_group("grass")
        self.coins = self.create_tile_group("coins")
        self.crates = self.create_tile_group("crates")
        self.fg_palms = self.create_tile_group("fg_palms")
        self.bg_palms = self.create_tile_group("bg_palms")
        self.enemies = self.create_tile_group("enemies")
        self.constraints = self.create_tile_group("constraints")

        # Player loading
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.create_player_and_goal()

        self.current_player_x = 0
        self.player_on_ground = False

        # Particles
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.explosions = pygame.sprite.Group()

        # Decorations
        self.sky = Sky(self.paths)
        self.clouds = Clouds(self.paths, self.world_width)
        self.ocean = Ocean(self.paths, self.world_width)
        self.ui = UI(self.state, self.paths)

        # Audio
        self.coin_sound = pygame.mixer.Sound(self.paths["audio"]["effect"]["coin"])
        self.coin_sound.set_volume(0.4)
        self.stomp_sound = pygame.mixer.Sound(self.paths["audio"]["effect"]["stomp"])
        self.stomp_sound.set_volume(0.4)

    def create_tile_group(self, type):
        group = pygame.sprite.Group()
        layout = import_layout_csv(self.world_layout, type)

        try:
            cut_graphics = import_cut_graphics(self.paths["terrain"]["image"][type])
        except KeyError:
            cut_graphics = []

        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col == "-1":
                    continue

                x_pos = tile_size * col_index
                y_pos = tile_size * row_index

                if type == "terrain" or type == "grass":
                    graphic = cut_graphics[int(col)]
                    tile = StaticTile(x_pos, y_pos, graphic)

                elif type == "crates":
                    tile = Crate(x_pos, y_pos, self.paths)

                elif type == "coins":
                    coin_type = "silver" if col == "1" else "gold"
                    tile = Coin(x_pos, y_pos, self.paths, coin_type)

                elif type == "fg_palms":
                    palm_type = "large" if col == "1" else "small"
                    tile = Palm(x_pos, y_pos, self.paths, palm_type)

                elif type == "bg_palms":
                    tile = Palm(x_pos, y_pos, self.paths, "bg")

                elif type == "enemies":
                    tile = Enemy(x_pos, y_pos, self.paths)

                elif type == "constraints":
                    tile = Tile(x_pos, y_pos)

                else:
                    continue

                group.add(tile)

        self.world_width = len(layout[0]) * tile_size
        return group

    def create_player_and_goal(self):
        layout = import_layout_csv(self.world_layout, "player")

        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x_pos = tile_size * col_index
                y_pos = tile_size * row_index

                if col == "0":
                    player = Player(
                        (x_pos, y_pos),
                        self.state,
                        self.paths,
                        self.create_jump_particles,
                    )
                    self.player.add(player)

                if col == "1":
                    graphic = pygame.image.load(
                        self.paths["character"]["image"]["hat"]
                    ).convert_alpha()

                    tile = StaticTile(x_pos, y_pos, graphic)

                    self.goal.add(tile)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        left_border = screen_width * 0.4
        right_border = screen_width * 0.6

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
        player.collision_rect.x += int(player.direction.x) * player.speed

        tiles = self.terrain.sprites() + self.crates.sprites() + self.fg_palms.sprites()

        for tile in tiles:
            if tile.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = tile.rect.right
                    player.on_left = True
                    self.current_player_x = player.collision_rect.left

                elif player.direction.x > 0:
                    player.collision_rect.right = tile.rect.left
                    player.on_right = True
                    self.current_player_x = player.collision_rect.right

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        tiles = self.terrain.sprites() + self.crates.sprites() + self.fg_palms.sprites()

        for tile in tiles:
            if tile.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = tile.rect.top
                    player.direction.y = 0
                    player.on_ground = True

                elif player.direction.y < 0:
                    player.collision_rect.top = tile.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)

        self.dust_sprite.add(ParticleEffect(pos, self.paths, "jump"))

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

        pos = self.player.sprite.rect.midbottom - offset
        particles = ParticleEffect(pos, self.paths, "land")

        self.dust_sprite.add(particles)

    def check_death(self):
        if self.player.sprite.rect.top <= screen_height:
            return

        self.show_menu()
        self.state.reset()
        self.state.save()

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, True):
            self.state.unlock_level()
            self.state.save_coins()
            self.state.save()
            self.state.reset_for_level()
            self.show_menu()

    def enemy_collisions(self):
        for enemy in self.enemies.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraints, False):
                enemy.reverse_movement()

        player_collisions = pygame.sprite.spritecollide(
            self.player.sprite, self.enemies, False
        )

        for enemy in player_collisions:
            enemy_center = enemy.rect.centery
            enemy_top = enemy.rect.top
            player_bottom = self.player.sprite.rect.bottom

            if (
                enemy_top < player_bottom < enemy_center
                and self.player.sprite.direction.y >= 0
            ):
                self.player.sprite.jump()
                self.explosions.add(
                    ParticleEffect(enemy.rect.center, self.paths, "explosion")
                )
                self.stomp_sound.play()
                enemy.kill()
            else:
                self.player.sprite.get_damage()

    def coin_collisions(self):
        collisions = pygame.sprite.spritecollide(self.player.sprite, self.coins, True)

        for coin in collisions:
            self.coin_sound.play()
            self.state.add_coin(coin)

    def handle_events(self, event):
        if event.key == pygame.K_ESCAPE:
            self.state.reset_for_level()
            self.show_menu()

    def draw(self):
        self.scroll_x()

        # Decorations
        self.sky.draw()
        self.clouds.draw(self.world_shift)

        # Particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

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
        self.explosions.update(self.world_shift)
        self.explosions.draw(self.display_surface)

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
        self.coin_collisions()

        # Fg Palms
        self.fg_palms.update(self.world_shift)
        self.fg_palms.draw(self.display_surface)

        # Goal
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # Player
        self.player.update()
        self.get_player_on_ground()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.player.draw(self.display_surface)

        # Ocean
        self.ocean.draw(self.world_shift)

        # UI
        self.ui.show_health()
        self.ui.show_coins()

        # Player functionality
        self.check_death()
        self.check_win()
