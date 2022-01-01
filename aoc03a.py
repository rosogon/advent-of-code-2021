import sys


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


def main():
    with open(sys.argv[1]) as f:
        lines = f.readlines()

    byte_len = len(lines[0]) - 1
    print(f"byte_len={byte_len}")
    vec = [0 for i in range(byte_len)]
    for line in lines:
        for bit in range(byte_len):
            vec[bit] += (int(line[bit]) << 1) - 1

    gamma_rate = calc_gamma_rate(vec, byte_len)
    epsilon_rate = calc_epsilon_rate(gamma_rate, byte_len)

    print(f"g={gamma_rate} e={epsilon_rate} g*e={gamma_rate*epsilon_rate}")
        

if __name__ == "__main__":
    main()
