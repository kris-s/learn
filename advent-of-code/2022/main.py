
import sys
from pathlib import Path
import re


print("\n🎄 It's time to save Christmas. 🎄")


def load(path):
    path = Path(path)
    return path.read_text()


SAMPLE = load('sample.txt')
INPUT = load('input.txt')


def extract_integers(line):
    return list(map(int, re.findall(r'(-?\d+)', line)))


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


def day_15_b(text, limit):
    lines = text.splitlines()

    sensors = []
    beacons = []

    excluded_rows = []
    occupied = set()

    for line in lines:
        sx, sy, bx, by = extract_integers(line)
        beacon = SB(bx, by, 'beacon', None)
        sensor = SB(sx, sy, 'sensor', beacon)

        beacons.append(beacon)
        sensors.append(sensor)

        occupied.add((sx, sy))
        occupied.add((bx, by))

    for row in range(limit+1):
        excluded_points = set()
        for sensor in sensors:
            distance = sensor.distance(sensor.closest_beacon)

            left_x = sensor.x - distance
            if left_x < 0:
                left_x = 0

            right_x = sx + distance
            if right_x > limit:
                right_x = limit

            bottom_y = sy + distance
            if bottom_y > limit:
                bottom_y = limit

            top_y = sy - distance
            if top_y < 0:
                top_y = 0

            for y in range(top_y, bottom_y+1):
                if y != row:
                    continue
                for x in range(left_x, right_x+1):

                    point = SB(x, y, 'excl', None)
                    raw_point = (x, y)

                    if sensor.distance(point) <= distance and raw_point not in occupied:
                        excluded_points.add(raw_point)

        excluded_rows.append(excluded_points)
    for i, row in enumerate(excluded_rows):
        if i == 11 or i == 10 or i == 12:
            print(row)
        # if len(row) == limit - 1:
        #     print(i, row)
        #     break

day_15_a(SAMPLE, 10)
day_15_b(SAMPLE, 20)

# day_15_a(INPUT, 2000000)
# day_15_b(INPUT, 4000000)
