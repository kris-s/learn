
from pathlib import Path
from collections import Counter

def load(path):
    path = Path(path)
    return path.read_text()

# content = load('example.txt')
content = load('input.txt')

print(content)

left = []
right = []

for line in content.splitlines():
    a, b = line.split()
    print(a, b)
    left.append(int(a))
    right.append(int(b))

left.sort()
right.sort()

total = 0
for i, value in enumerate(left):
    distance = abs(value - right[i])
    total += distance

print('part 1:', total)

counts = Counter(right)

part_two = 0

for value in left:
    part_two += value * counts[value]

print('part 2:', part_two)
