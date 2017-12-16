#!/usr/local/bin/python3


def day_one(captcha):
    captcha = [int(c) for c in str(captcha)]
    total = 0
    for i, digit in enumerate(captcha):
        doubled = captcha[:]
        doubled.extend(captcha[:])
        if digit == doubled[i+1]:
            total += digit
    return total


def day_two(spreadsheet):
    checksum = 0
    for row in spreadsheet.split('\n'):
        row = [int(val) for val in row.split()]
        if row:
            checksum += max(row) - min(row)
    return checksum


def day_three(memory):
    next_direction = {
        'right': 'up',
           'up': 'left',
         'left': 'down',
         'down': 'right',
    }

    step_count = 0
    step_size = 1
    step_sizes = []
    x = 0
    y = 0

    grid = {}

    direction = 'right'

    for val in range(1, memory + 1):
        grid[val] = (x, y)

        if direction == 'right':
            x += 1
        elif direction == 'up':
            y += 1
        elif direction == 'left':
            x -= 1
        elif direction == 'down':
            y -= 1

        step_count += 1

        if step_count == step_size:
            direction = next_direction[direction]
            step_count = 0
            step_sizes.append(step_size)
            if step_sizes.count(step_size) == 2:
                step_size += 1

    x, y = grid[memory]

    return abs(x) + abs(y)


def day_four(passphrases):
    valid = 0
    for phrase in passphrases.split('\n'):
        words = phrase.split()
        word_set = set(words)
        if not words:
            continue
        if len(words) == len(word_set):
            valid += 1
    return valid


def day_five(instructions):
    instructions = [int(val) for val in instructions.split('\n')]

    steps = 0
    idx = 0

    while True:
        try:
            jump = instructions[idx]
            instructions[idx] += 1
            idx += jump
            steps += 1
        except IndexError:
            break
    return steps


def day_six(banks):
    banks = [int(val) for val in banks.split()]
    steps = 0
    seen = []

    while True:
        largest = max(banks)
        index = banks.index(largest)
        banks[index] = 0

        for _ in range(largest):
            if index < len(banks) - 1:
                index += 1
            else:
                index = 0
            banks[index] += 1

        if banks in seen:
            steps += 1
            break
        else:
            steps += 1
            seen.append(banks[:])

    return steps


def day_seven(structure):
    values = []
    for row in structure.split('\n'):
        value = {'children': []}
        for i, a in enumerate(row.split()):
            if i == 0:
                value['name'] = a
            elif i == 1:
                value['weight'] = a
            elif i > 2:
                value['children'].append(a.replace(',', ''))
        values.append(value)

    children = []
    for c in [v['children'] for v in values]:
        children.extend(c)

    for value in values:
        if value['name'] not in children:
            return value['name']


def day_eight(instructions):
    def parse_op(op):
        if op == '>':
            return lambda x, y: x > y
        elif op == '>=':
            return lambda x, y: x >= y
        elif op == '<':
            return lambda x, y: x < y
        elif op == '<=':
            return lambda x, y: x <= y
        elif op == '==':
            return lambda x, y: x == y
        elif op == '!=':
            return lambda x, y: x != y

    commands = []
    registers = {}

    for row in instructions.split('\n'):
        name, sign, scalar, _, dependent, operation, trigger  = row.split()
        registers[name] = 0
        commands.append((
            name,
            int(scalar),
            sign == 'inc',
            dependent,
            parse_op(operation),
            int(trigger)
        ))

    for c in commands:
        name, scalar, sign, dependent, operation, trigger = c
        if operation(registers[dependent], trigger):
            if sign:
                registers[name] += scalar
            else:
                registers[name] -= scalar

    return max(registers.values())


def day_nine(stream):
    score = 0
    depth = 0
    open_garbage = False
    cancel_next = False

    for c in stream:
        if cancel_next:
            cancel_next = False
            continue
        elif c == '{' and not open_garbage:
            depth += 1
        elif c == '}' and not open_garbage:
            score += depth
            depth -= 1
        elif c == '<':
            open_garbage = True
        elif c == '>' and open_garbage:
            open_garbage = False
        elif c == '!':
            cancel_next = True

    return score


def day_ten(input):
    skip = 0
    total_rotation = 0

    commands = [int(val) for val in input.split(',')]
    knot = [i for i in range(256)]

    for c in commands:
        knot = list(reversed(knot[:c])) + knot[c:]
        rotate = (c + skip) % len(knot)
        knot = knot[rotate:] + knot[:rotate]
        total_rotation += c + skip
        skip += 1

    unwind = len(knot) - total_rotation % len(knot)
    knot = knot[unwind:] + knot[:unwind]

    return knot[0] * knot[1]


def day_eleven(moves):
    moves = moves.split(',')
    position = (0, 0)

    deltas = {
        'nw': (-1, 0),
        'n': (0, -1),
        'ne': (1, -1),
        'sw': (-1, 1),
        's': (0, 1),
        'se': (1, 0)}

    for move in moves:
        x, y = position
        dx, dy = deltas[move]
        position = (x + dx, y + dy)

    x, y = position

    if x > 0 and y > 0:
        steps = x + y
    elif x < 0 and y < 0:
        steps = abs(x) + abs(y)
    else:
        absolute = abs(x), abs(y)
        steps = max(absolute)

    return steps
