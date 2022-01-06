import sys
from collections import deque, defaultdict
from typing import NamedTuple, Any
from enum import Enum
import time
import heapq


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
        print(f"l_path_cost({start},{end})")
        cost = -self[start]
        print(f"cost={cost}")
        max_row = end.row
        max_col = end.col
        for row in range(start.row, max_row):
            cost += self[(row, start.col)]
            print(f"cost={cost}")
        for col in range(start.col, max_col + 1):
            cost += self[(max_row, col)]
            print(f"cost={cost}")
        return cost

    def print(self):
        for row in self.m:
            for v in row:
                print(f"{v}", end="")
            print()


class Item(NamedTuple):
    value: int
    item: Any


class SimpleSortedQueue:
    """Dumb implementation to check performance without priority queue.
    Pops from last element to be O(1)"""
    def __init__(self):
        self.array = []

    def set(self, item: Item):
        found = False
        for i in range(len(self.array)):
            if self.array[i] == item.item:
                if self.array[i] == item.value:
                    return
                self.array[i] = item
                found = True
                break
        if not found:
            self.array.append(item)   
        self.array.sort(key=lambda v: v.value, reverse=True)

    def pop(self):
        return self.array.pop()


class SortedQueue:

    def __init__(self):
        self.array = []
        self.removed = set()
        self.entries = {}
        heapq.heapify(self.array)

    def __bool__(self):
        return bool(self.entries)

    def _push(self, item: Item):
        heapq.heappush(self.array, item)
        self.entries[item.item] = item

    def set(self, item: Item):
        old_item = self.entries.get(item.item)
        if old_item:
            if old_item.value == item.value:    # Do nothing
                return
            self.removed.add(self.entries[item.item])
        self._push(item)

    def pop(self) -> Item:
        while True:
            item = heapq.heappop(self.array)
            if item in self.removed:
                self.removed.remove(item)
                continue
            del self.entries[item.item]
            return item


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


def dijkstra(matrix, start, end):

    def neighbours(node):
        return (n for n in matrix.adjacent(node) if n not in visited)

    def distance(source, target):
        return matrix[target]

    queue = SortedQueue()
    queue.set(Item(0, start))
    dist = {start: 0}
    visited = set()
    current = None

    while queue and current != end:
        d, current = queue.pop()
        visited.add(current)

        for neighbour in neighbours(current):
            new_d = dist[current] + distance(current, neighbour)
            old_d = dist.get(neighbour, 1e10)
            if new_d < old_d:
                dist[neighbour] = new_d
                queue.set(Item(new_d, neighbour))
    return dist


def build_full_matrix(old_m):
    m = []
    for tile_i in range(0, 5):
        for old_row in old_m.m:
            row = []
            for tile_j in range(0, 5):
                row.extend([(v - 1 + tile_i + tile_j) % 9 + 1 for v in old_row])
            m.append(row)
    return Matrix(m)


def main():
    matrix = read_file(sys.argv[1])
    start, end = matrix.bounds()

    costs = dijkstra(matrix, start, end)
    print(costs[end])

    full_matrix = build_full_matrix(matrix)
    start, end = full_matrix.bounds()

    costs = dijkstra(full_matrix, start, end)
    print(costs[end])

if __name__ == "__main__":
    main()
