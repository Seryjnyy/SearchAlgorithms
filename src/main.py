import pygame
from pygame import Rect
from enum import Enum

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

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHTBLUE = (0,0,120)
GREY = (192,192,192)
BLACK = (0,0,0)
BUTTON_COLOUR = BLUE
BUTTON_TEXT_COLOUR = WHITE
MARGIN = 2

EMPTY_NODE = 0
START_NODE = 1
END_NODE = 2
WALL_NODE = 3
FRONTIER_NODE = 4
SEARCHED_NODE = 5
PATH_NODE = 6
# Search result
FRONTIER_EMPTY = 0
FOUND_NOT = 1
FOUND_END = 2
# Determine grid
ROW = 20
COLUMN = ROW
CELL_WIDTH = (SCREEN_WIDTH-200)/ROW - MARGIN
CELL_HEIGHT = SCREEN_HEIGHT/COLUMN - MARGIN

COLOURS = {
    EMPTY_NODE : WHITE,
    START_NODE : RED, 
    END_NODE : GREEN, 
    WALL_NODE : GREY,
    FRONTIER_NODE : LIGHTBLUE,
    SEARCHED_NODE : BLUE,
    PATH_NODE : BLACK
}

class Grid:
    def __init__(self):
        self.create_grid()

    def create_grid(self):
        self.grid = []
        for row in range(ROW):
            for column in range(COLUMN):
                node = Node((row, column), (((MARGIN + CELL_WIDTH) * column + MARGIN), ((MARGIN + CELL_HEIGHT) * row + MARGIN), CELL_WIDTH, CELL_HEIGHT))
                self.grid.append(node)

    def reset_grid(self):
        for node in self.grid:
            node.set_state(EMPTY_NODE)
            node.came_from = None
    

