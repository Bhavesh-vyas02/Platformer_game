import pygame
from pygame.locals import *
import os

pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the game window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platformer")

# Load images
dirt_img = pygame.image.load("/img/dirt.png").convert_alpha()
grass_img = pygame.image.load("/img/grass.png").convert_alpha()

# Colors
white = (255, 255, 255)

# Clock
clock = pygame.time.Clock()
fps = 60


class World:
    def __init__(self, data):
        self.tile_list = []
        
        # Define images for tiles
        self.dirt = dirt_img
        self.grass = grass_img

        # Loop through rows and columns in the data
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:  # Dirt
                    img = pygame.transform.scale(self.dirt, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:  # Grass
                    img = pygame.transform.scale(self.grass, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load("player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False

    def update(self):
        dx = 0
        dy = 0

        # Movement
        key = pygame.key.get_pressed()
        if key[K_LEFT]:
            dx -= 5
        if key[K_RIGHT]:
            dx += 5
        if key[K_SPACE] and not self.jumped:
            self.vel_y = -15
            self.jumped = True

        # Gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Collision with ground
        if self.rect.bottom + dy > screen_height:
            dy = screen_height - self.rect.bottom
            self.jumped = False

        # Update player position
        self.rect.x += dx
        self.rect.y += dy

        # Draw player
        screen.blit(self.image, self.rect)


# Tile size
tile_size = 50

# Define a world layout (1 = dirt, 2 = grass)
world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]
]

# Create world and player objects
world = World(world_data)
player = Player(100, screen_height - 130)

# Main game loop
running = True
while running:
    clock.tick(fps)
    screen.fill(white)

    # Draw world
    world.draw()

    # Update and draw player
    player.update()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
