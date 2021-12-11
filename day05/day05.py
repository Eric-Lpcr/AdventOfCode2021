from collections import namedtuple
from itertools import zip_longest
from functools import partial
from operator import lt


def inclusive_range(start, stop=None, step=None):
    if stop is None:  # single arg call
        stop = start
        start = 0
    if step is None:
        step = 1 if stop > start else -1
    stop = stop + 1 if step >= 0 else stop - 1
    return range(start, stop, step)


Point = namedtuple('Point', ['x', 'y'])


class OceanFloor:
    def __init__(self):
        self._vents = dict()
        self._max = Point(0, 0)  # just for __repr__

    def map_lines(self, lines, filter_diagonals=False):
        for x1, y1, x2, y2 in lines:
            if filter_diagonals and not (x1 == x2 or y1 == y2):
                continue
            self.map_line(x1, y1, x2, y2)

    def map_line(self, x1, y1, x2, y2):
        fill_value = None
        if x1 == x2:
            fill_value = x1
        elif y1 == y2:
            fill_value = y1
        for x, y in zip_longest(inclusive_range(x1, x2), inclusive_range(y1, y2), fillvalue=fill_value):
            p = Point(x, y)
            self._vents[p] = self._vents.get(p, 0) + 1
        self._max = Point(max(self._max.x, x1, x2), max(self._max.y, y1, y2))

    def count_overlaps(self):
        return sum(v > 1 for v in self._vents.values())
        # return sum(1 for v in self._vents.values() if v > 1)

    def count_overlaps2(self):
        # just to learn about functools.partial...
        # partial(lt, 1) gives a function which states if 1 is lower than parameter
        # equivalent to sum(1 < v for v in self.vents.values())
        return sum(map(partial(lt, 1), self._vents.values()))

    def clear(self):
        self._vents = dict()

    def __repr__(self):
        s = ''
        for y in inclusive_range(self._max.y):
            for x in inclusive_range(self._max.x):
                s += f'{self._vents.get(Point(x, y), ".")}'
            s += '\n'
        return s


def main(filename):
    print(f'--------- {filename}')
    with open(filename) as f:
        lines = [[int(c) for c in line.replace('->', ',').split(',')] for line in f.readlines()]

    ocean_floor = OceanFloor()
    ocean_floor.map_lines(lines, filter_diagonals=True)

    overlaps = ocean_floor.count_overlaps()
    print(f'Part 1: count of overlaps is {overlaps}')

    ocean_floor.clear()
    ocean_floor.map_lines(lines)

    overlaps = ocean_floor.count_overlaps()
    print(f'Part 2: count of overlaps is {overlaps}')


if __name__ == '__main__':
    main('test.txt')
    main('input.txt')
