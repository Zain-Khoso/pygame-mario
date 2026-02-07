# Imports
import pygame
from game_data import levels

from support import import_folder


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, locked, icon_speed, path):
        super().__init__()

        # Animation
        self.frame = 0
        self.frame_speed = 0.15
        self.frames = import_folder(path)

        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect(center=pos)
        self.locked = locked

        detection_zone_x_pos = self.rect.centerx - (icon_speed / 2)
        detection_zone_y_pos = self.rect.centery - (icon_speed / 2)
        self.detection_zone = pygame.Rect(
            detection_zone_x_pos, detection_zone_y_pos, icon_speed, icon_speed
        )

    def animate(self):
        self.frame += self.frame_speed

        if self.frame >= len(self.frames):
            self.frame = 0

        self.image = self.frames[int(self.frame)]

    def update(self):
        if self.locked:
            tint_surf = self.image.copy()
            tint_surf.fill("black", None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surf, (0, 0))
        else:
            self.animate()


class Icon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.pos = pos
        self.image = pygame.image.load("./graphics/overworld/hat.png").convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.rect.center = self.pos


class Overworld:
    def __init__(self, start_level, max_level, screen, create_level):
        # Setup
        self.display_surface = screen
        self.max_level = max_level
        self.current_level = start_level
        self.create_level = create_level

        # Icon movement
        self.icon_vecter = pygame.Vector2(0, 0)
        self.icon_speed = 8
        self.icon_moving = False

        # Sprites
        self.nodes = self.create_nodes()
        self.icon = self.create_icon()

    def create_nodes(self):
        group = pygame.sprite.Group()

        for index, level_data in enumerate(levels.values()):
            pos = level_data["node_pos"]
            graphics = level_data["node_graphics"]
            locked = index > self.max_level

            group.add(Node(pos, locked, self.icon_speed, graphics))

        return group

    def draw_paths(self):
        points = [
            level_data["node_pos"]
            for index, level_data in enumerate(levels.values())
            if index <= self.max_level
        ]
        pygame.draw.lines(self.display_surface, "#a04f45", False, points, 6)

    def create_icon(self):
        group = pygame.sprite.GroupSingle()

        icon = Icon(self.nodes.sprites()[self.current_level].rect.center)
        group.add(icon)

        return group

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if self.icon_moving:
            return

        if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
            self.get_icon_vector(1)
            self.current_level += 1
            self.icon_moving = True

        elif keys[pygame.K_LEFT] and self.current_level > 0:
            self.get_icon_vector(-1)
            self.current_level -= 1
            self.icon_moving = True

        elif keys[pygame.K_SPACE]:
            self.create_level(self.current_level)

    def get_icon_vector(self, next):
        current_level_pos = self.nodes.sprites()[self.current_level].rect.center
        next_level_pos = self.nodes.sprites()[self.current_level + next].rect.center

        start_vector = pygame.math.Vector2(current_level_pos)
        end_vector = pygame.math.Vector2(next_level_pos)

        self.icon_vecter = (end_vector - start_vector).normalize()

    def update_icon_pos(self):
        if self.icon_moving and self.icon_vecter:
            self.icon.sprite.pos += self.icon_vecter * self.icon_speed
            target_node = self.nodes.sprites()[self.current_level]

            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.icon_moving = False
                self.icon_vecter = pygame.Vector2(0, 0)

    def run(self):
        self.handle_input()
        self.draw_paths()
        self.nodes.update()
        self.nodes.draw(self.display_surface)
        self.icon.update()
        self.icon.draw(self.display_surface)
        self.update_icon_pos()
