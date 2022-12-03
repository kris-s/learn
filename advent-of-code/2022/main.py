
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


def day_3(text):
    def item_value(item):
        if ord(item) - 96 > 0:
            return ord(item) - 96
        else:
            return ord(item) - 38

    items_of_interest = []
    for line in text.splitlines():
        split_at = int(len(line) / 2)
        left = line[:split_at]
        right = line[split_at:]

        common = list(set(left) & set(right))
        items_of_interest.append(common[0])

    print(sum(item_value(item) for item in items_of_interest))

    group_ids = []
    lines = text.splitlines()
    for i in range(0, len(lines), 3):
        one = set(lines[i])
        two = set(lines[i+1])
        thr = set(lines[i+2])
        common = list(set(one) & set(two) & set(thr))
        group_ids.append(common[0])

    print(sum(item_value(item) for item in group_ids))


day_3(SAMPLE)
day_3(INPUT)
