from collections import Counter


def read_file(filename):
    contents = ""
    with open(filename) as readfile:
        contents = readfile.read()
    return contents


# --- day eleven ---


def day_eleven_prep(data):
    grid = []
    for row in data.split('\n'):
        if not row:
            continue

        grid.append([int(v) for v in row])
    return grid

def grid_adjacents_diagonal(grid, x, y):
    points = [
        (-1, -1),
        (0, -1),
        (1, -1),
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),
        (-1, 0),
    ]

    neighbors = []
    for dx, dy in points:
        nx = x + dx
        ny = y + dy
        if nx > -1 and nx < len(grid[0]) and ny > -1 and ny < len(grid):
            neighbors.append((nx, ny))

    return neighbors

def grid_print(grid):
    for row in grid:
        print(''.join(str(v) for v in row))

def day_eleven_a(data, step_count=100):
    grid = day_eleven_prep(data)

    flashes = 0
    grid_print(grid)
    print()
    for step in range(step_count):
        # print('step', step)


        # First, the energy level of each octopus increases by 1.
        for y, row in enumerate(grid):
            for x, octopus in enumerate(row):
                grid[y][x] = octopus + 1

        # Then, any octopus with an energy level greater than 9 flashes.
        # This increases the energy level of all adjacent octopuses by 1,
        # including octopuses that are diagonally adjacent. If this causes
        # an octopus to have an energy level greater than 9, it also flashes.
        # This process continues as long as new octopuses keep having their
        # energy level increased beyond 9. (An octopus can only flash at
        # most once per step.)
        flashers = set()

        refresh = 1
        while refresh > 0:
            for y, row in enumerate(grid):
                for x, octopus in enumerate(row):
                    if octopus > 9 and (x, y) not in flashers:
                        flashers.add((x, y))
                        for nx, ny in grid_adjacents_diagonal(grid, x, y):
                            grid[ny][nx] += 1
                        refresh += 1
            refresh -= 1

        flashes += len(flashers)

        if len(flashers) == 100:
            print('sync flashes at step', step + 1)
            return

        for x, y in flashers:
            grid[y][x] = 0

    return flashes

# print(day_eleven_a(example))
# print(day_eleven_a(day_eleven_input, step_count=10000))


# --- day ten ---


def day_ten_prep(data):
    return [line for line in data.split("\n") if line]


def day_ten_a(data):
    # legal: ([]), {()()()}, <([{}])>
    # corrupt: (], {()()()>, (((()))}, and <([]){()}[{}])
    lines = day_ten_prep(data)

    opens = list("([{<")
    closes = list(")]}>")
    points = (3, 57, 1197, 25137)
    points = {ch: points[i] for i, ch in enumerate(closes)}
    close_to_open = {closes[i]: opens[i] for i in range(len(opens))}
    open_to_close = {opens[i]: closes[i] for i in range(len(opens))}

    corrupts = []
    for line in lines:
        corrupt = False
        stack = []

        for ch in line:
            if ch in opens:
                stack.append(ch)
            else:
                if len(stack) == 0:
                    corrupt = True
                    break
                prev = stack.pop()
                expected = open_to_close[prev]
                if expected != ch:
                    corrupt = True
                    corrupts.append(ch)
                    break

    score = 0
    counts = Counter(corrupts)
    for k, v in counts.items():
        score += points[k] * v

    return score


