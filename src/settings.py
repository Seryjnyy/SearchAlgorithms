# Determines size of grid
ROW = 50

# Controls pygame clock tick
# determines how fast the visualisation happens
SEARCH_SPEED = 120

# Screen resolution, changing it is not recommended
# button position will not adapt automatically
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

COLUMN = ROW
MARGIN = 1

CELL_WIDTH = (SCREEN_WIDTH-200)/ROW - MARGIN
CELL_HEIGHT = SCREEN_HEIGHT/COLUMN - MARGIN

FONT_SIZE = 21

# Noise generation
OCTAVES = 4
UNBIAS = True

# Colours
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (27,83,242)
LIGHTBLUE = (0,0,120)
GREY = (192,192,192)
BLACK = (0,0,0)
DARK_BLUE = (0,0,66)

# change [1] and or [2] to modify search gradient
COLOUR_GRADIENT = [0,0,123]

# Button decoration
BUTTON_COLOUR = BLUE
BUTTON_TEXT_COLOUR = WHITE

# Button size
BUTTON_WIDTH = 186
BUTTON_HEIGHT = 50

# Button starting position
BUTTON_X = 807
BUTTON_Y = 100

# Node states
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

# Associates node state with a colour
COLOURS = {
    EMPTY_NODE : WHITE,
    START_NODE : RED, 
    END_NODE : GREEN, 
    WALL_NODE : GREY,
    FRONTIER_NODE : LIGHTBLUE,
    SEARCHED_NODE : BLUE,
    PATH_NODE : WHITE
}