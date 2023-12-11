from functools import reduce

from day6_input import actual_input

example_input = """Time:      7  15   30
Distance:  9  40  200"""

def parse_input(s: str):
    lines = s.splitlines()
    times = [int(x.strip()) for x in lines[0].split()[1:]]
    distances = [int(x.strip()) for x in lines[1].split()[1:]]
    return zip(times, distances)

def count_winning_strategies(race_time: int, race_distance_record: int) -> int:
    # race distiance is (race_time - time_pressed) * time_pressed
    # so to beat the record, we need to solve for time_pressed
    return len([1 for x in range(1, race_time - 1) if (race_time - x) * x > race_distance_record])

def part1(s = example_input):
    times_and_distances = parse_input(s)
    return reduce(int.__mul__, map(lambda t: count_winning_strategies(*t), times_and_distances))


print(part1(actual_input))