def day_ten_b(data):
    lines = day_ten_prep(data)
    opens = list("([{<")
    closes = list(")]}>")
    close_to_open = {closes[i]: opens[i] for i in range(len(opens))}
    open_to_close = {opens[i]: closes[i] for i in range(len(opens))}

    incompletes = []
    corrupts = []
    for line in lines:
        corrupt = False
        stack = []

        for ch in line:
            if ch in opens:
                stack.append(ch)
            else:
                if len(stack) == 0:
                    corrupt = True
                    break
                prev = stack.pop()
                expected = open_to_close[prev]
                if expected != ch:
                    corrupt = True
                    corrupts.append(ch)
                    break
        if not corrupt:
            incompletes.append(line)

    autocomplete_score = {")": 1, "]": 2, "}": 3, ">": 4}
    completions = []
    scores = []

    for line in incompletes:
        index = 0
        score = 0
        stack = []

        while index < len(line):
            if line[index] in closes:
                stack.pop()
            else:
                stack.append(line[index])

            index += 1

        matches = [open_to_close[ch] for ch in stack]
        stack = reversed(matches)

        for ch in stack:
            score = score * 5 + autocomplete_score[ch]
        scores.append(score)

    scores.sort()
    return scores[len(scores) // 2]


# print(day_ten_a(example))
# print(day_ten_a(read_file('day10.txt')))
# print(day_ten_b(read_file('day10.txt')))


# --- day nine ---


def day_nine_prep(data):
    grid = []
    for row in data.split("\n"):
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
        up = grid[y - 1][x]

    if y < len(grid) - 1:
        down = grid[y + 1][x]

    if x > 0:
        left = grid[y][x - 1]

    if x < len(grid[0]) - 1:
        right = grid[y][x + 1]

    return [v for v in [up, down, left, right] if v is not None]


def grid_adjacents_points(grid, x, y):
    up = None
    down = None
    left = None
    right = None

    if y > 0:
        up = (x, y - 1, grid[y - 1][x])

    if y < len(grid) - 1:
        down = (x, y + 1, grid[y + 1][x])

    if x > 0:
        left = (x - 1, y, grid[y][x - 1])

    if x < len(grid[0]) - 1:
        right = (x + 1, y, grid[y][x + 1])

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
                low_points.append((x, y, value + 1))

    return sum(p[2] for p in low_points)


def day_nine_b(data):
    grid = day_nine_prep(data)
    seen_basin_points = set()
    basins = []

    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value != 9 and (x, y) not in seen_basin_points:
                basin_points = grid_basin(grid, x, y)
                for point in basin_points:
                    seen_basin_points.add(point)

                basins.append(len(basin_points))

    basins = sorted(basins, reverse=True)

    return basins[0] * basins[1] * basins[2]


# day_nine_input = read_file('day09.txt')
# print(day_nine_a(day_nine_input))
# print(day_nine_b(day_nine_input))


# --- day eight ---


"""
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
"""

SEGMENT_FREQ = {
    "a": 8,
    "b": 6,
    "c": 8,
    "d": 7,
    "e": 4,
    "f": 9,
    "g": 7,
}


IDEAL_WIRING = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}


SEGMENT_LENGTHS = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6,
}


def day_eight_prep(data):
    output = []
    for row in data.split("\n"):
        if not row:
            continue
        left, right = row.split("|")
        left_segments = left.split()
        right_segments = right.split()
        output.append((left_segments, right_segments))

    return output


def day_eight_a(data):
    data = day_eight_prep(data)
    count = 0

    for _, output_values in data:
        # 1, 4, 7, and 8
        lengths = [len(v) for v in output_values]
        count += lengths.count(SEGMENT_LENGTHS[1])
        count += lengths.count(SEGMENT_LENGTHS[4])
        count += lengths.count(SEGMENT_LENGTHS[7])
        count += lengths.count(SEGMENT_LENGTHS[8])

    return count


def get_wiring_map(signals):
    counts = Counter("".join(signals))
    segment_map = {}

    for ideal_wire, count in SEGMENT_FREQ.items():
        if count in (7, 8):
            continue

        for real_wire, real_count in counts.items():
            if real_count == count:
                segment_map[ideal_wire] = real_wire

    segments = {"a", "b", "c", "d", "e", "f", "g"}
    lengths_map = {len(sig): set(sig) for sig in signals}

    one = lengths_map[SEGMENT_LENGTHS[1]]
    four = lengths_map[SEGMENT_LENGTHS[4]]
    seven = lengths_map[SEGMENT_LENGTHS[7]]

    # in seven but not in one
    segment_map["a"] = (seven ^ one).pop()

    # the 8 count in one
    for wire in one:
        if wire not in segment_map.values():
            segment_map["c"] = wire

    # d from four
    for wire in four:
        if wire not in segment_map.values():
            segment_map["d"] = wire

    # g remains
    segment_map["g"] = (segments ^ set(segment_map.values())).pop()

    wiring_map = {}
    for number, ideal in IDEAL_WIRING.items():
        key = ""
        for wire in ideal:
            key += segment_map[wire]

        key = "".join(sorted(key))
        wiring_map[key] = str(number)

    return wiring_map


