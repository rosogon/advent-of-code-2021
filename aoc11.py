import sys
from collections import deque
from typing import NamedTuple

MAX_ENERGY = 9

class Pos(NamedTuple):
    row: int
    col: int

    def __add__(self, other):
        return Pos(self[0] + other[0], self[1] + other[1])


class Matrix:

    def __init__(self, m):
        self.m = m

    def __len__(self):
        return len(self.m) * len(self.m[0])

    def __getitem__(self, key):
        if len(key) != 2:
            raise TypeError("Not valid key")
        return self.m[key[0]][key[1]]

    def __setitem__(self, key, value):
        if len(key) != 2:
            raise TypeError("Not valid key")
        self.m[key[0]][key[1]] = value

    def print(self):
        # We can simplify here: as input does not contain 0s,
        # a 0 comes always from a flash
        for row in self.m:
            for v in row:
                if v == 0:
                    ch = "·"
                elif v > MAX_ENERGY:
                    ch = "#"
                else:
                    ch = v
                print(f"{ch}", end="")
            print()
            
    def inc(self):
        to_flash = set()
        for i in range(len(self.m)):
            for j in range(len(self.m[i])):
                self.m[i][j] += 1
                if self.m[i][j] > MAX_ENERGY:
                    to_flash.add(Pos(i,j))
        return to_flash

    def valid_position(self, pos):
        return 0 <= pos.row < len(self.m) and 0 <= pos.col < len(self.m[0])

    def adjacent(self, pos):
        deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for delta in deltas:
            p = pos + delta
            if self.valid_position(p):
                yield p
            


def do_step(m, step_n):
    to_flash = m.inc()
    queue = deque(to_flash)
    flashed = set()
    while queue:
        pos = queue.popleft()
        if pos in flashed:
            continue
        m[pos] = 0
        flashed.add(pos)
        adjacent = (a for a in m.adjacent(pos) if a not in flashed)
        for a in adjacent:
            m[a] += 1
            if m[a] > MAX_ENERGY:
                queue.append(a)
    return len(flashed)
    

def read_file(path):
    m = []
    with open(path) as f:
        for line in f:
            m.append([int(n) for n in line.rstrip()])

    return Matrix(m)


def main():
    p = Pos(0, 1)

    m = read_file(sys.argv[1])
    n = int(sys.argv[2])
    total_flashes = 0
    all_flashed = 0
    step = 0
    while step < n or not all_flashed:
        step += 1
        flashes = do_step(m, step)
        if step <= n:
            total_flashes += flashes
        if flashes == len(m):
            all_flashed = step
        m.print()
        print()

    print(f"Number of flashes after step {n}: {total_flashes}")
    print(f"All fish flashed after step {all_flashed}")


if __name__ == "__main__":
    main()
