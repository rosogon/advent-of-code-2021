import sys
from collections import deque, defaultdict
from typing import NamedTuple
from math import ceil


def do_step(template, rules):
    result = deque(template[0])
    for i in range(0, len(template) - 1):
        pair = template[i:i+2]
        if pair in rules:
            result.append(rules[pair])
        result.append(pair[1])
    return "".join(result)


def do_pair_counts_step(source_pair_counts, transform):
    dest_pair_counts = defaultdict(int)
    for pair in source_pair_counts:
        pair_0, pair_1 = transform[pair]
        dest_pair_counts[pair_0] += source_pair_counts[pair]
        dest_pair_counts[pair_1] += source_pair_counts[pair]
    return dest_pair_counts
        

def calc_counts(template):
    result = defaultdict(int)
    for ch in template:
        result[ch] += 1
    return result


def calc_counts_from_pair_counts(pair_counts):
    result = defaultdict(int)
    for pair, count in pair_counts.items():
        result[pair[0]] += count
        result[pair[1]] += count
    for letter in result:
        result[letter] = ceil(result[letter] / 2)
    return result


def sorted_dict_to_str(d):
    parts = []
    for k in sorted(d.keys()):
        parts.append(f"'{k}': {repr(d[k])}")
    return "{" + ", ".join(parts) + "}"
        
        
def build_pair_transform(rules):
    result = {}
    for left, right in rules.items():
        child0 = f"{left[0]}{right}"
        child1 = f"{right}{left[1]}"
        result[left] = [child0, child1]
    return result


def build_pair_counts(template):
    pair_counts = defaultdict(int)
    for i in range(0, len(template) - 1):
        pair = template[i:i+2]
        pair_counts[pair] += 1
    return pair_counts


def read_file(path):
    def read_template(line):
        nonlocal template
        template = line.rstrip()

    def read_rules(line):
        left, right = line.rstrip().split(" -> ")
        rules[left] = right

    template = ""
    rules = {}
    func = read_template
    with open(path) as f:
        for line in f:
            if line == "\n":
                func = read_rules
                continue
            func(line)

    return template, rules


def main():
    template, rules = read_file(sys.argv[1])

    pair_transform = build_pair_transform(rules)
    pair_counts = build_pair_counts(template)

    for i in range(0, 10):
        pair_counts = do_pair_counts_step(pair_counts, pair_transform)
        counts = calc_counts_from_pair_counts(pair_counts)
    print(max(counts.values()) - min(counts.values()))

    for i in range(10, 40):
        pair_counts = do_pair_counts_step(pair_counts, pair_transform)
        counts = calc_counts_from_pair_counts(pair_counts)
    print(max(counts.values()) - min(counts.values()))
        

if __name__ == "__main__":
    main()


