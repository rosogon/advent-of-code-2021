import sys
from typing import NamedTuple, Any
import operator
from functools import reduce

BYTE = 8


def prod(values):
    return reduce(operator.mul, values, 1)


operations = {
    0: ("sum", sum),
    1: ("prod", prod),
    2: ("min", min),
    3: ("max", max),
    5: ("gt", lambda l: int(operator.gt(*l))),
    6: ("lt", lambda l: int(operator.lt(*l))),
    7: ("eq", lambda l: int(operator.eq(*l))),
}


def byte_array_to_int(array):
    result = 0
    for byte in array:
        result = (result << 8) | byte
    return result
        

def parse_bits(packet, offset, length):
    end = offset + length - 1
    b1, o1 = divmod(offset, BYTE)
    b2, o2 = divmod(end, BYTE)

    aux = packet[b1:b2+1]
    n = byte_array_to_int(aux)

    n = n >> (BYTE - 1 - o2)
    mask = (1 << length) - 1 
    return n & mask, offset + length


class Parser:
    def __init__(self):
        self.sum = 0

    def parse_packet(self, packet, offset=0):
        
        version, offset = self._parse_version(packet, offset)
        kind, offset = self._parse_type(packet, offset)

        if kind == 4:
            return self._parse_literal(packet, offset)
        else:
            return self._parse_operator(kind, packet, offset)

    def _parse_version(self, packet, offset):
        version, offset = parse_bits(packet, offset, 3)
        self.sum += version
        return version, offset

    def _parse_type(self, packet, offset):
        kind, offset = parse_bits(packet, offset, 3)
        return kind, offset

    def _parse_literal(self, packet, offset):
        n = 0
        more = True
        while more:
            more, offset = parse_bits(packet, offset, 1)
            part, offset = parse_bits(packet, offset, 4)
            n = (n << 4) | part
        return n, offset

    def _parse_operator(self, kind, packet, offset):
        def bits_length():
            return parse_bits(packet, offset, 15)

        def subpacket_length():
            return parse_bits(packet, offset, 11)

        def operands_by_length(length, offset):
            final_offset = offset + length
            operands = []
            while offset < final_offset:
                operand, offset = self.parse_packet(packet, offset)
                operands.append(operand)
            return operands, final_offset

        def operands_by_subpackets(n_subpackets, offset):
            operands = []
            for i in range(n_subpackets):
                operand, offset = self.parse_packet(packet, offset)
                operands.append(operand)
            return operands, offset

        name, f = operations[kind]
        parse_fs = [operands_by_length, operands_by_subpackets]

        operand_spec, offset = parse_bits(packet, offset, 1)
        param, offset = subpacket_length() if operand_spec else bits_length()
        operands, offset = parse_fs[operand_spec](param, offset)
        result = f(operands)
        return result, offset


def read_file(path):
    lines = []
    packets = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            hexdigits = [ int(ch, 16) for ch in line ]
            # a packet is an array of bytes
            packet = [
                16*hexdigits[i] + hexdigits[i+1] 
                for i in range(0, len(hexdigits), 2)
            ]
            lines.append(line)
            packets.append(packet)

    return packets, lines

def main():
    packets, lines = read_file(sys.argv[1])
    
    for packet in packets:
        parser = Parser()
        print(f"{byte_array_to_int(packet):0x}")
        result, offset = parser.parse_packet(packet)
        print(f"RESULT={result}")
        print(f"VERSION SUM={parser.sum}")
        print()


if __name__ == "__main__":
    main()
