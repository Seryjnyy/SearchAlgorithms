import pygame
from enum import Enum
import sys
import collections

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

EMPTY_NODE = 0
START_NODE = 1
END_NODE = 2
WALL_NODE = 3
FRONTIER_NODE = 4
SEARCHED_NODE = 5
PATH_NODE = 6
# Determine grid
ROW = 60
COLUMN = ROW
CELL_WIDTH = (SCREEN_WIDTH-200)/ROW - MARGIN
CELL_HEIGHT = SCREEN_HEIGHT/COLUMN - MARGIN
# Set the state
state = States.SET_START
grid = []
node_states = {}
frontier = []
came_from = {}
found_end = False

start_node = None
end_node = None

def main():
    global state
    global grid
    global node_states
    global frontier
    global came_from
    global found_end

    global start_node
    global end_node

    blue_gradient = [0,0,123]

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT));

    # Grid
    for row in range(ROW):
        for column in range(COLUMN):
            node = (row, column)
            grid.append(node)
            node_states.update({node : EMPTY_NODE})

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
    
    # Game running loop 
    running = True
    mouse_down = False
    biggest_diff = 0
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
                    Reset_Grid()
                    print("state")
                    continue
                # Start button
                if pos[0] >=  850 and pos[0] <= 950 and pos[1] >= 200 and pos[1] <= 250 and state == States.SET_BLOCK:
                    state = States.START_SEARCH
                    continue

                node = find_node_through_position()
                if node == None:
                    continue
       
                if state == States.SET_START:
                    state = States.SET_END
                    node_states.update({node : START_NODE})
                    frontier.append(node)
                    start_node = node
                elif state == States.SET_END:
                    if node_states[node] == 0:
                        state = States.SET_BLOCK
                        node_states.update({node : END_NODE})  
                elif state == States.SET_BLOCK:
                    if node_states[node] == 0:
                        node_states.update({node : WALL_NODE})
            elif event.type == MOUSEBUTTONUP:
                mouse_down = False
            elif event.type == MOUSEMOTION and state == States.SET_BLOCK and mouse_down:
                node = find_node_through_position()
                if node != None:
                    if node_states[node] == EMPTY_NODE:
                        node_states.update({node : WALL_NODE})

        #the algo
        if state == States.START_SEARCH:
            if len(frontier) != 0 and not found_end:
                current_node = frontier.pop(0)
                node_state = node_states[current_node]
                if node_state == WALL_NODE:
                    continue
                if node_state == END_NODE:
                    end_node = current_node
                    found_end = True
                if node_state == FRONTIER_NODE:
                    node_states.update({current_node : SEARCHED_NODE})
                for next in neighbours(current_node):
                    if next not in came_from:
                        frontier.append(next)
                        came_from.update({next : current_node})
                        if node_states[next] == EMPTY_NODE:
                           node_states.update({next : FRONTIER_NODE})
            else:
                state = States.FOUND_END
                show_result()

        # Screen drawing
        for row in range(ROW):
            for column in range(COLUMN):
                color = WHITE
                node = (row, column)
                node_state = node_states[node]
                if node_state == START_NODE:
                    color = RED
                if node_state == END_NODE:
                    color = GREEN
                if node_state == WALL_NODE:
                    color = GREY
                if node_state == FRONTIER_NODE:
                    color = LIGHTBLUE   
                if node_state == SEARCHED_NODE:
                    diff = (start_node[0] - node[0]) + (start_node[1] - node[1])
                    if abs(diff) > biggest_diff:
                        biggest_diff = abs(diff)
                    # print(biggest_diff)
                    step_colour = blue_gradient
                    step_colour[0] = abs(int(diff*(255/(ROW-1 + ROW-1 - 1))))
                    color = step_colour    
                if state == PATH_NODE:
                    color = BLACK   
                pygame.draw.rect(screen, color,
                                [(MARGIN + CELL_WIDTH) * column + MARGIN,
                                (MARGIN + CELL_HEIGHT) * row + MARGIN,
                                CELL_WIDTH,
                                CELL_HEIGHT])
        clock.tick(120)
        pygame.display.update()
    quit()

def show_result():
    global node_states
    # if found_end == False:
    #     print("Sorry no path")
    #     return 

    current = end_node
    path = []
    print(end_node)
    while current != start_node:
        print(current)
        path.append(current)
        current = came_from[current]
    for node in path:
        if node_states[node] == SEARCHED_NODE:
            node_states.update({node : PATH_NODE})


def Reset_Grid():
    global state
    global frontier
    global came_from
    global node_states
    global found_end

    state = States.SET_START
    found_end = False

    frontier.clear() 
    came_from.clear()   
    
    for node in node_states:
        node_states.update({node : EMPTY_NODE})


def neighbours(node):
    dirs = [[1,0], [0,1], [-1,0], [0,-1]]
    result = []
    for dir in dirs:
        neighbour = (node[0] + dir[0], node[1] + dir[1])
        if neighbour in grid:
            result.append(neighbour)
    return result

def find_node_through_position():
    pos = pygame.mouse.get_pos()
    row = int(pos[1] // (CELL_WIDTH + MARGIN))
    column = int(pos[0] // (CELL_HEIGHT + MARGIN))
    if row >= ROW or column >= COLUMN or row < 0 or column < 0:
        return None
    return (row, column)

if __name__ == "__main__":
    main()
