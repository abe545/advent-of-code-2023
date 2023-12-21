from dataclasses import dataclass

from day9_input import actual_input

example_input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

@dataclass
class OasisHistory:
    sequence: list[int]

    @classmethod
    def from_str(cls, l: str):
        sequence = [int(s) for s in l.split()]
        return OasisHistory(sequence)

    @staticmethod
    def _diff(seq: list[int]):
        for i, v in enumerate(seq):
            if (i == 0):
                continue
            yield v - seq[i-1]
    def find_next_digit(self):
        seq = self.sequence
        steps = [seq]
        while len(set(seq)) > 1:
            seq = list(self._diff(seq))
            steps.append(seq)

        while len(steps) > 1:
            seq = steps.pop()
            diff = seq[-1]
            n = steps[-1]
            n.append(n[-1] + diff)

        return steps[-1][-1]

@dataclass
class OasisHistories:
    sequences: list[OasisHistory]

    @classmethod
    def from_str(cls, s: str):
        sequences = [OasisHistory.from_str(s) for s in s.splitlines()]
        return OasisHistories(sequences)

def part1(s: str = example_input):
    oh = OasisHistories.from_str(s)
    return sum(map(OasisHistory.find_next_digit, oh.sequences))


print(part1(actual_input))
