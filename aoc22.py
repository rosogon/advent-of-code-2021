import sys
from typing import NamedTuple, Tuple, Union


MAXINT = 1 << 31


class Cuboid(NamedTuple):
    x: Tuple[int, int]
    y: Tuple[int, int]
    z: Tuple[int, int] = (0, 0)

    def len(self, index):
        if self[index][1] < self[index][0]:
            return 0
        return self[index][1] - self[index][0] + 1

    def size(self):
        return self.len(0) * self.len(1) * self.len(2) 

    def __and__(self, other: Union["Cuboid", "Step"]):
        return self.intersection(other)

    def intersection(self, other: Union["Cuboid", "Step"]):
        if isinstance(other, Step):
            other = other.cuboid
        args = (
            (max(self[i][0], other[i][0]), min(self[i][1], other[i][1])) 
            for i in range(3)
        )
        return Cuboid(*args)

    def __sub__(self, other: Union["Cuboid", "Step"]):
        return self.difference(other)

    def difference(self, other: Union["Cuboid", "Step"]):
        """self - other = self & ¬other"""
        def lims(lower=-MAXINT, upper=MAXINT):
            return (lower + 1, upper - 1)

        if isinstance(other, Step):
            other = other.cuboid

        not_other_cuboids = [
            Cuboid(lims(upper=other.x[0]), lims(), lims()),
            Cuboid(lims(lower=other.x[1]), lims(), lims()),
            Cuboid(other.x, lims(upper=other.y[0]), lims()),
            Cuboid(other.x, lims(lower=other.y[1]), lims()),
            Cuboid(other.x, other.y, lims(upper=other.z[0])),
            Cuboid(other.x, other.y, lims(lower=other.z[1])),
        ]
        intersections = [self & c for c in not_other_cuboids]
        result = [i for i in intersections if i.size() > 0]
        return result

    def __or__(self, other: Union["Cuboid", "Step"]):
        return self.union(other)

    def union(self, other: Union["Cuboid", "Step"]):
        if isinstance(other, Step):
            other = other.cuboid
        inters = self & other
        if inters.size() ==  0:
            return [self, other]

        result = other - self
        result.append(self)
        return result

    def __contains__(self, other):
        return self.intersection(other) == other

    def __str__(self):
        coords = [f"{'xyz'[i]}={self[i][0]}..{self[i][1]}" for i in range(3)]
        return f"Cuboid({', '.join(coords)}, size={self.size()})"

    def __repr__(self):
        return self.__str__()


class Step(NamedTuple):
    pos: int
    value: bool
    cuboid: Cuboid

    def intersection(self, other):
        return self.cuboid.intersection(other.cuboid)

    def size(self):
        return self.cuboid.size()


class SmartReactor:
    def __init__(self):
        self.cuboids = set()

    def count(self):
        return sum(c.size() for c in self.cuboids)
    
    def run_step(self, step):
        collisions = [c for c in self.cuboids if (c & step).size() > 0]
        for c in collisions:
            self.cuboids.remove(c)
            self.cuboids.update(c - step)
        if step.value:
            # overall, we are adding step.union(c) for each collision
            self.cuboids.add(step.cuboid)
        
            
def is_initialization(step):
    b = [-50, 50]
    return all(
        b[0] <= step.cuboid[i][0] <= step.cuboid[i][1] <= b[1]
        for i in range(3)
    )
        

def read_file(path):
    def read_step(line):
        nonlocal c
        state, dims = line.split(" ")
        dims = dims.split(",")
        dim_list = []
        for dim in dims:
            dim = dim[2:]
            dim0, dim1 = (int(d) for d in dim.split(".."))
            dim_list.append((dim0, dim1))
        c += 1
        return Step(c, int(state == "on"), Cuboid(*dim_list))
    c = -1
    with open(path) as f:
        return [read_step(line) for line in f]

def main():
    steps = read_file(sys.argv[1])

    reactor = SmartReactor()
    for step in (s for s in steps if is_initialization(s)):
        reactor.run_step(step)
    print(reactor.count())

    reactor = SmartReactor()
    for step in steps:
        reactor.run_step(step)
    print(reactor.count())

    
if __name__ == "__main__":
    main()
