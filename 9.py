
import numpy as np
test = False

def parse_inputs():
    if test:
        data_file_name = "data/9_test"
    else :
        data_file_name = "data/9"

    data = []
 
    with open(data_file_name, 'r') as data_file:
        return np.array(list(map(int, data_file.read()[:-1])), dtype=np.uint64)

def create_memory(layout):
    pointer = 0
    current_id = 0
    memory = np.zeros(np.sum(layout), dtype=np.int64)
    for i, val in enumerate(layout):
        if i%2 == 0:
            memory[pointer:(pointer+val)] = current_id
            current_id += 1
        else :
            memory[pointer:(pointer+val)] = -1

        pointer+=val

    return memory

def compute_sum(memory):
    memory[memory == -1] = 0
    return np.sum(np.arange(start=0, stop=memory.shape[0])*memory)

def first(data):
    memory = create_memory(layout=data)
    lp, rp = 0, memory.shape[0] - 1
    while True:
        lval = memory[lp]
        while lval >= 0:
            lp += 1
            lval = memory[lp]

        rval = memory[rp]
        while rval < 0:
            rp -= 1
            rval = memory[rp]

        if lp >= rp:
            break
        memory[lp] = memory[rp]
        memory[rp] = -1

    print(compute_sum(memory))    

def second(data):
    memory = create_memory(layout=data)
    rp = memory.shape[0] - 1

    while rp >= 0:
        rval = memory[rp]
        while rval < 0:
            rp -= 1
            if rp < 0:
                break
            rval = memory[rp]
        
        if rp < 0:
            break

        rp2 = rp-1
        while memory[rp2] == rval:
            rp2-=1

        li = rp - rp2

        lp = 0
        lp2 = 0
        lo = 0
        while lo < li and lp < memory.shape[0]:
            lp = lp2
            while memory[lp] >= 0:
                lp += 1
                if lp >= rp:
                    break

            if lp >= rp:
                break

            lp2 = lp

            if lp2 >= memory.shape[0]:
                break

            while memory[lp2] < 0:
                lp2 += 1
                if lp2 >= memory.shape[0]:
                    break
            
            if lp2 >= memory.shape[0]:
                break
            
            lo = lp2 - lp


        if lo >= li:
            memory[lp:(lp+li)] = memory[rp]
            memory[rp2+1:rp+1] = -1

        rp = rp2

    print(compute_sum(memory))

if __name__ == "__main__":
    data = parse_inputs()
    first(data)
    second(data)
