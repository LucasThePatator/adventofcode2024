
import numpy as np
from tqdm import trange
from functools import cache
from itertools import combinations
import cv2 as cv
test = False  

def parse_inputs():
    global grid_size, nb_bytes
    if test:
        data_file_name = "data/20_test"
    else :
        data_file_name = "data/20"

    data = []
 
    with open(data_file_name, 'r') as data_file:
        for line in data_file.readlines():
            if line == '\n':
                continue
            data.append(list(line[:-1]))

    data = np.array(data)
    return data

def get_neighbours(board, pos):
    ret = []
    t_vecs = [np.array([0, 1]), np.array([1, 0]), np.array([0, -1]), np.array([-1, 0])] #
    pos = np.array([*pos])
    for t in t_vecs:
        test_pos = pos + t
        if board[*test_pos] != '#':
            ret.append((test_pos[0], test_pos[1]))

    return ret

def get_pos(board, val):
    return np.argwhere(board == val)[0]

def dijkstra(board, start, end):
    dist = np.full_like(board, -1 , dtype=np.int64)
    dist[*start] = 0
    candidate_list = [np.array(start)]

    while len(candidate_list) > 0:
        candidate_list.sort(key=lambda c : dist[*c])
        current_pos = candidate_list.pop(0)

        new_neigbours = get_neighbours(board, current_pos)
        for neighbour in new_neigbours:
            new_dist = dist[*current_pos] + 1
            if dist[*neighbour]< 0 or new_dist < dist[*neighbour]:
                dist[*neighbour] = new_dist
                candidate_list.append(neighbour)

    return dist

def manhattan(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def get_candidates(dist, pos):
    row, col = pos
    min_row = max(1, row-20)
    max_row = min(dist.shape[0] - 1, row+20) #included


    ret = []

    for new_row in range(min_row, max_row+1):
        delta = abs(row - new_row)
        min_col = max(1, col-20 + delta)
        max_col = min(dist.shape[1] - 1, col+20 - delta) #included

        for new_col in range(min_col, max_col+1):
            if dist[new_row, new_col] >= 0:
                ret.append((new_row, new_col))

    return ret


def first(data):
    start_pos = get_pos(data, 'S')
    end_pos = get_pos(data, 'E')
    dist = dijkstra(data, start_pos, end_pos)

    times_gained = []
    rows, cols = dist.shape
    for row in range(1, rows-1):
        for col in range(1, cols-1):
            if data[row, col] != '#':
                continue
            new_neigbours = get_neighbours(data, (row, col))
            for n1, n2 in combinations(new_neigbours, 2):
                if dist[*n1] >= 0 and dist[*n2] >= 0:
                    times_gained.append(abs(dist[*n1] - dist[*n2]) - 2)

    print(len(list(filter(lambda i : i >= 100, times_gained))))

def second(data):
    start_pos = get_pos(data, 'S')
    end_pos = get_pos(data, 'E')
    dist = dijkstra(data, start_pos, end_pos)

    times_gained = []
    rows, cols = dist.shape
    for row in range(1, rows-1):
        for col in range(1, cols-1):
            if data[row, col] == '#':
                continue

            candidates = get_candidates(dist, (row, col))
            for candidate in candidates:
                if manhattan((row, col), candidate) > 20:
                    print("Oh no")
                times_gained.append(dist[row, col] - dist[*candidate] - manhattan((row, col), candidate))

    print(len(list(filter(lambda i : i >= 100, times_gained))))


if __name__ == "__main__":
    data = parse_inputs()
    first(data)
    second(data)
