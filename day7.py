from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from functools import reduce

from day7_input import actual_input

example_input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

card_sort_order = {
    'A': 13,
    'K': 12,
    'Q': 11,
    'J': 10,
    'T': 9,
    '9': 8,
    '8': 7,
    '7': 6,
    '6': 5,
    '5': 4,
    '4': 3,
    '3': 2,
    '2': 1
}

class HandScore(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

def increment_card(agg: dict[str, int], card: str) -> dict[str, int]:
    agg[card] += 1
    return agg

def get_hand_score(cards: list[str]) -> HandScore:
    card_counts: dict[str, int] = reduce(increment_card, cards, defaultdict(int))
    if len(card_counts) == 1:
        return HandScore.FIVE_OF_A_KIND
    if len(card_counts) == 2:
        if max(card_counts.values()) == 4:
            return HandScore.FOUR_OF_A_KIND
        return HandScore.FULL_HOUSE
    if len(card_counts) == 3:
        if max(card_counts.values()) == 3:
            return HandScore.THREE_OF_A_KIND
        return HandScore.TWO_PAIR
    if len(card_counts) == 4:
        return HandScore.ONE_PAIR
    if len(card_counts) == 5:
        return HandScore.HIGH_CARD

@dataclass(frozen=True)
class Hand:
    cards: list[str]
    bid: int
    hand_score: HandScore

    @classmethod
    def from_str(cls, s: str):
        parts = s.split()
        cards = list(parts[0])
        return cls(cards, int(parts[1]), get_hand_score(cards))

    def __lt__(self, other):
        if self.hand_score.value < other.hand_score.value:
            return True
        if self.hand_score == other.hand_score:
            for x, y in zip(self.cards, other.cards):
                if x == y:
                    continue
                return card_sort_order[x] < card_sort_order[y]
        return False

def part1(s = example_input):
    hands = [Hand.from_str(l) for l in s.splitlines()]
    hands.sort()
    return sum((i + 1) * h.bid for i, h in enumerate(hands))


print(part1(actual_input))
