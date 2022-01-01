import sys
from typing import NamedTuple, List, Set


size = {
    0: 6,
    1: 2,
    2: 5,
    3: 5,
    4: 4,
    5: 5,
    6: 6,
    7: 3,
    8: 7,
    9: 6,
}


class Entry(NamedTuple):
    patterns: Set[set]
    output: List[set]


def build_decoder(entry):
    def find_single(n_segments, patterns):
        s = find(n_segments, patterns)
        result = s.pop()
        if s:
            raise ValueError(f"find_single(): more than one value in set {s}")
        return result
    
    def find(n_segments, patterns):
        return set(p for p in patterns if len(p) == n_segments)
    
    coder = {}
    for d in (1, 4, 7, 8):
        coder[d] = find_single(size[d], entry.patterns)

    _6_segments = find(6, entry.patterns)
    _5_segments = find(5, entry.patterns)

    coder[9] = next(d for d in _6_segments if len(d & coder[4]) == size[4])
    _6_segments.remove(coder[9])

    coder[0] = next(d for d in _6_segments if len(d & coder[7]) == size[7])
    _6_segments.remove(coder[0])

    coder[6] = _6_segments.pop()

    coder[3] = next(d for d in _5_segments if len(d & coder[1]) == size[1])
    _5_segments.remove(coder[3])

    coder[5] = next(d for d in _5_segments if len(d & coder[6]) == size[5])
    _5_segments.remove(coder[5])

    coder[2] = _5_segments.pop()

    decoder = {v: k for k, v in coder.items()}
    return decoder
    
def read_file(path):
    with open(path) as f:
        result = []
        for line in f:
            patterns_str, output_str = line.split(" | ")
            patterns = frozenset([frozenset(p) for p in patterns_str.split()])
            output = [frozenset(p) for p in output_str.split()]
            result.append(Entry(patterns, output))
    return result


def main():
    entries = read_file(sys.argv[1])

    unique_sizes = [size[i] for i in (1, 4, 7, 8)]
    searched = []
    for e in entries:
        unique_entry_digits = [o for o in e.output if len(o) in unique_sizes]
        searched.append(len(unique_entry_digits))
    print(sum(searched))

    s = 0
    bases = [1000, 100, 10, 1]
    for e in entries:
        decoder = build_decoder(e)
        decoded = [decoder[d] for d in e.output]
        n = sum(digit * base for digit, base in zip(decoded, bases))
        s += n
    print(s)

    
if __name__ == "__main__":
    main()
