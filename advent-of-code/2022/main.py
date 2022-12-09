
from pathlib import Path
import re


print("\n🎄 It's time to save Christmas. 🎄")


def load(path):
    path = Path(path)
    return path.read_text()


SAMPLE = load('sample.txt')
INPUT = load('input.txt')


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


day_9(SAMPLE)
day_9(INPUT)
