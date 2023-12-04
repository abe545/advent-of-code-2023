from dataclasses import dataclass

from day3_input import actual_input

example_input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

def has_symbol(s: str):
    return any(True for c in s if not c.isdigit() and c != ".")

@dataclass
class PotentialPartNumber:
    schematic_line: int
    start_x: int
    end_x: int

    def is_part_number(self, schematic_lines: list[str]):
        line_length = len(schematic_lines[0])
        if self.schematic_line > 0 and has_symbol(schematic_lines[self.schematic_line - 1][max(0, self.start_x - 1):min(line_length, self.end_x + 2)]):
            return True
        if (self.start_x > 0) and has_symbol((schematic_lines[self.schematic_line][self.start_x - 1])):
            return True
        if (self.end_x < line_length - 1) and has_symbol((schematic_lines[self.schematic_line][self.end_x + 1])):
            return True
        if (self.schematic_line < len(schematic_lines) - 1) and has_symbol(schematic_lines[self.schematic_line + 1][max(0, self.start_x - 1):min(line_length, self.end_x + 2)]):
            return True
        return False

    def get_part_number(self, schematic_lines: list[str]):
        return int(schematic_lines[self.schematic_line][self.start_x:self.end_x+1])

def find_part_numbers(schematic: str):
    potentialPartNumbers: list[PotentialPartNumber] = []
    schematicLines = schematic.splitlines()
    for y in range(0, len(schematicLines)):
        for x in range(0, len(schematicLines[y])):
            if (schematicLines[y][x].isdigit()):
                if len(potentialPartNumbers) and potentialPartNumbers[-1].schematic_line == y and potentialPartNumbers[-1].end_x == x-1:
                    potentialPartNumbers[-1].end_x = x
                else:
                    potentialPartNumbers.append(PotentialPartNumber(y, x, x))

    return list(ppn.get_part_number(schematicLines) for ppn in potentialPartNumbers if ppn.is_part_number(schematicLines))

def part1(schematic = example_input):
    return sum(find_part_numbers(schematic))


print(part1(actual_input))
