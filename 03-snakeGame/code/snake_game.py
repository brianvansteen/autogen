# filename: snake_game.py

import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = (0, 0)
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH, (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = (0, 0)

    def draw(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color, (p[0], p[1], GRID_SIZE, GRID_SIZE))

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    self.direction = (0, 1)
                elif event.key == pygame.K_LEFT:
                    self.direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.direction = (1, 0)

# Game class
class Game:
    def __init__(self):
        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.snake = Snake()

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.snake.handle_keys()
            self.snake.move()
            self.draw()
            clock.tick(FPS)
            if self.check_collision():
                running = False

    def draw(self):
        self.surface.fill(BLACK)
        self.snake.draw(self.surface)
        pygame.display.update()

    def check_collision(self):
        head = self.snake.get_head_position()
        if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
            return True
        return False

# Main function
def main():
    game = Game()
    game.run()

if __name__ == '__main__':
    main()