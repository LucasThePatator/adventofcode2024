
import numpy as np
from functools import cache

test = False

def parse_inputs():
    if test:
        data_file_name = "data/7_test"
    else :
        data_file_name = "data/7"

    targets, numbers = [], []
 
    with open(data_file_name, 'r') as data_file:
        for line in data_file.readlines():
            if line == '\n':
                continue
            tokens = line.split(':')
            targets.append(int(tokens[0]))
            numbers.append(tuple(map(int, tokens[1].split())))

    return targets, numbers

def check_op(target, current, numbers, op):
    if current > target:
        return False

    if current > target:
        return False
    if len(numbers) == 0:
        if current == target:
            return True
            
        return False

    if op == '+':
        return check_op(target, current + numbers[0], numbers[1:], '+') or check_op(target, current + numbers[0], numbers[1:], '*')
   
    elif op == '*':
        return check_op(target, current * numbers[0], numbers[1:], '+') or check_op(target, current * numbers[0], numbers[1:], '*')

def first(data):
    total = 0
    for target, numbers in zip(*data):
        if check_op(target, numbers[0], numbers[1:], '+') or check_op(target, numbers[0], numbers[1:], '*'):
            total += target

    print(total)

def cat(i1, i2):
    return int(str(i1) + str(i2))

def check_op2(target, current, numbers, op):
    if current > target:
        return False
    if len(numbers) == 0:
        if current == target:
            return True

        return False

    if op == '+':
        return check_op2(target, current + numbers[0], numbers[1:], '+') \
            or check_op2(target, current + numbers[0], numbers[1:], '*') \
            or check_op2(target, current + numbers[0], numbers[1:], '||')
   
    elif op == '*':
        return check_op2(target, current * numbers[0], numbers[1:], '+') \
            or check_op2(target, current * numbers[0], numbers[1:], '*') \
            or check_op2(target, current * numbers[0], numbers[1:], '||')

    elif op == '||':
        return check_op2(target, cat(current,  numbers[0]), numbers[1:], '+') \
            or check_op2(target, cat(current,  numbers[0]), numbers[1:], '*') \
            or check_op2(target, cat(current,  numbers[0]), numbers[1:], '||')


def second(data):
    total = 0
    for target, numbers in zip(*data):
        if check_op2(target, numbers[0], numbers[1:], '+') \
        or check_op2(target, numbers[0], numbers[1:], '*') \
        or check_op2(target, numbers[0], numbers[1:], '||'):
            total += target

    print(total)

if __name__ == "__main__":
    data = parse_inputs()
    first(data)
    second(data)
