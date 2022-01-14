import sys
from typing import NamedTuple
from collections import deque, defaultdict


DC = "X"


class Alu:
    def __init__(self, instructions):
        self.reset()
        self.ops = {
            "inp": self.inp,
            "add": self.add,
            "mul": self.mul,
            "div": self.div,
            "mod": self.mod,
            "eql": self.eql,
        }
        self.instructions = instructions

    @property
    def x(self):
        return self.r["x"]

    @property
    def y(self):
        return self.r["y"]

    @property
    def w(self):
        return self.r["w"]

    @property
    def z(self):
        return self.r["z"]

    def reset(self):
        self.r = dict(x=0, y=0, w=0, z=0)
        self.i = -1

    def eval_input(self, inp):
        self.reset()
        self.input = inp
        self.i = 0
        for inst in self.instructions:
            self.exec(inst)

    def next_inp(self):
        result = self.input[self.i]
        self.i += 1
        return result

    def value(self, operand):
        return operand if isinstance(operand, int) else self.r[operand]

    def exec(self, i):
        f = self.ops[i[0]]
        f(i[1], i[2] if len(i) > 2 else DC)

    def inp(self, a, *dc):
        v = self.next_inp()
        self.r[a] = v

    def add(self, a, b):
        self.r[a] += self.value(b)

    def mul(self, a, b):
        self.r[a] *= self.value(b)

    def div(self, a, b):
        self.r[a] //= self.value(b)

    def mod(self, a, b):
        self.r[a] %= self.value(b)

    def eql(self, a, b):
        self.r[a] = int(self.r[a] == self.value(b))


def search(alu, dir):

    ranges = { 0: (2, 9), 1: (1, 2), 2: (6, 9), 4: (1, 5), 6: (1, 7), 9: (1, 9), }
    ranges_list = [(k, ranges[k]) for k in sorted(ranges.keys())]

    def calc_range(l, dir):
        low, high = ranges_list[l][1]
        if dir > 0:
            return range(low, high + 1, 1)
        else:
            return range(high, low - 1, -1)

    def process(inp):
        inp[13] = inp[0] - 1
        inp[12] = inp[1] + 7
        inp[11] = inp[2] - 5
        inp[3] = 1
        inp[8] = 9
        inp[5] = inp[4] + 4
        inp[7] = inp[6] + 2
        inp[10] = inp[9]
        alu.eval_input(inp)
        if alu.z == 0:
            return inp
        
    def level(l, inp):
        if l == len(ranges):
            return process(inp)
        wi = ranges_list[l][0]
        for inp[wi] in calc_range(l, dir):
            r = level(l + 1, inp)
            if r:
                break
        return r

    inp = [0 for i in range(14)]
    return level(0, inp)


def read_file(path):
    def int_or_string(op):
        try:
            return int(op)
        except ValueError:
            return op

    with open(path) as f:
        lines = f.read().strip().split("\n")
    instructions = tuple(tuple(int_or_string(op) for op in line.split()) for line in lines)
    return instructions


def main():
    instructions = read_file(sys.argv[1])
    alu = Alu(instructions)

    inp = search(alu, -1)
    print(f"{''.join([str(d) for d in inp])}")

    inp = search(alu, +1)
    print(f"{''.join([str(d) for d in inp])}")


if __name__ == "__main__":
    main()
