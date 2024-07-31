import pygame
import sys
import random
from collections import deque

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TILE_SIZE = 40
FPS = 60
LEVELS = 3


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


pygame.mixer.init()
move_sound = pygame.mixer.Sound("move.wav")
win_sound = pygame.mixer.Sound("win.wav")


start_ticks = pygame.time.get_ticks()

def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]
    stack = [(1, 1)]
    maze[1][1] = 0

    def neighbors(x, y):
        n = []
        if x > 1 and maze[y][x - 2] == 1: n.append((x - 2, y))
        if x < width - 2 and maze[y][x + 2] == 1: n.append((x + 2, y))
        if y > 1 and maze[y - 2][x] == 1: n.append((x, y - 2))
        if y < height - 2 and maze[y + 2][x] == 1: n.append((x, y + 2))
        return n

    while stack:
        x, y = stack[-1]
        n = neighbors(x, y)
        if n:
            nx, ny = random.choice(n)
            maze[(y + ny) // 2][(x + nx) // 2] = 0
            maze[ny][nx] = 0
            stack.append((nx, ny))
        else:
            stack.pop()
    
    maze[-2][-2] = 0
    return maze


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        if maze[self.y + dy][self.x + dx] == 0:
            self.x += dx
            self.y += dy
            move_sound.play()

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))


player = Player(1, 1)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")


clock = pygame.time.Clock()

level = 1
running = True
while running and level <= LEVELS:
    maze = generate_maze(20, 15)
    player = Player(1, 1)
    level_running = True
    
    while level_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                level_running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            player.move(1, 0)
        if keys[pygame.K_UP]:
            player.move(0, -1)
        if keys[pygame.K_DOWN]:
            player.move(0, 1)

        screen.fill(BLACK)
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                color = WHITE if maze[y][x] == 1 else BLACK
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        player.draw(screen)

        pygame.draw.rect(screen, GREEN, ((len(maze[0]) - 2) * TILE_SIZE, (len(maze) - 2) * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        if player.x == len(maze[0]) - 2 and player.y == len(maze) - 2:
            win_sound.play()
            level += 1
            level_running = False

        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        timer_text = pygame.font.SysFont(None, 55).render(f'Time: {seconds:.2f}', True, RED)
        screen.blit(timer_text, (10, 10))

        pygame.display.flip()


        clock.tick(FPS)


screen.fill(BLACK)
game_over_text = pygame.font.SysFont(None, 75).render('You Win!', True, GREEN)
screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - game_over_text.get_height()//2))
pygame.display.flip()
pygame.time.wait(3000)

pygame.quit()
sys.exit()
