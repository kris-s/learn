import re
from array import array
from collections import Counter
from queue import PriorityQueue

from archive import read_file


print("Saving Christmas again!")

example = """[1,2]
[[1,2],3]
[9,[8,7]]
[[1,9],[8,5]]
[[[[1,2],[3,4]],[[5,6],[7,8]]],9]
[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]"""

ex2 = """[[[[4,3],4],4],[7,[[8,4],9]]]
[1,1]"""

def day_eighteen_prep(data):
    lines = []
    for line in data.split('\n'):
        lines.append(eval(line))

    return lines


def snailfish_add(a, b):
    return [a] + [b]


def snailfish_reduce(value):
    digits = re.compile(r'\d')

    value_str = str(value)

    def explode_walk(value, depth):
        print('explode_walking with', value, 'depth', depth)
        if depth > 3:
            return value
        elif isinstance(value, list):
            left, right = value

            return explode_walk(left, depth+1)
            return explode_walk(right, depth+1)
        else:
            return None

    explode_target = 1

    while explode_target is not None:
        explode_target = explode_walk(value, 0)

        if explode_target:
            print('exploding', explode_target)
            explode_str = str(explode_target)
            left, right = explode_target
            index = value_str.index(explode_str)

            left_sub = value_str[:index]
            left_digits = digits.findall(left_sub)
            if left_digits:
                left_replace = left_digits[-1]
                # print('left replace:', left_replace)
                left_sub = ''.join(reversed(left_sub))
                left_sub = left_sub.replace(left_replace, str(int(left_replace)+left), 1)
                left_sub = ''.join(reversed(left_sub))

            right_sub = value_str[index+len(explode_str):]
            right_digits = digits.findall(right_sub)
            if right_digits:
                right_replace = right_digits[0]
                # print('right_replace', int(right_replace))
                right_sub = right_sub.replace(right_replace, str(int(right_replace)+right), 1)

            value_str = f'{left_sub}0{right_sub}'
            value = eval(value_str)
            print(value)

    return eval(value_str)


def day_eighteen_a(data):
    numbers = day_eighteen_prep(data)
    value = numbers[0]

    for line in numbers[1:]:
        value = snailfish_add(value, line)
        value = snailfish_reduce(value)



print(day_eighteen_a(ex2))
