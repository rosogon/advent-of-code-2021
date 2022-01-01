import sys
from functools import reduce
import operator


MAX = 9


def read_file(path):
    result = []
    length = -1
    with open(path) as f:
        for line in f:
            line = line[0:-1]
            if length == -1:
                length = len(line) + 2
            heights = [MAX] + [int(h) for h in line] + [MAX]
            result.append(heights)
    result.insert(0, [MAX]*length)
    result.append([MAX]*length)
    return result


def print_map(m):
    for row in m:
        for h in row:
            print(h if h != -1 else "·", end="")
        print()


def adjacent(i, j):
    return [
        (i - 1, j),
        (i + 1, j),
        (i, j - 1),
        (i, j + 1),
    ]


def value(m, p):
    return m[p[0]][p[1]]


def calc_low_points(hmap):
    def is_low_point(i, j):
        h = hmap[i][j]

        adjacent_values = (
            value(hmap, p) for p in adjacent(i, j)
        )
        return all(value > h for value in adjacent_values)

    result = [
        (i, j)
        for i in range(1, len(hmap) - 1)
        for j in range(1, len(hmap[i]) - 1)
        if is_low_point(i, j)
    ]
    return result


def calc_basinmap(hmap, low_points):
    def spread(p, k):
        size = 1
        bmap[p[0]][p[1]] = k
        for ap in adjacent(p[0], p[1]):
            if value(hmap, ap) == 9 or value(bmap, ap) != -1:
                continue
            size += spread(ap, k)
        return size
        
    bmap = [[-1] * len(hmap[0]) for _ in hmap]
    sizes = []
    for k in range(len(low_points)):
        low_point = low_points[k] 
        size = spread(low_point, k)
        sizes.append(size)
    return bmap, sizes


def prod(values):
    return reduce(operator.mul, values, 1)

def main():
    heightmap = read_file(sys.argv[1])
    low_points = calc_low_points(heightmap)
    risk_levels = (1 + heightmap[p[0]][p[1]] for p in low_points)
    print(sum(risk_levels))
    bmap, basin_sizes = calc_basinmap(heightmap, low_points)
    sorted_sizes = sorted(basin_sizes, reverse=True)
    print(prod(sorted_sizes[0:3]))

    
if __name__ == "__main__":
    main()
