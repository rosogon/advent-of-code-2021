import sys

N = 5

class Board:
    def __init__(self, m):
        self.rows = []
        self.cols = []
        self.last_marked = -1
        
        # rows
        for m_row in m:
            row = Line(m_row)
            self.rows.append(row)

        # cols
        for i in range(N):
            m_col = []
            for j in range(N):
                m_col.append(m[j][i])
            col = Line(m_col)
            self.cols.append(col)
                
    def mark(self, n):
        self.last_marked = n
        return self.op(lambda l: l.mark(n))

    def is_winner(self):
        return self.op(lambda l: l.is_winner())
    
    def op(self, f):
        any_row = any(f(row) for row in self.rows)
        any_col = any(f(col) for col in self.cols)
        return any_row or any_col

    def score(self):
        unmarked = set()
        for row in self.rows:
            unmarked |= row.unmarked
        for col in self.cols:
            unmarked |= col.unmarked
        result = sum(unmarked) * self.last_marked
        return result
        
    def __str__(self):
        s = ""
        for row in self.rows:
            s += str(row)
        return s

    
class Line:
    def __init__(self, line):
        self.line = line
        self.unmarked = { n for n in line }

    def mark(self, n):
        result = n in self.unmarked
        if result:
            self.unmarked.remove(n)
        return result             

    def is_winner(self):
        return not self.unmarked

    def __str__(self):
        s = ""
        for n in self.line:
            if n in self.unmarked:
                p = f"{n}"
            else:
                p = f"<{n}>"
            s += f"{p:5}"
        return s + "\n"
    

def read_file(path):
    def read_board():
        board = []
        for i in range(N):
            l = f.readline()
            if l == "":
                return None
            line = [int(n) for n in l.split()]
            board.append(line)
        return Board(board)
    
    with open(path) as f:
        line = f.readline()
        numbers = [ int(n) for n in line.split(",") ]

        boards = set()
        while(True):
            f.readline()
            board = read_board()
            if not board:
                break
            boards.add(board)
        return numbers, boards


def print_board(b):
    b = b.m
    for i in range(N):
        for j in range(N):
            print(f"{b[i][j]} ", end="")
        print()



def winner_board(numbers, boards):
    for n in numbers:
        process_round(n, boards)
        for b in boards:
            if b.is_winner():
                return b

def last_winner_board(numbers, boards):
    last_winner = None
    while len(boards) > 0:
        n, numbers = numbers[0], numbers[1:]
        process_round(n, boards)
        for b in list(boards):
            if b.is_winner():
                boards.remove(b)
                last_winner = b
    return last_winner


def process_round(n, boards):
    for b in boards:
        b.mark(n)
    

def main():
    numbers, boards = read_file(sys.argv[1])

    winner = winner_board(numbers, boards)
    print(winner)
    print(winner.score())

    numbers, boards = read_file(sys.argv[1])
    loser = last_winner_board(numbers, boards)
    print(loser)
    print(loser.score())
    
    
if __name__ == "__main__":
    main()

