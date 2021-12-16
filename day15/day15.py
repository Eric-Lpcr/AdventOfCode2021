from functools import reduce
from implementation import *


class ListOfList(list):
    """This list allows indexing with a classic math syntax lol[1, 2]"""
    def __getitem__(self, item):
        if type(item) == tuple:
            return reduce(list.__getitem__, item, self)
        else:
            return list.__getitem__(self, item)

    def __setitem__(self, key, value):
        if type(key) == tuple:
            list.__setitem__(reduce(list.__getitem__, key[:-1], self), key[-1], value)
        else:
            list.__setitem__(self, key, value)

    def __repr__(self):
        return '\n'.join(''.join(f'{v:3d}' for v in line) for line in self)


class ExpandingGridWithWeights(SquareGrid):
    def __init__(self, weight_pattern, repeat_width=1, repeat_height=1):
        self.pattern_width = len(weight_pattern[0])
        self.pattern_height = len(weight_pattern)
        super().__init__(self.pattern_width * repeat_width, self.pattern_height * repeat_height)
        self.weights = weight_pattern

    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        x, y = to_node
        px = x % self.pattern_width
        py = y % self.pattern_height
        cost_increase = x // self.pattern_width + y // self.pattern_height
        cost = self.weights[py][px] + cost_increase
        cost = (cost - 1) % 9 + 1
        return cost


def shortest_path(risk_level, expand_grid_factor=1, testing=False):
    grid = ExpandingGridWithWeights(risk_level, expand_grid_factor, expand_grid_factor)
    start, goal = (0, 0), (grid.width-1, grid.height-1)

    came_from, cost_so_far = a_star_search(grid, start, goal)
    if testing:
        # draw_grid(grid, number=grid.weights, start=start, goal=goal)
        # print()
        draw_grid(grid, point_to=came_from, start=start, goal=goal)
        print()
        draw_grid(grid, path=reconstruct_path(came_from, start=start, goal=goal))
        # print()
        # draw_grid(grid, number=cost_so_far, start=start, goal=goal)

    return cost_so_far[goal]


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')
    with open(filename) as f:
        risk_level = [[int(c) for c in line] for line in f.read().splitlines()]

    shortest_path_risk = shortest_path(risk_level, testing=testing)
    print(f'Part 1: shortest path risk is {shortest_path_risk}')
    if testing:
        assert shortest_path_risk == expected1

    shortest_path_risk = shortest_path(risk_level, 5, testing=testing)
    print(f'Part 2: shortest path risk is {shortest_path_risk}')
    if testing:
        assert shortest_path_risk == expected2


if __name__ == '__main__':
    main('test.txt', True, 40, 315)
    main('input.txt')
