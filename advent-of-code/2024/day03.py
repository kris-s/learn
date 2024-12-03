from pathlib import Path
import re


def load(path):
    path = Path(path)
    return path.read_text()

content = load('example.txt')
# content = load('input.txt')


def p1re(content):
    def _mul(mul):
        mul = mul.lstrip('mul(')
        mul = mul.rstrip(')')
        a, b = mul.split(',')
        return int(a) * int(b)

    matches = re.findall(r'mul\(\d+,\d+\)', content)

    total = 0

    for match in matches:
        total += _mul(match)

    return total


def p2re(content):
    def _mul(mul):
        mul = mul.lstrip('mul(')
        mul = mul.rstrip(')')
        a, b = mul.split(',')
        return int(a) * int(b)

    matches = re.findall(r"mul\(\d+,\d+\)|don't\(\)|do\(\)", content)

    total = 0
    enable = True

    dont = "don't()"
    do = "do()"

    for match in matches:
        if not enable and match == do:
            enable = True
            continue

        if enable and match == dont:
            enable = False
            continue

        if enable and match.startswith('mul'):
            total += _mul(match)

    return total


print('part one:', p1re(content))
print('part two:', p2re(content))
