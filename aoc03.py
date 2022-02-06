import sys


verbose = False


def part_1(lines):

    def calc_gamma_rate(vec, byte_len):
        gamma_rate_vec = []
        for i in range(byte_len):
            gamma_rate_vec.append(int(vec[i] > 0))
        print(gamma_rate_vec)

        gamma_rate = 0
        for i in range(byte_len):
            if vec[i] > 0:
                shift = byte_len - 1 - i
                gamma_rate |= 1 << shift
        return gamma_rate


    def calc_epsilon_rate(gamma_rate, byte_len):
        mask = (1 << byte_len) - 1
        epsilon_rate = ~gamma_rate & mask
        return epsilon_rate

    byte_len = len(lines[0]) - 1
    if verbose:
        print(f"byte_len={byte_len}")

    vec = [0 for i in range(byte_len)]
    for line in lines:
        for bit in range(byte_len):
            vec[bit] += (int(line[bit]) << 1) - 1

    gamma_rate = calc_gamma_rate(vec, byte_len)
    epsilon_rate = calc_epsilon_rate(gamma_rate, byte_len)

    if verbose:
        print(f"g={gamma_rate} e={epsilon_rate} g*e={gamma_rate*epsilon_rate}")
    else:
        print(f"{gamma_rate*epsilon_rate}")


def part_2(lines):

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

    byte_len = len(lines[0]) - 1
    if verbose:
        print(f"byte_len={byte_len}")

    o2 = do_filter(lines, byte_len, True)
    co2 = do_filter(lines, byte_len, False)

    if verbose:
        print(f"o2={o2}({o2:08b}) co2={co2}({co2:08b}) o2*co2 = {o2*co2}")
    else:
        print(f"{o2*co2}")


def main():
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    part_1(lines)
    part_2(lines)


if __name__ == "__main__":
    main()
