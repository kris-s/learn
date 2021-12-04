from archive import read_file


print("Saving Christmas again!")


example = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


def day_five_prep(data):
    return []


def day_five_a(data):
    data = day_five_prep(data)
    return None


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
