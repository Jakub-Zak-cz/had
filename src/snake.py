# Snake the videogame coded with python run on pygame
# 
# Autors : Jakub Zak
# Colaborators : Jakub Senkyr
#
# Version : 0.0
# adding pygame
import sys
import pygame
import random

pygame.init()

window_resolution = (800, 600)

window = pygame.display.set_mode(window_resolution)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.is_food_on_screen = False
        self.spawn_food()

    def spawn_food(self):
        self.position = (random.randint(0, (window_resolution[0] // 10) - 1) * 10, 
                         random.randint(0, (window_resolution[1] // 10) - 1) * 10)
        self.is_food_on_screen = True

    def render(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (*self.position, 10, 10))

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((window_resolution[0] // 2), (window_resolution[1] // 2))]
        self.direction = (1, 0)
        self.speed = 10

    def get_head_position(self):
        return self.positions[0]
    
    def eat(self, food):
        head_position = self.get_head_position()
        if (
            head_position[0] < food.position[0] + 10 and
            head_position[0] + 10 > food.position[0] and
            head_position[1] < food.position[1] + 10 and
            head_position[1] + 10 > food.position[1]
        ):
            self.length += 1
            food.spawn_food()
            food.is_food_on_screen = False

    def update(self, food):
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + x * self.speed, cur[1] + y * self.speed)
        
        # Implementace "teleportace" na druhou stranu, když narazí na okraj
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
        for p in self.positions:
            pygame.draw.rect(surface, (0, 255, 0), (p[0], p[1], 10, 10))

# Vytvoření instance hada a potravy
snake = Snake()
food = Food()

# Hlavní smyčka hry
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keyword_pressed = pygame.key.get_pressed()

    # Změna směru hada
    if keyword_pressed[pygame.K_UP]:
        snake.direction = (0, -1)
    elif keyword_pressed[pygame.K_DOWN]:
        snake.direction = (0, 1)
    elif keyword_pressed[pygame.K_LEFT]:
        snake.direction = (-1, 0)
    elif keyword_pressed[pygame.K_RIGHT]:
        snake.direction = (1, 0)

    snake.update(food)

    window.fill((255, 255, 255))
    snake.render(window) 
    food.render(window)   
    
    pygame.display.update()
    pygame.time.Clock().tick(30)
