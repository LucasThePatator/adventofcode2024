import numpy as np

from collections import OrderedDict
from functools import cmp_to_key
test = False

def parse_inputs():
    if test:
        data_file_name = "data/5_test"
    else :
        data_file_name = "data/5"

    data = []
    with open(data_file_name, 'r') as data_file:
        data_txt = data_file.read()

    pairs, updates = data_txt.split('\n\n')
    pairs = pairs.split('\n')
    pairs_list = []
    for pair in pairs:
        l, r = pair.split('|')
        pairs_list.append((int(l), int(r)))

    updates_list = []
    for update in updates.split('\n'):
        values = list(map(int, update.split(',')))
        updates_list.append(values)

    return pairs_list, updates_list


def first():
    pairs, updates = parse_inputs()

    total = 0
    for update in updates:
        d = dict([( v, i) for i, v in enumerate(update)])

        for pair in pairs:
            if pair[0] in d.keys() and pair[1] in d.keys():
                if d[pair[0]] > d[pair[1]]:
                    break
        else:
            total += update[len(update) // 2]
    
    print(total)

def sort_func(pairs, i1, i2):
    if (i1, i2) in pairs:
        return -1
    if (i2, i1) in pairs:
        return +1
    else:
        print("Nique")


def second():
    pairs, updates = parse_inputs()

    total = 0
    for update in updates:

        sorted_update = sorted(update, key=cmp_to_key(lambda i1, i2 : sort_func(pairs, i1, i2)))
        if sorted_update == update:
            continue
        else:
            total += sorted_update[len(update) // 2]
    
    print(total)
if __name__ == "__main__":
    first()
    second()