import pygame
from enum import Enum
import sys
import collections
import random
# only in dijkstras
from queue import Queue
import heapq
from perlin import PerlinNoiseFactory
import perlin
import math

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
LIGHTBLUE = (0,0,120)
GREY = (192,192,192)
BLACK = (0,0,0)
MARGIN = 2
# Determine grid
ROW = 40
COLUMN = ROW
CELL_WIDTH = (SCREEN_WIDTH-200)/ROW - MARGIN
CELL_HEIGHT = SCREEN_HEIGHT/COLUMN - MARGIN
# Set the state
state = States.SET_START
grid = []
grid_weights = []
pnf = PerlinNoiseFactory(2, octaves = 8)
all_nodes = []
found_end = False




def add_all_nodes():
    global all_nodes
    for cell in grid:
        if cell[2] != 3:
            all_nodes.append(cell)


def neighbours(node):
    dirs = [[1,0], [0,1], [-1,0], [0,-1]]
    result = []
    for dir in dirs:
        index = node[1] + dir[1] + ((node[0] + dir[0]) * ROW)
        if index > 0 and index < 64:
            if neighbour in all_nodes:
                result.append(all_nodes[index])
                break
    return result

def print_all():
    for node in all_nodes:
        print("Node at ", node[0], node[1], "value of ", node[2])
        n = neighbours(node)
        for x in n:
            print(x)

def main():
    global state
    global grid
    global found_end
    global grid_weights
    blue_gradient = [0,0,123]

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT));

    # serch stuff
    start_node = []
    target_node = []

    biggest_noise = 0
    # Grid
    for row in range(ROW):
        for column in range(COLUMN):
            n = pnf(row/ROW*0.3, column/COLUMN*0.5)
            noise =n*n*10
            grid.append([row, column, 0, noise])
            grid_weights.append(noise)
            if noise > biggest_noise:
                biggest_noise = noise
            # grid_weights.append(random.randint(1,20))


    # for x in grid_weights:
    #     print(x)

    colour_split = math.floor(255/biggest_noise)
    # print(colour_split, biggest_noise)

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
    # Search stuff
    frontier = []
    came_from = dict()
    cost_sofar = dict()
    
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
                    Reset_Grid(frontier, came_from)
                    continue
                # Reset button check
                if pos[0] >=  850 and pos[0] <= 950 and pos[1] >= 200 and pos[1] <= 250 and state == States.SET_BLOCK:
                    state = States.START_SEARCH
                    add_all_nodes()
                    continue
                # Grid cells check
                row = int(pos[1] // (CELL_WIDTH + MARGIN))
                column = int(pos[0] // (CELL_HEIGHT + MARGIN))
                if row >= ROW or column >= COLUMN or node[2] != 0:
                    continue
                node = grid[column + (row * ROW)]
                set_mode = 0
                if state == States.SET_START:
                    set_mode = 1
                    state = States.SET_END
                    start_node = [row, column, 1]
                    frontier.append([start_node[0], start_node[1]])
                    came_from[str([start_node[0], start_node[1]])] = None
                    cost_sofar[str([start_node[0], start_node[1]])] = 0
                    # neighbours.append(pos_start)
                elif state == States.SET_END:
                    if grid[column + (row*ROW)][2] != 0:
                        continue
                    set_mode = 2
                    state = States.SET_BLOCK
                    target_node = [row, column, 2]
                elif state == States.SET_BLOCK:
                    set_mode = 3
                node[2] = set_mode
            elif event.type == MOUSEBUTTONUP:
                mouse_down = False
            elif event.type == MOUSEMOTION and state == States.SET_BLOCK and mouse_down:
                # Calculate the indexes, and leve if out of bounds
                pos = pygame.mouse.get_pos()
                row = int(pos[1] // (CELL_WIDTH + MARGIN))
                column = int(pos[0] // (CELL_HEIGHT + MARGIN))
                if row >= ROW or column >= COLUMN:
                    continue
                node = grid[column + (row * ROW)]
                if node[2] == 0:
                    node[2] = 3


        #the algo
        if state == States.START_SEARCH:
            if len(frontier) != 0:
                # current = heapq.heappop(frontier)
                smallest_cell = 0
                smallest_weight = 9999

                for i, cell in enumerate(frontier):
                    if cell[3] < smallest_weight:
                        smallest_weight = cell[3]
                        smallest_cell = i


                current = frontier.pop(smallest_cell)
                print(old_indexes)
                print(current)
                if grid[current[1] + (current[0] * ROW)][2] == 2:
                   found_end = True
                if grid[current[1] + (current[0] * ROW)][2] == 4:
                    grid[current[1] + (current[0] * ROW)][2] = 5
                for next in neighbours(current):
                    # new_cost =cost_sofar[str(current)] + grid_weights

                    if str(next) not in came_from:
                        heapq.heappush(frontier, next)
                        came_from[str(next)] = current
                        if grid[next[1] + (next[0] * ROW)][2] == 0:
                            grid[next[1] + (next[0] * ROW)][2] = 4
            else:
                show_result(start_node, target_node, came_from)

        # Screen drawing
        for row in range(ROW):
            for column in range(COLUMN):
                color = WHITE
                node =  grid[column + (row * ROW)]
                if node[2] == 0:
                    weight = grid_weights[column + (row*ROW)]
                    color = [255 - colour_split*weight,255-colour_split*weight,255-colour_split*weight]
                if node[2] == 1:
                    color = RED
                if node[2] == 2:
                    color = GREEN
                if node[2] == 3:
                    color = GREY
                if node[2] == 4:
                    color = LIGHTBLUE   
                if node[2] == 5:
                    diff = (start_node[0] - node[0]) + (start_node[1] - node[1])
                    step_colour = blue_gradient
                    step_colour[0] = abs(int(diff*(255/(ROW-1 + ROW-1 - 1))))
                    color = step_colour    
                if node[2] == 6:
                    color = BLACK   
                pygame.draw.rect(screen, color,
                                [(MARGIN + CELL_WIDTH) * column + MARGIN,
                                (MARGIN + CELL_HEIGHT) * row + MARGIN,
                                CELL_WIDTH,
                                CELL_HEIGHT])
        

        clock.tick(120)
        pygame.display.update()
    quit()

def show_result(start_node, target_node, came_from):
    global state
    state = States.FOUND_END

    if found_end == False:
        print("Sorry no path")
        return 

    current = [target_node[0], target_node[1]]
    path = []
    while current != [start_node[0], start_node[1]]:
        path.append(current)
        current = came_from[str(current)]
    path.append([start_node[0], start_node[1]])
    path.reverse()
    # for p in path:
    #     print(p)
    paint_path(path)

def paint_path(path):
    global grid
    for step in path:
        if grid[step[1] + (step[0]*ROW)][2] == 5:
            grid[step[1] + (step[0]*ROW)][2] = 6

# Functions
def Reset_Grid(frontier, came_from):
    global state
    global grid
    global all_nodes

    frontier.clear() 
    came_from.clear()   
    all_nodes.clear()

    for cell in grid:
        cell[2] = 0
    state = States.SET_START
    

if __name__ == "__main__":
    main()
