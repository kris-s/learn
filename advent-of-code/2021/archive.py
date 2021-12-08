from collections import Counter


def read_file(filename):
    contents = ''
    with open(filename) as readfile:
        contents = readfile.read()
    return contents



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
