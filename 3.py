
import re

def first():
    with open('data/3', 'r') as data_file:
        string = data_file.read()

    prog = re.compile(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)')
    groups = re.findall(prog, string)

    total = 0
    for a, b in groups:
        total += int(a)*int(b)

    print(total)

def second():
    with open('data/3', 'r') as data_file:
        string = data_file.read()

    prog_remove = re.compile(r"don't\(\).*?do(?!n't)\(\)", flags=re.DOTALL)
    new_string, nb_subs = re.subn(prog_remove, "", string, count=0)
    index = new_string.find("don't()")

    new_string = new_string[:index]

    prog = re.compile(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)')
    groups = re.findall(prog, new_string)

    total = 0
    for a, b in groups:
        total += int(a)*int(b)

    print(total)

if __name__ == "__main__":
    first()
    second()