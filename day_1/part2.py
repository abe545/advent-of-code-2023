from itertools import count

example_input = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

_numberMap = dict(zip("one two three four five six seven eight nine".split(), count(1)))
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

    for k,v in _numberMap.items():
        if find(input_string, k):
            return v

def get_digits_part2(input_string: str = example_input):
    lines = input_string.splitlines()
    for line in lines:
        first_digit=None
        second_digit=None
        line_len = len(line)
        for i in range(line_len):
            first_digit = maybe_integer(line[i:])
            if first_digit is not None:
                break
        for i in range(line_len):
            second_digit = maybe_integer(line[:line_len-i], from_end=True)
            if second_digit is not None:
                break
        yield 10*first_digit+second_digit
