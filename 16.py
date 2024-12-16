
import numpy as np
from tqdm import trange
from functools import cache, lru_cache
import cv2 as cv
test = False

def parse_inputs():
    if test:
        data_file_name = "data/16_test"
    else :
        data_file_name = "data/16"

    data = []
 
    with open(data_file_name, 'r') as data_file:
        for line in data_file.readlines():
            if line == '\n':
                continue
            data.append(list(line[:-1]))

    data = np.array(data)
    return data

def get_pos(board, val):
    return np.argwhere(board == val)[0]

def inbounds(data, loc):
    return loc[0] >= 0 and loc[0] < data.shape[0] \
        and loc[1] >= 0 and loc[1] < data.shape[1]

def get_neighbours1(board, pos):
    ret = []
    t_vecs = [np.array([0, 1, 0]), np.array([1, 0, 0]), np.array([0, -1, 0]), np.array([-1, 0, 0])] #
    
    forward = pos + t_vecs[pos[2]]
    if board[forward[0], forward[1]] != '#':
        ret.append(forward)

    #rotate
    rot1 = np.copy(pos)
    rot2 = np.copy(pos)
    rot1[2] = (rot1[2] + 1) % 4
    rot2[2] = (rot2[2] - 1) % 4
    ret.extend([rot1, rot2])

    return ret

def dijkstra(board, start, end):
    dist = np.full((*board.shape, 4), 2**63, dtype=np.uint64) #E, D, W, U
    prev = {(*start, 0) : None}
    dist[*start, 0] = 0
    candidate_list = [np.array([*start, 0])]

    while len(candidate_list) > 0:
        candidate_list.sort(key=lambda c : dist[*c])
        new_pos = candidate_list.pop(0)

        new_neigbours = get_neighbours1(board, new_pos)
        for neighbour in new_neigbours:
            if neighbour[2] == new_pos[2]:
                new_dist = dist[*new_pos] + 1
            else:
                new_dist = dist[*new_pos] + 1000
            if new_dist < dist[*neighbour]:
                dist[*neighbour] = new_dist
                candidate_list.append(neighbour)
                prev[(neighbour[0],neighbour[1],neighbour[2])] = [(new_pos[0],new_pos[1],new_pos[2])]
            elif new_dist == dist[*neighbour]:
                prev[(neighbour[0],neighbour[1],neighbour[2])].append((new_pos[0],new_pos[1],new_pos[2]))

    last_position = np.argmin(dist[*end, :])
    return (*end, last_position), np.min(dist[*end, 3]), prev

def first(data):
    start_pos = get_pos(data, 'S')
    end_pos = get_pos(data, 'E')
    last_pos, dist, prev = dijkstra(data, start_pos, end_pos)
    print(dist)
    return last_pos, prev

def second(data, last_pos, prev):
    on_path = {(last_pos[0], last_pos[1])}
    current_tiles = [last_pos]
    while len(current_tiles) > 0:
        current_tile = current_tiles.pop(0)
        if current_tile is not None:
            on_path.add((current_tile[0], current_tile[1]))
            if prev[current_tile] is not None:
                current_tiles.extend(prev[current_tile])

    print(len(on_path))

if __name__ == "__main__":
    data = parse_inputs()
    last_pos, prev = first(data)
    second(data, last_pos, prev)
