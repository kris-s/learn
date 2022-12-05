import re


def day_1(text):
    elves = []
    calories = 0
    for line in text.splitlines():
        if line:
            calories += int(line)
        else:
            elves.append(calories)
            calories = 0
    print('Part A:', max(elves))
    elves.sort(reverse=True)
    print('Part B:', sum(elves[:3]))


def day_2_a(text):
    shapes = {
        'X': 1, # rock (A)
        'Y': 2, # paper (B)
        'Z': 3, # scissor (C)
    }

    a_to_x = {
        'A': 'X',
        'B': 'Y',
        'C': 'Z',
    }

    # key beats value
    outcome_table = {
        'X': 'Z',
        'Y': 'X',
        'Z': 'Y',
    }

    def outcome_points(opponent, mine):
        opponent = a_to_x[opponent]

        if opponent == mine:
            return 3

        if outcome_table[mine] == opponent:
            return 6
        else:
            return 0

    points = 0
    for line in text.splitlines():
        opponent, mine = line.split()
        points += outcome_points(opponent, mine)
        points += shapes[mine]
    print(points)


def day_2_b(text):
    shapes = {
        'A': 1, # rock
        'B': 2, # paper
        'C': 3, # scissors
    }

    # key beats value
    lose_table = {
        'A': 'C',
        'B': 'A',
        'C': 'B',
    }
    # key loses to value
    win_table = {
        'A': 'B',
        'B': 'C',
        'C': 'A',
    }

    def outcome_points(opponent, goal):
        # lose
        if goal == 'X':
            choice = lose_table[opponent]
            points = 0
        # draw
        elif goal == 'Y':
            choice = opponent
            points = 3
        # win
        else:
            choice = win_table[opponent]
            points = 6

        return points + shapes[choice]


    points = 0
    for line in text.splitlines():
        opponent, goal = line.split()
        points += outcome_points(opponent, goal)
    print(points)


def day_3(text):
    def item_value(item):
        if ord(item) - 96 > 0:
            return ord(item) - 96
        else:
            return ord(item) - 38

    items_of_interest = []
    for line in text.splitlines():
        split_at = int(len(line) / 2)
        left = line[:split_at]
        right = line[split_at:]

        common = list(set(left) & set(right))
        items_of_interest.append(common[0])

    print(sum(item_value(item) for item in items_of_interest))

    group_ids = []
    lines = text.splitlines()
    for i in range(0, len(lines), 3):
        one = set(lines[i])
        two = set(lines[i+1])
        thr = set(lines[i+2])
        common = list(set(one) & set(two) & set(thr))
        group_ids.append(common[0])

    print(sum(item_value(item) for item in group_ids))


def day_4(text):
    full = 0
    partial = 0

    for line in text.splitlines():
        a, b = line.split(',')

        a_lower, a_upper = a.split('-')
        a_set = set(range(int(a_lower), int(a_upper)+1))

        b_lower, b_upper = b.split('-')
        b_set = set(range(int(b_lower), int(b_upper)+1))

        if a_set.issubset(b_set) or b_set.issubset(a_set):
            full += 1

        if a_set & b_set:
            partial += 1

    print(full)
    print(partial)


def day_5_a(text):
    def execute_instructions(cargo, instructions):
        for inst in instructions:
            moves, source, dest = map(int, re.findall(r'move (\d+) from (\d+) to (\d+)', inst)[0])
            for i in range(moves):
                crate = cargo[source-1].pop(0)
                cargo[dest-1].insert(0, crate)

    cargo = {}

    raw_crates = []
    instructions = []
    n_stacks = 0

    lines = text.splitlines()
    for i, line in enumerate(lines):


        if not line:
            n_stacks = max(map(int, lines[i-1].split()))
            raw_crates = lines[:i-1]
            instructions = lines[i+1:]

    cursor = 1
    for col in range(n_stacks):
        cargo[col] = []
        for line in raw_crates:
            if len(line) > cursor and line[cursor] != ' ':
                cargo[col].append(line[cursor])
        cursor += 4

    print('cargo:', cargo)
    print(instructions)
    execute_instructions(cargo, instructions)

    topline = []
    for k, v in cargo.items():
        print(k, v[0])
        topline.append(v[0])

    print(''.join(topline))


def day_5_b(text):
    def execute_instructions(cargo, instructions):
        for inst in instructions:
            moves, source, dest = map(int, re.findall(r'move (\d+) from (\d+) to (\d+)', inst)[0])

            crates = []
            for i in range(moves):
                crates.append(cargo[source-1].pop(0))

            for crate in reversed(crates):
                cargo[dest-1].insert(0, crate)

    cargo = {}

    raw_crates = []
    instructions = []
    n_stacks = 0

    lines = text.splitlines()
    for i, line in enumerate(lines):


        if not line:
            n_stacks = max(map(int, lines[i-1].split()))
            raw_crates = lines[:i-1]
            instructions = lines[i+1:]

    cursor = 1
    for col in range(n_stacks):
        cargo[col] = []
        for line in raw_crates:
            if len(line) > cursor and line[cursor] != ' ':
                cargo[col].append(line[cursor])
        cursor += 4

    print('cargo:', cargo)
    print(instructions)
    execute_instructions(cargo, instructions)

    topline = []
    for k, v in cargo.items():
        print(k, v[0])
        topline.append(v[0])

    print(''.join(topline))
