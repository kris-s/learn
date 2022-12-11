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


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def as_tuple(self):
        return (self.x, self.y)

    def follow(self, target):
        tx = target.x
        ty = target.y

        dx = abs(self.x - tx)
        dy = abs(self.y - ty)

        # print('in follow:', dx, dy, self, target)

        if dx <= 1 and dy <= 1:
            return

        if tx != self.x:
            if tx > self.x:
                self.x += 1
            else:
                self.x -= 1

        if ty != self.y:
            if ty > self.y:
                self.y += 1
            else:
                self.y -= 1

    def __repr__(self):
        return f'({self.x}, {self.y})'

moves = {
    'U': (0, 1),
    'D': (0, -1),
    'L': (-1, 0),
    'R': (1, 0),
}

def day_9(text):
    lines = text.splitlines()

    head_pos = Point(0, 0)
    tail_pos = Point(0, 0)

    tail_positions = {(0, 0)}

    for line in lines:
        direction, amount = line.split()
        amount = int(amount)

        dx, dy = moves[direction]

        for _ in range(amount):
            head_pos.x += dx
            head_pos.y += dy

            tail_pos.follow(head_pos)
            tail_positions.add(tail_pos.as_tuple())

            print('head:', head_pos, 'tail:', tail_pos)

    print(tail_positions)
    print('part 1:', len(tail_positions))


    snake = [Point(0, 0) for _ in range(10)]

    tail_positions = {(0, 0)}

    for line in lines:
        direction, amount = line.split()
        amount = int(amount)

        dx, dy = moves[direction]

        for _ in range(amount):
            snake[0].x += dx
            snake[0].y += dy

            for i, segment in enumerate(snake):
                if i == 0:
                    continue

                segment.follow(snake[i-1])

                if i == 9:
                    print('updating tail pos:', segment)
                    tail_positions.add(segment.as_tuple())
        print(snake)

    print('part 2:', len(tail_positions))


def day_10_a(text):
    lines = text.splitlines()

    x = 1
    cursor = 0
    tick = 1

    working = False
    amount_to_add = 0
    signal_strengths = []
    current_inst = ''
    values_added = []

    target_cycle = [20, 60, 100, 140, 180, 220]

    while True:
        if working:
            working = False
            tick += 1
            continue
        elif amount_to_add is not None:
            values_added.append(amount_to_add)
            x += amount_to_add
            amount_to_add = None

        if tick in target_cycle:
            target_cycle.remove(tick)
            signal_strengths.append(tick * x)

        if cursor == len(lines):
            break

        line = lines[cursor]
        cursor += 1

        if line == 'noop':
            working = False
            tick += 1
        else:
            amount_to_add = int(line.split()[1])
            working = True
            tick += 1
        if tick in target_cycle:
            target_cycle.remove(tick)
            signal_strengths.append(tick * x)

    print(signal_strengths)
    print('part 1', sum(signal_strengths))


def day_10_b(text):
    lines = text.splitlines()

    x = 1
    cursor = 0
    tick = 1

    working = False
    amount_to_add = 0
    signal_strengths = []
    current_inst = ''
    values_added = []
    grid = list('.' * 240)
    grid[80] = '%'
    grid[239] = '?'
    grid_two = []

    target_cycle = [20, 60, 100, 140, 180, 220]

    # If the sprite is positioned such that one of its three pixels
    # is the pixel currently being drawn, the screen produces a lit pixel (#);
    # otherwise, the screen leaves the pixel dark (.).
    def draw(x, tick, grid):
        sprite = [x-1, x, x+1]

        draw_tick = (tick - 1) % 40
        print('draw_tick:', draw_tick)

        if draw_tick in sprite:
            print('drawing pixel at', tick-1)
            grid[tick-1]='#'

    get_next_instruction = True

    while cursor < len(lines):
        if get_next_instruction:
            line = lines[cursor]
            print('starting executing', line)
            cursor += 1
            if line.startswith('addx'):
                get_next_instruction = False
                prepare_to_add = int(line.split()[1])
        else:
            get_next_instruction = True
            amount_to_add = prepare_to_add
            prepare_to_add = 0

        draw(x, tick, grid)
        if amount_to_add is not None:
            x += amount_to_add
            amount_to_add = None
        print('x reg:', x)
        tick += 1

    print(signal_strengths)
    print('part 1', sum(signal_strengths))

    for i in range(6):
        lower = i * 40
        upper = lower + 40
        print(''.join(grid[lower:upper]))

    for i in range(6):
        lower = i * 40
        upper = lower + 40
        print(''.join(grid_two[lower:upper]))
