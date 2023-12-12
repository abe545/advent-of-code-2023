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

card_sort_order_with_jokers = {
    'A': 13,
    'K': 12,
    'Q': 11,
    'J': 1,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2
}

class HandScore(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


joker_hand_score_increments = {
    (HandScore.HIGH_CARD, 1): HandScore.ONE_PAIR,
    (HandScore.HIGH_CARD, 2): HandScore.THREE_OF_A_KIND,
    (HandScore.HIGH_CARD, 3): HandScore.FOUR_OF_A_KIND,
    (HandScore.HIGH_CARD, 4): HandScore.FIVE_OF_A_KIND,
    (HandScore.ONE_PAIR, 1): HandScore.THREE_OF_A_KIND,
    (HandScore.ONE_PAIR, 2): HandScore.FOUR_OF_A_KIND,
    (HandScore.ONE_PAIR, 3): HandScore.FIVE_OF_A_KIND,
    (HandScore.THREE_OF_A_KIND, 1): HandScore.FOUR_OF_A_KIND,
    (HandScore.THREE_OF_A_KIND, 2): HandScore.FIVE_OF_A_KIND,
    (HandScore.FOUR_OF_A_KIND, 1): HandScore.FIVE_OF_A_KIND,
    (HandScore.TWO_PAIR, 1): HandScore.FULL_HOUSE,
}

def increment_card(agg: dict[str, int], card: str) -> dict[str, int]:
    agg[card] += 1
    return agg

def get_hand_score(cards: list[str]) -> HandScore:
    card_counts: dict[str, int] = reduce(increment_card, cards, defaultdict(int))
    max_card_count = max(card_counts.values())
    if max_card_count == 5:
        return HandScore.FIVE_OF_A_KIND
    if max_card_count == 4:
        return HandScore.FOUR_OF_A_KIND
    if max_card_count == 3:
        if min(card_counts.values()) == 2:
            return HandScore.FULL_HOUSE
        return HandScore.THREE_OF_A_KIND
    if max_card_count == 2:
        pair_count = sum((1 for cc in card_counts.values() if cc == 2))
        return HandScore.TWO_PAIR if pair_count == 2 else HandScore.ONE_PAIR

    return HandScore.HIGH_CARD

def get_hand_score_with_jokers(cards: list[str]) -> HandScore:
    joker_count = sum((1 for c in cards if c == 'J'))
    if joker_count == 5:
        return HandScore.FIVE_OF_A_KIND

    base_score = get_hand_score([c for c in cards if c != 'J'])

    if joker_count == 0:
        return base_score

    return joker_hand_score_increments[base_score, joker_count]

@dataclass(frozen=True)
class Hand:
    cards: list[str]
    bid: int
    hand_score: HandScore
    jokers_enabled: bool

    @classmethod
    def from_str(cls, s: str, jokers_enabled = False):
        parts = s.split()
        cards = list(parts[0])
        return cls(
            cards,
            int(parts[1]),
            get_hand_score_with_jokers(cards) if jokers_enabled else get_hand_score(cards),
            jokers_enabled
        )

    def __lt__(self, other):
        if self.hand_score.value < other.hand_score.value:
            return True
        if self.hand_score == other.hand_score:
            for x, y in zip(self.cards, other.cards):
                if x == y:
                    continue
                if self.jokers_enabled:
                    return card_sort_order_with_jokers[x] < card_sort_order_with_jokers[y]
                return card_sort_order[x] < card_sort_order[y]
        return False

def part1(s = example_input):
    hands = [Hand.from_str(l) for l in s.splitlines()]
    hands.sort()
    return sum((i + 1) * h.bid for i, h in enumerate(hands))

def part2(s = example_input):
    hands = [Hand.from_str(l, jokers_enabled=True) for l in s.splitlines()]
    hands.sort()
    return sum((i + 1) * h.bid for i, h in enumerate(hands))


print(part1(actual_input), part2(actual_input))
