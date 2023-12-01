example_input = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

def part1(input_string: str = example_input):
    lines = input_string.split('\n')
    for line in map(_ints, lines):
        yield line[0]*10+line[-1]

def _ints(input_string: str):
    return list(int(c) for c in input_string if c.isdigit())