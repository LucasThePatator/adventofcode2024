
import numpy as np
from tqdm import trange
from functools import cache, lru_cache
import cv2 as cv
test = True

def parse_inputs():
    if test:
        data_file_name = "data/15_test"
    else :
        data_file_name = "data/15"

    data = []
 
    with open(data_file_name, 'r') as data_file:
        content = data_file.read()
        board, commands = content.split('\n\n')
        for line in board.split('\n'):
            if line == '\n':
                continue
            line = line.replace('#', '##')
            line = line.replace('O', '[]')
            line = line.replace('.', '..')
            line = line.replace('@', '@.')

            data.append(list(line))

    return np.array(data), commands.replace('\n', '')

def get_start_pos(board):
    return np.argwhere(board == '@')[0]

def inbounds(data, loc):
    return loc[0] >= 0 and loc[0] < data.shape[0] \
        and loc[1] >= 0 and loc[1] < data.shape[1]


def can_move_1(board, row, col, direction, preceding):
    if direction == '^':
        new_row, new_col = row-1, col
    elif direction == '>':
        new_row, new_col = row, col + 1 
    elif direction == 'v':
        new_row, new_col = row+1, col
    elif direction == '<':
        new_row, new_col = row, col-1


    if board[new_row][new_col] == '#':
        return False
    elif board[new_row][new_col] == 'O':
        preceding.append((new_row, new_col))
        return can_move(board, new_row, new_col, direction, preceding)
    elif board[new_row][new_col] == '.':
        preceding.append((new_row, new_col))
        return True

def compute_score(board):
    boxes = np.argwhere(board == 'O')
    return np.sum(100*boxes[:, 0] + boxes[:, 1])

def first(data):
    board, commands = data
    pos = get_start_pos(board)

    print(board)
    for c in commands:
        row, col = pos
        preceding = []
        if can_move_1(board, row, col, c, preceding):
            for i in range(1, len(preceding)):
                board[preceding[-i]] = board[preceding[-i - 1]]

            pos = preceding[0]
            board[preceding[0]] = '@'
            board[row, col] = '.'
            print(board)
            pass

    print(compute_score(board))

def can_move_2(board, row, col, direction, to_move):
    if direction == '^':
        new_row, new_col = row - 1, col
    elif direction == '>':
        new_row, new_col = row, col + 1 
    elif direction == 'v':
        new_row, new_col = row + 1, col
    elif direction == '<':
        new_row, new_col = row, col-1

    if direction == '<' or direction == '>':
        if board[new_row][new_col] == '#':
            return False
        elif board[new_row][new_col] == '[' or  board[new_row][new_col] == ']':
            to_move.append((new_row, new_col))
            return can_move_2(board, new_row, new_col, direction, to_move)
        elif board[new_row][new_col] == '.':
            to_move.append((new_row, new_col))
            return True

    else:
        if board[new_row][new_col] == '#':
            return False
        elif board[new_row][new_col] == ']':
            to_move.append((new_row, new_col))
            to_move.append((new_row, new_col-1))
            return can_move_2(board, new_row, new_col, direction, to_move) and can_move_2(board, new_row, new_col-1, direction, to_move)
        elif board[new_row][new_col] == '[':
            to_move.append((new_row, new_col))
            to_move.append((new_row, new_col + 1))
            return can_move_2(board, new_row, new_col, direction, to_move) and can_move_2(board, new_row, new_col+1, direction, to_move)
        elif board[new_row][new_col] == '.':
            return True

def get_next(position, direction):
    if direction == '^':
        return position + np.array([-1, 0])
    elif direction == '>':
        return position + np.array([0, 1])
    elif direction == 'v':
        return position + np.array([1, 0])
    elif direction == '<':
        return position + np.array([0, -1])

def get_precursor(position, direction):
    if direction == '^':
        return position + np.array([1, 0])
    elif direction == '>':
        return position + np.array([0, -1])
    elif direction == 'v':
        return position + np.array([-1, 0])
    elif direction == '<':
        return position + np.array([0, 1])

def sort_positions(positions, direction):
    if direction == '^':
        return sorted(positions, key= lambda p : p[0])
    elif direction == '>':
        return sorted(positions, key= lambda p : -p[1])
    elif direction == 'v':
        return sorted(positions, key= lambda p : -p[0])
    elif direction == '<':
        return sorted(positions, key= lambda p : p[1])

def move_boxes(board, positions, direction):
    new_board = np.copy(board)
    positions = sort_positions(positions, direction)
    for p in positions:
        prec = get_precursor(p, direction)
        new_board[p] = board[prec[0],prec[1]]
        new_board[prec[0],prec[1]]='.'

    return new_board

def second(data):
    board, commands = data
    pos = get_start_pos(board)
    np.set_printoptions(linewidth = 120)

    print(board)
    for c in commands:
        row, col = pos
        to_move = []
        if can_move_2(board, row, col, c, to_move):    
            board = move_boxes(board, to_move, c)
            pos = get_next(pos, c)
            board[pos[0], pos[1]] = '@'
            board[row, col] = '.'
            print(board)
            pass

    print(compute_score(board))

if __name__ == "__main__":
    data = parse_inputs()
    #first(data)
    second(data)
