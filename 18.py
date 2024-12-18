
import numpy as np
from tqdm import trange
from functools import cache, lru_cache
import cv2 as cv
test = False  

grid_size = None
nb_bytes = None

def parse_inputs():
    global grid_size, nb_bytes
    if test:
        grid_size = 7
        nb_bytes = 12
        data_file_name = "data/18_test"
    else :
        grid_size = 71
        nb_bytes = 1024
        data_file_name = "data/18"

    data = []
 
    with open(data_file_name, 'r') as data_file:
        for line in data_file.readlines():
            if line == '\n':
                continue
            data.append(list(map(int, line.split(','))))

    data = np.array(data)
    return data

def inbounds(data, loc):
    return loc[0] >= 0 and loc[0] < data.shape[0] \
        and loc[1] >= 0 and loc[1] < data.shape[1]

def get_neighbours1(board, pos):
    ret = []
    t_vecs = [np.array([0, 1]), np.array([1, 0]), np.array([0, -1]), np.array([-1, 0])] #
    pos = np.array([*pos])
    for t in t_vecs:
        test_pos = pos + t
        if inbounds(board, test_pos) and board[*test_pos] == 0:
            ret.append((test_pos[0], test_pos[1]))


    return ret

def dijkstra1(board, start, end):
    dist = np.full_like(board, 2**63, dtype=np.uint64)
    dist[*start] = 0
    candidate_list = [np.array(start)]

    while len(candidate_list) > 0:
        candidate_list.sort(key=lambda c : dist[*c])
        current_pos = candidate_list.pop(0)

        new_neigbours = get_neighbours1(board, current_pos)
        for neighbour in new_neigbours:
            new_dist = dist[*current_pos] + 1
            if new_dist < dist[*neighbour]:
                dist[*neighbour] = new_dist
                candidate_list.append(neighbour)

            if neighbour == end:
                return True, new_dist

    return False, None

def first(data):
    start = 0, 0 #Y, X
    end = 70, 70
    if test:
        end = 6, 6
    grid = np.zeros((grid_size, grid_size))
    grid[data[:nb_bytes, 1], data[:nb_bytes, 0]] = 1
    _, min_dist = dijkstra1(grid, start, end)
    print(min_dist)

def second(data):
    start = 0, 0 #Y, X
    end = 70, 70
    min_bytes = 1024

    if test:
        end = 6, 6
        min_bytes = 12

    
    max_bytes = len(data)
    #binary search
    while min_bytes < max_bytes:
        nb_bytes = (min_bytes + max_bytes) // 2
        grid = np.zeros((grid_size, grid_size))
        grid[data[:nb_bytes, 1], data[:nb_bytes, 0]] = 1
        ret, min_dist = dijkstra1(grid, start, end)
        if ret:
            min_bytes = nb_bytes + 1
        else:
            max_bytes = nb_bytes

    print(data[nb_bytes-1])   


if __name__ == "__main__":
    data = parse_inputs()
    first(data)
    second(data)
