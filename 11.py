
import numpy as np
from tqdm import trange
from functools import cache, lru_cache
test = False

def parse_inputs():
    if test:
        data_file_name = "data/11_test"
    else :
        data_file_name = "data/11"

    data = []
 
    with open(data_file_name, 'r') as data_file:
        data = list(map(int, data_file.read().split()))

    data = np.array(data, dtype=np.int64)
    return data

@cache
def it(number):
    if number == 0:
        return [1]
    elif len(str(number)) % 2 == 0:
        n_str = str(number)
        l = len(n_str)
        return [int(n_str[:(l//2)]), int(n_str[(l//2):])]
    else:
        return [number*2024]

def first(data):
    numbers = data
    new_numbers = []
    for i in range(25):
        for number in numbers:
            new_numbers.extend(it(number))
            
        numbers = new_numbers
        new_numbers = []
    
    print(len(numbers))

@cache
def rec_it(number, n):
    if n == 75:
        return 1

    if number == 0:
        return rec_it(1, n+1)

    elif len(str(number)) % 2 == 0:
        n_str = str(number)
        l = len(n_str)
        return rec_it(int(n_str[:(l//2)]), n+1)+ rec_it(int(n_str[(l//2):]), n+1)
    else:
        return rec_it(number*2024, n+1)

def second(data):
    total = 0
    for n in data:
        total += rec_it(n, 0)

    print(total)

if __name__ == "__main__":
    data = parse_inputs()
    first(data)
    second(data)
