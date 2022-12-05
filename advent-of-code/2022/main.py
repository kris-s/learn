
from pathlib import Path
import re

print("\n🎄 It's time to save Christmas. 🎄")


def load(path):
    path = Path(path)
    return path.read_text()


def lines_to_objects(text, cls):
    contents = []
    for line in text.splitlines():
        if line:
            contents.append(cls(line))
    return contents


class Point:
    def __init__(self, line):
        x, y = line.split(',')
        self.x = int(x.strip())
        self.y = int(y.strip())

    def __repr__(self):
        return f'({self.x}, {self.y})'


SAMPLE = load('sample.txt')
INPUT = load('input.txt')


def day_5_a(text):
    def execute_instructions(cargo, instructions):
        for inst in instructions:
            moves, source, dest = map(int, re.findall(r'move (\d+) from (\d+) to (\d+)', inst)[0])
            for i in range(moves):
                crate = cargo[source-1].pop(0)
                cargo[dest-1].insert(0, crate)

    cargo = {}

    raw_crates = []
    instructions = []
    n_stacks = 0

    lines = text.splitlines()
    for i, line in enumerate(lines):


        if not line:
            n_stacks = max(map(int, lines[i-1].split()))
            raw_crates = lines[:i-1]
            instructions = lines[i+1:]

    cursor = 1
    for col in range(n_stacks):
        cargo[col] = []
        for line in raw_crates:
            if len(line) > cursor and line[cursor] != ' ':
                cargo[col].append(line[cursor])
        cursor += 4

    print('cargo:', cargo)
    print(instructions)
    execute_instructions(cargo, instructions)

    topline = []
    for k, v in cargo.items():
        print(k, v[0])
        topline.append(v[0])

    print(''.join(topline))


def day_5_b(text):
    def execute_instructions(cargo, instructions):
        for inst in instructions:
            moves, source, dest = map(int, re.findall(r'move (\d+) from (\d+) to (\d+)', inst)[0])

            crates = []
            for i in range(moves):
                crates.append(cargo[source-1].pop(0))

            for crate in reversed(crates):
                cargo[dest-1].insert(0, crate)

    cargo = {}

    raw_crates = []
    instructions = []
    n_stacks = 0

    lines = text.splitlines()
    for i, line in enumerate(lines):


        if not line:
            n_stacks = max(map(int, lines[i-1].split()))
            raw_crates = lines[:i-1]
            instructions = lines[i+1:]

    cursor = 1
    for col in range(n_stacks):
        cargo[col] = []
        for line in raw_crates:
            if len(line) > cursor and line[cursor] != ' ':
                cargo[col].append(line[cursor])
        cursor += 4

    print('cargo:', cargo)
    print(instructions)
    execute_instructions(cargo, instructions)

    topline = []
    for k, v in cargo.items():
        print(k, v[0])
        topline.append(v[0])

    print(''.join(topline))



    # print(n_stacks)
    # print(raw_crates)



day_5_b(SAMPLE)
day_5_b(INPUT)
