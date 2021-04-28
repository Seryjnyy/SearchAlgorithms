import pygame
from enum import Enum
import sys

from pygame.locals import (
    QUIT,
    KEYDOWN,
    K_ESCAPE,
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    MOUSEMOTION
)

States = Enum(
    'States',
    'SET_START SET_END SET_BLOCK START_SEARCH FOUND_END'
)

# Initialise screen object (the main surface) f
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHTBLUE = (0,0,180)
GREY = (192,192,192)
BLACK = (0,0,0)
MARGIN = 2
# Determine grid
ROW = 20
COLUMN = 20
CELL_WIDTH = (SCREEN_WIDTH-200)/ROW - MARGIN
CELL_HEIGHT = SCREEN_HEIGHT/COLUMN - MARGIN
# Set the state
state = States.SET_START

def main():
    global state

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT));

    # serch stuff
    pos_start = (-1,-1)
    pos_end = (-1,-1)
    neighbours = []
    current_cell = 0


    # Grid
    grid = []   
    for row in range(ROW):
        grid.append([])
        for column in range(COLUMN):
            grid[row].append(0)

    # Clock
    clock = pygame.time.Clock()

    # Draw initial, thigs that dont change
    screen.fill(BLACK)
    font = pygame.font.SysFont('Comic Sans Ms', 30)
    # Reset button
    pygame.draw.rect(screen, BLUE, [850, 100, 100, 50])
    txt_reset = font.render('Reset', False, WHITE)
    screen.blit(txt_reset, (850,100))
    # Start search button
    pygame.draw.rect(screen, BLUE, [850, 200, 100, 50])
    txt_reset = font.render('Start', False, WHITE)
    screen.blit(txt_reset, (850,200))

    # Game running loop 
    running = True
    mouse_down = False
    while running:

        # Handle events
        for event in pygame.event.get():
            # Quitting the game
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            # Mouse handling 
            elif event.type == MOUSEBUTTONDOWN:
                mouse_down = True
                pos = pygame.mouse.get_pos()
                # Reset button check
                if pos[0] >=  850 and pos[0] <= 950 and pos[1] >= 100 and pos[1] <= 150:
                    Reset_Grid(grid)
                    continue
                # Reset button check
                if pos[0] >=  850 and pos[0] <= 950 and pos[1] >= 200 and pos[1] <= 250 and state == States.SET_BLOCK:
                    state = States.START_SEARCH
                    continue
                # Grid cells check
                row = int(pos[1] // (CELL_WIDTH + MARGIN))
                column = int(pos[0] // (CELL_HEIGHT + MARGIN))
                if row >= ROW or column >= COLUMN or grid[row][column] != 0:
                    continue
                set_mode = 0
                if state == States.SET_START:
                    set_mode = 1
                    state = States.SET_END
                    pos_start = (row, column)
                    neighbours.append(pos_start)
                elif state == States.SET_END:
                    set_mode = 2
                    state = States.SET_BLOCK
                    pos_end = (row, column)
                elif state == States.SET_BLOCK:
                    set_mode = 3
                grid[row][column] = set_mode
            elif event.type == MOUSEBUTTONUP:
                mouse_down = False
            elif event.type == MOUSEMOTION and state == States.SET_BLOCK and mouse_down:
                # Calculate the indexes, and leve if out of bounds
                pos = pygame.mouse.get_pos()
                row = int(pos[1] // (CELL_WIDTH + MARGIN))
                column = int(pos[0] // (CELL_HEIGHT + MARGIN))
                if row >= ROW or column >= COLUMN:
                    continue
                # if cell is empty then set it to 3, else leave it as is
                grid[row][column] = 3 if grid[row][column] == 0 else grid[row][column]

                # print("Click ", pos, "Grid coordinates: ", row, column)

        # Screen drawing
        for row in range(ROW):
            for column in range(COLUMN):
                color = WHITE
                if grid[row][column] == 1:
                    color = RED
                if grid[row][column] == 2:
                    color = GREEN
                if grid[row][column] == 3:
                    color = GREY
                if grid[row][column] == 4:
                    color = LIGHTBLUE   
                if grid[row][column] == 5:
                    color = BLACK   
                pygame.draw.rect(screen, color,
                                [(MARGIN + CELL_WIDTH) * column + MARGIN,
                                (MARGIN + CELL_HEIGHT) * row + MARGIN,
                                CELL_WIDTH,
                                CELL_HEIGHT])


        # Breadth first search
        # print("The neighbour :", len(neighbours))

        if current_cell-1 == Count_Cells(grid) or pos_end in neighbours:
            quit()

        if current_cell < len(neighbours) and state == States.START_SEARCH:
            print("Current cell" ,current_cell)
            print("Count", Count_Cells(grid))
            r, c = neighbours[current_cell]
            prev_count = len(neighbours)
            if r-1 >= 0: 
                if grid[r-1][c] == 2:
                    Found_end((r-1, c))

                if grid[r-1][c] == 0:       
                    grid[r-1][c] = 4
                    if (r-1, c) not in neighbours:
                        neighbours.append((r-1, c))
            if r+1 < ROW:
                if grid[r+1][c] == 2:
                    Found_end(r+1, c)

                if grid[r+1][c] == 0: 
                    grid[r+1][c] = 4
                    if (r+1, c) not in neighbours:
                        neighbours.append((r+1, c))
            if c - 1>= 0:
                if grid[r][c-1] == 2:
                    Found_end(r, c-1)

                if grid[r][c-1] == 0:
                    grid[r][c-1] = 4
                    if (r, c-1) not in neighbours:
                        neighbours.append((r, c-1))
            if c + 1 < COLUMN:
                if grid[r][c+1] == 2:
                    Found_end(r, c+1)

                if grid[r][c+1] == 0: 
                    grid[r][c+1] = 4
                    if (r, c+1) not in neighbours:
                        neighbours.append((r, c+1))
            current_cell = current_cell + 1 if (current_cell + 1) <= len(neighbours) else current_cell

        clock.tick(60)
        pygame.display.update()
    quit()

# Functions
def Reset_Grid(grid):
    global state
    for row in range(ROW):
        for column in range(COLUMN):
            grid[row][column] = 0
    state = States.SET_START

def Count_Cells(grid):
    count = 0
    for row in range(ROW):
        for column in range(COLUMN):
            if grid[row][column] != 0 and  grid[row][column] != 4:
                count += 1

    rows = len(grid)
    columns = len(grid[0])
    return rows*columns - count

def Found_end(row, column):
    global state
    state = States.FOUND_END
    print("found the end at :", row, column)
    

if __name__ == "__main__":
    main()
