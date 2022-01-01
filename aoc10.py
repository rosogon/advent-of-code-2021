import sys
from collections import deque


open_tokens = {
    "(" : ")",
    "[" : "]",
    "{" : "}",
    "<" : ">",
}

close_tokens = {v: k for k, v in open_tokens.items()}

error_scores = {
    ")": 3,
    "]" : 57,
    "}" : 1197,
    ">" : 25137,
}

completion_scores = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}

class Chunk:
    def __init__(self, kind: str):
        self.kind = kind
        self.children = []

    def add(chunk):
        self.children.append(chunk)


def read_file(path):
    result = []
    with open(path) as f:
        for line in f:
            result.append(line.rstrip())
    return result


class Parser:
    def __init__(self):
        pass


    def _nexttoken(self):
        for ch in self.line:
            yield ch
        return

    def _get_completion_score(self, queue):
        score = 0
        while queue:
            tok = queue.pop()
            score = score * 5 + completion_scores[tok]
        return score

    def parse(self, line):
        self.line = line
        queue = deque()
        for tok in self._nexttoken():
            if tok in open_tokens:
                queue.append(tok)
            elif tok in close_tokens:
                last_tok = queue.pop()
                if close_tokens[tok] != last_tok:
                    expected = open_tokens[last_tok]
                    print(f"Expected {expected} but found {tok} instead")
                    return error_scores[tok], 0
            else:
                pass
                
        if queue:
            print(f"Incomplete: {queue}")
            return 0, self._get_completion_score(queue)           
        return 0, 0


def main():
    lines = read_file(sys.argv[1])
    parser = Parser()
    error_score = 0
    completion_scores = []
    for line in lines:
        scores = parser.parse(line)
        error_score += scores[0]
        if scores[1] > 0:
            completion_scores.append(scores[1])
    completion_scores = sorted(completion_scores)
    completion_score = completion_scores[(len(completion_scores) - 1) // 2]
    print(error_score)
    print(completion_score)

    
if __name__ == "__main__":
    main()
