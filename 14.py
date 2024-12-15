# %%
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.animation as animation
test = False

width, height = 11, 7

def parse_inputs():
    global width
    global height
    if test:
        data_file_name = "data/14_test"
        width, height = 11, 7

    else :
        data_file_name = "data/14"
        width, height = 101, 103


    positions = []
    speeds = []
 
    with open(data_file_name, 'r') as data_file:
        for l in data_file.readlines():
            p, v = l.split(' ')
            px, py = p.split(',')
            p = [int(px[2:]), int(py)]

            positions.append(p)
            vx, vy = v.split(',')
            v = [int(vx[2:]), int(vy)]
            speeds.append(v)
            pass

    return np.array(positions).transpose(), np.array(speeds).transpose()

def make_image(positions):
    image = np.zeros((height, width))    
    image[positions[1,:], positions[0, :]] = 255

    return image

def first(data):
    positions, speeds = data
    positions = np.mod(positions + speeds*100, [[width], [height]])
    score = np.count_nonzero(np.logical_and(positions[0, :] < width // 2, positions[1, :] < height // 2))
    score *= np.count_nonzero(np.logical_and(positions[0, :] > width // 2, positions[1, :] < height // 2))
    score *= np.count_nonzero(np.logical_and(positions[0, :] < width // 2, positions[1, :] > height // 2))
    score *= np.count_nonzero(np.logical_and(positions[0, :] > width // 2, positions[1, :] > height // 2))

    print(score)

    image = make_image(positions)
    #plt.matshow(image)
    #plt.show()

def second(data):
    positions, speeds = data
    max_it = 10000
    
    pos_list = []
    stds = np.zeros((2, max_it))
    for i in range(max_it):
        positions = np.mod(positions + speeds, [[width], [height]])
        pos_list.append(positions)
        std = np.std(positions, axis=1)
        stds[:, i] = std

    tr = stds[0]+stds[1]
    tree_i = np.argmin(tr)
    image = make_image(pos_list[tree_i])
    plt.matshow(image)
    plt.show()

    print(tree_i + 1)

if __name__ == "__main__":

    data = parse_inputs()
# %%
    first(data)
# %%
    second(data)


# %%
