example_input = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

def get_digits_part1(input_string: str = example_input):
    lines = input_string.split('\n')
    for line in lines:
        first_digit = ''
        last_digit = ''
        for char in line:
            if char.isdigit():
                first_digit = char
                break
        for char in reversed(line):
            if char.isdigit():
                last_digit = char
                break

        yield int(first_digit+last_digit)

