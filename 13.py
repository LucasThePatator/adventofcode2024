
import numpy as np
test = False

def parse_inputs():
    if test:
        data_file_name = "data/13_test"
    else :
        data_file_name = "data/13"

    data = []
 
    with open(data_file_name, 'r') as data_file:
        tokens1 = data_file.read().split('\n\n')
        for t in tokens1:
            lines = t.split('\n')
            _, _, X, Y = lines[0].split(' ')
            XA, YA = int(X[2:-1]), int(Y[2:])
            _, _, X, Y = lines[1].split(' ')
            XB, YB = int(X[2:-1]), int(Y[2:])
            _, X, Y = lines[2].split(' ')
            PX, PY = int(X[2:-1]), int(Y[2:])
            data.append((XA, YA, XB, YB, PX, PY))
            pass

    return data

def first(data):
    total = 0
    for arcade in data:
        det = arcade[0]*arcade[3] - arcade[1]*arcade[2]
        A = arcade[3]*arcade[4] - arcade[2]*arcade[5]
        B = -arcade[1]*arcade[4] + arcade[0]*arcade[5]
        if A % det != 0 or B%det != 0:
            continue

        A //= det
        B //= det

        total += A*3+B

    print(total)

def second(data):
    total = 0
    for arcade in data:
        PX = arcade[4] + 10000000000000
        PY = arcade[5] + 10000000000000
        det = arcade[0]*arcade[3] - arcade[1]*arcade[2]
        A = arcade[3]*PX - arcade[2]*PY
        B = -arcade[1]*PX + arcade[0]*PY
        if A % det != 0 or B%det != 0:
            continue

        A //= det
        B //= det

        total += A*3+B

    print(total)

if __name__ == "__main__":
    data = parse_inputs()
    first(data)
    second(data)
