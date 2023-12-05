import pygame

from labirint_game_settings import *


class Sprite():

    def __init__(self, image):
        self.image = pygame.transform.scale(image, (TILE_SIZE * INCREASE, TILE_SIZE * INCREASE))
        self.positions = set()

    def set_position(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos

    def save_position(self):
        self.positions.add((self.x_pos, self.y_pos))

    def get_position(self):
        return self.x_pos, self.y_pos

    def get_positions(self):
        return self.positions

    def draw_sprite(self, screen):
        screen.blit(self.image, (self.x_pos, self.y_pos))


class Player(Sprite):

    def __init__(self, image, map):
        self.image = pygame.transform.scale(image, (TILE_SIZE * INCREASE, TILE_SIZE * INCREASE))
        self.player_pos = None
        for y, row in enumerate(map):
            for x, col in enumerate(row):
                if col == 3:
                    self.x_pos = x * TILE_SIZE * INCREASE
                    self.y_pos = y * TILE_SIZE * INCREASE

    def move(self, direction_x, direction_y, wall):
        old_pos = [self.x_pos, self.y_pos]
        self.x_pos += direction_x * TILE_SIZE * INCREASE
        self.y_pos += direction_y * TILE_SIZE * INCREASE
        if self.collide(wall):
            screen.blit(self.image, (self.x_pos, self.y_pos))
        else:
            self.x_pos, self.y_pos = old_pos


    def collide(self, object):
        obj_pos = object.get_positions()
        if obj_pos:
            pos = (self.x_pos, self.y_pos)
            if pos not in list(obj_pos):
                return True
        else:
            obj_pos = list(object.get_position())
            if self.x_pos == obj_pos[0] and self.y_pos == obj_pos[1]:
                return True


def draw_labyrinth(screen, map, wall_sprite, floor_sprite, finish_sprite, player_sprite):
    for y, row in enumerate(map):
        for x, col in enumerate(row):
            if col == 1:
                wall_sprite.set_position(x * TILE_SIZE * INCREASE, y * TILE_SIZE * INCREASE)
                wall_sprite.save_position()
                wall_sprite.draw_sprite(screen)
            elif col == 0:
                floor_sprite.set_position(x * TILE_SIZE * INCREASE, y * TILE_SIZE * INCREASE)
                floor_sprite.draw_sprite(screen)
            elif col == 2:
                finish_sprite.set_position(x * TILE_SIZE * INCREASE, y * TILE_SIZE * INCREASE)
                finish_sprite.draw_sprite(screen)
            elif col == 3:
                floor_sprite.set_position(x * TILE_SIZE * INCREASE, y * TILE_SIZE * INCREASE)
                floor_sprite.draw_sprite(screen)
    player_sprite.draw_sprite(screen)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

wall_surface = pygame.image.load("graphics/wall.png").convert()
wall = Sprite(wall_surface)

floor_surface = pygame.image.load("graphics/flor.png").convert()
floor = Sprite(floor_surface)

carpet_surface = pygame.image.load("graphics/carpet.png").convert()
carpet = Sprite(carpet_surface)

player_surface = pygame.image.load("graphics/skull.png").convert_alpha()
player = Player(player_surface, MAP)

font = pygame.font.Font("fonts/Minecraft Rus NEW.otf", 80)
text = font.render("You Win!", True, "#d2c9a5")

win = False

while True:

    draw_labyrinth(screen, MAP, wall, floor, carpet, player)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if not win:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    player.move(1, 0, wall)
                elif event.key == pygame.K_a:
                    player.move(-1, 0, wall)
                elif event.key == pygame.K_w:
                    player.move(0, -1, wall)
                elif event.key == pygame.K_s:
                    player.move(0, 1, wall)

    if player.collide(carpet):
        win = True
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = HEIGHT // 2 - text.get_height() // 2
        screen.blit(text, (text_x, text_y))
    pygame.display.update()
    clock.tick(FPS)