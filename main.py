import pygame
import random
from czastka import Czastka, collision

CELL_SIZE = 4
GRID_WIDTH = 200
GRID_HEIGHT = 190
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE

grid = [[1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def init_grid():
    for x in range(GRID_WIDTH):
        grid[0][x] = 0
        grid[GRID_HEIGHT - 1][x] = 0
    for y in range (GRID_HEIGHT):
        grid[y][0] = 0
        grid[y][GRID_WIDTH - 1] = 0

    barrier_x = GRID_WIDTH // 4
    for y in range(GRID_HEIGHT):
        if GRID_HEIGHT // 2 -10 <= y<= GRID_HEIGHT//2+10:
            continue
        grid[y][barrier_x]= 0

def draw_board(screen):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x] == 0:
                color = (255,255,255)
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            elif grid[y][x] == 2:
                color = (255,165,0)
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def generate_particles_left(num_particles):
    particles = []
    for _ in range(num_particles):
        x = random.randint(1, GRID_WIDTH // 4 - 2)
        y = random.randint(1, GRID_HEIGHT - 2)
        dx, dy = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
        particle = Czastka(x, y, dx, dy)
        particles.append(particle)
    return particles

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    init_grid()

    #czastka1 = Czastka(GRID_WIDTH - 2, GRID_HEIGHT - 100, -1, 0)  # Cząstka leci w lewo (w osi X)
    #czastka2 = Czastka(2, GRID_HEIGHT - 100, 1, 0)  # Cząstka leci w prawo (w osi X)

    czastki = generate_particles_left(1000)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        init_grid()
        #colision_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

        for czastka in czastki:
            czastka.move(grid)

        #draw_grid(screen)
        screen.fill((0,0,0))
        draw_board(screen)
        collision(czastki)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

main()