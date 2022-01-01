import sys


def calc_most_common_bit(lines, i):
    """Return
    -1 if most common bit is 0
    1 if most common bit is 1
    0 if both are equal"""
    result = 0
    for line in lines:
        result += (int(line[i]) << 1) - 1
    if result < 0:
        result = -1
    elif result > 0:
        result = 1
    return result


def do_filter(lines, byte_len, most_common: bool):
    for i in range(byte_len):
        lines = do_filter_by_bit(lines, i, most_common)
        if len(lines) == 1:
            return binary(lines[0], byte_len)


def do_filter_by_bit(lines, i, most_common: bool):
    mcb = calc_most_common_bit(lines, i)
    bit = current_bit(mcb, most_common)
    lines = list(filter(lambda l: int(l[i]) == bit, lines))
    return lines


def current_bit(mcb, most_common: bool):
    if mcb == 0:
        return int(most_common)
    return int(mcb > 0) if most_common else int(mcb < 0)


def binary(line, byte_len):
    n = 0
    for i in range(byte_len):
        shift = byte_len - 1 - i
        if line[i] != "0":
            n |= 1 << shift
    return n


def main():
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    byte_len = len(lines[0]) - 1
    print(f"byte_len={byte_len}")

    o2 = do_filter(lines, byte_len, True)
    co2 = do_filter(lines, byte_len, False)

    print(f"o2={o2}({o2:08b}) co2={co2}({co2:08b}) o2*co2 = {o2*co2}")


if __name__ == "__main__":
    main()
