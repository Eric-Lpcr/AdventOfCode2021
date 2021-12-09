from collections import deque
from itertools import islice
from math import prod


neighborhood = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def add_borders(heightmap):
    w = len(heightmap[0]) + 2
    return ['9' * w] + ['9' + line + '9' for line in heightmap] + ['9' * w]


def find_low_points(heightmap):
    low_points = list()
    h = len(heightmap)
    w = len(heightmap[0])
    for i in range(1, h-1):
        for j in range(1, w-1):
            if all(heightmap[i][j] < heightmap[i+di][j+dj] for di, dj in neighborhood):
                low_points.append((i, j))
    return low_points


def compute_risk_level(heightmap):
    return sum(int(heightmap[i][j]) + 1 for i, j in find_low_points(heightmap))


def flood_fill(heightmap, i, j):
    count_points = 0
    colored_map = [[ch if ch == '9' else '0' for ch in line] for line in heightmap]
    queue = deque([(i, j)])
    while len(queue) > 0:
        i, j = queue.pop()
        if colored_map[i][j] == '0':
            colored_map[i][j] = '1'
            count_points += 1
            queue.extend([(i+di, j+dj) for di, dj in neighborhood])
    return colored_map, count_points


def compute_basins(heightmap):
    low_points = find_low_points(heightmap)
    basins = list()
    for low_point in low_points:
        _, basin_size = flood_fill(heightmap, *low_point)
        basins.append(basin_size)
    return prod(islice(reversed(sorted(basins)), 3))


def main(filename):
    print(f'--------- {filename}')
    with open(filename) as f:
        heightmap = f.read().splitlines()
    heightmap = add_borders(heightmap)

    print(f'Part 1: total risk level is {compute_risk_level(heightmap)}')
    print(f'Part 2: product of the three largest basins sizes is {compute_basins(heightmap)}')


if __name__ == '__main__':
    main('test.txt')
    main('input.txt')
