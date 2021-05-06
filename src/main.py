import pygame
from pygame import Rect
from enum import Enum
import math
from settings import *
import sys
import random
import pandas
from opensimplex import OpenSimplex

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

class Grid:
    def __init__(self):
        self.create_grid()
        self.openSimplex = OpenSimplex(12345)
        # self.offset = 0

    def create_grid(self):
        self.grid = []
        for row in range(ROW):
            for column in range(COLUMN):
                node = Node((row, column), (((MARGIN + CELL_WIDTH) * column + MARGIN), ((MARGIN + CELL_HEIGHT) * row + MARGIN), CELL_WIDTH, CELL_HEIGHT))
                self.grid.append(node)


    def reset_grid(self):
        for node in self.grid:
            node.set_state(EMPTY_NODE)
            node.clear_came_from()
            node.weight = 0

    def claer_weight_map(self):
        # weight
        node.weight = 0

    def clear_searched_nodes(self):
        for node in self.grid:
            if node.state == SEARCHED_NODE or node.state == FRONTIER_NODE or node.state == PATH_NODE:
                node.set_state(EMPTY_NODE)
                node.clear_came_from()
            if node.state == END_NODE:
                node.clear_came_from()

    def clear_wall_nodes(self):
        for node in self.grid:
            if node.state == WALL_NODE:
                node.set_state(EMPTY_NODE)

    def find_pressed_node(self, mouse_pos):
        for node in self.grid:
            if node.is_pressed(mouse_pos):
                return node
    # weight
    def create_weighted_grid(self):
        # self.offset = self.offset + 1
        for node in self.grid:
            node.weight = self.calculate_noise_value(node)
        self.map_values()

    def calculate_noise_value(self, node, offset = 1):
        x = node.index[0]
        y = node.index[1]
        return self.openSimplex.noise2d(x, y)
        # octaves = 2
        # offset = 0
        # start_amplitude = 2
        # output = 0
        # og_offset = random.random() * 2 * math.pi
        # for n in range(octaves):
        #     frequency = 2**n
        #     amplitude = start_amplitude / float(n+1)

        #     offset = x * frequency * 2 * math.pi + og_offset
        #     output += math.sin(y* frequency * 2* math.pi + og_offset) * amplitude

        # return output # number is temporary
    
    def map_values(self):
        smallest_value = sys.maxsize
        biggest_value =  - sys.maxsize 

        for node in self.grid:
            if node.weight > biggest_value:
                biggest_value = node.weight
            elif node.weight < smallest_value:
                smallest_value = node.weight
        
        smallest_value = math.floor(smallest_value)
        biggest_value = math.floor(biggest_value)


        value_range = abs(smallest_value) + abs(biggest_value)
        bound = 127 / value_range 
        for node in self.grid:
            node.weight = math.floor(127 + (node.weight * bound))


    def check_if_end_node_set(self):
        for node in self.grid:
            if node.state == END_NODE:
                return True

    def check_if_start_node_set(self):
        for node in self.grid:
            if node.state == START_NODE:
                return True
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
        # A star stuff
        self.came_from_cost = 0
        self.goal_cost = None
        # weight
        self.weight = 0
        

    def is_pressed(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            return True
        
    def get_colour(self):
        if self.state == EMPTY_NODE:
            # (0,0,0) looks really cool for emty cells
            weigth_colour = (0, self.weight, self.weight)
            return weigth_colour
        return COLOURS[self.state]

    def calculate_gradient(self, start_node, start_colour):
        diff = abs(start_node.index[0] - self.index[0]) + abs(start_node.index[1] - self.index[1])
        new_colour = start_colour
        new_colour[0] = abs(int(diff*(255/(ROW*2))))
        return new_colour

    def set_state(self, node_state):
        self.state = node_state

    def set_came_from(self, came_from_node):
        self.came_from = came_from_node
        # A start stuff
        self.came_from_cost = self.calculate_came_from_cost(came_from_node)

    def clear_came_from(self):
        self.came_from = None
        self.came_from_cost = 0
        
    def calculate_came_from_cost(self, came_from_node):
        diff = (self.index[0] - came_from_node.index[0], 
                self.index[1] - came_from_node.index[1])
        came_from_to = math.sqrt(diff[0] ** 2 + diff[1] ** 2) * 10
        return came_from_node.get_came_from_cost() + math.floor(came_from_to)

    def calculate_goal_cost(self, end_node, multiplier):
        diff = (self.index[0] - end_node.index[0], 
                self.index[1] - end_node.index[1])
        # self.goal_cost = abs(diff[0]) + abs(diff[1]) # manhattan distance
        self.goal_cost = math.floor(math.sqrt(diff[0] ** 2 + diff[1] ** 2) * multiplier)

    def turn_into_wall(self):
        if self.state == EMPTY_NODE:
            self.set_state(WALL_NODE)

    def from_wall_turn_into_empty(self):
        if self.state == WALL_NODE:
            self.set_state(EMPTY_NODE)
            
    def get_came_from_cost(self):
        return self.came_from_cost

    def get_goal_cost(self):
        return self.goal_cost

    def get_heuristic(self):
        return self.came_from_cost + self.goal_cost

class Breadth_First_Search():
    def __init__(self, grid, start_node, end_node):
        self.grid = grid
        self.frontier = [start_node]
        self.start_node = start_node
        self.end_node = end_node

    def search_for_end(self):
        if len(self.frontier) == 0:
            return FRONTIER_EMPTY

        current_node = self.pop_node_from_frontier()
        if current_node.state == WALL_NODE:
            return FOUND_NOT
        if current_node.state == END_NODE:
            return FOUND_END
        if current_node.state == FRONTIER_NODE:
            current_node.set_state(SEARCHED_NODE)
        for next in self.neighbours(current_node):
            if next.state == WALL_NODE:
                continue

            if next.came_from == None or next.calculate_came_from_cost(current_node) < next.get_came_from_cost():
                self.frontier.append(next)
                next.set_came_from(current_node)
                if next.state == EMPTY_NODE:
                   next.set_state(FRONTIER_NODE)

    def pop_node_from_frontier(self):
        return self.frontier.pop(0)

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

class Heuristic_Search(Breadth_First_Search):
    def __init__(self, grid, start_node, end_node, multiplier = 10):
        Breadth_First_Search.__init__(self, grid, start_node, end_node)
        for node in self.grid:
            self.goal_cost = node.calculate_goal_cost(self.end_node, multiplier)

    def pop_node_from_frontier(self):
        lowest_heuristic = 9999999
        lowest_heuristic_index = None
        for index, node in enumerate(self.frontier):
            if self.calculate_node_score(node) <= lowest_heuristic:
                lowest_heuristic = self.calculate_node_score(node)
                lowest_heuristic_index = index
        return self.frontier.pop(lowest_heuristic_index)
    
class Greedy_Best_First_Search(Heuristic_Search):
    def calculate_node_score(self, node):
        return node.get_goal_cost()

class AStar_Search(Heuristic_Search):
    def __init__(self, grid, start_node, end_node):
        Heuristic_Search.__init__(self, grid, start_node, end_node, 18)

    def calculate_node_score(self, node):
        return node.get_goal_cost() + node.get_came_from_cost()

class Depth_First_Search(Breadth_First_Search):
    def pop_node_from_frontier(self):
        return self.frontier.pop()

class GUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT));
        self.screen.fill(DARK_BLUE)
        self.font = pygame.font.Font('../fonts/OpenSans-Bold.ttf', FONT_SIZE)
        self.y_button_stack = 0

    def create_button(self, text):
        self.y_button_stack = self.y_button_stack + 1
        return Button(self.screen, self.font, BUTTON_X, BUTTON_Y*self.y_button_stack, BUTTON_WIDTH, BUTTON_HEIGHT, text)


