import collections
from itertools import tee, islice


def my_triplewise(iterable):
    # triplet_wise('ABCDEFG') --> ABC BCD CDE DEF EFG
    a, b, c = tee(iterable, 3)
    next(b, None)
    next(c, None)
    next(c, None)
    return zip(a, b, c)


def n_wise(iterable, size):
    tees = list(tee(iterable, size))
    for slide in range(size):
        tees[slide] = islice(tees[slide], slide, None)
    for a_tuple in zip(*tees):
        yield a_tuple


def n_wise2(iterable, size):
    for index in range(len(iterable) - size + 1):
        yield tuple(islice(iterable, index, index + size))


# https://docs.python.org/3/library/itertools.html#itertools-recipes
def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def map_wise(fn, iterable, size):
    return (fn(item) for item in n_wise2(iterable, size))


if __name__ == '__main__':
    print(list(my_triplewise('ABCDEFG')))
    print(list(n_wise('ABCDEFG', 3)))
    print(list(n_wise('ABCDEFG', 4)))
    print(list(n_wise2('ABCDEFG', 3)))
    print(list(sliding_window('ABCDEFG', 4)))

    print(list(map_wise(lambda t: ''.join(t), 'ABCDEFG', 3)))
    print(list(map_wise(sum, range(10), 4)))

