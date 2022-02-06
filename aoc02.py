import sys
from typing import NamedTuple


class Position(NamedTuple):
    horizontal: int
    depth: int
    aim: int = 0

    def __add__(a, b):
        return Position(
            horizontal=a.horizontal + b.horizontal, 
            depth = a.depth + b.depth,
            aim = a.aim + b.aim,
        )


def run(lines, actions):
    position = Position(0, 0, 0)
    for line in lines:
        action, value = line.split()
        value = int(value)
        position = actions[action](position, value)
    print(f"{position.horizontal*position.depth}")


def main():

    with open(sys.argv[1]) as f:
        lines = f.readlines()

    actions = {
        "forward": lambda p, v : p + Position(v, 0),
        "down": lambda p, v : p + Position(0, v),
        "up": lambda p, v : p + Position(0, -v),
    }
    run(lines, actions) 

    actions = {
        "forward": lambda p, v : p + Position(v, p.aim * v, 0),
        "down": lambda p, v : p + Position(0, 0, v),
        "up": lambda p, v : p + Position(0, 0, -v),
    }
    run(lines, actions) 


if __name__ == "__main__":
    main()
