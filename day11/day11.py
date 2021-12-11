from copy import deepcopy
from itertools import product

grid_size = 10
neighborhood = set(product([-1, 0, 1], repeat=2)) - {(0, 0)}


def neighbors(i, j):
    return ((i + di, j + dj) for di, dj in neighborhood
            if 0 <= i + di < grid_size and 0 <= j + dj < grid_size)


def flash(octopuses, i, j):
    octopuses[i][j] = 0
    count_flashes = 1
    for ni, nj in neighbors(i, j):
        if octopuses[ni][nj] == 0:  # just flashed in this step
            continue
        octopuses[ni][nj] += 1
        if octopuses[ni][nj] == 10:  # proximity triggered flash
            count_flashes += flash(octopuses, ni, nj)
    return count_flashes


def step_once(octopuses):
    for i, j in product(range(grid_size), repeat=2):
        octopuses[i][j] += 1

    count_flashes = 0
    for i, j in product(range(grid_size), repeat=2):
        if octopuses[i][j] > 9:
            count_flashes += flash(octopuses, i, j)
    return count_flashes


def step_some(octopuses, n_steps):
    count_flashes = 0
    for step in range(n_steps):
        count_flashes += step_once(octopuses)
        # if step+1 < 10 or (step+1) % 10 == 0:
        #     print(f'\nAfter step {step+1}:')
        #     print('\n'.join(''.join(str(o) for o in line) for line in octopuses))
    return count_flashes


def find_synchro(octopuses):
    step = count_flashes = 0
    while count_flashes != grid_size * grid_size:
        count_flashes = step_once(octopuses)
        step += 1
    return step


def main(filename):
    print(f'--------- {filename}')
    with open(filename) as f:
        puzzle = [[int(c) for c in line] for line in f.read().splitlines()]

    octopuses = deepcopy(puzzle)
    print(f'Part 1: number of flashes is {step_some(octopuses, 100)}')
    octopuses = deepcopy(puzzle)
    print(f'Part 2: first synchro is at step {find_synchro(octopuses)}')


if __name__ == '__main__':
    main('test.txt')
    main('input.txt')
