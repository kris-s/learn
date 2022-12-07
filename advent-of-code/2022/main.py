
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


def day_7(text):
    lines = text.splitlines()

    cwd = ['/']
    directories = {}

    for line in lines:
        if line[0] == '$':
            command = line.split()[1]
            if command == 'cd':
                destination = line.split()[2]
                if destination == '..' and len(cwd) > 1:
                    cwd.pop()
                elif cwd != [destination]:
                    cwd.append(destination)
            elif command == 'ls':
                pass
        else:
            dirname = '/'.join(cwd)
            entry = line
            if line.startswith('dir'):
                entry = dirname + '/' + line.split()[1]
            if dirname not in directories:
                directories[dirname] = {entry}
            else:
                directories[dirname].add(entry)

    def walk(contents):
        total = 0
        for entry in contents:
            if entry.startswith('/'):
                total += walk(directories[entry])
            else:
                total += int(entry.split()[0])
        return total

    dir_sizes = {}

    for directory, contents in directories.items():
        dir_sizes[directory] = walk(contents)

    for k, v in dir_sizes.items():
        print(k, v)

    limit = 100000
    total = 0

    for key, value in dir_sizes.items():
        if value <= limit:
            total += value

    print('part 1', total)

    total_space = 70000000
    target = 30000000
    total_unused = total_space - dir_sizes['/']
    print('total_unused', total_unused)

    could_work = []

    for key, value in dir_sizes.items():
        if value + total_unused >= target:
            could_work.append(value)

    print('part 2', min(could_work))


day_7(SAMPLE)
day_7(INPUT)
