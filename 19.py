
import numpy as np
from tqdm import trange
from functools import cache
import cv2 as cv
test = False   

def parse_inputs():
    global grid_size, nb_bytes
    if test:
        data_file_name = "data/19_test"
    else :
        data_file_name = "data/19"

    data = []
 
    with open(data_file_name, 'r') as data_file:
        towels, patterns = data_file.read().split('\n\n')
        towels = towels.split(', ')
        patterns = patterns.split('\n')[:-1]

    return tuple(towels), patterns



@cache
def make_pattern_rec(pattern, towels):
    p_len = len(pattern)

    total = 0
    if p_len == 0:
        return 1

    for t_i, towel in enumerate(towels):
        if len(towel) > p_len:
            continue

        if towel == pattern[:len(towel)]:
            total += make_pattern_rec(pattern[len(towel):], towels)
        
    return total

def first(data):
    towels, patterns = data
    total = 0
    for p in patterns:
        total += int(make_pattern_rec(p, towels) > 0)
        pass

    print(total)

def second(data):
    towels, patterns = data
    total = 0
    for p in patterns:
        total += make_pattern_rec(p, towels)
        pass

    print(total)


if __name__ == "__main__":
    data = parse_inputs()
    first(data)
    second(data)
