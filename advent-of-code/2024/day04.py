from pathlib import Path


def load(path):
    path = Path(path)
    return path.read_text()

# content = [l for l in load('example.txt').splitlines() if l]
content = [l for l in load('input.txt').splitlines() if l]

# 2426 was wrong
# 2427?


def cast(x, y, dx, dy):
    word = content[y][x]

    for i in range(3):

        y += dy
        x += dx

        if y < 0 or x < 0:
            return word

        try:
            word += content[y][x]
        except:
            return word

    return word


def matches_at(x, y):
    if content[y][x] != 'X':
        return 0

    raycasts = [
        # ortho
        cast(x, y, dx=0, dy=-1),
        cast(x, y, dx=0, dy=1),
        cast(x, y, dx=1, dy=0),
        cast(x, y, dx=-1, dy=0),
        # diag
        cast(x, y, dx=1, dy=-1),
        cast(x, y, dx=1, dy=1),
        cast(x, y, dx=-1, dy=-1),
        cast(x, y, dx=-1, dy=1),
    ]

    count = 0

    for c in raycasts:
        if c == 'XMAS':
            count += 1

    return count


def mas_cast(x, y):
    grid = list('?.?\n.A.\n?.?')

    points = {
        0: (x-1, y-1),
        2: (x+1, y-1),
        8: (x-1, y+1),
        10: (x+1, y+1),
    }

    for i, (px, py) in points.items():
        if px < 0 or py < 0:
            return grid
        try:
            grid[i] = content[py][px]
        except:
            return grid

    return grid


def x_mas_matches_at(x, y):
    if content[y][x] != 'A':
        return 0

    cast = mas_cast(x, y)
    cast = ''.join(cast)

    ok = (
        'S.S\n.A.\nM.M',
        'M.M\n.A.\nS.S',
        'M.S\n.A.\nM.S',
        'S.M\n.A.\nS.M',
    )

    if cast in ok:
        print('match centered at', x, y)
        print(cast)
        return 1
    else:
        return 0



def p1():
    count = 0
    for y in range(len(content)):
        for x in range(len(content[0])):
            count =+ matches_at(x, y)
    return count


def p2():
    count = 0
    # x_mas_matches_at(2, 1)
    for y in range(len(content)):
        for x in range(len(content[0])):
            count += x_mas_matches_at(x, y)
    return count


print('p1:', p1())
print('p2:', p2())
