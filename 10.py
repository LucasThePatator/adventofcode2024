
import numpy as np
test = False

def parse_inputs():
    if test:
        data_file_name = "data/10_test"
    else :
        data_file_name = "data/10"

    data = []
 
    with open(data_file_name, 'r') as data_file:
        for line in data_file.readlines():
            data.append(list(map(int, list(line[:-1]))))

    data = np.array(data, dtype=np.int32)
    return data

def ib(p, data):
    return 0 <= p[0] < data.shape[0] and 0 <= p[1] < data.shape[1]

def first(data):
    top = np.array([0, -1])
    right = np.array([1, 0])
    bottom = np.array([0, 1])
    left = np.array([-1, 0])

    heads = np.argwhere(data == 0)
    total = 0
    for head in heads:
        current_positions = [head]
        new_positions = []
        for i in range(1, 10):
            for p in current_positions:
                t = p+top
                r = p+right
                b = p+bottom
                l = p+left

                posl = [t,r,b,l]

                for pos in posl:
                    if ib(pos, data) and data[pos[0], pos[1]] == i:
                        new_positions.append(pos)
            
            current_positions = new_positions
            new_positions = []

        tailset = set()
        for p in current_positions:
            tailset.add((p[0], p[1]))

        total += len(tailset)

    print(total)

def second(data):
    top = np.array([0, -1])
    right = np.array([1, 0])
    bottom = np.array([0, 1])
    left = np.array([-1, 0])

    heads = np.argwhere(data == 0)
    total = 0
    for head in heads:
        current_positions = [head]
        new_positions = []
        for i in range(1, 10):
            for p in current_positions:
                t = p+top
                r = p+right
                b = p+bottom
                l = p+left

                posl = [t,r,b,l]

                for pos in posl:
                    if ib(pos, data) and data[pos[0], pos[1]] == i:
                        new_positions.append(pos)
            
            current_positions = new_positions
            new_positions = []

        total += len(current_positions)

    print(total)

if __name__ == "__main__":
    data = parse_inputs()
    first(data)
    second(data)
