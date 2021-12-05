import sys
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


class OceanFloor:
    def __init__(self):
        self.vents = dict()
        self.max_x = self.max_y = 0  # just for __repr__

    def map_lines(self, lines, filter_diagonals=False):
        for line in lines:
            x1, y1, x2, y2 = [int(c) for c in line.replace('->', ',').split(',')]
            if filter_diagonals and not (x1 == x2 or y1 == y2):
                continue
            self.map_line(x1, y1, x2, y2)

    Point = namedtuple('Point', ['x', 'y'])

    def map_line(self, x1, y1, x2, y2):
        fill_value = None
        if x1 == x2:
            fill_value = x1
        elif y1 == y2:
            fill_value = y1
        for x, y in zip_longest(inclusive_range(x1, x2), inclusive_range(y1, y2), fillvalue=fill_value):
            p = OceanFloor.Point(x, y)
            self.vents[p] = self.vents.get(p, 0) + 1
        self.max_x = max(self.max_x, x1, x2)
        self.max_y = max(self.max_y, y1, y2)

    def count_overlaps(self):
        return sum(v > 1 for v in self.vents.values())

    def count_overlaps2(self):
        # just to learn about functools.partial...
        # partial(lt, 1) gives a function which states if 1 is lower than parameter
        # equivalent to sum(1 < v for v in self.vents.values())
        return sum(map(partial(lt, 1), self.vents.values()))

    def clear(self):
        self.vents = dict()

    def __repr__(self):
        s = ''
        for y in inclusive_range(self.max_y):
            for x in inclusive_range(self.max_x):
                s += f'{self.vents.get(OceanFloor.Point(x, y), ".")}'
            s += '\n'
        return s


def main():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    with open(filename) as f:
        lines = f.readlines()

    ocean_floor = OceanFloor()
    ocean_floor.map_lines(lines, filter_diagonals=True)

    overlaps = ocean_floor.count_overlaps()
    print(f'Part 1: count of overlaps is {overlaps}')

    ocean_floor.clear()
    ocean_floor.map_lines(lines)

    overlaps = ocean_floor.count_overlaps()
    print(f'Part 2: count of overlaps is {overlaps}')


if __name__ == '__main__':
    main()
