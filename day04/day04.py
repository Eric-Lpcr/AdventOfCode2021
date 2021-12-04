import sys
from operator import not_
from itertools import compress


class Board:
    def __init__(self, text):
        self.n_cols = len(text.splitlines())
        self.cells = [int(value) for value in text.split()]  # split w/o args manages multiple standard separators
        self.n_lines = int(len(self.cells) / self.n_cols)
        self.marked = [False] * len(self.cells)

    def clear(self):
        self.marked = [False] * len(self.cells)

    def match(self, number):
        try:
            index = self.cells.index(number)
            self.marked[index] = True
            line = int(index / self.n_cols)
            col = index - line * self.n_cols
            if self.check_line(line) or self.check_column(col):
                return self.score(number)
            else:
                return -1

        except ValueError:
            return -1

    def check_line(self, line):
        i = line * self.n_cols
        j = i + self.n_cols
        return sum(self.marked[i:j]) == self.n_cols

    def check_column(self, col):
        return sum(self.marked[col::self.n_cols]) == self.n_lines

    def score(self, last_draw):
        return sum(compress(self.cells, map(not_, self.marked))) * last_draw

    def __repr__(self):
        s = ''
        for line in range(self.n_lines):
            for col in range(self.n_cols):
                index = line * self.n_lines + col
                s += '{:2d}'.format(self.cells[index])
                if self.marked[index]:
                    s += '* '
                else:
                    s += '  '
            s += '\n'
        return s


def play_to_win(draws, boards):
    for draw in draws:
        for board in boards:
            score = board.match(draw)
            if score > 0:
                return score
    return -1


def play_to_loose(draws, boards):
    for draw in draws:
        for board in list(boards):  # need a copy of boards because we may remove some
            score = board.match(draw)
            if score > 0:
                boards.remove(board)
            if len(boards) == 0:
                return board.score(draw)
    return -1


def main():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    with open(filename) as f:
        blocks = f.read().split('\n\n')
        draws = [int(d) for d in blocks.pop(0).split(',')]
        boards = [Board(block) for block in blocks]

    score1 = play_to_win(draws, boards)
    print(f'Part 1: score is {score1}')

    for board in boards:
        board.clear()

    score2 = play_to_loose(draws, boards)
    print(f'Part 2: score is {score2}')


if __name__ == '__main__':
    main()
