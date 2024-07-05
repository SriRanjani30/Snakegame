import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.apple_position = self.randomize_apple_position()

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.direction == UP and point != DOWN:
            self.direction = point
        elif self.direction == DOWN and point != UP:
            self.direction = point
        elif self.direction == LEFT and point != RIGHT:
            self.direction = point
        elif self.direction == RIGHT and point != LEFT:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH, (cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if self.apple_position == self.get_head_position():
                self.score += 1
                self.apple_position = self.randomize_apple_position()
            else:
                self.positions.pop()

    def reset(self):
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.apple_position = self.randomize_apple_position()

    def randomize_apple_position(self):
        return (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, GREEN, r)
        r = pygame.Rect((self.apple_position[0], self.apple_position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, RED, r)

# Main function
def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption('Snake Game')
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    snake = Snake()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn(UP)
                elif event.key == pygame.K_DOWN:
                    snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.turn(RIGHT)

        snake.move()
        surface.fill(BLACK)
        snake.draw(surface)
        screen.blit(surface, (0, 0))
        pygame.display.update()
        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()
