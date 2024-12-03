from pathlib import Path


def load(path):
    path = Path(path)
    return path.read_text()

# content = load('example.txt')
content = load('input.txt')


def safe(numbers):
    deltas = []

    for i, n in enumerate(numbers):
        if i == 0:
            continue
        deltas.append(n - numbers[i-1])

    for d in deltas:
        if d == 0:
            return False

    first = deltas[0]

    if first < 0:
        for d in deltas:
            if d > 0:
                return False
    else:
        for d in deltas:
            if d < 0:
                return False

    for d in deltas:
        if abs(d) > 3:
            return False

    return True


def safe2(numbers):
    if safe(numbers):
        return True

    for i in range(len(numbers)):
        new = list(numbers)
        new.pop(i)

        if safe(new):
            return True
    
    return False


part_1 = 0
part_2 = 0

for line in content.splitlines():
    numbers = [int(n) for n in line.split()]

    if safe(numbers):
        part_1 += 1

    if safe2(numbers):
        part_2 += 1


print('part one:', part_1)
print('part two:', part_2)
