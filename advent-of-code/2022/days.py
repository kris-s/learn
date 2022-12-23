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


class Monkey:
    def __init__(self, n, lines):
        clean = lambda x: x.split(':')[1].strip()
        clean_target = lambda x: int(x.split('throw to monkey')[1])

        self.n = n
        self.items = [int(i) for i in clean(lines[1]).split(',')]
        self.operation = clean(lines[2])
        test = clean(lines[3])
        self.test_divisor = int(test.split(' by ')[1])
        self.test_true_target = clean_target(lines[4])
        self.test_false_target = clean_target(lines[5])
        self.inspection_count = 0

    def __repr__(self):
        return f'{self.n}\n{self.items}\n{self.operation}\n{test_divisor}\n{self.test_true}\n{self.test_false}'

    def run(self, monkeys):
        while self.items:
            item = self.items.pop(0)
            self.inspection_count += 1

            _, _, l, op, r = self.operation.split()
            if op == '+':
                opfunc = lambda x, a: x + a
            else:
                opfunc = lambda x, a: x * a

            if r == 'old':
                item = opfunc(item, item)
            else:
                item = opfunc(item, int(r))

            item = item // 3

            if item % self.test_divisor == 0:
                monkeys[self.test_true_target].items.append(item)
            else:
                monkeys[self.test_false_target].items.append(item)

    def run3(self, monkeys, lcm):
        while self.items:
            item = self.items.pop(0)
            self.inspection_count += 1

            _, _, l, op, r = self.operation.split()
            if op == '+':
                opfunc = lambda x, a: x + a
            else:
                opfunc = lambda x, a: x * a

            if r == 'old':
                item = opfunc(item, item)
            else:
                item = opfunc(item, int(r))

            item = item % lcm

            if item % self.test_divisor == 0:
                monkeys[self.test_true_target].items.append(item)
            else:
                monkeys[self.test_false_target].items.append(item)


# NOTE: part 2 incomplete
def day_11(text):
    lines = text.splitlines()
    monkeys = []
    new_monkey = []
    count = 0

    for line in lines:
        if line:
            new_monkey.append(line)
        else:
            monkeys.append(Monkey(count, new_monkey))
            count += 1
            new_monkey = []

    monkeys.append(Monkey(count, new_monkey))

    lcm = 1
    for m in monkeys:
        lcm *= m.test_divisor

    print('lcm is', lcm)

    assert len(monkeys) == 4
    for r in range(20):
        for m in monkeys:
            m.run3(monkeys, lcm)
            # m.run(monkeys)
        print('done with round:', r)
        for m in monkeys:
            print(m.n, m.items)

    monkey_biz = sorted(m.inspection_count for m in monkeys)
    for m in monkey_biz:
        print(m)
    a = monkey_biz.pop()
    b = monkey_biz.pop()
    print(a * b)


# NOTE: part 1 and 2 incomplete
def day_12(text):
    from random import shuffle
    lines = text.splitlines()
    g_elevation = lambda x: ord(x) - 97

    grid = []
    starting_pos = (0, 0, 0)
    destination = (0, 0)
    steps = 0
    backtrack = None

    for row in lines:
        grid.append(list(row))

    for y, row in enumerate(lines):
        if 'S' in row:
            x = row.index('S')
            starting_pos = (x, y, 0)
            break


    for y, row in enumerate(lines):
        if 'E' in row:
            x = row.index('E')
            destination = (x, y)
            break

    MOVES = {
        'up': (0, -1),
        'down': (0, 1),
        'left': (-1, 0),
        'right': (1, 0)
    }

    OPPOSITES = {
        'up': 'down',
        'down': 'up',
        'left': 'right',
        'right': 'left',
    }

    def get_adjacents(pos, grid):
        x, y, current_elevation = pos

        width = len(grid[0])
        height = len(grid)
        moves = []

        if x + 1 < width and current_elevation >= g_elevation(grid[y][x+1]) - 1:
            moves.append('right')

        if x - 1 > -1 and current_elevation >= g_elevation(grid[y][x-1]) - 1:
            moves.append('left')

        if y + 1 < height and current_elevation >= g_elevation(grid[y+1][x]) - 1:
            moves.append('down')

        if y - 1 > -1 and current_elevation >= g_elevation(grid[y-1][x]) - 1:
            moves.append('up')

        return moves

    step_counts = []
    for i in range(1000):
        steps = 0
        pos = starting_pos
        while True:
            if (pos[0], pos[1]) == destination:
                print('made it!')
                step_counts.append(steps)
                break

            adjacents = get_adjacents(pos, grid)
            if not adjacents or adjacents == [backtrack]:
                steps = 1000
                print('stuck')
                break

            if backtrack is None:
                choice = adjacents.pop()
                backtrack = OPPOSITES[choice]
            elif backtrack in adjacents:
                adjacents.remove(backtrack)
                shuffle(adjacents)
                choice = adjacents.pop()
                backtrack = OPPOSITES[choice]

            x, y, old_height = pos
            print('moving', choice)
            dx, dy = MOVES[choice]
            x += dx
            y += dy
            pos = (x, y, g_elevation(grid[y][x]))
            steps += 1
        step_counts.append(steps)

    print(step_counts)
    print(min(step_counts))
    for g in grid:
        print(''.join(g))


