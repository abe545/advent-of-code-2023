import itertools
from collections import defaultdict
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
        if self.start_x > 0 and has_symbol((schematic_lines[self.schematic_line][self.start_x - 1])):
            return True
        if self.end_x < line_length - 1 and has_symbol((schematic_lines[self.schematic_line][self.end_x + 1])):
            return True
        if self.schematic_line < len(schematic_lines) - 1 and has_symbol(schematic_lines[self.schematic_line + 1][max(0, self.start_x - 1):min(line_length, self.end_x + 2)]):
            return True
        return False

    def get_part_number(self, schematic_lines: list[str]):
        return int(schematic_lines[self.schematic_line][self.start_x:self.end_x+1])

@dataclass
class PartNumber:
    schematic_line: int
    start_x: int
    end_x: int
    part_number: int

@dataclass
class PotentialGear:
    schematic_line: int
    x: int

    def is_gear(self, part_numbers: dict[int,list[PartNumber]]):
        return sum(itertools.chain.from_iterable([
            [1 for ppn in part_numbers.get(self.schematic_line - 1, []) if self.is_connected_horizontally(ppn)],
            [1 for ppn in part_numbers.get(self.schematic_line, []) if self.is_connected_horizontally(ppn)],
            [1 for ppn in part_numbers.get(self.schematic_line + 1, []) if self.is_connected_horizontally(ppn)]
        ])) == 2

    def is_connected_horizontally(self, pn: PartNumber):
        return pn.start_x - 1 <= self.x <= pn.end_x + 1

    def gear_ratio(self, part_numbers: dict[int,list[PartNumber]]):
        adjacent_parts = list(itertools.chain.from_iterable([
            [pn.part_number for pn in part_numbers.get(self.schematic_line - 1, []) if self.is_connected_horizontally(pn)],
            [pn.part_number for pn in part_numbers.get(self.schematic_line, []) if self.is_connected_horizontally(pn)],
            [pn.part_number for pn in part_numbers.get(self.schematic_line + 1, []) if self.is_connected_horizontally(pn)]
        ]))
        return adjacent_parts[0] * adjacent_parts[1]

def find_potential_part_numbers(schematic_lines: list[str]):
    for y, _ in enumerate(schematic_lines):
        x = 0
        while x < len(schematic_lines[y]):
            if schematic_lines[y][x].isdigit():
                first_x = x
                while x < len(schematic_lines[y]) and schematic_lines[y][x].isdigit():
                    x += 1
                yield PotentialPartNumber(y, first_x, x-1)
            else:
                x += 1

def find_part_numbers(schematic_lines: list[str]):
    return [
        PartNumber(ppn.schematic_line, ppn.start_x, ppn.end_x, ppn.get_part_number(schematic_lines))
        for ppn in find_potential_part_numbers(schematic_lines) if ppn.is_part_number(schematic_lines)
    ]

def part1(schematic = example_input):
    return sum(pn.part_number for pn in find_part_numbers(schematic.splitlines()))

def part2(schematic = example_input):
    schematic_lines = schematic.splitlines()
    part_numbers = find_part_numbers(schematic_lines)
    part_numbers_by_line = defaultdict(list)
    for pn in part_numbers:
        part_numbers_by_line[pn.schematic_line].append(pn)

    potential_gears = [PotentialGear(y, x) for y, line in enumerate(schematic_lines) for x, c in enumerate(line) if c == "*"]
    return sum(gear.gear_ratio(part_numbers_by_line) for gear in potential_gears if gear.is_gear(part_numbers_by_line))


print(part1(actual_input), part2(actual_input))