def main():
    clock = pygame.time.Clock()
    state = States.SET_START

    _grid = Grid()
    grid = _grid.grid
    search = None
    gui = GUI()

    clear_button = gui.create_button("           Clear")
    reset_button = gui.create_button("           Reset")
    bfs_button = gui.create_button("    Breadth First")
    dfs_button  = gui.create_button("     Depth First")
    gfs_button = gui.create_button("Greedy Best-First")
    astar_button = gui.create_button("              A*")
    create_noise_map_button =  gui.create_button("Create Noise Map")

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
                    start_node = None
                    end_node = None
                    continue
                if clear_button.is_pressed(mouse_pos):
                    _grid.clear_searched_nodes()
                    if start_node and end_node:
                        state = States.SET_BLOCK
                    continue
                if create_noise_map_button.is_pressed(mouse_pos):
                    _grid.create_weighted_grid()

                _search = None
                if (start_node != None) and (end_node != None) :
                    _search = check_which_algorithm_was_choosen(mouse_pos, grid, start_node, end_node, bfs_button, dfs_button, gfs_button, astar_button)
                    if _search :
                        _grid.clear_searched_nodes()
                        state = States.START_SEARCH
                        search = _search
                        continue

                node = _grid.find_pressed_node(mouse_pos)
                if node is None:
                    continue

                if event.button == 3:
                    right_mouse_down = True
                    if node.state == END_NODE:
                        node.set_state(EMPTY_NODE)
                        end_node = None
                        if start_node == None:
                            state = States.SET_START
                        else:
                            state = States.SET_END
                    if node.state == START_NODE:
                        node.set_state(EMPTY_NODE)
                        start_node = None
                        state = States.SET_START
                    #     if _grid.check_if_start_node_set():
                    #         state = States.SET_START
                    #     else:
                    #         state = States.SET_END

                    # if node.state == START_NODE:
                    #     node.set_state(EMPTY_NODE)
                    #     start_node == None
                    #     state = States.SET_START
                    if node.state == WALL_NODE:
                        node.set_state(EMPTY_NODE)
                        continue
                if event.button == 1:
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
                        node.turn_into_wall()
            elif event.type == MOUSEBUTTONUP:
                mouse_down = False
                right_mouse_down = False
            elif event.type == MOUSEMOTION and state == States.SET_BLOCK and (mouse_down or right_mouse_down):
                node = _grid.find_pressed_node(mouse_pos)
                if node != None:
                    if right_mouse_down:
                        node.from_wall_turn_into_empty()
                    elif mouse_down:
                        node.turn_into_wall()


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
                colour = node.calculate_gradient(start_node, COLOUR_GRADIENT) # [0,0,123]
            pygame.draw.rect(gui.screen, colour, node.rect)

        clock.tick(SEARCH_SPEED)
        pygame.display.update()


def check_which_algorithm_was_choosen(mouse_pos, grid, start_node, end_node, bfs_button, dfs_button, gfs_button, astar_button):
    if bfs_button.is_pressed(mouse_pos):
        return Breadth_First_Search(grid, start_node, end_node)
    if dfs_button.is_pressed(mouse_pos):
        return Depth_First_Search(grid, start_node, end_node)
    if gfs_button.is_pressed(mouse_pos):
        return Greedy_Best_First_Search(grid, start_node, end_node)
    if astar_button.is_pressed(mouse_pos):
        return AStar_Search(grid, start_node, end_node)

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
    print(len(path)-1)

if __name__ == '__main__':
    main()


        