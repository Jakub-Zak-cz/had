# Snake the video game coded with Python using Pygame
# 
# Author: Jakub Zak
# Collaborators: Jakub Senkyr
#
# Version: 1.0
# Adding Pygame
import sys
import pygame
import random

pygame.init()

window_resolution = (800, 600)
cell_size = 40  # Size of each cell on the chessboard

window = pygame.display.set_mode(window_resolution)

# Music
# Initialize mixer for music
pygame.mixer.init()

# Load music
pygame.mixer.music.load("src/assets/Kevin MacLeod - Pixelland.mp3")
# Set music repetition to infinite (you can change it as needed)
pygame.mixer.music.play(-1)

class Food:
    def __init__(self):
        self.image = pygame.image.load("src/assets/food.png")  # Our food image
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))  # Adjust image size
        self.position = (0, 0)
        self.is_food_on_screen = False
        self.spawn_food()

    def spawn_food(self):
        self.position = (random.randint(0, (window_resolution[0] // cell_size) - 1) * cell_size, 
                         random.randint(0, (window_resolution[1] // cell_size) - 1) * cell_size)
        self.is_food_on_screen = True

    def render(self, surface):
        surface.blit(self.image, self.position)


class Snake:
    def __init__(self):
        self.head_image = pygame.image.load("src/assets/head.png")  # Our snake head image
        self.head_image = pygame.transform.scale(self.head_image, (cell_size, cell_size))  # Adjust image size
        self.length = 1
        self.positions = [((window_resolution[0] // 2), (window_resolution[1] // 2))]
        self.direction = (1, 0)
        self.speed = cell_size

    def get_head_position(self):
        return self.positions[0]
    
    def eat(self, food):
        head_position = self.get_head_position()
        if (
            head_position[0] < food.position[0] + cell_size and
            head_position[0] + cell_size > food.position[0] and
            head_position[1] < food.position[1] + cell_size and
            head_position[1] + cell_size > food.position[1]
        ):
            self.length += 1
            food.spawn_food()
            food.is_food_on_screen = False

    def update(self, food):
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + x * self.speed, cur[1] + y * self.speed)
        
        # Implementation of "teleportation" to the other side when hitting the edge
        new = (new[0] % window_resolution[0], new[1] % window_resolution[1])
        
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset(food)
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

        self.check_collision(food)
        self.eat(food)

    def check_collision(self, food):
        if self.get_head_position() in self.positions[1:]:
            self.reset(food)          
    
    def reset(self, food):
        self.length = 1
        self.positions = [((window_resolution[0] // 2), (window_resolution[1] // 2))]
        self.direction = (1, 0)
        food.spawn_food()

    def render(self, surface):
        for idx, p in enumerate(self.positions):
            if idx == 0:
                surface.blit(self.head_image, p)
            else:
                color = (0, 0, 255)  # Snake body color
                pygame.draw.rect(surface, color, (p[0], p[1], cell_size, cell_size))


# Create instances of snake and food
snake = Snake()
food = Food()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            sys.exit()

    keyword_pressed = pygame.key.get_pressed()

    # Change snake direction
    if keyword_pressed[pygame.K_UP]:
        snake.direction = (0, -1)
    elif keyword_pressed[pygame.K_DOWN]:
        snake.direction = (0, 1)
    elif keyword_pressed[pygame.K_LEFT]:
        snake.direction = (-1, 0)
    elif keyword_pressed[pygame.K_RIGHT]:
        snake.direction = (1, 0)

    window.fill((255, 255, 255))

    # Draw chessboard
    for i in range(0, window_resolution[0], cell_size):
        for j in range(0, window_resolution[1], cell_size):
            color = (0, 255, 0) if (i // cell_size + j // cell_size) % 2 == 0 else (0, 200, 0)
            pygame.draw.rect(window, color, (i, j, cell_size, cell_size))

    snake.update(food)
    snake.render(window) 
    food.render(window)   
    
    pygame.display.update()
    pygame.time.Clock().tick(15)
