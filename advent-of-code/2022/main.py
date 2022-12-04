
from pathlib import Path

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


def day_4(text):
    full = 0
    partial = 0

    for line in text.splitlines():
        a, b = line.split(',')

        a_lower, a_upper = a.split('-')
        a_set = set(range(int(a_lower), int(a_upper)+1))

        b_lower, b_upper = b.split('-')
        b_set = set(range(int(b_lower), int(b_upper)+1))

        if a_set.issubset(b_set) or b_set.issubset(a_set):
            full += 1

        if a_set & b_set:
            partial += 1

    print(full)
    print(partial)


day_4(SAMPLE)
day_4(INPUT)
