
test = False
import numpy as np

def parse_inputs():
    if test:
        data_file_name = "data/2_test"
    else :
        data_file_name = "data/2"

    data = []
    with open(data_file_name, 'r') as data_file:
        for l in data_file.readlines():
            data.append(np.array(list(map(lambda t: int(t), l.split())), dtype=np.int32))

    return data

def first():
    data = parse_inputs()

    count = 0
    for report in data:
        diff = report[1:] - report[:-1]
        invalid = not np.logical_or(np.all(diff > 0), np.all(diff < 0))
        if invalid : 
            continue
        invalid = np.logical_or(np.abs(diff) < 1, np.abs(diff) > 3)
        if np.any(invalid):
            continue
        count += 1

    print(count)


def check_valid(array):
    diff = array[1:] - array[:-1]
    invalid = not np.logical_or(np.all(diff > 0), np.all(diff < 0))
    if invalid : 
        return False
    invalid = np.logical_or(np.abs(diff) < 1, np.abs(diff) > 3)
    if np.any(invalid):
        return False
    
    return True

def second():
    data = parse_inputs()

    count = 0
    for report in data:

        if check_valid(report):
            count += 1
            continue
        
        for i in range(0, len(report)):
            local_data = np.delete(report, i)
            if check_valid(local_data):
                count += 1
                break
    
    print(count) 

if __name__ == "__main__":
    first()
    second()