
test = False
import numpy as np

def parse_inputs():
    if test:
        data_file_name = "data/1_test"
    else :
        data_file_name = "data/1"

    ll = []
    lr = []

    with open(data_file_name, 'r') as data_file:
        file_content = data_file.read()
        lines = file_content.split('\n')
        for l in lines:
            tokens = l.split('  ')
            ll.append(int(tokens[0]))
            lr.append(int(tokens[1]))

    return ll, lr

def first():
    ll, lr = parse_inputs()

    ll.sort()
    lr.sort()

    ll = np.array(ll)
    lr = np.array(lr)

    print(np.sum(np.abs(lr-ll)))

def second():
    ll, lr = parse_inputs()

    total = 0
    for n in ll:
        total += n*lr.count(n)

    print(total)

if __name__ == "__main__":
    second()