def day_eight_b(data):
    data = day_eight_prep(data)

    total = 0

    for signals, output_values in data:
        wiring_map = get_wiring_map(signals)
        display = ""

        for digit in output_values:
            display += wiring_map["".join(sorted(digit))]

        total += int(display)

    return total


# day_eight_input = read_file("day08.txt")
# print(day_eight_a(example))
# print(day_eight_a(day_eight_input))
# print(day_eight_b(example))
# print(day_eight_b(day_eight_input))


# -- day seven --


def day_seven_prep(data):
    return [int(v) for v in data.split(",")]


def day_seven_a(data):
    data = day_seven_prep(data)
    med = median(data)

    fuel = 0
    for crab_pos in data:
        fuel += abs(med - crab_pos)

    return fuel


def day_seven_b(data):
    data = day_seven_prep(data)
    average = round(mean(data))

    fuels = {}

    for i in range(-10, 11, 1):
        guess = average + i
        fuel = 0
        for crab_pos in data:
            fuel += sum(i for i in range(abs(crab_pos - guess) + 1))

        fuels[guess] = fuel

    return min(fuels.values())


def median(data):
    data = sorted(data)

    mid = len(data) // 2
    if len(data) % 2 == 0:
        return (data[mid] + data[mid - 1]) / 2
    else:
        return data[mid]


def mean(data):
    return sum(data) / len(data)


# day_seven_input = read_file("day07.txt")
# print(day_seven_a(example))
# print(day_seven_a(day_seven_input))
# print(day_seven_b(example))
# print(day_seven_b(day_seven_input))


# --- day six ---


class Fish:
    def __init__(self, tick):
        self.tick = tick

    def day(self):
        if self.tick == 0:
            self.tick = 6
            return True

        self.tick -= 1

    def __str__(self):
        return str(self.tick)

    def __repr__(self):
        return str(self)


def day_six_prep(data):
    return [Fish(int(v)) for v in data.split(",")]


def print_school(fish):
    print(",".join([str(f) for f in fish]))


def day_six_a(data, days=80):
    fish = day_six_prep(data)
    print(fish)

    for i in range(days):
        print("day:", i)
        new_fish = []

        for f in fish:
            spawn_new_fish = f.day()
            if spawn_new_fish:
                new_fish.append(Fish(8))

        fish.extend(new_fish)

        # print_school(fish)

    return len(fish)


def day_six_b(data):
    pop_table = {}

    for tick in range(9):
        sample = [Fish(tick)]
        for i in range(128):
            new_fish = []

            for f in sample:
                spawn_new_fish = f.day()
                if spawn_new_fish:
                    new_fish.append(Fish(8))

            sample.extend(new_fish)

        pop_table[tick] = len(sample)

    fish_128 = day_six_prep(data)
    for i in range(128):
        new_fish = []

        for f in fish_128:
            spawn_new_fish = f.day()
            if spawn_new_fish:
                new_fish.append(Fish(8))

        fish_128.extend(new_fish)

    total = 0
    for fish in fish_128:
        total += pop_table[fish.tick]

    return total


# day_six_input = read_file("day06.txt")
# print(day_six_a(example))
# print(day_six_a(day_six_input))
# print(day_six_b(example))
# print(day_six_b(day_six_input))


# --- day five ---


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.x1},{self.y1} -> {self.x2},{self.y2}"

    def points(self):
        points = []

        if self.x1 == self.x2:
            if self.y1 > self.y2:
                for i in range(self.y1 - self.y2 + 1):
                    points.append((self.x1, self.y1 - i))
            else:
                for i in range(self.y2 - self.y1 + 1):
                    points.append((self.x1, self.y1 + i))
        elif self.y1 == self.y2:
            if self.x1 > self.x2:
                for i in range(self.x1 - self.x2 + 1):
                    points.append((self.x1 - i, self.y1))
            else:
                for i in range(self.x2 - self.x1 + 1):
                    points.append((self.x1 + i, self.y1))
        elif abs(self.x1 - self.x2) == abs(self.y1 - self.y2):
            if self.x1 > self.x2:
                step = 1
                if self.y1 > self.y2:
                    step = -1
                y = self.y1
                for i in range(self.x1 - self.x2):
                    points.append((self.x1 - i, y))
                    y += step
                points.append((self.x2, self.y2))
            else:
                step = -1
                if self.y2 > self.y1:
                    step = 1
                y = self.y1
                for i in range(self.x2 - self.x1):
                    points.append((self.x1 + i, y))
                    y += step
                points.append((self.x2, self.y2))

        return points


