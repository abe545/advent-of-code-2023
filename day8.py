from __future__ import annotations
from dataclasses import dataclass

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
        nodes = [GraphNode.from_str(s) for s in lines[2:]]
        nodes_by_name = { n.name:n for n in nodes }

        return Graph(operations, nodes_by_name)

    def steps_required(self):
        count = 0
        cur_node = self.nodes["AAA"]
        while cur_node.name != "ZZZ":
            op = self.operations[count % len(self.operations)]
            count += 1
            cur_node = self.nodes[cur_node.left if op == "L" else cur_node.right]
        return count

@timer
def part1(s = example_input_2):
    graph = Graph.from_str(s)
    return graph.steps_required()


print(part1(actual_input))
