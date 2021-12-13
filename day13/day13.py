from collections import namedtuple, deque

Dot = namedtuple('Dot', ['x', 'y'])
Folding = namedtuple('Folding', ['axis', 'value'])


class Paper:
    def __init__(self):
        self.dots = set()

    def mark(self, x, y):
        self.dots.add(Dot(x, y))

    @property
    def dot_count(self):
        return len(self.dots)

    def fold_along_x(self, x):
        folded = {dot for dot in self.dots if dot.x > x}
        new_dots = {Dot(2 * x - dot.x, dot.y) for dot in folded}
        self.dots -= folded
        self.dots.update(new_dots)

    def fold_along_y(self, y):
        folded = {dot for dot in self.dots if dot.y > y}
        new_dots = {Dot(dot.x, 2 * y - dot.y) for dot in folded}
        self.dots -= folded
        self.dots.update(new_dots)

    def fold_along(self, axis, value):
        if axis == 'x':
            self.fold_along_x(value)
        elif axis == 'y':
            self.fold_along_y(value)

    def __repr__(self):
        width = height = 0
        for dot in self.dots:
            width = max(width, dot.x)
            height = max(height, dot.y)
        s = ''
        for y in range(height + 1):
            for x in range(width + 1):
                s += '#' if Dot(x, y) in self.dots else ' '
            s += '\n'
        return s


def main(filename, testing=False, expected1=None):

    paper = Paper()
    folding_instructions = deque()

    print(f'--------- {filename}')
    with open(filename) as f:
        for line in f.read().splitlines():
            if line.startswith('fold along'):
                (axis, value) = line.split()[-1].split('=')
                folding_instructions.append(Folding(axis, int(value)))
            elif len(line) > 0:
                x, y = line.split(',')
                paper.mark(int(x), int(y))

    folding = folding_instructions.popleft()
    paper.fold_along(folding.axis, folding.value)

    print(f'Part 1: number of dots is {paper.dot_count}')
    if testing:
        assert paper.dot_count == expected1

    while len(folding_instructions) > 0:
        folding = folding_instructions.popleft()
        paper.fold_along(folding.axis, folding.value)

    print(f'Part 2: code is:\n{paper}\n')
    if testing:
        assert 'you should read the paper'


if __name__ == '__main__':
    main('test.txt', True, 17)
    main('input.txt')
