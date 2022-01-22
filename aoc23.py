import sys
from typing import NamedTuple, Dict
from copy import copy
import time


HIDDEN=[
"  #D#C#B#A#",
"  #D#B#A#C#",
]

A = "A"
B = "B"
C = "C"
D = "D"
W = "#"

MAXINT = 1<<31

energy_point = { A: 1, B: 10, C: 100, D: 1000 }


GREEN = "\033[1;32m"
BLUE = "\033[1;44m"
REV_GREEN = "\033[97;42m"
REV_DIM_BLUE = "\033[97;44m"
REV_BLUE = "\033[97;104m"
NORMAL = "\033[1;0m"


class Pos(NamedTuple):
    row: int
    col: int

    def __sub__(self, other):
        return Pos(self.row - other.row, self.col - other.col)


def distance(p1, p2, m=None):
    if isinstance(p1, Amphipod):
        p1 = p1.pos
    if isinstance(p2, Amphipod):
        p2 = p2.pos
    if p1.row > m.hallway_row and p2.row > m.hallway_row:
        interim = Pos(m.hallway_row, p2.col)
        return (distance(p1, interim, m) + distance(interim, p2, m))
    d = p1 - p2
    return abs(d.row) + abs(d.col)


class Amphipod(NamedTuple):
    pos: Pos
    kind: str
    at_home: bool

    def goto(self, pos, to_home):
        return Amphipod(pos, self.kind, to_home)


class State(NamedTuple):
    cost: int
    positions: Dict[Pos, Amphipod]

    @property
    def amphipods(self):
        return self.positions.values()

    def for_set(self):
        return (frozenset(self.amphipods))

    def is_solution(self, m):
        return all(a.at_home for a in self.amphipods)

    def heur(self, m):
        def heur_a(a):
            if a.at_home:
                return 0
            home = m.home[a.kind]
            home_pos = Pos(home.upper.row - n_at_home[a.kind], home.col)
            n_at_home[a.kind] += 1
            return energy_point[a.kind] * distance(a.pos, home_pos, m)
        n_at_home = {
            h: sum(self.positions[p].at_home if p in self.positions else 0 for p in m.home[h]) 
            for h in (A, B, C, D)
        }
        return sum(heur_a(a) for a in self.amphipods)

    def next_states_amphipod(self, a, m):
        if a.at_home:
            return []

        states = []
        if a in m.hallway:
            if self.can_go_home(a, m):
                states.append(self.go_home(a, m))
        else:
            home_cols = [h.col for h in m.home.values()]
            f = ord(D) - ord(a.kind) + 1
            M = 4
            for p in (
                    p 
                    for p in m.hallway 
                    if self.is_available(p) 
                    and (
                        abs(p.col - a.pos.col) <= f + M or
                        abs(p.col - m.home[a.kind].col) <= f + M
                    )
                    and p.col not in home_cols
            ):
                road = self.road(a, p, m)
                if not all(self.is_available(r) for r in road):
                    continue
                states.append(self.goto(a, p, m))
        states.sort(key=lambda s: s.cost)
        return states

    def next_states(self, m):
        states = []
        as_ = sorted(self.amphipods, key=lambda a: energy_point[a.kind], reverse=True)
        for a in as_:
            states.extend(self.next_states_amphipod(a, m))
        return states

    def road(self, a, p, m):
        result = []
        p1, p2 = (a.pos, p) if a in m.hallway else (p, a.pos)
        min_col = min(p.col for p in (p1, p2))
        max_col = max(p.col for p in (p1, p2))
        for j in range(min_col, max_col +1):
            p = Pos(p1.row, j)
            if p != a.pos:
                yield p
        for i in range(m.hallway_row + 1, p2.row + 1):
            p = Pos(i, p2.col)
            if p != a.pos:
                yield p
        return result
        
    def is_available(self, pos):
        return pos not in self.positions

    def can_go_home(self, a, m):
        if a not in m.hallway:
            return False
        home = m.home[a.kind]
        road = self.road(a, home.lower, m)
        # check road to lower
        if not all(self.is_available(r) for r in road):
            return False

        pos = home.lower
        while pos.row <= home.upper.row:
            if not self.is_available(pos) and not self.positions.get(pos).at_home:
                return False
            pos = Pos(pos.row + 1, pos.col)
        return True

    def go_home(self, a, m):
        def calc_home_target(kind, pos, bound):
            if pos.row < bound:
                return None
            if pos not in self.positions:
                return pos
            return calc_home_target(kind, Pos(pos.row - 1, pos.col), bound)
        target = calc_home_target(a.kind, m.home[a.kind].upper, m.home[a.kind].lower.row)
        if not target:
            raise ValueError(f"{a} cannot go home in {self}")
        return self.goto(a, target, m, to_home=True)

    def goto(self, a, pos, m, to_home=False):
        if pos in self.positions:
            raise ValueError(f"Position {pos} already busy in {self}")
        new_a = a.goto(pos, to_home)
        new_positions = copy(self.positions)
        new_positions.pop(a.pos)
        new_positions[new_a.pos] = new_a
        return State(
            self.cost + distance(a, new_a, m) * energy_point[new_a.kind],
            new_positions,
        )


