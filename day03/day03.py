from itertools import compress


def get_bits_at(bit_pos, integers):
    return (i >> bit_pos & 1 for i in integers)


def compute_power_consumption(reports):
    bit_length = max(reports).bit_length()
    half_report_count = len(reports) / 2
    gamma_rate = 0
    for bit_pos in range(bit_length):
        bits = get_bits_at(bit_pos, reports)
        if sum(bits) > half_report_count:  # more ones than zeroes
            gamma_rate |= 1 << bit_pos

    epsilon_rate = gamma_rate ^ (pow(2, bit_length) - 1)  # flip all bits (xor with ones)

    return gamma_rate * epsilon_rate


def find_report(reports, selector_criteria):
    bit_length = max(reports).bit_length()
    report = 0

    for bit_pos in reversed(range(bit_length)):
        # reversed is necessary here because each loop prunes the reports, and we have to start at left bit
        bits = get_bits_at(bit_pos, reports)
        selector = selector_criteria(bits)
        reports = list(compress(reports, selector))
        if len(reports) == 1:
            report = reports[0]
            break

    return report


def least_frequent_bit_selector(bits):
    bits = list(bits)
    if sum(bits) < len(bits) / 2:  # sum(bits) is number of ones
        return bits  # select ones
    else:
        return [not bit for bit in bits]  # select zeroes


def most_frequent_bit_selector(bits):
    bits = list(bits)
    if sum(bits) >= len(bits) / 2:  # sum(bits) is number of ones
        return bits  # select ones
    else:
        return [not bit for bit in bits]  # select zeroes


def compute_life_support_rating(reports):
    oxygen_generator_rating = find_report(reports, most_frequent_bit_selector)
    co2_scrubber_rating = find_report(reports, least_frequent_bit_selector)

    return oxygen_generator_rating * co2_scrubber_rating


def main(filename):
    print(f'--------- {filename}')
    with open(filename) as f:
        reports = [int(line, 2) for line in f.readlines()]

    pc = compute_power_consumption(reports)
    print(f'Part 1: power consumption is {pc}')

    lsr = compute_life_support_rating(reports)
    print(f'Part 2: life support rating is {lsr}')


if __name__ == '__main__':
    main('test.txt')
    main('input.txt')
