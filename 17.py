
import numpy as np
from tqdm import trange
from functools import cache, lru_cache
import cv2 as cv
test = False
test_i = 6

A = 0
B = 0
C = 0

def parse_inputs():
    if test:
        data_file_name = f"data/17_test{test_i}"
    else :
        data_file_name = "data/17"

    A = B = C = 0    

    with open(data_file_name, 'r') as data_file:
        content = data_file.read()
        registers, commands = content.split('\n\n')
        registers = registers.split('\n')
        A = int(registers[0][11:])
        B = int(registers[1][11:])
        C = int(registers[2][11:])

        commands = np.array(list(map(int, commands[9:-1].split(','))))

    return commands, (A, B, C)

class Emulator:

    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C

        self.stack_pointer = 0

    def get_combo_value(self, operand):
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.A
        elif operand == 5:
            return self.B
        elif operand == 6:
            return self.C
        else:
            return None

    def run_code(self, code):
        outputs = []
        code_len = code.shape[0]
        while self.stack_pointer < code_len:
            output = self.process_command(code[self.stack_pointer], code[self.stack_pointer + 1])
            if output is not None:
                outputs.append(output)

        print(','.join(map(str, outputs)))

    def find_code_quine(self, code):
        code_len = code.shape[0]            
        stack = [(code_len-1, 0)]

        good_As = []

        while stack:
            position, a = stack.pop(0)
            for bit_val in range(8):
                test_A = (a << 3) + bit_val
                self.A = test_A
                outputs = []
                self.stack_pointer=0
                while self.stack_pointer < code_len:
                    output = self.process_command(code[self.stack_pointer], code[self.stack_pointer + 1])
                    if output is not None:
                        outputs.append(output)

                if len(outputs) == len(code[position:]) and np.all(outputs == code[position:]):
                    stack.append((position - 1, test_A))

                if position == 0 and len(outputs) == code_len and np.all(outputs == code):
                    good_As.append(test_A)

        print(min(good_As))
    

    def process_command(self, opcode, operand ):
        if opcode == 0:
            val = self.get_combo_value(operand)
            self.A = int(self.A / (2**val))
            self.stack_pointer += 2
            return
        elif opcode == 1:
            self.B ^= operand
            self.stack_pointer += 2
            return
        elif opcode == 2:
            self.B = self.get_combo_value(operand) % 8
            self.stack_pointer += 2
            return
        elif opcode == 3:
            if self.A != 0:
                self.stack_pointer = operand
            else:
                self.stack_pointer += 2
            return
        elif opcode == 4:
            self.B ^= self.C
            self.stack_pointer += 2
            return
        elif opcode == 5:
            output = self.get_combo_value(operand) % 8
            self.stack_pointer += 2
            return output
        elif opcode == 6:
            val = self.get_combo_value(operand)
            self.B = int(self.A / (2**val))
            self.stack_pointer += 2
            return
        elif opcode == 7:
            val = self.get_combo_value(operand)
            self.C = int(self.A / (2**val))
            self.stack_pointer += 2
            return

def first(data):
    emulator = Emulator(*data[1])
    emulator.run_code(data[0])
    print(data)

def second(data):

    emulator = Emulator(0, 0, 0)
    ret = emulator.find_code_quine(data[0])
  

if __name__ == "__main__":
    data = parse_inputs()
    first(data)
    second(data)
