from collections import Counter

from archive import read_file


print("Saving Christmas again!")


"""
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
"""

SEGMENT_FREQ = {
    "a": 8,
    "b": 6,
    "c": 8,
    "d": 7,
    "e": 4,
    "f": 9,
    "g": 7,
}


IDEAL_WIRING = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}

example = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""


SEGMENT_LENGTHS = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6,
}


def day_eight_prep(data):
    output = []
    for row in data.split("\n"):
        if not row:
            continue
        left, right = row.split("|")
        left_segments = left.split()
        right_segments = right.split()
        output.append((left_segments, right_segments))

    return output


def day_eight_a(data):
    data = day_eight_prep(data)
    count = 0

    for _, output_values in data:
        # 1, 4, 7, and 8
        lengths = [len(v) for v in output_values]
        count += lengths.count(SEGMENT_LENGTHS[1])
        count += lengths.count(SEGMENT_LENGTHS[4])
        count += lengths.count(SEGMENT_LENGTHS[7])
        count += lengths.count(SEGMENT_LENGTHS[8])

    return count


def get_wiring_map(signals):
    counts = Counter("".join(signals))
    segment_map = {}

    for ideal_wire, count in SEGMENT_FREQ.items():
        if count in (7, 8):
            continue

        for real_wire, real_count in counts.items():
            if real_count == count:
                segment_map[ideal_wire] = real_wire

    segments = {"a", "b", "c", "d", "e", "f", "g"}
    lengths_map = {len(sig): set(sig) for sig in signals}

    one = lengths_map[SEGMENT_LENGTHS[1]]
    four = lengths_map[SEGMENT_LENGTHS[4]]
    seven = lengths_map[SEGMENT_LENGTHS[7]]

    # in seven but not in one
    segment_map["a"] = (seven ^ one).pop()

    # the 8 count in one
    for wire in one:
        if wire not in segment_map.values():
            segment_map["c"] = wire

    # d from four
    for wire in four:
        if wire not in segment_map.values():
            segment_map["d"] = wire

    # g remains
    segment_map["g"] = (segments ^ set(segment_map.values())).pop()

    wiring_map = {}
    for number, ideal in IDEAL_WIRING.items():
        key = ""
        for wire in ideal:
            key += segment_map[wire]

        key = "".join(sorted(key))
        wiring_map[key] = str(number)

    return wiring_map


def day_eight_b(data):
    data = day_eight_prep(data)

    total = 0

    for signals, output_values in data:
        wiring_map = get_wiring_map(signals)
        display = ""

        for digit in output_values:
            display += wiring_map["".join(sorted(digit))]

        total += int(display)

    return total


# day_eight_input = read_file("day08.txt")
# print(day_eight_a(example))
# print(day_eight_a(day_eight_input))
# print(day_eight_b(example))
# print(day_eight_b(day_eight_input))
