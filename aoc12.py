import sys
from collections import deque, defaultdict
from typing import NamedTuple
from enum import Enum


START = "start"
END = "end"


class Kind(str, Enum):
    BIG = "big"
    SMALL = "small"


class Graph(dict):
    def __init__(self):
        self.nodes = {}

    def addlink(self, n1: str, n2: str):
        if not isinstance(n1, Node):
            n1 = Node(n1)
        if not isinstance(n2, Node):
            n2 = Node(n2)
        self._addlink(n1, n2)
        self._addlink(n2, n1)
        
    def _addlink(self, n1, n2):
        if not n1 in self:
            self[n1] = set()
        if n1 == END:
            return
        self[n1].add(n2)
        

class Node(str):
    def __init__(self, *args, **kwargs):
        super().__init__()

    @property
    def kind(self):
        return Kind.BIG if self.isupper() else Kind.SMALL


def read_file(path):
    result = []
    with open(path) as f:
        for line in f:
            result.append(line.rstrip().split("-"))

    return result


def check_path(paths, path, visited, small_max_visited):
    def small_visited_once(node):
        if node.kind == Kind.BIG:
            return True
        return path.count(node) == 1

    def valid_visited(path, visited):
        if small_max_visited == 1:
            return all(small_visited_once(n) for n in path)
        elif small_max_visited == 2:
            # Hack: substract one to all; only one must be non-zero
            return sum(max(v - 1, 0) for v in visited.values()) <= 1
        else:
            raise ValueError(f"small_max_visited={small_max_visited}")
        
    return (
        path not in paths and 
        valid_visited(path, visited) and
        path[0] == START and
        path[len(path) - 1] == END
    )

def find_paths(g, start, small_max_visited):
    def _get_nodes_to_visit(from_):

        def one_small_twice(node):
            return (
                visited[node] == 0 or 
                (visited[node] == 1 and not small_visited_twice)
            )

        small_visited_twice = \
            small_max_visited == 2 and any(v == 2 for v in visited.values())

        for n in g[from_]:
            if (
                n != START and 
                visited[n] < small_max_visited and
                (
                    (small_max_visited == 1) or
                    (small_max_visited == 2 and one_small_twice(n))
                )
            ):
                yield n

    def _find_paths(node):

        path.append(node)
        if node == END:
            if check_path(paths, path, visited, small_max_visited):
                #paths.append(list(path))
                result = 1
        else:
            if node.kind is Kind.SMALL:
                visited[node] += 1

            to_visit = _get_nodes_to_visit(node)
            result = 0
            for node_to_visit in to_visit:
                result += _find_paths(node_to_visit)

        if visited[node] > 0:
            visited[node] -= 1
        path.pop()
        return result

    paths = []
    visited = defaultdict(int)
    path = deque()
    n_paths = _find_paths(start)
    return n_paths, paths


def main():
    links = read_file(sys.argv[1])
    g = Graph()
    for link in links:
        g.addlink(*link)
    print(g)

    n_paths, paths = find_paths(g, Node(START), 1)
    print(n_paths)

    n_paths, paths = find_paths(g, Node(START), 2)
    #for p in paths:
    #    print(",".join(p))
    print(n_paths)


if __name__ == "__main__":
    main()
