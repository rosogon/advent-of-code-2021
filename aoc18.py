import sys
from math import ceil
from collections import deque
from typing import NamedTuple
from copy import deepcopy as copy


class ParentChild(NamedTuple):
    parent: list
    child_idx: int

    @property
    def child(self):
        return self.parent[self.child_idx]

    @child.setter
    def child(self, value):
        self.parent[self.child_idx] = value


def read_file(path):
    expressions = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            expression = eval(line)
            expressions.append(expression)

    return expressions


def explode(ge, pc):

    def search(current_pc, to_find_pc, result):
        nonlocal found, last_number_pc

        e = current_pc.child
        if e is to_find_pc.child:
            found = True
            result[0] = last_number_pc
        elif isinstance(e, int):
            if found:
                result[1] = current_pc
            last_number_pc = current_pc
        else:   # isinstance(e, list)
            if result[1] is None:
                result = search(ParentChild(e, 0), to_find_pc, result)
            if result[1] is None:
                result = search(ParentChild(e, 1), to_find_pc, result)
        return result
        
    last_number_pc = None
    found = False
    left, right = search(ParentChild((ge,), 0), pc, [None, None])

    if left is not None:
        left.child += pc.child[0]
    if right is not None:
        right.child += pc.child[1]
    pc.child = 0


def split(pc):
    e = pc.child
    pc.child = [e // 2, ceil(e / 2)]


def reduce(ge):

    def _reduce(pc, action, level=0):
        e = pc.child
        
        changed = False
        if isinstance(e, list):
            if action == 1 and level >= 4:
                explode(ge, pc)
                return True

            changed = _reduce(ParentChild(e, 0), action, level + 1)
            if not changed:
                changed = _reduce(ParentChild(e, 1), action, level + 1)
            return changed

        if isinstance(e, int):
            if e >= 10 and action == 2:
                split(pc)
                return True
            return False

    changed = True
    while changed:
        changed = _reduce(ParentChild((ge,), 0), 1)
        if not changed:
            changed = _reduce(ParentChild((ge,), 0), 2)
    return ge


def add(e1, e2):
    if e1 is None:
        return e2
    result = [e1, e2]
    return result


def magnitude(e):
    if isinstance(e, list):
        return 3 * magnitude(e[0]) + 2 * magnitude(e[1])
    return e


def main():
    expressions = read_file(sys.argv[1])
    last = None
    for current in expressions:
        added = add(last, copy(current))
        last = reduce(added)
    print(magnitude(last))

    m = max(
        magnitude(reduce(add(copy(e1), copy(e2))))
        for e1 in expressions
        for e2 in expressions
        if e1 is not e2
    )
    print(m)


if __name__ == "__main__":
    main()
