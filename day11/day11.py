from collections import deque
from copy import deepcopy
from itertools import product


class OctopusGrid:
    def __init__(self, levels, print_steps=False):
        self.flash_count = 0
        self.steps = 0

        self._levels = deepcopy(levels)
        self._lines, self._cols = len(self._levels), len(self._levels[0])
        self._print_steps = print_steps

    def step_times(self, times=1):
        for _ in range(times):
            self._step_once()

    def find_synchro(self):
        step_flash_count = 0
        while step_flash_count != self._lines * self._cols:
            step_flash_count = self._step_once()

    def _step_once(self):
        previous_flash_count = self.flash_count
        self.steps += 1
        wanna_flash = deque()
        for i, j in product(range(self._lines), range(self._cols)):
            self._levels[i][j] += 1
            if self._levels[i][j] > 9:
                wanna_flash.append((i, j))
        for i, j in wanna_flash:
            self._wanna_flash(i, j)

        if self._print_steps and (self.steps < 10 or self.steps % 10 == 0):
            print(f'After step {self.steps}:\n{self}\n')

        return self.flash_count - previous_flash_count

    def _wanna_flash(self, i, j):
        if self._levels[i][j] > 9:
            self._levels[i][j] = 0
            self.flash_count += 1
            for ni, nj in self._neighbors(i, j):
                if self._levels[ni][nj] == 0:  # just flashed in the current step
                    continue
                self._levels[ni][nj] += 1
                if self._levels[ni][nj] == 10:  # proximity triggered flash
                    self._wanna_flash(ni, nj)

    _neighborhood = set(product([-1, 0, 1], repeat=2)) - {(0, 0)}

    def _neighbors(self, i, j):
        return ((i + di, j + dj) for di, dj in OctopusGrid._neighborhood
                if 0 <= i + di < self._lines and 0 <= j + dj < self._cols)

    def __repr__(self):
        return '\n'.join(''.join(str(level) for level in line) for line in self._levels)


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')
    with open(filename) as f:
        levels = [[int(c) for c in line] for line in f.read().splitlines()]

    octopuses = OctopusGrid(levels, testing)
    octopuses.step_times(100)
    print(f'Part 1: number of flashes is {octopuses.flash_count}')
    if testing:
        assert(octopuses.flash_count == expected1)

    octopuses = OctopusGrid(levels)
    octopuses.find_synchro()
    print(f'Part 2: first synchro is at step {octopuses.steps}')
    if testing:
        assert(octopuses.steps == expected2)


if __name__ == '__main__':
    main('test.txt', True, 1656, 195)
    main('input.txt')