def day_five_prep(data):
    lines = []
    for line in data.split("\n"):
        if not line:
            continue
        one, two = line.split("->")

        x1, y1 = one.split(",")
        x2, y2 = two.split(",")

        lines.append(Line(int(x1), int(y1), int(x2), int(y2)))

    return lines


def day_five_b(data):
    data = day_five_prep(data)

    x_values = [l.x1 for l in data]
    x_values.extend([l.x2 for l in data])
    max_x = max(x_values) + 1

    y_values = [l.y1 for l in data]
    y_values.extend([l.y2 for l in data])
    max_y = max(y_values) + 1
    print("max_x:", max_x, "max_y:", max_y)

    grid = []
    for i in range(max_y):
        row = []
        for j in range(max_x):
            row.append(0)
        grid.append(row)

    for row in grid:
        print(row)

    for line in data:
        print(line, line.points())
        for x, y in line.points():
            grid[y][x] += 1

    count = 0

    for row in grid:
        for value in row:
            if value > 1:
                count += 1

    return count


# day_five_input = read_file("day05.txt")
# print(day_five_a(example))
# print(day_five_a(day_five_input))
# print(day_five_b(example))
# print(day_five_b(day_five_input))


# --- day four ---


class Board:
    def __init__(self, index, board):
        assert len(board) == 5
        for row in board:
            assert len(row) == 5

        status = []

        for _ in range(5):
            row = []
            for _ in range(5):
                row.append(False)

            status.append(row)

        print(status)

        self.index = index
        self.board = board
        self.status = status

    def update(self, num):
        for i, row in enumerate(self.board):
            if num in row:
                index = row.index(num)
                self.status[i][index] = True

    def unmarked(self):
        nums = []
        for i, row in enumerate(self.status):
            for j, stat in enumerate(row):
                if not stat:
                    nums.append(self.board[i][j])
        return nums

    def is_winner(self):
        for i, row in enumerate(self.status):
            if all(row):
                return True, self.board[i]

        for i in range(5):
            row = [
                self.status[0][i],
                self.status[1][i],
                self.status[2][i],
                self.status[3][i],
                self.status[4][i],
            ]
            if all(row):
                return True, [
                    self.board[0][i],
                    self.board[1][i],
                    self.board[2][i],
                    self.board[3][i],
                    self.board[4][i],
                ]

        # diagonal support was not needed...
        # row = [self.status[0][0], self.status[1][1], self.status[2][2], self.status[3][3], self.status[4][4]]
        # if all(row):
        #     print('diag 1')
        #     return True, [self.board[0][0], self.board[1][1], self.board[2][2], self.board[3][3], self.board[4][4]]

        # row = [self.status[0][4], self.status[1][3], self.status[2][2], self.status[3][1], self.status[4][0]]
        # if all(row):
        #     print('diag 2')
        #     return True, [self.board[0][4], self.board[1][3], self.board[2][2], self.board[3][1], self.board[4][0]]

        return False, []


def day_four_prep(data):
    lines = data.split("\n")

    numbers = [int(v) for v in lines.pop(0).split(",")]
    lines.pop(0)

    lines = [l for l in lines if l]
    boards = []
    board = []
    index = 0

    for row in lines:
        board.append([int(v) for v in row.split()])
        if len(board) == 5:
            boards.append(Board(index, list(board)))
            index += 1
            board = []

    return numbers, boards


def day_four_a(data):
    numbers, boards = day_four_prep(data)

    for num in numbers:
        print("Drawing number:", num)
        for board in boards:
            board.update(num)

        for board in boards:
            is_winner, row = board.is_winner()
            if is_winner:
                print("winner!", row, num, board.index)
                return num * sum(board.unmarked())


