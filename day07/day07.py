from collections import defaultdict
from itertools import accumulate


def histogram(data):
    counts = defaultdict(int)
    for d in data:
        counts[d] += 1
    return counts


def median(data):
    counts = histogram(data)
    distinct_values = sorted(counts.keys())
    frequencies = [counts[d] for d in distinct_values]
    cumulated_frequencies = accumulate(frequencies)
    total_count = sum(frequencies)
    cumulated_relative_frequencies = [f / total_count for f in cumulated_frequencies]
    median_index = next(i for i, frequency in enumerate(cumulated_relative_frequencies) if frequency > 0.5)
    median_value = distinct_values[median_index]
    return median_value, counts


def mean(data):
    counts = histogram(data)
    total_count = sum(counts.values())
    mean_value = sum(v * c for v, c in counts.items()) / total_count
    return mean_value, counts


def compute_minimal_fuel1(crab_positions):
    optimal_crab_position, counts = median(crab_positions)
    fuel = sum((position - optimal_crab_position) * count for position, count in counts.items())
    return fuel, optimal_crab_position


def sum_of_k(k):
    """Sum of the k first integers starting at 1"""
    k = abs(int(k))  # k must be a positive integer
    return k * (k + 1) // 2


def compute_minimal_fuel2(crab_positions):
    optimal_crab_position, counts = mean(crab_positions)

    # mean() is a decimal, let's try with previous and next int values
    optimal_crab_position1 = int(optimal_crab_position)
    fuel1 = sum(sum_of_k(position - optimal_crab_position1) * count for position, count in counts.items())

    optimal_crab_position2 = int(round(optimal_crab_position, 0))
    fuel2 = sum(sum_of_k(position - optimal_crab_position2) * count for position, count in counts.items())

    if fuel1 < fuel2:
        return fuel1, optimal_crab_position1
    else:
        return fuel2, optimal_crab_position2


def main(filename):
    print(f'--------- {filename}')
    with open(filename) as f:
        crab_positions = [int(s) for s in f.readline().split(',')]

    fuel, position = compute_minimal_fuel1(crab_positions)
    print(f'Part 1: optimal crabs position is {position}, minimal fuel consumption is {fuel}')

    fuel, position = compute_minimal_fuel2(crab_positions)
    print(f'Part 2: optimal crabs position is {position}, minimal fuel consumption is {fuel}')


if __name__ == '__main__':
    main('test.txt')
    main('input.txt')
