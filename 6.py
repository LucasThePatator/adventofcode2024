import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from functools import cache

test = False


def parse_inputs():
    if test:
        data_file_name = "data/6_test"
    else :
        data_file_name = "data/6"
    
    data = []
    with open(data_file_name, 'r') as data_file:
        for line in data_file.readlines():
            data.append(list((map(lambda c : {'.':0,'#':1,'^':2}[c], line[:-1]))))

    return np.array(data)

def first(data):

    y, x = np.argwhere(data == 2)[0]
    data[y, x] = 0
    direction = 0
    visited = np.zeros((*data.shape, 4), dtype=np.int32)
    while True:
        if direction == 0:
            wall = np.argwhere(data[:y, x])
            if len(wall) == 0:
                visited[:(y+1), x, 0] = 1
                break
            else:
                visited[(wall[-1][0]+1):(y+1), x, 0] = 1
                y = wall[-1][0] + 1

        if direction == 1:
            wall = np.argwhere(data[y, x:])
            if len(wall) == 0:
                visited[y, x:, 1] = 1
                break
            else:
                visited[y, x:(x+wall[0][0]), 1] = 1
                x += wall[0][0] - 1

        if direction == 2:
            wall = np.argwhere(data[y:, x])
            if len(wall) == 0:
                visited[y:, x, 2] = 1
                break
            else:
                visited[y:(y+wall[0][0]), x, 2] = 1
                y += wall[0][0] - 1

        if direction == 3:
            wall = np.argwhere(data[y, :x])
            if len(wall) == 0:
                visited[y, :(x+1), 3] = 1
                break
            else:
                visited[y, (wall[-1][0]+1):(x+1), 3] = 1
                x = wall[-1][0] + 1

        direction = (direction + 1) % 4
  
        if visited[y, x, direction] == 1:
            break

    print(np.count_nonzero(np.sum(visited, axis=2)))

ugly_data = None

def new_pos(x, y, direction):
    global ugly_data
    if direction == 0:
        wall = np.argwhere(ugly_data[:y, x])
        if len(wall) == 0:
            return None, None, None
        else:
            y = wall[-1][0] + 1

    if direction == 1:
        wall = np.argwhere(ugly_data[y, x:])
        if len(wall) == 0:
            return None, None, None
        else:
            x += wall[0][0] - 1

    if direction == 2:
        wall = np.argwhere(ugly_data[y:, x])
        if len(wall) == 0:
            return None, None, None
        else:
            y += wall[0][0] - 1

    if direction == 3:
        wall = np.argwhere(ugly_data[y, :x])
        if len(wall) == 0:
            return None, None, None
        else:
            x = wall[-1][0] + 1
    direction = (direction + 1) % 4

    return x, y, direction

def check_loop():
    global ugly_data
    y, x = np.argwhere(ugly_data == 2)[0]
    ugly_data[y, x] = 0
    direction = 0
    visited = {(x, y, direction)}
    while True:
        x, y, direction = new_pos(x, y, direction)
        if x == None:
            return 0

        if (x, y, direction) in visited:
            return 1

        visited.add((x, y, direction))

def second(data):
    global ugly_data
    total = 0
    rows, cols = data.shape
    for y in range(rows):
        for x in range(cols):
            if data[y, x] == 0:
                ugly_data = np.copy(data)
                ugly_data[y, x] = 1

                total += check_loop()

    print(total)

if __name__ == "__main__":
    data = parse_inputs()
    first(np.copy(data))
    second(data)
