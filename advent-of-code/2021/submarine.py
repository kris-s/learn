from collections import Counter

from archive import read_file


print("Saving Christmas again!")


example = """16,1,2,0,4,2,7,1,2,14"""


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
