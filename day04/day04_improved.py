import sys
from operator import not_
from itertools import compress, filterfalse


class Board:
    def __init__(self, text):
        self.n_cols = len(text.splitlines())
        self.cells = [int(value) for value in text.split()]  # split w/o args manages multiple standard separators
        self.n_lines = int(len(self.cells) / self.n_cols)
        self.marked = [False] * len(self.cells)
        self.bingo = False
        self.score = None

    def clear(self):
        self.marked = [False] * len(self.cells)
        self.bingo = False
        self.score = None

    def match(self, draw):
        if not self.bingo:
            try:
                index = self.cells.index(draw)
                self.marked[index] = True
                line = int(index / self.n_cols)
                col = index - line * self.n_cols
                if self.check_line(line) or self.check_column(col):
                    self.bingo = True
                    self.score = sum(compress(self.cells, map(not_, self.marked))) * draw
            except ValueError:
                pass

    def check_line(self, line):
        i = line * self.n_cols
        j = i + self.n_cols
        return sum(self.marked[i:j]) == self.n_cols

    def check_column(self, col):
        return sum(self.marked[col::self.n_cols]) == self.n_lines

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


class BoardSet:
    def __init__(self, text_blocks):
        self.boards = [Board(block) for block in text_blocks]

    def clear(self):
        for board in self.boards:
            board.clear()

    def play_to_win(self, draws):
        self.clear()
        for draw in draws:
            for board in self.boards:
                board.match(draw)
                if board.bingo:
                    return board.score
        return None

    def play_to_loose(self, draws):
        self.clear()
        remaining_boards = len(self.boards)
        for draw in draws:
            for board in filterfalse(lambda b: b.bingo, self.boards):
                board.match(draw)
                if board.bingo:
                    remaining_boards -= 1
                    if remaining_boards == 0:
                        return board.score
        return None


def main():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    with open(filename) as f:
        blocks = f.read().split('\n\n')
        draws = [int(d) for d in blocks.pop(0).split(',')]
        boards = BoardSet(blocks)

    score1 = boards.play_to_win(draws)
    print(f'Part 1: score is {score1}')

    score2 = boards.play_to_loose(draws)
    print(f'Part 2: score is {score2}')


if __name__ == '__main__':
    main()
