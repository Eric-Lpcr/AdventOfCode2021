from operator import not_
from itertools import compress


LOST = -1  # beware that 0 can be a winning score if winning draw is 0 ball!


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
        except ValueError:
            pass
        return LOST

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
                score = board.match(draw)
                if score != LOST:
                    return score
        return LOST

    def play_to_loose(self, draws):
        self.clear()
        remaining_boards = list(self.boards)  # don't want to modify board set during game
        for draw in draws:
            for board in list(remaining_boards):  # need a copy of remaining boards because we may remove some
                score = board.match(draw)
                if score != LOST:
                    remaining_boards.remove(board)
                if len(remaining_boards) == 0:
                    return board.score(draw)
        return LOST


def main(filename):
    print(f'--------- {filename}')
    with open(filename) as f:
        blocks = f.read().split('\n\n')
        draws = [int(d) for d in blocks.pop(0).split(',')]
        boards = BoardSet(blocks)

    score1 = boards.play_to_win(draws)
    print(f'Part 1: score is {score1}')

    score2 = boards.play_to_loose(draws)
    print(f'Part 2: score is {score2}')


if __name__ == '__main__':
    main('test.txt')
    main('input.txt')
