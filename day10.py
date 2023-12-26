from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from shared import timer
from day10_input import actual_input

simple_example_input = """.....
.S-7.
.|.|.
.L-J.
....."""

complex_example_input = """7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ"""

class NodeDirection(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

@dataclass(frozen=True)
class Node:
    is_start: bool
    row: int
    column: int
    connection1: Optional[NodeDirection]
    connection2: Optional[NodeDirection]
    char: str

    @classmethod
    def from_str(cls, s: str, row, column) -> Optional[Node]:
        is_start = False
        connection1 = None
        connection2 = None

        match s:
            case "S":
                is_start = True
            case "|":
                connection1 = NodeDirection.NORTH
                connection2 = NodeDirection.SOUTH
            case "-":
                connection1 = NodeDirection.EAST
                connection2 = NodeDirection.WEST
            case "L":
                connection1 = NodeDirection.NORTH
                connection2 = NodeDirection.EAST
            case "J":
                connection1 = NodeDirection.NORTH
                connection2 = NodeDirection.WEST
            case "7":
                connection1 = NodeDirection.WEST
                connection2 = NodeDirection.SOUTH
            case "F":
                connection1 = NodeDirection.EAST
                connection2 = NodeDirection.SOUTH
            case _:
                return None

        return Node(is_start, row, column, connection1, connection2, s)

@dataclass(frozen=True)
class Graph:
    nodes: dict[Tuple[int, int], Node]
    start: Node
    max_row: int
    max_column: int

    @classmethod
    def from_str(cls, s: str):
        nodes: dict[Tuple[int, int], Node] = {}
        start: Node = None
        lines = s.splitlines()
        for row, line in enumerate(lines):
            for column, c in enumerate(line):
                b = Node.from_str(c, row, column)
                if b:
                    nodes[(row, column)] = b
                    if b.is_start:
                        start = b
        assert start is not None
        return Graph(nodes, start, len(lines), len(lines[0]))

    def get_max_distance(self):
        max_distance = 0
        valid_start_directions = self._posible_start_directions()
        for start_direction in valid_start_directions:
            cur_distance = 1
            # print(20*'-')
            cur_node, from_direction = self._get_connected_node(self.start.row, self.start.column, start_direction)
            while cur_node and cur_node != self.start:
                # print(f"{from_direction}->{cur_node} {cur_distance=}")
                cur_distance += 1
                cur_node, from_direction = self._get_connected_node(cur_node.row, cur_node.column, from_direction)

            if cur_node == self.start:
                max_distance = max(max_distance, cur_distance)
        return int(max_distance / 2)

    def _get_connected_node(self, from_row, from_column, direction) -> Optional[Node]:
        match direction:
            case NodeDirection.NORTH:
                if from_row > 0:
                    node = self.nodes.get((from_row - 1, from_column))
                    if node.is_start:
                        return node, None
                    if node.connection1 != NodeDirection.SOUTH and node.connection2 != NodeDirection.SOUTH:
                        return None, None
                    exit_direction = node.connection2 if node.connection1 == NodeDirection.SOUTH else node.connection1
                    return node, exit_direction
            case NodeDirection.SOUTH:
                if from_row < self.max_row - 1:
                    node = self.nodes.get((from_row + 1, from_column))
                    if node.is_start:
                        return node, None
                    if node.connection1 != NodeDirection.NORTH and node.connection2 != NodeDirection.NORTH:
                        return None, None
                    exit_direction = node.connection2 if node.connection1 == NodeDirection.NORTH else node.connection1
                    return node, exit_direction
            case NodeDirection.WEST:
                if from_column > 0:
                    node = self.nodes.get((from_row, from_column - 1))
                    if node.is_start:
                        return node, None
                    if node.connection1 != NodeDirection.EAST and node.connection2 != NodeDirection.EAST:
                        return None, None
                    exit_direction = node.connection2 if node.connection1 == NodeDirection.EAST else node.connection1
                    return node, exit_direction
            case NodeDirection.EAST:
                if from_column < self.max_column - 1:
                    node = self.nodes.get((from_row, from_column + 1))
                    if node.is_start:
                        return node, None
                    if node.connection1 != NodeDirection.WEST and node.connection2 != NodeDirection.WEST:
                        return None, None
                    exit_direction = node.connection2 if node.connection1 == NodeDirection.WEST else node.connection1
                    return node, exit_direction
        return None, None

    def _posible_start_directions(self):
        directions = set()
        if self.start.row > 0:
            if ((above := self.nodes.get((self.start.row - 1, self.start.column)))
                    and above.connection2 == NodeDirection.SOUTH):
                directions.add(NodeDirection.NORTH)
        if self.start.row < self.max_row - 1:
            if ((below := self.nodes.get((self.start.row + 1, self.start.column)))
                    and below.connection1 == NodeDirection.NORTH):
                directions.add(NodeDirection.SOUTH)
        if self.start.column > 0:
            if ((left := self.nodes.get((self.start.row, self.start.column - 1)))
                    and (left.connection1 == NodeDirection.EAST or left.connection2 == NodeDirection.EAST)):
                directions.add(NodeDirection.WEST)
        if self.start.column < self.max_column - 1:
            if ((right := self.nodes.get((self.start.row, self.start.column + 1)))
                    and (right.connection1 == NodeDirection.WEST or right.connection2 == NodeDirection.WEST)):
                directions.add(NodeDirection.EAST)
        return directions

@timer
def part1(s = simple_example_input):
    graph = Graph.from_str(s)
    return graph.get_max_distance()


print(part1(actual_input))
