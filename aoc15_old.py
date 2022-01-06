import sys
from collections import deque, defaultdict
from typing import NamedTuple, Any
from enum import Enum
import time
import heapq
from dataclasses import dataclass, field


class Pos(NamedTuple):
    row: int
    col: int

    def __add__(self, other):
        return Pos(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other):
        return Pos(self[0] - other[0], self[1] - other[1])

    def distance(self):
        return abs(self[0]) + abs(self[1])


class Matrix:

    def __init__(self, m):
        self.m = m

    def __getitem__(self, key):
        if len(key) != 2:
            raise TypeError("Not valid key")
        return self.m[key[0]][key[1]]

    def __setitem__(self, key, value):
        if len(key) != 2:
            raise TypeError("Not valid key")
        self.m[key[0]][key[1]] = value

    def bounds(self):
        return Pos(0, 0), Pos(len(self.m) - 1, len(self.m[0]) - 1)

    def valid_position(self, pos):
        return 0 <= pos.row < len(self.m) and 0 <= pos.col < len(self.m[0])

    def adjacent(self, pos):
        deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for delta in deltas:
            p = pos + delta
            if self.valid_position(p):
                yield p

    def positions(self):
        for i in range(0, len(self.m)):
            for j in range(0, len(self.m[0])):
                yield Pos(i, j)

    def l_path_cost(self, start, end):
        cost = -self[start]
        max_row = end.row
        max_col = end.col
        for row in range(start.row, max_row):
            cost += self[(row, start.col)]
        for col in range(start.col, max_col + 1):
            cost += self[(max_row, col)]
        return cost

    def print(self):
        for row in self.m:
            for v in row:
                print(f"{v}", end="")
            print()


def distance(node1, node2):
    d = (node2 - node1).distance()
    return d


def calc_border_costs(matrix, best_costs):
    return  (
        n 
        for n in best_costs 
        if any(n2 not in best_costs for n2 in matrix.adjacent(n))
    )


def calc_initial_costs(matrix, start, end):
    result = {}
    for row in range(start.row, end.row + 1):
        for col in range(start.col, end.col + 1):
            pos = Pos(row, col)
            result[pos] = matrix.l_path_cost(pos, end)
    return result


def find_path(m, start, end, costs, best_costs):
    def _initial_path2(start):
        for p in m.adjacent(start):
            if p in border_nodes and p != end:
                return m[p] + best_costs[p]
        return m.l_path_cost(start, end)

    def _next_nodes(node):
        return (
            n 
            for n in m.adjacent(node) 
            if n not in visited and (n - start).distance() < 10
        )

    def _heur(node):
        return distance(node, end)

    def _heur2(node):
        if not border_nodes:
            return _heur(node)
        return min(distance(node, bn) + best_costs[bn] for bn in border_nodes)

    def _find_path(node):
        nonlocal cost
        nonlocal best_cost
        global n

        visited.add(node)
        cost += m[node]

        if node in best_costs:
            if cost + best_costs[node] < best_cost:
                best_cost = cost + best_costs[node]
        elif cost + _heur2(node) < best_cost:
            n += 1
            next_nodes = _next_nodes(node)
            for next_node in next_nodes:
                _find_path(next_node)

        visited.remove(node)
        cost -= m[node]

    visited = set()
    t0 = time.time()
    border_nodes = list(calc_border_costs(m, best_costs))
    best_cost = _initial_path2(start)
    t1 = time.time()
    cost = -m[start]
    _find_path(start)
    return best_cost, t1 - t0

n = 0

def print_costs(matrix, costs, bounds):
    for pos in matrix.positions():
        ch = costs.get(pos, "·")
        print(f"{ch:3}", end="")
        if pos.col == bounds[1].col:
            print()


def read_file(path):
    m = []
    with open(path) as f:
        for line in f:
            m.append([int(n) for n in line.rstrip()])

    return Matrix(m)


def mode1(matrix):
    start, end = matrix.bounds()
    best_costs = {end: 0}
    costs = calc_initial_costs(matrix, start, end)
    print_costs(matrix, costs, (start, end))

    sorted_positions = \
        sorted(list(matrix.positions()), key=lambda pos: distance(end, pos))

    for pos in sorted_positions:
        print(f"Processing cost for {pos}")
        cost, _ = find_path(matrix, pos, end, costs, best_costs)
        best_costs[pos] = cost
        #print_costs(matrix, best_costs, (start, end))
    print(cost)
    print(f"n = {n}")

    print_costs(matrix, best_costs, (start, end))


def main():
    matrix = read_file(sys.argv[1])
    mode1(matrix)

if __name__ == "__main__":
    main()
