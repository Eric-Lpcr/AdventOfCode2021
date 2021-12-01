from itertools import pairwise, tee


def nb_increases(iterable):
    # number of increasing pairwise values
    return sum(map(lambda p: p[0] < p[1], pairwise(iterable)))  # sum of bools gives number of True values


# def triplewise(iterable):
#     # triplet_wise('ABCDEFG') --> ABC BCD CDE DEF EFG
#     a, b, c = tee(iterable, 3)
#     next(b, None)
#     next(c, None)
#     next(c, None)
#     return zip(a, b, c)


def triplewise(iterable):
    """Return overlapping triplets from an iterable"""
    # triplewise('ABCDEFG') -> ABC BCD CDE DEF EFG
    for (a, _), (b, c) in pairwise(pairwise(iterable)):
        yield a, b, c


def main():
    with open('input.txt') as f:
        depths = list(map(int, f.readlines()))

    # depths = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]

    result1 = nb_increases(depths)
    print(f"Part 1: number of increases is {result1}")

    result2 = nb_increases(list(map(sum, triplewise(depths))))
    print(f"Part 2: number of increases is {result2}")


if __name__ == '__main__':
    main()
