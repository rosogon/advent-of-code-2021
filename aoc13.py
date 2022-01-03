import sys
from collections import deque
from typing import NamedTuple


class Pos(NamedTuple):
    x: int
    y: int


def fold_points(points, axis):
    return { 
        fold_point(p, axis) if to_fold(p, axis) else p
        for p in points 
    }


def to_fold(point, axis):
    return (axis.x > 0 and point.x > axis.x) or (axis.y > 0 and point.y > axis.y)


def fold_point(point: Pos, axis: Pos):
    """If axis is x --> xf = ax - (x0 - ax) ==> 2ax - x0
       for each p / x0 > ax"""
    def _fold_x(point, axis):
        return Pos(2 * axis.x - point.x, point.y)

    def _fold_y(point, axis):
        return Pos(point.x, 2 * axis.y - point.y)

    _fold = _fold_x if axis.x else _fold_y
    return _fold(point, axis)


def print_map(points):
    bounds = calc_bounds(points)
    for y in range(bounds[0].y, bounds[1].y + 1):
        for x in range(bounds[0].x, bounds[1].x + 1):
            ch = "#" if (x, y) in points else "·"
            print(ch, end="")
        print()
    

def calc_bounds(points):
    min_x = min(p.x for p in points)
    max_x = max(p.x for p in points)
    min_y = min(p.y for p in points)
    max_y = max(p.y for p in points)
    return  (Pos(min_x, min_y), Pos(max_x, max_y))


def read_file(path):
    def read_point(line):
        point = Pos(*(int(n) for n in line.split(",")))
        points.add(point)

    def read_fold(line):
        parts = line.split()
        parts = parts[2].split("=")
        if parts[0] == "x":
            fold = Pos(int(parts[1]), 0)
        else:
            fold = Pos(0, int(parts[1]))
        folds.append(fold)

    points = set()
    folds = []
    func = read_point
    with open(path) as f:
        for line in f:
            if line == "\n":
                func = read_fold
                continue
            func(line)

    return points, folds


def main():
    points, folds = read_file(sys.argv[1])
    points = fold_points(points, folds[0])
    print(len(points))
    for i in range(1, len(folds)):
        points = fold_points(points, folds[i])
    print_map(points)


if __name__ == "__main__":
    main()


