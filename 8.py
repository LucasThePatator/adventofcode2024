
import numpy as np
from functools import cache
import itertools
test = False

def parse_inputs():
    if test:
        data_file_name = "data/8_test"
    else :
        data_file_name = "data/8"

    data = []
 
    with open(data_file_name, 'r') as data_file:
        for line in data_file.readlines():
            if line == '\n':
                continue
            data.append(tuple(map(ord, list(line[:-1]))))

    data = np.array(data, dtype=np.int32)
    data[data== ord('.')] = 0
    return data

def inbounds(data, loc):
    return loc[0] >= 0 and loc[0] < data.shape[0] \
        and loc[1] >= 0 and loc[1] < data.shape[1]

def first(data):

    antinodes = np.zeros_like(data)
    antenna_values = np.unique(data)

    for value in antenna_values[1:]:
        antenna_locs = np.argwhere(data == value)
        for loc1, loc2 in itertools.combinations(antenna_locs, 2):
            antinode_pos = 2*loc2 - loc1
            if inbounds(data, antinode_pos):
                antinodes[antinode_pos[0], antinode_pos[1]] = 1

            antinode_pos = 2*loc1 - loc2
            if inbounds(data, antinode_pos):
                antinodes[antinode_pos[0], antinode_pos[1]] = 1

    print(np.count_nonzero(antinodes))

def second(data):

    antinodes = np.zeros_like(data)
    antenna_values = np.unique(data)

    for value in antenna_values[1:]:
        antenna_locs = np.argwhere(data == value)
        for loc1, loc2 in itertools.combinations(antenna_locs,2):

            diff = loc2 - loc1
            d = np.gcd(diff[0], diff[1])
            delta = diff // d
            antinode_pos = np.copy(loc1)
            while inbounds(data, antinode_pos):
                antinodes[antinode_pos[0], antinode_pos[1]] = 1
                antinode_pos += delta

            antinode_pos = loc1 - delta
            while inbounds(data, antinode_pos):
                antinodes[antinode_pos[0], antinode_pos[1]] = 1
                antinode_pos -= delta

    print(np.count_nonzero(antinodes))

if __name__ == "__main__":
    data = parse_inputs()
    first(data)
    second(data)
