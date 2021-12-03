import sys
from itertools import compress
from math import log


def compute_power_consumption(reports):
    bit_width = int(log(max(reports), 2) + 1)
    half_length = len(reports) / 2
    gamma_rate = 0
    for bit_pos in range(bit_width):
        ones = (report >> bit_pos & 1 for report in reports)
        if sum(ones) > half_length:  # more ones than zeroes
            gamma_rate |= 1 << bit_pos

    epsilon_rate = gamma_rate ^ (pow(2, bit_width) - 1)  # flip all bits (xor with ones)

    return gamma_rate * epsilon_rate


def find_report(reports, selector_criteria):
    bit_width = int(log(max(reports), 2) + 1)
    rating_reports = reports
    rating_report = 0

    for bit_pos in reversed(range(bit_width)):
        # reversed is necessary here because each loop prunes the reports, and we have to start at left bit
        bits = [report >> bit_pos & 1 for report in rating_reports]
        selector = selector_criteria(bits)
        rating_reports = list(compress(rating_reports, selector))
        if len(rating_reports) == 1:
            rating_report = rating_reports[0]
            break

    return rating_report


def least_frequent_bit_selector(bits):
    if sum(bits) < len(bits) / 2:  # sum(bits) is number of ones
        return bits  # select ones
    else:
        return [not bit for bit in bits]  # select zeroes


def most_frequent_bit_selector(bits):
    if sum(bits) >= len(bits) / 2:  # sum(bits) is number of ones
        return bits  # select ones
    else:
        return [not bit for bit in bits]  # select zeroes


def compute_life_support_rating(reports):
    oxygen_generator_rating = find_report(reports, most_frequent_bit_selector)
    co2_scrubber_rating = find_report(reports, least_frequent_bit_selector)

    return oxygen_generator_rating * co2_scrubber_rating


def main():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    with open(filename) as f:
        reports = [int(line, 2) for line in f.readlines()]

    pc = compute_power_consumption(reports)
    print(f'Part 1: power consumption is {pc}')

    lsr = compute_life_support_rating(reports)
    print(f'Part 2: life support rating is {lsr}')


if __name__ == '__main__':
    main()
