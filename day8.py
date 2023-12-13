from __future__ import annotations
from dataclasses import dataclass

from day8_input import actual_input

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
class GraphNodeBuilder:
    name: str
    left: str
    right: str

    @classmethod
    def from_str(cls, s: str):
        name = s[:3]
        left = s[7:10]
        right = s[12:-1]
        return GraphNodeBuilder(name, left, right)

class GraphNode:
    name: str
    left: GraphNode
    right: GraphNode
    is_terminal_node: bool

    def __init__(self, name: str):
        self.name = name
        self.is_terminal_node = name == "ZZZ"

    def __repr__(self):
        return f"{self.name=}, left={self.left.name}, right={self.right.name}"

@dataclass
class Graph:
    operations: list[str]
    start_node: GraphNode

    @classmethod
    def from_str(cls, s: str):
        lines = s.splitlines()
        operations = list(lines[0])
        nodes = [GraphNodeBuilder.from_str(s) for s in lines[2:]]
        nodes_by_name = { n.name:GraphNode(n.name) for n in nodes }
        for node in nodes:
            nodes_by_name[node.name].left = nodes_by_name[node.left]
            nodes_by_name[node.name].right = nodes_by_name[node.right]

        return Graph(operations, nodes_by_name[nodes[0].name])

    def steps_required(self):
        count = 0
        cur_node = self.start_node
        while not cur_node.is_terminal_node:
            op = self.operations[count % len(self.operations)]
            print(f"{op=} {cur_node=}")
            count += 1
            cur_node = cur_node.left if op == "L" else cur_node.right
        return count

def part1(s = example_input_2):
    graph = Graph.from_str(s)
    return graph.steps_required()


print(part1(actual_input))
