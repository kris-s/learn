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


def day_6(text):
    window = []
    for i, char in enumerate(text.strip()):
        window.insert(0, char)
        if len(window) > 14:
            window.pop()

        if len(set(window)) == 14:
            print(i+1)
            break


def day_7(text):
    lines = text.splitlines()

    cwd = ['/']
    directories = {}

    for line in lines:
        if line[0] == '$':
            command = line.split()[1]
            if command == 'cd':
                destination = line.split()[2]
                if destination == '..' and len(cwd) > 1:
                    cwd.pop()
                elif cwd != [destination]:
                    cwd.append(destination)
            elif command == 'ls':
                pass
        else:
            dirname = '/'.join(cwd)
            entry = line
            if line.startswith('dir'):
                entry = dirname + '/' + line.split()[1]
            if dirname not in directories:
                directories[dirname] = {entry}
            else:
                directories[dirname].add(entry)

    def walk(contents):
        total = 0
        for entry in contents:
            if entry.startswith('/'):
                total += walk(directories[entry])
            else:
                total += int(entry.split()[0])
        return total

    dir_sizes = {}

    for directory, contents in directories.items():
        dir_sizes[directory] = walk(contents)

    for k, v in dir_sizes.items():
        print(k, v)

    limit = 100000
    total = 0

    for key, value in dir_sizes.items():
        if value <= limit:
            total += value

    print('part 1', total)

    total_space = 70000000
    target = 30000000
    total_unused = total_space - dir_sizes['/']
    print('total_unused', total_unused)

    could_work = []

    for key, value in dir_sizes.items():
        if value + total_unused >= target:
            could_work.append(value)

    print('part 2', min(could_work))


def day_8(text):
    lines = text.splitlines()
    grid = []

    for line in lines:
        grid.append([int(h) for h in line])

    width = len(grid[0]) - 1
    height = len(grid) - 1

    def is_visible(x, y):
        if x == 0 or y == 0:
            return True
        if x == width or y == height:
            return True

        tree_height = grid[y][x]

        # left
        left = grid[y][:x]
        if tree_height > max(left):
            return True

        # right
        if tree_height > max(grid[y][x+1:]):
            return True

        above = [grid[i][x] for i in range(y)]
        if tree_height > max(above):
            return True

        below = [grid[i+y+1][x] for i in range(height-y)]
        if tree_height > max(below):
            return True

        return False

    visible_trees = set()

    for y, row in enumerate(grid):
        for x, tree in enumerate(row):
            if is_visible(x, y):
                visible_trees.add((x, y))

    print('part 1:', len(visible_trees))

    def scenic_score(x, y):
        tree_height = grid[y][x]

        left = list(reversed(grid[y][:x]))
        right = grid[y][x+1:]
        above = list(reversed([grid[i][x] for i in range(y)]))
        below = [grid[i+y+1][x] for i in range(height-y)]

        views = [left, right, above, below]

        for view in views:
            if not view:
                return 0

        visible_trees = [1, 1, 1, 1]

        for i, view in enumerate(views):
            current_tree = view[0]
            if current_tree >= tree_height:
                continue
            for tree in view[1:]:
                if current_tree >= tree_height:
                    break
                else:
                    visible_trees[i] += 1
                    current_tree = tree
        a, b, c, d = visible_trees

        return a * b * c * d

    scores = []
    for y, row in enumerate(grid):
        for x, tree in enumerate(row):
            score = scenic_score(x, y)
            scores.append(score)

    print('part 2:', max(scores))
