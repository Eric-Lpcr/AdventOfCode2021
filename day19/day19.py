from dataclasses import dataclass
from enum import Enum
from itertools import product, combinations
from operator import mul


def dot_product(vec1, vec2):
    return sum(map(mul, vec1, vec2))


class Transformation:
    def __init__(self, tx, ty, tz):
        self.tx = tx
        self.ty = ty
        self.tz = tz

    def __call__(self, coord):
        c = (coord.x, coord.y, coord.z)
        return Coordinate(dot_product(c, self.tx),
                          dot_product(c, self.ty),
                          dot_product(c, self.tz))


class Axis(Enum):
    X = 0
    Y = 1
    Z = 2


class Transformations:
    identity = Transformation([1, 0, 0], [0, 1, 0], [0, 0, 1])

    rotate_x_90 = Transformation([1, 0, 0], [0, 0, -1], [0, 1, 0])  # rotate 90° on x axis: y=-z, z=y
    rotate_x_180 = Transformation([1, 0, 0], [0, -1, 0], [0, 0, -1])  # rotate 180° on x axis: y=-y, z=-z
    rotate_x_270 = Transformation([1, 0, 0], [0, 0, 1], [0, -1, 0])  # rotate -90° on x axis: y=z, z=-y

    rotate_y_90 = Transformation([0, 0, -1], [0, 1, 0], [1, 0, 0])  # rotate 90° on y axis: x=-z, z=x
    rotate_y_180 = Transformation([-1, 0, 0], [0, 1, 0], [0, 0, -1])  # rotate 180° on y axis: x=-x, z=-z
    rotate_y_270 = Transformation([0, 0, 1], [0, 1, 0], [-1, 0, 0])  # rotate -90° on y axis: x=z, z=-x

    rotate_z_90 = Transformation([0, -1, 0], [1, 0, 0], [0, 0, 1])  # rotate 90° on z axis: x=-y, y=x
    rotate_z_180 = Transformation([-1, 0, 0], [0, -1, 0], [0, 0, 1])  # rotate 180° on z axis: x=-x, y=-y
    rotate_z_270 = Transformation([0, 1, 0], [-1, 0, 0], [0, 0, 1])  # rotate -90° on z axis: x=y, y=-x

    rotations = {Axis.X: [identity, rotate_x_90, rotate_x_180, rotate_x_270],
                 Axis.Y: [identity, rotate_y_90, rotate_y_180, rotate_y_270],
                 Axis.Z: [identity, rotate_z_90, rotate_z_180, rotate_z_270]}

    facing_x = identity
    facing_x_neg = rotate_y_180
    facing_y = rotate_z_270
    facing_y_neg = rotate_z_90
    facing_z = rotate_y_270
    facing_z_neg = rotate_y_90


@dataclass
class Coordinate:
    x: int
    y: int
    z: int

    def rotations24(self):
        """List all 24 rotations of the given coordinate"""
        """Inspired from https://stackoverflow.com/questions/33190042/how-to-calculate-all-24-rotations-of-3d-array"""

        def rotations4(coord, axe):
            for rotation in Transformations.rotations[axe]:
                yield rotation(coord)

        yield from rotations4(Transformations.facing_x(self), Axis.X)
        yield from rotations4(Transformations.facing_x_neg(self), Axis.X)

        yield from rotations4(Transformations.facing_y(self), Axis.Y)
        yield from rotations4(Transformations.facing_y_neg(self), Axis.Y)

        yield from rotations4(Transformations.facing_z(self), Axis.Z)
        yield from rotations4(Transformations.facing_z_neg(self), Axis.Z)

    @property
    def manhattan(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y, self.z + other.z)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __str__(self):
        return f'[{self.x},{self.y},{self.z}]'

    def __repr__(self):
        return str(self)


class Scanner:
    def __init__(self, scanner_id='', beacons=None):
        self.scanner_id = scanner_id
        self.position = Coordinate(0, 0, 0)
        if beacons is None:
            self.beacons = set()
        else:
            self.beacons = set(beacons)

    def add_beacon(self, beacon: Coordinate):
        self.beacons.add(beacon)

    def rotations24(self):
        for rotation_index, beacons in enumerate(zip(*list(list(beacon.rotations24()) for beacon in self.beacons))):
            yield Scanner(self.scanner_id + ' R' + str(rotation_index), beacons)

    def move(self, offset: Coordinate):
        beacons = [b + offset for b in self.beacons]
        s = Scanner(self.scanner_id + f' M({offset})', beacons)
        s.position = self.position + offset
        return s

    matching_beacons_criteria = 12

    def match(self, other):
        if len(self.beacons) == 0:
            return other

        for candidate in other.rotations24():
            for self_beacon, candidate_beacon in product(self.beacons, candidate.beacons):
                offset = self_beacon - candidate_beacon
                moved_candidate = candidate.move(offset)
                matching_beacons = self.beacons.intersection(moved_candidate.beacons)
                if len(matching_beacons) >= Scanner.matching_beacons_criteria:
                    return moved_candidate
        return None

    def __str__(self):
        return f'Scanner {self.scanner_id} ({len(self.beacons)})'

    def __repr__(self):
        return str(self)


class ScannerMap:
    def __init__(self):
        self.scanners = []

    @property
    def beacons(self):
        s = set()
        s.update(*[scanner.beacons for scanner in self.scanners])
        return s

    @property
    def extension(self):
        distances = [(p1 - p2).manhattan for p1, p2 in combinations(list(s.position for s in self.scanners), 2)]
        return max(distances)

    def append_all(self, scanners):
        remaining_scanners = list(scanners)
        if len(self.scanners) == 0:
            self.scanners.append(remaining_scanners.pop(0))
            print(f'Matched {self.scanners[0]}, {len(remaining_scanners)} remaining')

        # match remaining ones against some that already in the map and are transformed to self coordinate system
        # (they are lighter than the big assembly which becomes bigger and bigger)
        # this is a proximity matching
        extension_happened = True
        while len(remaining_scanners) != 0 and extension_happened:
            extension_happened = False
            for scanner in list(remaining_scanners):
                for base in self.scanners:
                    match = base.match(scanner)
                    if match is not None:
                        remaining_scanners.remove(scanner)
                        self.scanners.append(match)
                        extension_happened = True
                        print(f'Matched {match} with {base}, {len(remaining_scanners)} remaining')
                        break


def main(filename, testing=False, expected1=None, expected2=None):
    scanners = []

    print(f'--------- {filename}')
    with open(filename) as f:
        for line in f.read().splitlines():
            if line.startswith('--- scanner'):
                scanner = Scanner(line.split()[2])
                scanners.append(scanner)
            elif len(line) > 0 and line[0] in '-0123456789':
                beacon = Coordinate(* [int(c) for c in line.split(',')])
                scanner.add_beacon(beacon)

    full_scan = ScannerMap()
    full_scan.append_all(scanners)
    beacons_count = len(full_scan.beacons)

    print(f'Part 1: number of beacons is {beacons_count}')
    if testing:
        assert beacons_count == expected1

    extension = full_scan.extension

    print(f'Part 2: ocean extension is {extension}')
    if testing:
        assert extension == expected2


if __name__ == '__main__':
    main('test.txt', True, 79, 3621)
    main('input.txt')
