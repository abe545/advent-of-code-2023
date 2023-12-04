from __future__ import annotations
from dataclasses import dataclass
from day4_input import actual_input

example_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

@dataclass
class ScratchCard:
    winning_numbers: set[int]
    numbers: list[int]
    card_number: int

    def part1_score(self):
        matches = sum(1 for n in self.numbers if n in self.winning_numbers)
        return 0 if matches == 0 else 2 ** (matches-1)

    @classmethod
    def from_str(cls, s: str) -> ScratchCard:
        parts = s.split(':')

        number_parts = parts[1].split('|')
        return ScratchCard(
            {int(n) for n in number_parts[0].split()},
            {int(n) for n in number_parts[1].split()},
            int(parts[0][5:])
        )

def part1(cards=example_input):
    return sum(ScratchCard.from_str(s).part1_score() for s in cards.splitlines())


print(part1(actual_input))
