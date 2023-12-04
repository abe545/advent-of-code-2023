from day1_input import real_input
from itertools import count

part1_example_input = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

part2_example_input = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

_numberMap = dict(zip("one two three four five six seven eight nine".split(), count(1)))

def part1(input_string: str = part1_example_input):
    lines = input_string.split('\n')
    for line in map(_ints, lines):
        yield line[0] * 10 + line[-1]


def _ints(input_string: str):
    return list(int(c) for c in input_string if c.isdigit())


def maybe_integer(input_string: str, *, from_end: bool = False):
    if not len(input_string):
        return

    find = str.startswith
    if from_end:
        find = str.endswith
        if input_string[-1].isdigit():
            return int(input_string[-1])
    elif input_string[0].isdigit():
        return int(input_string[0])

    for k, v in _numberMap.items():
        if find(input_string, k):
            return v


def get_digits_part2(input_string: str = part2_example_input):
    lines = input_string.splitlines()
    for line in lines:
        first_digit = None
        second_digit = None
        line_len = len(line)
        for i in range(line_len):
            first_digit = maybe_integer(line[i:])
            if first_digit is not None:
                break
        for i in range(line_len):
            second_digit = maybe_integer(line[:line_len - i], from_end=True)
            if second_digit is not None:
                break
        yield 10 * first_digit + second_digit


print(sum(part1(real_input)), sum(get_digits_part2(real_input)))
