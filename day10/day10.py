from collections import deque
from functools import reduce
from statistics import median
from enum import Enum

syntax = [('(', ')', 3, 1),
          ('[', ']', 57, 2),
          ('{', '}', 1197, 3),
          ('<', '>', 25137, 4)]

openings = {opening: closing for opening, closing, _, _ in syntax}
error_points = {closing: points for _, closing, points, _ in syntax}
autocomplete_points = {opening: points for opening, _, _, points in syntax}


class LineStatus(Enum):
    CORRUPTED = 0
    CORRECT = 1
    INCOMPLETE = -1


def check_line(line):
    """Returns status and corresponding score"""
    stack = deque()
    for current in line:
        if current in openings:
            stack.append(current)
        else:
            try:
                previous = stack.pop()
            except IndexError:  # whenever first instruction is a closing one, stack is still empty
                previous = None
            if openings.get(previous, None) != current:
                return LineStatus.CORRUPTED, error_points[current]
    if len(stack) == 0:
        return LineStatus.CORRECT, 0
    else:
        return (LineStatus.INCOMPLETE,
                reduce(lambda score, remaining: score * 5 + autocomplete_points[remaining], reversed(stack), 0))


def check_code(code):
    scores = [check_line(line) for line in code]
    return (sum(score for status, score in scores if status == LineStatus.CORRUPTED),
            median(score for status, score in scores if status == LineStatus.INCOMPLETE))


def main(filename):
    print(f'--------- {filename}')
    with open(filename) as f:
        code = f.read().splitlines()

    error_score, autocomplete_score = check_code(code)
    print(f'Part 1: syntax error detection score is {error_score}')
    print(f'Part 2: autocomplete score is {autocomplete_score}')


if __name__ == '__main__':
    main('test.txt')
    main('input.txt')
