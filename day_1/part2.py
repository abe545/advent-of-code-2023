from itertools import count

example_input = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

def maybe_integer(input_string: str, from_end: bool = False):
    if not len(input_string):
        return
    if input_string[0].isdigit():
        return input_string[0]
    if (not from_end and input_string.startswith("one")) or (from_end and input_string.startswith("eno")):
        return "1"
    if (not from_end and input_string.startswith("two")) or (from_end and input_string.startswith("owt")):
        return "2"
    if (not from_end and input_string.startswith("three")) or (from_end and input_string.startswith("eerht")):
        return "3"
    if (not from_end and input_string.startswith("four")) or (from_end and input_string.startswith("ruof")):
        return "4"
    if (not from_end and input_string.startswith("five")) or (from_end and input_string.startswith("evif")):
        return "5"
    if (not from_end and input_string.startswith("six")) or (from_end and input_string.startswith("xis")):
        return "6"
    if (not from_end and input_string.startswith("seven")) or (from_end and input_string.startswith("neves")):
        return "7"
    if (not from_end and input_string.startswith("eight")) or (from_end and input_string.startswith("thgie")):
        return "8"
    if (not from_end and input_string.startswith("nine")) or (from_end and input_string.startswith("enin")):
        return "9"

def get_digits_part2(input_string: str = example_input):
    lines = input_string.splitlines()
    for line in lines:
        first_digit=None
        second_digit=None
        for i in range(len(line)):
            first_digit = maybe_integer(line[i:], False)
            if first_digit is not None:
                break
        line = line[::-1]
        for i in range(len(line)):
            second_digit = maybe_integer(line[i:], True)
            if second_digit is not None:
                break
        yield int(first_digit+second_digit)