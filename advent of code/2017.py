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
