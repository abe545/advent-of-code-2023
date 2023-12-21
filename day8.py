from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
from typing import Callable

from day8_input import actual_input
from shared import timer

example_input_1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

example_input_2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

example_input_3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

@dataclass
class GraphNode:
    name: str
    left: str
    right: str

    @classmethod
    def from_str(cls, s: str):
        name = s[:3]
        left = s[7:10]
        right = s[12:-1]
        return GraphNode(name, left, right)

@dataclass
class Graph:
    operations: list[str]
    nodes: dict[str, GraphNode]

    @classmethod
    def from_str(cls, s: str):
        lines = s.splitlines()
        operations = list(lines[0])
        nodes = { s[:3]:GraphNode.from_str(s) for s in lines[2:] }

        return Graph(operations, nodes)

    def steps_required(self, is_final_node: Callable[[str], bool], start_node = "AAA"):
        count = 0
        cur_node = self.nodes[start_node]
        while not is_final_node(cur_node.name):
            op = self.operations[count % len(self.operations)]
            count += 1
            cur_node = self.nodes[cur_node.left if op == "L" else cur_node.right]
        return count

@timer
def part1(s = example_input_2):
    graph = Graph.from_str(s)
    return graph.steps_required(lambda node: node == "ZZZ")

def lcm(a: int, b: int) -> int:
    return int(a * b / gcd(a, b))

def gcd(a: int, b: int) -> int:
    return a if b == 0 else gcd(b, a % b)

@timer
def part2(s = example_input_3):
    graph = Graph.from_str(s)
    start_nodes = (n for n in graph.nodes.keys() if n[-1] == "A")
    all_steps_required = map(lambda n: graph.steps_required(lambda node: node[-1] == "Z", start_node=n), start_nodes)

    return reduce(lcm, all_steps_required, 1)


print(part1(actual_input), part2(actual_input))
