from functools import reduce
from math import ceil, floor, sqrt

from day6_input import actual_input

example_input = """Time:      7  15   30
Distance:  9  40  200"""

def parse_input_for_part1(s: str):
    lines = s.splitlines()
    times = [int(x.strip()) for x in lines[0].split()[1:]]
    distances = [int(x.strip()) for x in lines[1].split()[1:]]
    return zip(times, distances)

def parse_input_for_part2(s: str):
    lines = s.splitlines()
    time = int(lines[0].split(":")[1].replace(" ", "").strip())
    distance = int(lines[1].split(":")[1].replace(" ", "").strip())
    return time, distance

def count_winning_strategies(race_time: int, race_distance_record: int) -> int:
    # race distiance is (race_time - time_pressed) * time_pressed
    # so to beat the record, we need to solve for time_pressed using the quadratic formula
    # this reduces to -race_time +/- sqrt(race_time^2 - 4 * race_distance_record) / -2
    temp_square = sqrt(race_time**2 - 4*(race_distance_record+1)) / -2.0
    half_race_time = race_time / 2.0
    minimum_press = ceil(half_race_time + temp_square)
    maximum_press = floor(half_race_time - temp_square)
    return 1 + maximum_press - minimum_press

def part1(s = example_input):
    times_and_distances = parse_input_for_part1(s)
    return reduce(int.__mul__, map(lambda t: count_winning_strategies(*t), times_and_distances))

def part2(s = example_input):
    time, distance = parse_input_for_part2(s)
    return count_winning_strategies(time, distance)


print(part1(actual_input), part2(actual_input))
