import sys
from typing import NamedTuple
from collections import defaultdict


class Matrix(dict):
    @property
    def max_x(self):
        return max(p.x for p in self)

    @property
    def max_y(self):
        return max(p.y for p in self)
    
    def __str__(self):
        def _char(x, y):
            if Pos(x, y) not in self:
                return "."
            return str(self.get(Pos(x, y)))
        
        parts_y = []
        for y in range(self.max_y + 1):
            parts = [_char(x, y) for x in range(self.max_x + 1)]
            parts_y.append("".join(parts))
        return "\n".join(parts_y) + "\n"

    def mark(self, p):
        self[p] = self.get(p, 0) + 1

    def overlaps(self):
        return filter(lambda p: self.get(p) > 1, self.keys())

        
class Pos(NamedTuple):
    x: int
    y: int


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def points(self, include_diagonal):
        def calc_inc(delta):
            if delta > 0:
                return 1
            elif delta < 0:
                return -1
            return 0
        
        def _points(n_steps, inc_x, inc_y):
            result = []
            for i in range(n_steps):
                x, y = p.x + i * inc_x, p.y + i * inc_y
                result.append(Pos(x, y))
            return result
        
        delta_x = self.p2.x - self.p1.x
        delta_y = self.p2.y - self.p1.y
        p = self.p1
        inc_x, inc_y = calc_inc(delta_x), calc_inc(delta_y)
        steps_x = abs(delta_x) + 1
        steps_y = abs(delta_y) + 1
        if delta_x == 0 or delta_y == 0 or (include_diagonal and steps_x == steps_y):
            return _points(max((steps_x, steps_y)), inc_x, inc_y)
        return []

    def __str__(self):
        p1 = self.p1
        p2 = self.p2
        return f"({p1.x},{p1.y}) -> ({p2.x},{p2.y})"

    def __repr__(self):
        return str(self)
    
def read_file(path):
    lines = []
    with open(path) as f:
        for line in f:
            p1, _, p2 = line.split()
            p1 = Pos(*(int(n) for n in p1.split(",")))
            p2 = Pos(*(int(n) for n in p2.split(",")))
            line = Line(p1, p2)
            lines.append(line)
    return lines


def main(include_diagonal):
    lines = read_file(sys.argv[1])
    matrix = Matrix()
    for line in lines:
        points = line.points(include_diagonal)
        for point in points:
            matrix.mark(point)
    print(len(list(matrix.overlaps())))
    
if __name__ == "__main__":
    main(False)
    main(True)

