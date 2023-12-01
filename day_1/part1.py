from input import example_input

def get_digits(input_string: str = example_input):
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

