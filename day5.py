from __future__ import annotations
from dataclasses import dataclass
from itertools import accumulate
from day5_input import actual_input

example_input = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

@dataclass
class AlmanacRanges:
    ranges: list[AlmanacRange]

    @classmethod
    def from_str(cls, s: str):
        ranges = [AlmanacRange.from_str(x) for x in s.splitlines()[1:]]
        return AlmanacRanges(ranges)

    def get_next(self, item: int):
        for r in self.ranges:
            if r.in_range(item):
                return r.destination_start + item - r.source_start
        return item

@dataclass
class AlmanacRange:
    source_start: int
    destination_start: int
    source_end: int

    @classmethod
    def from_str(cls, s: str):
        parts = s.split()
        source_range_start = int(parts[1])
        destination_range_start = int(parts[0])
        count = int(parts[2])
        return AlmanacRange(source_range_start, destination_range_start, source_range_start+count)

    def in_range(self, value: int):
        return self.source_start <= value <= self.source_end

@dataclass
class Almanac:
    seeds: list[int]
    seed_to_soil_map: AlmanacRanges
    soil_to_fertilizer_map: AlmanacRanges
    fertilizer_to_water_map: AlmanacRanges
    water_to_light_map: AlmanacRanges
    light_to_temperature_map: AlmanacRanges
    temperature_to_humidity_map: AlmanacRanges
    humidity_to_location_map: AlmanacRanges

    @classmethod
    def from_str(cls, s: str) -> Almanac:
        parts = s.split("\n\n")
        seeds = [int(n) for n in parts[0][7:].split()]
        seed_to_soil_map = AlmanacRanges.from_str(parts[1])
        soil_to_fertilizer_map = AlmanacRanges.from_str(parts[2])
        fertilizer_to_water_map = AlmanacRanges.from_str(parts[3])
        water_to_light_map = AlmanacRanges.from_str(parts[4])
        light_to_temperature_map = AlmanacRanges.from_str(parts[5])
        temperature_to_humidity_map = AlmanacRanges.from_str(parts[6])
        humidity_to_location_map = AlmanacRanges.from_str(parts[7])

        return Almanac(
            seeds,
            seed_to_soil_map,
            soil_to_fertilizer_map,
            fertilizer_to_water_map,
            water_to_light_map,
            light_to_temperature_map,
            temperature_to_humidity_map,
            humidity_to_location_map,
        )

    def get_location_numbers(self) -> list[int]:
        ranges = [
            self.seed_to_soil_map,
            self.soil_to_fertilizer_map,
            self.fertilizer_to_water_map,
            self.water_to_light_map,
            self.light_to_temperature_map,
            self.temperature_to_humidity_map,
            self.humidity_to_location_map,
        ]
        return [[x for x in accumulate(ranges, lambda acc, d: d.get_next(acc), initial=seed)][-1] for seed in self.seeds]

def part1(s=example_input):
    almanac = Almanac.from_str(s)
    return min(almanac.get_location_numbers())


print(part1(actual_input))
