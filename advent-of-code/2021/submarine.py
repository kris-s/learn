from collections import Counter

from archive import read_file


print("Saving Christmas again!")

example = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""


def day_nine_prep(data):
    grid = []
    for row in data.split('\n'):
        if not row:
            continue
        grid.append([int(v) for v in row])
    return grid


def grid_adjacents(grid, x, y):
    up = None
    down = None
    left = None
    right = None

    if y > 0:
        up = grid[y-1][x]

    if y < len(grid) - 1:
        down = grid[y+1][x]

    if x > 0:
        left = grid[y][x-1]

    if x < len(grid[0]) - 1:
        right = grid[y][x+1]

    return [v for v in [up, down, left, right] if v is not None]


def grid_adjacents_points(grid, x, y):
    up = None
    down = None
    left = None
    right = None

    if y > 0:
        up = (x, y-1, grid[y-1][x])

    if y < len(grid) - 1:
        down = (x, y+1, grid[y+1][x])

    if x > 0:
        left = (x-1, y, grid[y][x-1])

    if x < len(grid[0]) - 1:
        right = (x+1, y, grid[y][x+1])

    return [v for v in [up, down, left, right] if v is not None]


def grid_basin(grid, x, y):
    basin_points = set()

    def walk(grid, x, y, basin_points):
        for x, y, value in grid_adjacents_points(grid, x, y):
            if (x, y) not in basin_points and value != 9:
                basin_points.add((x, y))
                walk(grid, x, y, basin_points)

    walk(grid, x, y, basin_points)
    return basin_points


def day_nine_a(data):
    grid = day_nine_prep(data)
    print(grid)

    low_points = []

    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            is_low_point = True
            for neighbor in grid_adjacents(grid, x, y):
                if neighbor <= value:
                    is_low_point = False

            if is_low_point:
                low_points.append((x, y, value+1))

    return sum(p[2] for p in low_points)


def day_nine_b(data):
    grid = day_nine_prep(data)
    seen_basin_points = set()
    basins = []

    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value != 9 and (x,y) not in seen_basin_points:
                basin_points = grid_basin(grid, x, y)
                for point in basin_points:
                    seen_basin_points.add(point)

                basins.append(len(basin_points))

    basins = sorted(basins, reverse=True)

    return basins[0] * basins[1] * basins[2]


# day_nine_input = read_file('day09.txt')
# print(day_nine_a(day_nine_input))
# print(day_nine_b(day_nine_input))
