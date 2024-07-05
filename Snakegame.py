import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800  # Adjusted screen width
SCREEN_HEIGHT = 600  # Adjusted screen height
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Load background image
background_image = pygame.image.load("Images/Background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Particle class for visual effects
class Particle:
    def __init__(self, position):
        self.image = pygame.Surface((2, 2))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=position)
        self.lifetime = 10

    def update(self):
        self.lifetime -= 1
        self.rect.move_ip(1, 0)  # Example movement, adjust as needed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)

# Snake class
class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.apple_position = self.randomize_apple_position()
        self.particles = []

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
                self.spawn_particles(self.apple_position)
            else:
                self.positions.pop()

    def reset(self):
        self.positions = [(GRID_WIDTH // 2 * GRID_SIZE, GRID_HEIGHT // 2 * GRID_SIZE)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.apple_position = self.randomize_apple_position()

    def randomize_apple_position(self):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if position not in self.positions:
                return position

    def spawn_particles(self, position):
        for _ in range(10):  # Number of particles to create
            particle = Particle(position)
            self.particles.append(particle)

    def update_particles(self):
        for particle in self.particles:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, GREEN, r)
        r = pygame.Rect((self.apple_position[0], self.apple_position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, RED, r)
        self.draw_particles(surface)

    def draw_particles(self, surface):
        for particle in self.particles:
            particle.draw(surface)

    def draw_score(self, surface):
        font = pygame.font.Font(None, 36)
        text = font.render(f'Score: {self.score}', True, WHITE)
        surface.blit(text, (10, 10))

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
        surface.blit(background_image, (0, 0))
        snake.draw(surface)
        snake.draw_score(surface)
        screen.blit(surface, (0, 0))
        pygame.display.update()
        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()
