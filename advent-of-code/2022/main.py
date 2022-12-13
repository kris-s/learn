
import sys
from pathlib import Path
import re


print("\n🎄 It's time to save Christmas. 🎄")


def load(path):
    path = Path(path)
    return path.read_text()


SAMPLE = load('sample.txt')
INPUT = load('input.txt')


def day_13(text):
    lines = text.splitlines()
    pairs = []
    pair = []
    for line in lines:
        if line and len(pair) < 2:
            pair.append(eval(line))
            if len(pair) == 2:
                pairs.append(pair)
                pair = []


    def ordered(left, right):
        if isinstance(left, int) and isinstance(right, int):
            if left == right:
                return None
            else:
                return left < right
        elif isinstance(left, list) and isinstance(right, list):
            for i, val in enumerate(left):
                try:
                    right_val = right[i]
                except IndexError:
                    return False
                result = ordered(val, right_val)
                if result is None:
                    continue
                else:
                    return result
            return True
        elif isinstance(left, int) and isinstance(right, list):
            return ordered([left], right)
        elif isinstance(left, list) and isinstance(right, int):
            return ordered(left, [right])
        else:
            raise ValueError(f'not sure what to do with: {left} {right}')

    ordered_pairs = []
    for i, p in enumerate(pairs):
        left, right = p
        if ordered(left, right):
            ordered_pairs.append(i+1)

    print('part 1:', sum(ordered_pairs))

    def cmp(a, b):
        result = ordered(a, b)
        if result == True:
            return 1
        elif result == False:
            return -1
        else:
            return 0

    packets = []
    for line in lines:
        if line:
            packets.append(eval(line))

    div_1 = [[2]]
    div_2 = [[6]]
    packets.append(div_1)
    packets.append(div_2)

    from functools import cmp_to_key
    packets = sorted(packets, key=cmp_to_key(cmp), reverse=True)
    for i, p in enumerate(packets):
        print(i, p)

    a = packets.index(div_1) + 1
    b = packets.index(div_2) + 1
    print('part 2:', a, b, a * b)


day_13(SAMPLE)
day_13(INPUT)
