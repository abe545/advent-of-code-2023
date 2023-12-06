from __future__ import annotations
from dataclasses import dataclass
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
        ranges.sort(key=lambda ar: ar.source.start)
        return AlmanacRanges(ranges)

    def map_range(self, rs: list[range]) -> list[range]:
        acc = []
        while rs:
            r = rs.pop()
            found_overlap = False
            for known_range in self.ranges:
                if found_overlap := known_range.is_overlapping(r):
                    if r.start >= known_range.source.start and r.stop <= known_range.source.stop:
                        # the range is fully contained in the known range, so offset it and add it to the result
                        acc.append(range(r.start + known_range.offset, r.stop + known_range.offset))
                    elif r.start < known_range.source.start:
                        # the range partially overlaps the start of the known range, so add the portion in the
                        # known range to the result (after offsetting it)
                        # add the remainder back to rs, so we can process it in future iterations
                        acc.append(range(known_range.source.start + known_range.offset, r.stop + known_range.offset))
                        rs.append(range(r.start, known_range.source.start))
                    elif r.stop > known_range.source.stop:
                        # the range partially overlaps the end of the known range, so add the portion in the
                        # known range to the result (after offsetting it)
                        # add the remainder back to rs, so we can process it in future iterations
                        acc.append(range(r.start + known_range.offset, known_range.source.stop + known_range.offset))
                        rs.append(range(known_range.source.stop, r.stop))
                    break
            if not found_overlap:
                # no known overlapping ranges, so just add it as-is to the results
                acc.append(r)

        return acc

@dataclass
class AlmanacRange:
    source: range
    offset: int

    @classmethod
    def from_str(cls, s: str):
        parts = s.split()
        source_start = int(parts[1])
        destination_start = int(parts[0])
        count = int(parts[2])
        return AlmanacRange(range(source_start, source_start+count), destination_start - source_start)

    def is_overlapping(self, value: range):
        return value.start in self.source or value.stop - 1 in self.source

@dataclass
class Almanac:
    seeds: list[int]
    ranges: list[AlmanacRanges]

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
            [
                seed_to_soil_map,
                soil_to_fertilizer_map,
                fertilizer_to_water_map,
                water_to_light_map,
                light_to_temperature_map,
                temperature_to_humidity_map,
                humidity_to_location_map,
            ],
        )

    def _get_min_seed_location(self, seed_ranges: list[range]) -> list[int]:
        cur = seed_ranges
        for r in self.ranges:
            cur = r.map_range(cur)
        return min(map(lambda r: r.start, cur))

    def get_min_location_number(self) -> int:
        return min(self._get_min_seed_location([range(s, s)]) for s in self.seeds)

    def get_min_location_number_if_seeds_are_ranges(self):
        acc = []
        i = 0
        while i < len(self.seeds):
            seed_start = self.seeds[i]
            seed_count = self.seeds[i + 1]
            acc.append(self._get_min_seed_location([range(seed_start, seed_start + seed_count - 1)]))
            i += 2
        return min(acc)

def part1(s=example_input):
    almanac = Almanac.from_str(s)
    return almanac.get_min_location_number()

def part2(s=example_input):
    almanac = Almanac.from_str(s)
    return almanac.get_min_location_number_if_seeds_are_ranges()


print(part1(actual_input), part2(actual_input))
