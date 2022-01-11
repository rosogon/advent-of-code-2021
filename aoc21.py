import sys
from typing import NamedTuple
from collections import deque, defaultdict


M = 10
N = 100
W_D = 1000
W_Q = 21
Q = 3


def calc_rolls_count():
    count = defaultdict(int)
    for i in range(1, Q + 1):
        for j in range(1, Q + 1):
            for k in range(1, Q + 1):
                count[i+j+k] += 1 
    return count

rolls_count = calc_rolls_count()


class Die:
    def __init__(self):
        self.rolls = 0
        self._it = self._gen()
        
    def roll(self):
        self.rolls += 1
        return next(self._it)

    def _gen(self):
        result = 0
        while True:
            result = (result % N) + 1 
            yield result
    

class Player:
    def __init__(self, position, points_to_win=W_D):
        self.position = position
        self.points = 0
        self.stack = deque()
        self.points_to_win = points_to_win

    @property
    def state(self):
        return (self.position, self.points)

    def _push(self):
        self.stack.append((self.position, self.points))

    def move(self, spaces):
        self._push()
        self.position = (self.position - 1 + spaces) % M + 1
        self.points += self.position

    def rollback(self):
        self.position, self.points = self.stack.pop()

    def won(self):
        return self.points >= self.points_to_win

    def __str__(self):
        return f"Player({self.position},{self.points})"


def deterministic_game(players):
    die = Die()
    done = False
    i = 0
    while not done:
         rolls = sum([die.roll(), die.roll(), die.roll()])
         p = players[i]
         p.move(rolls)
         done = p.won()
         i = (i + 1) % 2
    return (players[i].points * die.rolls)


def quantum_game(players):

    def f(to_play, r):
        p = players[to_play]
        p.move(r)

        state = (players[0].state, players[1].state, to_play)
        if state in cache:
            result = cache[state]
        elif p.won():
            result = [to_play == i for i in range(2)]
        else:
            result = turn(to_play ^ 1)

        cache[state] = result
        p.rollback()
        return result

    def turn(to_play):
        p = players[to_play]
        result = [0, 0]

        for r, c in rolls_count.items():
            w0, w1 = f(to_play, r)
            result[0] += w0 * c
            result[1] += w1 * c
        return result
    n = 0
    cache = {}
    return turn(0)


def read_file(path):
    with open(path) as f:
        lines = f.read().strip().split("\n")
    positions = [int(line.split(": ")[1]) for line in lines]
    return positions


def main():
    positions = read_file(sys.argv[1])
    players = [Player(pos, W_D) for pos in positions]
    print(deterministic_game(players))

    players = [Player(pos, W_Q) for pos in positions]
    print(quantum_game(players))


if __name__ == "__main__":
    main()