def day_four_b(data):
    numbers, boards = day_four_prep(data)
    deletes = []

    for num in numbers:
        for i in sorted(deletes, reverse=True):
            boards.pop(i)

        deletes = []

        print("Drawing number:", num)
        for board in boards:
            board.update(num)

        for i, board in enumerate(boards):
            is_winner, row = board.is_winner()
            if is_winner and len(boards) > 1:
                deletes.append(i)
            elif is_winner:
                return num * sum(board.unmarked())


# day_four_input = read_file("day04.txt")
# print(day_four_a(example))
# print(day_four_a(day_four_input))
# print(day_four_b(example))
# print(day_four_b(day_four_input))


# --- day three ---


def day_three_prep(data):
    binary_strings = []
    for row in data.split("\n"):
        if not row:
            continue
        binary_strings.append(row)
    return binary_strings


def day_three_to_columns(data):
    columns = []
    for _ in range(len(data[0])):
        columns.append([])

    for row in data:
        for i, bit in enumerate(row):
            columns[i].append(bit)

    return columns


def day_three_a(data):
    binary_strings = day_three_prep(data)

    gamma = ""
    epsilon = ""

    columns = day_three_to_columns(binary_strings)

    for col in columns:
        zeros = col.count("0")
        ones = col.count("1")

        if zeros > ones:
            gamma += "0"
            epsilon += "1"
        else:
            gamma += "1"
            epsilon += "0"

    return int(gamma, 2) * int(epsilon, 2)


def day_three_life_support(data, use_most_common, tiebreak):
    result = ""
    tiebreak = str(tiebreak)

    binary_strings = list(data)

    for i in range(len(data[0])):
        if len(binary_strings) == 1:
            break

        columns = day_three_to_columns(binary_strings)

        zeros = columns[i].count("0")
        ones = columns[i].count("1")

        filtered_binary_strings = []
        for binary in binary_strings:
            bit = binary[i]

            if zeros == ones and bit == tiebreak:
                filtered_binary_strings.append(binary)
            elif zeros > ones:
                if use_most_common and bit == "0":
                    filtered_binary_strings.append(binary)
                elif not use_most_common and bit == "1":
                    filtered_binary_strings.append(binary)
            elif ones > zeros:
                if use_most_common and bit == "1":
                    filtered_binary_strings.append(binary)
                elif not use_most_common and bit == "0":
                    filtered_binary_strings.append(binary)

        binary_strings = filtered_binary_strings

    print("done filtering:", binary_strings)

    return binary_strings[0]


def day_three_b(data):
    binary_strings = day_three_prep(data)

    oxygen = day_three_life_support(binary_strings, True, 1)
    co2 = day_three_life_support(binary_strings, False, 0)

    return int(oxygen, 2) * int(co2, 2)


# day_three_input = read_file('day03.txt')
# print(day_three_a(example))
# print(day_three_a(day_three_input))
# print(day_three_b(example))
# print(day_three_b(day_three_input))


# --- day two ---


def day_two_prep(data):
    commands = []

    for row in data.split("\n"):
        if not row:
            continue
        inst, value = row.split()
        command = (inst, int(value))
        commands.append(command)

    return commands


def day_two_a(data):
    commands = day_two_prep(data)

    pos = 0
    depth = 0

    for inst, value in commands:
        if inst == "forward":
            pos += value
        elif inst == "down":
            depth += value
        elif inst == "up":
            depth -= value
        else:
            print(f"Unknown instruction: {inst} {value}")

    return pos * depth


def day_two_b(data):
    commands = day_two_prep(data)

    pos = 0
    depth = 0
    aim = 0

    for inst, value in commands:
        if inst == "forward":
            pos += value
            depth += aim * value
        elif inst == "down":
            aim += value
        elif inst == "up":
            aim -= value
        else:
            print(f"Unknown instruction: {inst} {value}")

    print(f"final pos: {pos} depth: {depth} aim: {aim}")
    return pos * depth


# day_two_data = read_file('day02.txt')
# print(day_two_a(example))
# print(day_two_a(day_two_data))
# print(day_two_b(example))
# print(day_two_b(day_two_data))
