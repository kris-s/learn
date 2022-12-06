
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


def day_6(text):
    window = []
    for i, char in enumerate(text.strip()):
        window.insert(0, char)
        if len(window) > 14:
            window.pop()

        if len(set(window)) == 14:
            print(i+1)
            break


day_6(SAMPLE)
day_6(INPUT)
