import re
from enum import IntEnum
from itertools import product
from math import prod
from typing import Union


class Coordinate:
    def __init__(self, coord1, coord2=None, coord3=None):
        if coord2 is None:
            self.coord = coord1
        else:
            self.coord = (coord1, coord2, coord3)

    @property
    def dimension(self) -> int:
        return len(self.coord)

    def zeroes(self) -> 'Coordinate':
        return Coordinate([0] * self.dimension)

    def ones(self) -> 'Coordinate':
        return Coordinate([1] * self.dimension)

    def __sub__(self, other: 'Coordinate'):
        return Coordinate([a - b for a, b in zip(self.coord, other.coord)])

    def __add__(self, other: 'Coordinate'):
        return Coordinate([a + b for a, b in zip(self.coord, other.coord)])

    def __eq__(self, other: 'Coordinate') -> bool:
        return self.coord == other.coord

    def __hash__(self) -> int:
        return hash(tuple(self.coord))

    def __str__(self) -> str:
        return f"[{','.join(str(c) for c in self.coord)}]"

    def __repr__(self) -> str:
        return str(self)


class Cuboid:
    def __init__(self, c_min: Coordinate, c_max: Coordinate):
        self.c_min = Coordinate([min(a, b) for a, b in zip(c_min.coord, c_max.coord)])
        self.c_max = Coordinate([max(a, b) for a, b in zip(c_min.coord, c_max.coord)])

    @property
    def size(self) -> int:
        return prod((self.c_max - self.c_min + self.c_min.ones()).coord)

    def contains(self, item: Union[Coordinate, 'Cuboid']) -> bool:
        if type(item) == Coordinate:
            return all(c_min <= c <= c_max for c_min, c, c_max in zip(self.c_min.coord, item.coord, self.c_max.coord))
        elif type(item) == Cuboid:
            return item.c_min in self and item.c_max in self

    def __contains__(self, item: Union[Coordinate, 'Cuboid']) -> bool:
        return self.contains(item)

    def intersects(self, other: 'Cuboid') -> bool:
        return all(not (c2_max < c1_min or c2_min > c1_max)
                   for c1_min, c1_max, c2_min, c2_max
                   in zip(self.c_min.coord, self.c_max.coord, other.c_min.coord, other.c_max.coord))

    def intersection(self, other: 'Cuboid') -> Union['Cuboid', None]:
        if self.intersects(other):
            i_min = Coordinate([max(a, b) for a, b in zip(self.c_min.coord, other.c_min.coord)])
            i_max = Coordinate([min(a, b) for a, b in zip(self.c_max.coord, other.c_max.coord)])
            return Cuboid(i_min, i_max)
        else:
            return None

    def minus(self, other: 'Cuboid') -> 'list[Cuboid]':
        """Break self in pieces to remove intersection with other"""
        if other.contains(self):
            return []
        intersection = self.intersection(other)
        if intersection is None:
            return [self]

        cuts = []
        for c in range(3):
            cuts.append([self.c_min.coord[c]])
            if self.c_min.coord[c] < other.c_min.coord[c] <= self.c_max.coord[c]:
                cuts[c].extend([other.c_min.coord[c] - 1, other.c_min.coord[c]])
            if self.c_min.coord[c] <= other.c_max.coord[c] < self.c_max.coord[c]:
                cuts[c].extend([other.c_max.coord[c], other.c_max.coord[c] + 1])
            cuts[c].append(self.c_max.coord[c])
            cuts[c] = [(a, b) for a, b in zip(cuts[c][0::2], cuts[c][1::2])]

        remainder_coord = product(*cuts)
        remaining_cuboids = list()
        for (x1, x2), (y1, y2), (z1, z2) in remainder_coord:
            cuboid = Cuboid(Coordinate(x1, y1, z1), Coordinate(x2, y2, z2))
            if cuboid != intersection:
                remaining_cuboids.append(cuboid)

        return remaining_cuboids

    def union(self, other: 'Cuboid') -> 'list[Cuboid]':
        u = [self]
        u.extend(other.minus(self))
        return u

    def __eq__(self, other):
        return self.c_min == other.c_min and self.c_max == other.c_max

    def __str__(self) -> str:
        c = [val + str(a) + '..' + str(b) for val, a, b in zip(['x=', 'y=', 'z='], self.c_min.coord, self.c_max.coord)]
        return f"({','.join(c)})"

    def __repr__(self) -> str:
        return str(self)


class Status(IntEnum):
    off = 0
    on = 1


class Reactor:
    def __init__(self):
        self.cuboids = list()

    def extend(self, other: Cuboid, status: Status) -> None:
        if other is None:
            return
        new_cuboids = list()
        for cuboid in self.cuboids:
            new_cuboids.extend(cuboid.minus(other))
        self.cuboids = new_cuboids
        if status is Status.on:
            self.cuboids.append(other)

    @property
    def size(self):
        return sum(c.size for c in self.cuboids)


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')

    cuboids = list()

    pattern = re.compile(r'(?P<on_off>on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)')
    with open(filename) as f:
        for line in f.readlines():
            match = pattern.match(line)
            status = Status[match['on_off']]
            values = [int(g) for g in match.groups()[1:]]
            cuboids.append((Cuboid(Coordinate(values[0:6:2]), Coordinate(values[1:6:2])), status))
    del filename, f, line, match, pattern, values

    reactor = Reactor()
    domain = Cuboid(Coordinate(-50, -50, -50), Coordinate(50, 50, 50))
    for cuboid, status in cuboids:
        domain_cuboid = domain.intersection(cuboid)
        reactor.extend(domain_cuboid, status)

    on_cubes = reactor.size
    print(f'Part 1: there are {on_cubes} cubes on')
    if testing and expected1 is not None:
        assert on_cubes == expected1

    reactor = Reactor()
    for cuboid, status in cuboids:
        reactor.extend(cuboid, status)

    on_cubes = reactor.size
    print(f'Part 2: there are {on_cubes} cubes on')
    if testing and expected2 is not None:
        assert on_cubes == expected2


if __name__ == '__main__':
    main('minitest.txt', True, 39, 39)
    main('test.txt', True, 590784, 39769202357779)
    main('test2.txt', True, 474140, 2758514936282235)
    main('input.txt')