def day_13(text):
    lines = text.splitlines()
    pairs = []
    pair = []
    for line in lines:
        if line and len(pair) < 2:
            pair.append(eval(line))
            if len(pair) == 2:
                pairs.append(pair)
                pair = []


    def ordered(left, right):
        if isinstance(left, int) and isinstance(right, int):
            if left == right:
                return None
            else:
                return left < right
        elif isinstance(left, list) and isinstance(right, list):
            for i, val in enumerate(left):
                try:
                    right_val = right[i]
                except IndexError:
                    return False
                result = ordered(val, right_val)
                if result is None:
                    continue
                else:
                    return result
            return True
        elif isinstance(left, int) and isinstance(right, list):
            return ordered([left], right)
        elif isinstance(left, list) and isinstance(right, int):
            return ordered(left, [right])
        else:
            raise ValueError(f'not sure what to do with: {left} {right}')

    ordered_pairs = []
    for i, p in enumerate(pairs):
        left, right = p
        if ordered(left, right):
            ordered_pairs.append(i+1)

    print('part 1:', sum(ordered_pairs))

    def cmp(a, b):
        result = ordered(a, b)
        if result == True:
            return 1
        elif result == False:
            return -1
        else:
            return 0

    packets = []
    for line in lines:
        if line:
            packets.append(eval(line))

    div_1 = [[2]]
    div_2 = [[6]]
    packets.append(div_1)
    packets.append(div_2)

    from functools import cmp_to_key
    packets = sorted(packets, key=cmp_to_key(cmp), reverse=True)
    for i, p in enumerate(packets):
        print(i, p)

    a = packets.index(div_1) + 1
    b = packets.index(div_2) + 1
    print('part 2:', a, b, a * b)


class RockPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.at_rest = False

    def __repr__(self):
        return f'({self.x},{self.y})'

    def fall(self, grid, with_floor=None):
        try:
            if grid[self.y+1][self.x] == '.':
                self.y += 1
            elif grid[self.y+1][self.x-1] == '.':
                self.y += 1
                self.x -= 1
            elif grid[self.y+1][self.x+1] == '.':
                self.y += 1
                self.x += 1
            else:
                return 'stop'

        except IndexError:
            return 'out'

    def fall_with_floor(self, grid):
        try:
            if grid[self.y+1][self.x] == '.':
                self.y += 1
            elif grid[self.y+1][self.x-1] == '.':
                self.y += 1
                self.x -= 1
            elif grid[self.y+1][self.x+1] == '.':
                self.y += 1
                self.x += 1
            else:
                return 'stop'
        except IndexError:
            return '?'


    def at_source(self):
        return self.x == 500 and self.y == 0

    # def fall(self, grid):



class RockFormation:
    def __init__(self, points):
        self.points = points

    def __repr__(self):
        return f'{self.points}'



def day_14_a(text):
    lines = text.splitlines()

    rocks = []
    for line in lines:
        raw_points = line.split('->')
        raw_points = [p.strip().split(',') for p in raw_points]
        points = []
        for point in raw_points:
            x, y = point
            points.append(RockPoint(int(x), int(y)))
        rocks.append(RockFormation(points))

    x_values = []
    y_values = []
    for r in rocks:
        for point in r.points:
            x_values.append(point.x)
            y_values.append(point.y)

    height = max(y_values) + 1
    width = max(x_values) + 1

    def make_grid():
        grid = []

        for y in range(height):
            grid.append([])
            for _ in range(width):
                grid[y].append('.')

        print('height:', height)
        print('width:', width)

        for r in rocks:
            for i, point in enumerate(r.points):
                if i == 0:
                    continue
                start = r.points[i-1]
                end = point

                grid[start.y][start.x] = '#'
                grid[end.y][end.x] = '#'

                # draw vertically
                if start.x == end.x:
                    draw_y = min(start.y, end.y)
                    for dy in range(abs(start.y - end.y)):
                        grid[draw_y + dy][start.x] = '#'
                # draw horizontally
                elif start.y == end.y:
                    draw_x = min(start.x, end.x)
                    for dx in range(abs(start.x - end.x)):
                        print('trying to draw at', start.y, draw_x + dx)
                        grid[start.y][draw_x + dx] = '#'
                else:
                    raise ValueError('cannot draw diagonally', start, end)
        return grid

    grid = make_grid()

    for row in grid:
        print(''.join(row[450:]))

    def emit_sand(grid):
        sand = RockPoint(500, 0)

        while True:
            result = sand.fall(grid, with_floor=height+2)
            if result in ('stop', 'out'):
                break

        if result == 'stop':
            return sand
        return None


    sand_particles = []
    while True:
        print(' - - - - ')
        rest_position = emit_sand(grid)
        if rest_position is None:
            break
        sand_particles.append(rest_position)
        grid[rest_position.y][rest_position.x] = 'o'
        for row in grid:
            print(''.join(row[450:]))

    print('part 1:', len(sand_particles))


