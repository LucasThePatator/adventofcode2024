
import numpy as np
from tqdm import trange
from functools import cache, lru_cache
import cv2 as cv
test = False

def parse_inputs():
    if test:
        data_file_name = "data/12_test"
    else :
        data_file_name = "data/12"

    data = []
 
    with open(data_file_name, 'r') as data_file:
        for line in data_file.readlines():
            if line == '\n':
                continue
            data.append(list(map(ord, list(line[:-1]))))

    data = np.array(data, dtype=np.int64)
    return data - 65

def nb_contour(row, col, data, value):
    
    if data[row][col] != value:
        return 0
    p = int(row == 0) + int(row == data.shape[0] - 1) + int(col == 0) + int(col == data.shape[1] - 1)
    p +=  int(row > 0 and data[row-1][col] != value)
    p +=  int(row < data.shape[0] -1 and data[row+1][col] != value)
    p +=  int(col > 0 and data[row][col-1] != value)
    p +=  int(col < data.shape[1] - 1 and data[row][col+1] != value)

    return p

def compute_peri(image, label):
    p = 0
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            p += nb_contour(i, j, image, label)

    return p


def compute_sides(image, label):
    p = 0
    #horizontal
    above = False
    under = False
    for col in range(image.shape[1]):
        if image[0,col] != label:
            above=False
            under=False
        if image[0,col] == label and not above:
            p += 1
            above = True

        if image.shape[0] > 1:
            if image[1,col] == label:
                under = False
            elif image[0,col] == label and not under:
                p += 1
                under = True

    for row in range(1, image.shape[0] - 1):
        above = False
        under = False
        for col in range(image.shape[1]):
            if image[row,col] != label:
                above=False
                under=False

            if image[row-1,col] == label:
                above = False
            elif image[row,col] == label  and not above:
                p += 1
                above = True

            if image[row+1,col] == label:
                under = False
            elif image[row,col] == label and not under:
                p += 1
                under = True

    above = False
    under = False
    for col in range(image.shape[1]):
        if image[image.shape[0]-1,col] != label:
            under=False
            above = False   
        if image[image.shape[0]-1,col] == label and not under:
            p += 1
            under = True

        if image.shape[0] > 1:
            if image[image.shape[0]-2,col] == label:
                above = False
            elif image[image.shape[0]-1,col] == label and not above:
                p += 1
                above = True

    return p

def first(data):
    rows, cols = data.shape
    total = 0
    for c in range(26):
        nbComp, labels, stats, centroid = cv.connectedComponentsWithStats((data == c).astype(np.uint8), connectivity=4)
        for comp in range(1, nbComp):
            t, l, h, w = stats[comp][cv.CC_STAT_TOP], stats[comp][cv.CC_STAT_LEFT ], stats[comp][cv.CC_STAT_HEIGHT ], stats[comp][cv.CC_STAT_WIDTH ]
            image = labels[t:t + h,l:l+w]
            p = compute_peri(image,comp)
            total += p*stats[comp][cv.CC_STAT_AREA]

    print(total)

def second(data):
    rows, cols = data.shape
    total = 0
    for c in range(26):
        nbComp, labels, stats, centroid = cv.connectedComponentsWithStats((data == c).astype(np.uint8), connectivity=4)
        for comp in range(1, nbComp):
            t, l, h, w = stats[comp][cv.CC_STAT_TOP], stats[comp][cv.CC_STAT_LEFT ], stats[comp][cv.CC_STAT_HEIGHT ], stats[comp][cv.CC_STAT_WIDTH ]
            image = labels[t:t + h,l:l+w]
            p = compute_sides(image, comp) + compute_sides(np.rot90(image), comp)
            total += p*stats[comp][cv.CC_STAT_AREA]

    print(total)

if __name__ == "__main__":
    data = parse_inputs()
    first(data)
    second(data)
