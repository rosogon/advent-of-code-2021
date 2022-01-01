import sys
from collections import defaultdict


def read_file(path):
    with open(path) as f:
        line = f.readline()
        numbers = [int(n) for n in line.split(",")]
    return numbers


def cost(crabs, position):
    result = 0
    for crab in crabs:
        result += abs(position - crab)
    return result


def cost2(crabs, position):
    result = 0
    for crab in filter(lambda c: c != position, crabs):
        n = abs(crab - position)
        result += (1 + n) / 2 * n
    return result


def main():
    crabs = read_file(sys.argv[1])
    l1 = min(crabs)
    l2 = max(crabs)

    result = min(cost(crabs, p) for p in range(l1, l2 + 1))
    print(result)

    result = min(cost2(crabs, p) for p in range(l1, l2 + 1))
    print(result)

    
if __name__ == "__main__":
    main()
