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

    def matches(self) -> int:
        return sum(1 for n in self.numbers if n in self.winning_numbers)

    def part1_score(self) -> int:
        return 0 if (matches := self.matches()) == 0 else 2 ** (matches-1)

    @classmethod
    def from_str(cls, s: str) -> ScratchCard:
        parts = s.split(':')

        number_parts = parts[1].split('|')
        return ScratchCard(
            {int(n) for n in number_parts[0].split()},
            {int(n) for n in number_parts[1].split()},
            int(parts[0][5:])
        )

def get_cards(cards: str) -> list[ScratchCard]:
    return [ScratchCard.from_str(s) for s in cards.splitlines()]

def part1(cards=example_input) -> int:
    return sum(c.part1_score() for c in get_cards(cards))

def part2(cards=example_input) -> int:
    card_counts = [(c.card_number, c.matches(), 1) for c in get_cards(cards)]
    for i, matches, count in card_counts:
        for j in range(i, i+matches):
            (card_number, card_matches, current_count) = card_counts[j]
            card_counts[j] = (card_number, card_matches, current_count + count)
    return sum(count for _,_,count in card_counts)


print(part1(actual_input), part2(actual_input))
