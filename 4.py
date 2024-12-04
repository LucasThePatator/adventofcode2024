import numpy as np

test = False

xmas_val = ord('X') + 256 * ord('M') + (256**2) * ord('A' )+ (256**3) * ord('S')
xmas_val_inv = ord('S') + 256 * ord('A') + (256**2) * ord('M' )+ (256**3) * ord('X')

x_mas_val = ord('M') + 256 * ord('S') + (256**2) * ord('A' ) + (256**3) * ord('M') + (256**4) * ord('S')
x_mas_val2 = ord('S') + 256 * ord('M') + (256**2) * ord('A' ) + (256**3) * ord('S') + (256**4) * ord('M')
x_mas_val3 = ord('S') + 256 * ord('S') + (256**2) * ord('A' ) + (256**3) * ord('M') + (256**4) * ord('M')
x_mas_val4 = ord('M') + 256 * ord('M') + (256**2) * ord('A' ) + (256**3) * ord('S') + (256**4) * ord('S')

def parse_inputs():
    if test:
        data_file_name = "data/4_test"
    else :
        data_file_name = "data/4"

    data = []
    with open(data_file_name, 'r') as data_file:
        for line in data_file.readlines():
            data.append(list(map(ord, line[:-1])))

    data = np.array(data, dtype=np.int64)
    return data

def check_horizontal(arr):
    test_data = arr[:, 0:-3] + 256*arr[:, 1:-2] + (256**2)*arr[:, 2:-1] + (256**3)*arr[:, 3:]
    val = np.count_nonzero(test_data == xmas_val)
    test_data = arr[:, 3:] + 256*arr[:, 2:-1] + (256**2)*arr[:, 1:-2] + (256**3)*arr[:, 0:-3]

    return val + np.count_nonzero(test_data == xmas_val)

def check_diag(arr):
    test_data = arr[0:-3, 0:-3] + 256*arr[1:-2, 1:-2] + (256**2)*arr[2:-1, 2:-1] + (256**3)*arr[3:, 3:]
    val = np.count_nonzero(test_data == xmas_val)
    val += np.count_nonzero(test_data == xmas_val_inv)

    test_data = arr[0:-3, 3:] + 256*arr[1:-2, 2:-1] + (256**2)*arr[2:-1, 1:-2] + (256**3)*arr[3:, 0:-3]
    val += np.count_nonzero(test_data == xmas_val_inv)
    return val + np.count_nonzero(test_data == xmas_val)

def check_xmas(arr):
    test_data = arr[0:-2, 0:-2] + 256*arr[0:-2, 2:] + (256**2)*arr[1:-1, 1:-1] + (256**3)*arr[2:, 0:-2] + (256**4)*arr[2:, 2:]
    val = np.count_nonzero(test_data == x_mas_val) + np.count_nonzero(test_data == x_mas_val2) + np.count_nonzero(test_data == x_mas_val3) + np.count_nonzero(test_data == x_mas_val4)
    return val

def first():
    data = parse_inputs()

    total = check_horizontal(data)
    data = np.rot90(data)
    total += check_horizontal(data)
    total += check_diag(data)

    print(total)

def second():
    data = parse_inputs()
    print(check_xmas(data))

if __name__ == "__main__":
    first()
    second()