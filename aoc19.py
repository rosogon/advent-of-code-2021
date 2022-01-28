import sys
from typing import NamedTuple, Dict, Callable, Tuple, List
from copy import copy
import time
from collections import defaultdict
from collections import deque


class Pos(NamedTuple):
    x: int
    y: int
    z: int

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y, self.z - other.z)


def distance(a: Pos, b: Pos):
    return sum(abs(a[i] - b[i]) for i in range(3))


class Scanner(NamedTuple):
    name: str
    beacons: Tuple[Pos]
    pos: Pos = Pos(0, 0, 0)

    def rel_to(self, new_pos):
        return Scanner(
            self.name, 
            tuple(new_pos + b for b in self.beacons),
            new_pos
        )


def identity(n):
    return n


class Coord(NamedTuple):
    index: int
    t: Callable = identity
    prefix: str = ""

    def __neg__(self):
        return Coord(self.index, lambda n: -self.t(n), f"{'' if self.prefix else '-'}")

    def __str__(self):
        return f"{self.prefix}{'xyz'[self.index]}"

    def __call__(self, pos: Pos):
        return self.t(pos[self.index])
        

def pairs(sa, sb):
    """O(n!) implementation of pairs between two sets"""
    def pairs_r(sa, sb, partial):
        nonlocal result
        if not sa or not sb:
            result.append(partial)
            return
        a = next(iter(sa))
        for b in sb:
            pairs_r(sa - {a}, sb - {b}, partial + [(a, b)])
        return
    result = []
    pairs_r(set(sa), set(sb), [])
    return result


def substract_pairs(sa, sb, threshold=1):
    """Calculate a - b for each a in sa, b in sb. 
    If the result >= threshold, both sets match. 
    The difference results to be the location of b relative to a
    """
    matches = defaultdict(int)
    for a in sa:
        for b in sb:
            matches[a - b] += 1
    return {k: v for k, v in matches.items() if v >= threshold}


def calc_rotators():
    x = Coord(0)
    y = Coord(1)
    z = Coord(2)
    #
    # generators describe how to rotate x axis after rotating x axis to each possible direction
    # generators[i][0] is the starting position of axes
    # generators[i][1] is a function that rotates along x-axis the previous step
    #   (x-axis keeps position, while y and z switch position, but changing sign one of them)
    #
    generators = [
        ((x, y, z), lambda a, b, c: (a, c, -b)),
        ((-x, y, -z), lambda a, b, c: (a, c, -b)),
        ((-y, x, z), lambda a, b, c: (c, b, -a)),
        ((-y, -x, -z), lambda a, b, c: (c, b, -a)),
        ((-y, -z, x), lambda a, b, c: (b, -a, c)),
        ((z, y, -x), lambda a, b, c: (b, -a, c)),
    ]
    rotators = []
    for g, step in generators:
        partial = [g]
        for i in range(1, 4):
            prev = partial[i - 1]
            partial.append(step(*prev))
        rotators.extend(partial)
    return rotators


def rotate(scanner):
    rotators = calc_rotators()
    
    for g_ in rotators:
        rotation = tuple(
            Pos(g_[0](p), g_[1](p), g_[2](p))
            for p in scanner.beacons
        )
        yield Scanner(scanner.name, rotation)


def find_matching_rotation(s, normalized):
    for n in normalized.values():
        for sr in rotate(s):
            matches = substract_pairs(n.beacons, sr.beacons, 12)
            if matches:
                norm_pos, _ = matches.popitem()
                norm_scanner = sr.rel_to(norm_pos)
                return norm_scanner
    return None


def normalize(scanners: List[Scanner]):
    normalized = {scanners[0].name: scanners[0]}
    stack = deque(scanners[1:])
    while stack:
        s = stack.popleft() 
        sm = find_matching_rotation(s, normalized)
        if sm:
            normalized[sm.name] = sm
        else:
            stack.append(s)
    return list(normalized.values())
    

def read_file(path):
    scanners = []
    with open(path) as f:
        groups = f.read().split("\n\n")
    for group in groups:
        lines = group.rstrip().split("\n")
        beacons = tuple(Pos(*(int(n) for n in line.split(","))) for line in lines[1:])
        scanner = Scanner(lines[0], beacons)
        scanners.append(scanner)
        
    return scanners


def main():

    scanners = read_file(sys.argv[1])

    scanners = normalize(scanners)

    beacons = {b for s in scanners for b in s.beacons}
    print(len(beacons))

    max_distance = max(distance(a.pos, b.pos) for a in scanners for b in scanners)
    print(max_distance)

                
if __name__ == "__main__":
    main()