class Place(NamedTuple):
    lower: Pos
    upper: Pos

    @property
    def row(self):
        return self.upper.row

    @property
    def col(self):
        return self.upper.col

    def __iter__(self):
        for row in range(self.lower.row, self.upper.row + 1):
            for col in range(self.lower.col, self.upper.col + 1):
                yield Pos(row, col)

    def __contains__(self, item):
        if isinstance(item, Amphipod):
            item = item.pos
        return (
            self.lower.row <= item.row <= self.upper.row and
            self.lower.col <= item.col <= self.upper.col
        )


class Map:
    def __init__(self, lines):
        self.lines = lines
        self.hallway_row = 1
        home_upper_row = len(lines) - 2
        self.home = {
            k: Place(Pos(2, 2 * i + 3), Pos(home_upper_row, 2 * i + 3)) 
            for i, k in enumerate([A, B, C, D])
        }
        hw_row = self.hallway_row
        min_hw_col = 1
        max_hw_col = len(lines[hw_row]) - 2
        self.hallway = Place(Pos(hw_row, min_hw_col), Pos(hw_row, max_hw_col))

    def __repr__(self):
        return f"H={self.hallway} T={self.home}"

    def print(self, state, road=None, highlight=None, row=None):
        def color(s, color):
            return color + s + NORMAL

        if road is None:
            road = ()

        range_i = (row, row + 1) if row is not None else (0, len(self.lines))
        for i in range(*range_i):
            for j in range(0, len(self.lines[0])):
                p = Pos(i, j)
                a = state.positions.get(p)
                if p in road:
                    ch = color(" ", REV_BLUE)
                elif a is not None:
                    ch = a.kind if a.at_home else a.kind.lower()
                    if p == highlight:
                        ch = color(ch, REV_DIM_BLUE)
                elif p in self.hallway:
                    ch = "."
                elif any(p in home for home in self.home.values()):
                    ch = " "
                else:
                    ch = W
                print(ch, end="")
            if row is None:
                print()
        if row is None:
            print(f"Cost={state.cost}")


def solve(m, state):
    def solve_state(state, path) -> int:
        nonlocal best, visited, best_path

        if state.is_solution(m) and state.cost < best:
            best = state.cost
            print("Found", best)
            best_path = path[:]
            return state.cost
        costs = [MAXINT]

        visited[state.for_set()] = state.cost
        next_states = state.next_states(m)
        for next_state in next_states:
            ns = next_state.for_set()
            to_visit = ns not in visited or next_state.cost < visited[ns]
            if not to_visit or next_state.cost + next_state.heur(m) >= best:
                continue
            costs.append(solve_state(next_state, path + [next_state]))
        return min(costs)

    best = MAXINT
    visited = {}
    best_path = None
    result = solve_state(state, [state])
    print("visited: ", len(visited))
    return result, best_path


#def print_path(path, m):
#    
#    prev = path[0]
#    m.print(prev)
#    for state in path[1:]:
#        p1 = next(a for a in prev.positions if a not in state.positions)
#        p2 = next(a for a in state.positions if a not in prev.positions)
#        road = list(state.road(state.positions[p2], p1, m))
#        m.print(state, road, p2)
#        print("-" * 10)
#        prev = state


def print_path(path, m):
    N = 5
    n_rows = len(m.lines)
    for group in range(len(path) // N + 1):
        for row in range(0, n_rows):
            for group_idx in range(N):
                path_idx = group * N + group_idx
                if path_idx >= len(path):
                    continue
                state = path[path_idx]
                prev = path[path_idx - 1] if path_idx > 0 else path[0]
                p1 = next((a for a in prev.positions if a not in state.positions), None)
                p2 = next((a for a in state.positions if a not in prev.positions), None)
                if p2 is not None and p1 is not None:
                    road = list(state.road(state.positions[p2], p1, m))
                else:
                    road = None
                m.print(state, road=road, highlight=p2, row=row)
                print(" " * 3, end="")
            print()
        print()
    print()


def is_amphipod(ch):
    return A <= ch <= D


def initialize(lines, use_hidden):
    def at_home(kind, pos, m, lines):
        down = Pos(pos.row + 1, pos.col)
        return (
            pos in m.home[kind] 
            and lines[pos.row][pos.col] == kind
            and (lines[down.row][down.col] == W or at_home(kind, down, m, lines))
        )

    if use_hidden:
        lines = lines[0:3] + HIDDEN + lines[3:]
    positions = {}
    m = Map(lines)
    for i, line in enumerate(lines):
        for j, ch in enumerate(line):
            ch = ch.upper()
            pos = Pos(i, j)
            if is_amphipod(ch):
                positions[pos] = Amphipod(pos, ch, at_home(ch, pos, m, lines))
    return m, State(0, positions)

def read_file(path):
    with open(path) as f:
        return f.read().rstrip().split("\n")


def main():
    lines = read_file(sys.argv[1])

    for use_hidden in (False, True):
        m, state = initialize(lines, use_hidden)
        print("=" * 15)
        m.print(state)
        cost, path = solve(m, state)
        print_path(path, m)
        print(f"Result: {cost}")


if __name__ == "__main__":
    main()
