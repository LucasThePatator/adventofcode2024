
test = False
import numpy as np

def parse_inputs():
    if test:
        data_file_name = "data/1_test"
    else :
        data_file_name = "data/1"

    with open(data_file_name, 'r') as data_file:
        data = np.genfromtxt(data_file, dtype=np.int32)

    return data

def first():
    data = parse_inputs()
 
    data[:, 0].sort()
    data[:, 1].sort()

    print(np.sum(np.abs(data[:, 0]- data[:, 1])))

def second():
    data = parse_inputs()

    total = 0
    ll = list(data[:, 0])
    lr = list(data[:, 1])
    for n in ll:
        total += n*lr.count(n)

    print(total)

if __name__ == "__main__":
    first()
    second()
