import sys
from typing import NamedTuple, Dict
from copy import copy
import time


MAXINT = 1<<31


class Pos(NamedTuple):
    row: int
    col: int

    def __sub__(self, other):
        return Pos(self.row - other.row, self.col - other.col)

def herd_step(prev, kind):
    def cell(i, j):
        i0 = (i - 1) % len_i if kind == "v" else i
        j0 = (j - 1) % len_j if kind == ">" else j
        i1 = (i + 1) % len_i if kind == "v" else i
        j1 = (j + 1) % len_j if kind == ">" else j
        if prev[i0][j0] == kind and prev[i][j] == ".":
            return kind
        if prev[i][j] == kind and prev[i1][j1] == ".":
            return "."
        return prev[i][j]
    
    len_i = len(prev)
    len_j = len(prev[0])
    result = [
        [cell(i, j) for j in range(len_j)] for i in range(len_i)
    ]
    return result


def step(prev):
    m  = herd_step(prev, ">")
    return herd_step(m, "v")


def print_m(m):
    for i in range(len(m)):
        for j in range(len(m[i])):
            print(m[i][j], end="")
        print()


def read_file(path):
    with open(path) as f:
        return f.read().rstrip().split("\n")


def main():
    m = read_file(sys.argv[1])
    n_step = 0
    m0 = None
    while m0 != m:
        m0 = m
        m = step(m)
        n_step += 1
    print(n_step)


if __name__ == "__main__":
    main()