class Button:
    def __init__(self,screen, font, x, y, width, height, message):
        pygame.draw.rect(screen, BUTTON_COLOUR, [x, y, width, height])
        button_text = font.render(message, False, BUTTON_TEXT_COLOUR)
        screen.blit(button_text, (x,y))
        self.rect = Rect(x, y, width, height)

    def is_pressed(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True


class Node:
    def __init__(self, index, rect):
        self.state = 0
        self.index = index
        self.came_from = None
        self.rect = Rect(rect)

    def is_pressed(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        
    def get_colour(self):
        return COLOURS[self.state]

    def set_state(self, node_state):
        self.state = node_state

    def set_came_from(self, came_from_node):
        if self.came_from == None:
            self.came_from = came_from_node


class Breadth_First_Search():
    def __init__(self, grid, start_node, end_node):
        self.grid = grid
        self.frontier = [start_node]
        self.start_node = start_node
        self.end_node = end_node
        self.came_from = {}

    def search_for_end(self):
        if len(self.frontier) == 0:
            return FRONTIER_EMPTY

        current_node = self.frontier.pop(0)
        if current_node.state == WALL_NODE:
            return FOUND_NOT
        if current_node.state == END_NODE:
            return FOUND_END
        if current_node.state == FRONTIER_NODE:
            current_node.set_state(SEARCHED_NODE)
        for next in self.neighbours(current_node):
            if next.came_from == None:
                self.frontier.append(next)
                next.set_came_from(current_node)
                if next.state == EMPTY_NODE:
                   next.set_state(FRONTIER_NODE)

    def neighbours(self, node):
        dirs = [[1,0], [0,1], [-1,0], [0,-1]]
        result = []
        for dir in dirs:
            neighbour_index = (node.index[0] + dir[0], node.index[1] + dir[1])
            neighbour_node = self.find_node_by_index(neighbour_index)
            if neighbour_node:
                result.append(neighbour_node)
        return result
    
    def find_node_by_index(self, index):
        for node in self.grid:
            if node.index == index:
                return node

class Depth_First_Search():
    def __init__(self, grid, start_node, end_node):
        self.grid = grid
        self.frontier = [start_node]
        self.start_node = start_node
        self.end_node = end_node
        self.came_from = {}

    def search_for_end(self):
        if len(self.frontier) == 0:
            return FRONTIER_EMPTY

        current_node = self.frontier.pop()
        if current_node.state == WALL_NODE:
            return FOUND_NOT
        if current_node.state == END_NODE:
            return FOUND_END
        if current_node.state == FRONTIER_NODE:
            current_node.set_state(SEARCHED_NODE)
        for next in self.neighbours(current_node):
            if next.came_from == None:
                self.frontier.append(next)
                next.set_came_from(current_node)
                if next.state == EMPTY_NODE:
                   next.set_state(FRONTIER_NODE)

    def neighbours(self, node):
        dirs = [[1,0], [0,1], [-1,0], [0,-1]]
        result = []
        for dir in dirs:
            neighbour_index = (node.index[0] + dir[0], node.index[1] + dir[1])
            neighbour_node = self.find_node_by_index(neighbour_index)
            if neighbour_node:
                result.append(neighbour_node)
        return result
    
    def find_node_by_index(self, index):
        for node in self.grid:
            if node.index == index:
                return node

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT));
    blue_gradient = [0,0,123]
    screen.fill(BLACK)
    clock = pygame.time.Clock()
    state = States.SET_START

    _grid = Grid()
    grid = _grid.grid
    search = None

    font = pygame.font.SysFont('Comic Sans Ms', 30)

    reset_button = Button(screen, font, 850, 100, 100, 50, "Reset")
    start_button = Button(screen, font, 850, 200, 100, 50, "Start")

    running = True
    mouse_down = False
    start_node = None
    end_node = None
    while running:

        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()

            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_down = True

                if reset_button.is_pressed(mouse_pos):
                    _grid.reset_grid()
                    state = States.SET_START
                    continue
                if start_button.is_pressed(mouse_pos):
                    if start_node and end_node:
                        state = States.START_SEARCH
                        search = get_search_algorithm(grid, start_node, end_node)
                        continue

                node = find_pressed_node(grid, mouse_pos)
                if node is None:
                    continue

                if state == States.SET_START:
                    state = States.SET_END
                    node.set_state(START_NODE)
                    start_node = node
                elif state == States.SET_END:
                    state = States.SET_BLOCK
                    if node.state == EMPTY_NODE:
                        node.set_state(END_NODE)
                        end_node = node
                elif state == States.SET_BLOCK:
                    if node.state == EMPTY_NODE:
                        node.set_state(WALL_NODE)
            elif event.type == MOUSEBUTTONUP:
                mouse_down = False
            elif event.type == MOUSEMOTION and state == States.SET_BLOCK and mouse_down:
                node = find_pressed_node(grid, mouse_pos)
                if node != None:
                    if node.state == EMPTY_NODE:
                        node.set_state(WALL_NODE)


        if state == States.START_SEARCH:
            search_result = search.search_for_end() 

            if search_result == FOUND_END:
                state = States.FOUND_END
                show_result(True, start_node, end_node)
            elif search_result == FRONTIER_EMPTY:
                state = States.FOUND_END
                show_result(False,  start_node, end_node)


        for node in grid:
            colour = node.get_colour()
            if colour == BLUE:
                colour = calculate_colour_gradient(start_node, node, blue_gradient)
            
           # if colour == BLACK:
               # print("PAINTING PATH")
            pygame.draw.rect(screen, colour, node.rect)

        
        clock.tick(120)
        pygame.display.update()


def show_result(end_found, start_node, end_node):
    if not end_found:
        print("Cannot find end")
        return

    current = end_node
    path = []
    while current != start_node:
        path.append(current)
        current = current.came_from
    for node in path:
        if node.state == SEARCHED_NODE:
            node.state = PATH_NODE

def get_search_algorithm(grid, start_node, end_node):
    return Depth_First_Search(grid, start_node, end_node)

def calculate_colour_gradient(start_node, node, starting_colour):
    diff = (start_node.index[0] - node.index[0]) + (start_node.index[1] - node.index[1])
    new_colour = starting_colour
    new_colour[0] = abs(int(diff*(255/(ROW-1 + ROW-1 - 1))))
    return new_colour



def find_pressed_node(grid, mouse_pos):
    for node in grid:
        if node.is_pressed(mouse_pos):
            return node


if __name__ == '__main__':
    main()