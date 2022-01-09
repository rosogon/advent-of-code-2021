import sys
from typing import NamedTuple


Y = 0
X = 1
MIN = 0
MAX = 1


class Pos(NamedTuple):
    row: int
    col: int

    def __add__(self, other):
        return Pos(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other):
        return Pos(self[0] - other[0], self[1] - other[1])

    def __repr__(self):
        return f"({self.row},{self.col})"


class Matrix:

    def __init__(self, m, ranges, default=0):
        self.m = m
        self.values = {}
        self.default = default

        # range[axis][0]..rangesaxis][1] => min(axis)..max(axis) + 1
        self.ranges= ranges
        self.deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for i in range(0, len(m)):
            for j in range(0, len(m[i])):
                v = m[i][j]
                self[(i, j)] = int(v == "#" or v == 1)

    def __getitem__(self, pos):
        if len(pos) != 2:
            raise TypeError("Not valid pos")
        return self.values.get(pos, self.default)

    def __setitem__(self, pos, value):
        if len(pos) != 2:
            raise TypeError("Not valid pos")
        self.values[pos] = value

    def kernel_values(self, pos):
        return [self.values.get(pos + d, self.default) for d in self.deltas]
        
    def kernel_magnitude(self, values):
        result = 0
        for digit in values:
            result = (result << 1) | digit
        return result

    def enhance(self, algorithm, new_default):
        ranges = [
            (self.ranges[Y][MIN] - 1, self.ranges[Y][MAX] + 1),
            (self.ranges[X][MIN] - 1, self.ranges[X][MAX] + 1),
        ]
        m = Matrix([[]], ranges, new_default)
        lit = 0
        for i in range(*ranges[Y]):
            for j in range(*ranges[X]):
                pos = Pos(i, j)
                kernel_values = self.kernel_values(pos)
                value = algorithm[self.kernel_magnitude(kernel_values)]
                m.values[pos] = value
                lit += value
        return m, lit
    
    def print(self):
        for i in range(*self.ranges[Y]):
            for j in range(*self.ranges[X]):
                ch = "#" if self.values[(i, j)] else "·"
                print(ch, end="")
            print()


def read_file(path):
    with open(path) as f:
        algorithm, lines = f.read().strip().split("\n\n")
    algorithm = [int(ch == "#") for ch in algorithm]
    if len(algorithm) > 512:
        raise ValueError(f"len(algorithm) = {len(algorithm)}")
    m = lines.split("\n")
    ranges = [(0, len(m)), (0, len(m[0]))]
    return algorithm, Matrix(m, ranges)


def main():
    algorithm, matrix = read_file(sys.argv[1])
    orig_matrix = matrix
    for i in range(2):
        default = int((i + 1) % 2 and algorithm[0] == 1)
        matrix, lit = matrix.enhance(algorithm, new_default=default)
    print(lit)

    matrix = orig_matrix
    for i in range(50):
        default = int((i + 1) % 2 and algorithm[0] == 1)
        matrix, lit = matrix.enhance(algorithm, new_default=default)
    print(lit)


if __name__ == "__main__":
    main()
