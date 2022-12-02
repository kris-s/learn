
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
