import numpy as np
import math
ROW = 5

def create_map():
    map = []
    for x in range(ROW):
        for y in range(ROW):
            map.append([x,y])
    return map

def map_value(value):
    mapped_value = 127 + (value * 127)
    return math.floor(mapped_value)

def get_value(point, offset = 1):
    x = point[0]
    y = point[1]
    offset = offset
    return map_value(math.sin(x + y + offset))

def create_noise_map(map):
    noise_map = []
    for point in map:
        noise_map.append(get_value(point))
    return noise_map

def main():
    map = create_map()
    noise_map = create_noise_map(map)
    noise_array = np.array(noise_map)
    print(noise_array.reshape((ROW,ROW)))


if __name__ == '__main__':
    main()
