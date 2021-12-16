from collections import namedtuple
from math import prod
from operator import gt, lt, eq


class BitStream:
    def __init__(self, hex_string):
        self._hex_string = hex_string
        self._bit_string = ''

    def get_int(self, bit_length):
        needed_bits = bit_length - len(self._bit_string)
        if needed_bits > 0:
            needed_hex = needed_bits // 4 + 1
            self._bit_string += format(int(self._hex_string[:needed_hex], 16), f'0{needed_hex * 4}b')
            self._hex_string = self._hex_string[needed_hex:]

        get_bits = self._bit_string[:bit_length]
        self._bit_string = self._bit_string[bit_length:]
        return int(get_bits, 2)


class Packet:
    def __init__(self, length, version):
        self.length = length
        self.version = version

    @property
    def version_sum(self):
        return self.version
    
    
class LiteralPacket(Packet):
    ID = 4

    def __init__(self, length, version, value):
        super().__init__(length, version)
        self.value = value

    def __repr__(self):
        return f'{self.value} v{self.version} '


class OperatorPacket(Packet):
    OperatorDescriptor = namedtuple('OperatorDescriptor', ['label', 'compute', 'take_list'])
    OPERATORS = {0: OperatorDescriptor('+', sum, True),
                 1: OperatorDescriptor('*', prod, True),
                 2: OperatorDescriptor('min', min, True),
                 3: OperatorDescriptor('max', max, True),
                 5: OperatorDescriptor('>', gt, False),
                 6: OperatorDescriptor('<', lt, False),
                 7: OperatorDescriptor('=', eq, False)
                 }

    def __init__(self, length, version, type_id):
        super().__init__(length, version)
        self.operator_id = type_id
        self._sub_packets = []
    
    def append(self, sub_packet):
        self._sub_packets.append(sub_packet)
        self.length += sub_packet.length
        
    @property
    def version_sum(self):
        return self.version + sum(sp.version_sum for sp in self._sub_packets)

    @property
    def value(self):
        operator = self.OPERATORS[self.operator_id]
        params = [sp.value for sp in self._sub_packets]
        if operator.take_list:
            return operator.compute(params)
        else:
            return operator.compute(*params)

    def __repr__(self):
        sub_packets_str = ", ".join(sp.__repr__() for sp in self._sub_packets)
        return f'{self.OPERATORS[self.operator_id].label} v{self.version} [{sub_packets_str}] '


class PacketDecoder:
    def __init__(self, bit_stream):
        self.bit_stream = bit_stream

    def decode_packet(self):
        version = self.bit_stream.get_int(3)
        type_id = self.bit_stream.get_int(3)
        if type_id == LiteralPacket.ID:
            p = self._decode_literal(version)
        else:
            p = self._decode_operator(version, type_id)
        p.length += 6
        return p

    def _decode_literal(self, version):
        p = LiteralPacket(0, version, 0)
        while True:
            continuation = self.bit_stream.get_int(1)
            p.value <<= 4
            p.value += self.bit_stream.get_int(4)
            p.length += 5
            if not continuation:
                break
        return p

    def _decode_operator(self, version, type_id):
        length_type_id = self.bit_stream.get_int(1)
        p = OperatorPacket(1, version, type_id)
        if length_type_id == 0:
            sub_packets_length = self.bit_stream.get_int(15)
            p.length += 15
            while sub_packets_length > 0:
                sp = self.decode_packet()
                p.append(sp)
                sub_packets_length -= sp.length
        elif length_type_id == 1:
            sub_packets_count = self.bit_stream.get_int(11)
            p.length += 11
            for _ in range(sub_packets_count):
                sp = self.decode_packet()
                p.append(sp)
        return p
        

def main(filename, testing=False, expected1=None):
    print(f'--------- {filename}')
    with open(filename) as f:
        hex_strings = f.read().splitlines()

    for i, hex_string in enumerate(hex_strings):
        if hex_string.startswith('#'):
            continue

        decoder = PacketDecoder(BitStream(hex_string))
        packet = decoder.decode_packet()
        print(f'Part 1: packet version sum is {packet.version_sum}')
        if testing:
            assert packet.version_sum == expected1[i]

        print(f'Part 2: packet value is {packet.value}')


if __name__ == '__main__':
    main('test.txt', True, [6, 9, 14, 16, 12, 23, 31])
    main('input.txt')
