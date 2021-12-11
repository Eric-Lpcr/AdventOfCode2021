from itertools import filterfalse


class Board:
    def __init__(self, text):
        self._cells = [int(value) for value in text.split()]  # split w/o args manages multiple standard separators
        self._n_cols = len(text.splitlines())
        self._n_lines = int(len(self._cells) / self._n_cols)
        self._line_match = [0] * self._n_lines
        self._col_match = [0] * self._n_cols

        self.bingo = False
        self.score = sum(self._cells)

    def clear(self):
        self._line_match = [0] * self._n_lines
        self._col_match = [0] * self._n_cols
        self.bingo = False
        self.score = sum(self._cells)

    def match(self, draw):
        if not self.bingo:
            try:
                index = self._cells.index(draw)
                self.score -= draw
                line = int(index / self._n_cols)
                col = index - line * self._n_cols
                self._line_match[line] += 1
                self._col_match[col] += 1
                if self._line_match[line] == self._n_cols or self._col_match[col] == self._n_lines:
                    self.bingo = True
                    self.score *= draw
            except ValueError:
                pass


class BoardSet:
    def __init__(self, text_blocks):
        self._boards = [Board(block) for block in text_blocks]

    def clear(self):
        for board in self._boards:
            board.clear()

    def play_to_win(self, draws):
        self.clear()
        for draw in draws:
            for board in self._boards:
                board.match(draw)
                if board.bingo:
                    return board.score
        return None

    def play_to_loose(self, draws):
        self.clear()
        remaining_boards = len(self._boards)
        for draw in draws:
            for board in filterfalse(lambda b: b.bingo, self._boards):
                board.match(draw)
                if board.bingo:
                    remaining_boards -= 1
                    if remaining_boards == 0:
                        return board.score
        return None


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
