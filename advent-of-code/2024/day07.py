from pathlib import Path
import itertools
import random

def load(path):
    path = Path(path)
    return path.read_text()

# content = load('example.txt')
content = load('input.txt')

def parse():
    lines = []

    for line in content.splitlines():
        target, tail = line.split(':')

        values = [int(v) for v in tail.split()]
        lines.append((int(target), values))

    return lines

content = parse()
print(content)


ADD = '+'
MUL = '*'
CAT = '|'
OPS = [ADD, MUL, CAT]


TABLE = {}

def permutations(length):
    if length in TABLE:
        return TABLE[length]

    perms = []

    for i in range(1000000):
        p = []
        for _ in range(length):
            p.append(random.choice(OPS))
        perms.append(tuple(p))

    TABLE[length] = set(perms)
    return perms


def check(target, source_values):
    # for combo in itertools.combinations_with_replacement(OPS, len(source_values) - 1):
    for combo in permutations(len(source_values) - 1):
        values = list(source_values)
        # print(combo)
        r = values.pop(0)
        for i, op in enumerate(combo):
            if op == ADD:
                r += values[i]
            elif op == MUL:
                r *= values[i]
            else:
                r = int(str(r) + str(values[i]))
        if r == target:
            return True

    return False

total = 0

for target, source_values in content:
    if check(target, source_values):
        print('target found', target)
        total += target

print('p1', total)


# print(check(292, [11, 6, 16, 20]))


# 1248779017261
# 1260333054159

# p2 150299506253388
#    152711512114057 (too low!)
#    162042343638683
