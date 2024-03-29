from itertools import pairwise, tee, islice


def count_increases(iterable):
    # Counts increasing pairwise values
    return sum(map(lambda p: p[0] < p[1], pairwise(iterable)))  # sum of bools gives number of True values


def triplewise(iterable):
    """Return overlapping triplets from an iterable"""
    # triplewise('ABCDEFG') -> ABC BCD CDE DEF EFG
    # https://docs.python.org/3/library/itertools.html#itertools-recipes
    for (a, _), (b, c) in pairwise(pairwise(iterable)):
        yield a, b, c


def main(filename):
    print(f'--------- {filename}')
    with open(filename) as f:
        depths = list(map(int, f.readlines()))

    result1 = count_increases(depths)
    print(f"Part 1: number of increases is {result1}")

    result2 = count_increases(list(map(sum, triplewise(depths))))
    print(f"Part 2: number of increases is {result2}")


if __name__ == '__main__':
    main('test.txt')
    main('input.txt')
