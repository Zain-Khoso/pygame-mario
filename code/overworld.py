# Imports
import pygame
from game_data import levels


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, is_locked, icon_speed):
        super().__init__()

        self.image = pygame.Surface((100, 80))
        self.image.fill("gray" if is_locked else "red")
        self.rect = self.image.get_rect(center=pos)

        detection_zone_x_pos = self.rect.centerx - (icon_speed / 2)
        detection_zone_y_pos = self.rect.centery - (icon_speed / 2)
        self.detection_zone = pygame.Rect(
            detection_zone_x_pos, detection_zone_y_pos, icon_speed, icon_speed
        )


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
            node = Node(level_data["node_pos"], index > self.max_level, self.icon_speed)
            group.add(node)

        return group

    def draw_paths(self):
        points = [
            level_data["node_pos"]
            for index, level_data in enumerate(levels.values())
            if index <= self.max_level
        ]
        pygame.draw.lines(self.display_surface, "red", False, points, 6)

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
        self.nodes.draw(self.display_surface)
        self.icon.update()
        self.icon.draw(self.display_surface)
        self.update_icon_pos()
