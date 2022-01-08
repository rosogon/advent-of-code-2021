import sys
from typing import NamedTuple, Any
from math import sqrt, ceil


class Pos(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        return Pos(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other):
        return Pos(self[0] - other[0], self[1] - other[1])


class Target(NamedTuple):
    p1: Pos
    p2: Pos

    def __contains__(self, pos):
        return (
            self.p1.x <= pos.x <= self.p2.x and 
            self.p1.y >= pos.y >= self.p2.y
            # p1.y and p2.y are negative values!!
        )

def calc_max_y(target):
    max_vy = calc_max_vy(target)
    return (max_vy**2 + max_vy) / 2


def calc_max_vy(target):
    return abs(target.p2.y) - 1
    

def calc_min_vy(target):
    return target.p2.y


def calc_max_vx(target):
    return target.p2.x


def calc_min_vx(target):
    # positive solution of (vx**2 + vx) / 2 = m     // m = target.p1.x
    # => vx = (-1 + sqrt(1 + 8m)) / 2
    m = target.p1.x
    vx = (-1 + sqrt(1 + 8 * m)) / 2
    return ceil(vx)


def step_y(vy, min_y):
    y = 0
    while y >= min_y:
        y += vy
        vy -= 1
        yield y


def step_x(vx, max_x):
    x = 0
    while x <= max_x or vx:
        x += vx
        vx = max(0, vx - 1)
        yield x


def step(vx, vy, max_x, min_y):
    return zip(step_x(vx, max_x), step_y(vy, min_y))


def read_file(path):
    targets = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            parts = line.split(",")
            x_range, y_range = [ p.split("=")[1] for p in parts ]
            bounds = [
                Pos(int(x), int(y)) 
                for x, y in zip(x_range.split(".."), reversed(y_range.split("..")))
            ]
            targets.append(Target(*bounds))

    return targets


def main():
    targets = read_file(sys.argv[1])
    for target in targets:
        print(calc_max_y(target))

        max_x, min_y = target.p2
        min_vx, max_vx = calc_min_vx(target), calc_max_vx(target)
        min_vy, max_vy = calc_min_vy(target), calc_max_vy(target)

        s = 0

        s = sum(
            any(
                Pos(x, y) in target
                for x, y in step(vx, vy, max_x, min_y)
            )
            for vy in range(min_vy, max_vy + 1)
            for vx in range(min_vx, max_vx + 1)
        )
        print(s)
    
if __name__ == "__main__":
    main()
