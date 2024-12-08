from pathlib import Path
import copy

def load(path):
    path = Path(path)
    return path.read_text()

content = load('example.txt')
content = load('input.txt')

'''
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
'''

class P:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

grid = [list(r) for r in content.splitlines()]
START = P(0, 0)

def p1():
    guard = P(0, 0)
    direction = 'u'

    dirs = ['u', 'r', 'd', 'l']

    print(grid)

    for y, row in enumerate(grid):
        for x, t in enumerate(row): 
            if t == '^':
                guard.x = x
                guard.y = y
                grid[y][x] = '.'

    START.x = guard.x
    START.y = guard.y

    tiles_visited = [guard]
    count = 0

    g = copy.deepcopy(grid)
    while True:
        g[guard.y][guard.x] = 'G'

        # print('\n'.join([''.join(row) for row in g]))
        dx = 0
        dy = 0
        next_d = None

        # print('guard:', guard, direction)

        if direction == 'u':
            dy = -1
            next_d = 'r'
        elif direction == 'r':
            dx = 1
            next_d = 'd'
        elif direction == 'd':
            dy = 1
            next_d = 'l'
        else:
            dx = -1
            next_d  = 'u'

        next_point = P(guard.x + dx, guard.y + dy)

        if next_point.x < 0 or next_point.x > (len(grid[0]) - 1) or next_point.y < 0 or next_point.y > (len(grid) - 1):
            break
        elif grid[next_point.y][next_point.x] == '.':
            guard = next_point
            tiles_visited.append(guard)
        else:
            direction = next_d

        if guard == START:
            break

    return set((t.x, t.y) for t in tiles_visited)


def sim_loops(grid):
    visited = {}
    direction = 'u'

    guard = P(START.x, START.y)
    # print('guard at:', guard)

    while True:
        dx = 0
        dy = 0
        next_d = None

        if direction == 'u':
            dy = -1
            next_d = 'r'
        elif direction == 'r':
            dx = 1
            next_d = 'd'
        elif direction == 'd':
            dy = 1
            next_d = 'l'
        else:
            dx = -1
            next_d  = 'u'

        next_point = P(guard.x + dx, guard.y + dy)

        point_tuple = (next_point.x, next_point.y)
        if point_tuple in visited and visited[point_tuple] == direction:
            return True

        if next_point.x < 0 or next_point.x > (len(grid[0]) - 1) or next_point.y < 0 or next_point.y > (len(grid) - 1):
            break
        elif grid[next_point.y][next_point.x] == '.':
            guard = next_point
            visited[(guard.x, guard.y)] = direction
            # print('visited', visited)
        else:
            direction = next_d

        if guard == START:
            break

    return False


def p2(grid):
    candidates = p1()
    print(candidates)

    loops = []

    for p in candidates:
        print('checking', p)
        x, y = p
        g = copy.deepcopy(grid)
        # insert the new obstruction
        g[y][x] = '#'

        # rerun the sim
        if sim_loops(g):
            loops.append(p)

    return len(loops)

# print('p1', len(p1()))
print('p2', p2(grid))
