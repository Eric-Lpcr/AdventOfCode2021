import sys
from itertools import pairwise, tee


def nb_increases(iterable):
    # number of increasing pairwise values
    return sum(map(lambda p: p[0] < p[1], pairwise(iterable)))  # sum of bools gives number of True values


def my_triplewise(iterable):
    # triplet_wise('ABCDEFG') --> ABC BCD CDE DEF EFG
    a, b, c = tee(iterable, 3)
    next(b, None)
    next(c, None)
    next(c, None)
    return zip(a, b, c)


def triplewise(iterable):
    """Return overlapping triplets from an iterable"""
    # triplewise('ABCDEFG') -> ABC BCD CDE DEF EFG
    # https://docs.python.org/3/library/itertools.html#itertools-recipes
    for (a, _), (b, c) in pairwise(pairwise(iterable)):
        yield a, b, c


def main():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    with open(filename) as f:
        depths = list(map(int, f.readlines()))

    result1 = nb_increases(depths)
    print(f"Part 1: number of increases is {result1}")

    result2 = nb_increases(list(map(sum, triplewise(depths))))
    print(f"Part 2: number of increases is {result2}")


if __name__ == '__main__':
    main()