def day_14_b(text):
    lines = text.splitlines()

    rocks = []
    for line in lines:
        raw_points = line.split('->')
        raw_points = [p.strip().split(',') for p in raw_points]
        points = []
        for point in raw_points:
            x, y = point
            points.append(RockPoint(int(x), int(y)))
        rocks.append(RockFormation(points))

    x_values = []
    y_values = []
    for r in rocks:
        for point in r.points:
            x_values.append(point.x)
            y_values.append(point.y)

    height = max(y_values) + 1 + 2
    width = max(x_values) + 1
    width *= 2

    def make_grid():
        grid = []

        for y in range(height):
            grid.append([])
            for _ in range(width):
                grid[y].append('.')

        print('height:', height)
        print('width:', width)

        for r in rocks:
            for i, point in enumerate(r.points):
                if i == 0:
                    continue
                start = r.points[i-1]
                end = point

                grid[start.y][start.x] = '#'
                grid[end.y][end.x] = '#'

                # draw vertically
                if start.x == end.x:
                    draw_y = min(start.y, end.y)
                    for dy in range(abs(start.y - end.y)):
                        grid[draw_y + dy][start.x] = '#'
                # draw horizontally
                elif start.y == end.y:
                    draw_x = min(start.x, end.x)
                    for dx in range(abs(start.x - end.x)):
                        print('trying to draw at', start.y, draw_x + dx)
                        grid[start.y][draw_x + dx] = '#'
                else:
                    raise ValueError('cannot draw diagonally', start, end)

        for x in range(width):
            grid[height-1][x] = '#'
        return grid

    grid = make_grid()

    for row in grid:
        print(''.join(row[450:510]))

    def emit_sand(grid):
        sand = RockPoint(500, 0)

        while True:
            result = sand.fall_with_floor(grid)
            if result:
                break

        return sand


    sand_particles = []
    rest_position = RockPoint(0, 0)
    while not rest_position.at_source():
        print(' - - - - ')
        rest_position = emit_sand(grid)
        if rest_position is None:
            break
        sand_particles.append(rest_position)
        grid[rest_position.y][rest_position.x] = 'o'
        # for row in grid:
            # print(''.join(row[450:510]))
        print('rest_position:', rest_position)

    print('part 2:', len(sand_particles))


class SB:
    def __init__(self, x, y, kind, closest_beacon):
        self.x = x
        self.y = y
        self.kind = kind
        self.closest_beacon = closest_beacon

    def __repr__(self):
        return f'({self.x},{self.y})'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)


def day_15_a(text, target_y):
    lines = text.splitlines()

    excluded_points = set()
    occupied = set()

    for line in lines:
        sx, sy, bx, by = extract_integers(line)
        beacon = SB(bx, by, 'beacon', None)
        sensor = SB(sx, sy, 'sensor', beacon)

        occupied.add((sx, sy))
        occupied.add((bx, by))


    for line in lines:
        sx, sy, bx, by = extract_integers(line)
        beacon = SB(bx, by, 'beacon', None)
        sensor = SB(sx, sy, 'sensor', beacon)

        distance = beacon.distance(sensor)

        left_x = sx - distance
        right_x = sx + distance
        bottom_y = sy + distance
        top_y = sy - distance

        for y in range(top_y, bottom_y+1):
            if y != target_y:
                continue
            for x in range(left_x, right_x+1):

                point = SB(x, y, 'excl', None)
                raw_point = (x, y)

                if sensor.distance(point) <= distance and raw_point not in occupied:
                    excluded_points.add(raw_point)

    print(len(excluded_points))
