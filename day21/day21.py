from collections import Counter
from dataclasses import dataclass
from functools import cache
from itertools import cycle, islice, product


class DeterministicDice:
    def __init__(self, max_value):
        self.max_value = max_value
        self.rolls = 0

    def roll(self, times=1):
        values = cycle(range(1, self.max_value+1))
        while True:
            self.rolls += times
            yield sum(islice(values, times))


@dataclass
class Player:
    player_id: str
    position: int
    score: int = 0

    def move(self, n, spaces):
        self.position = (self.position - 1 + n) % spaces + 1
        self.score += self.position


class Game:
    def __init__(self, players, spaces=10, win_score=1000, dice=DeterministicDice(100), dice_rolls=3):
        self.players = players
        self.spaces = spaces
        self.win_score = win_score
        self.dice = dice
        self.dice_rolls = dice_rolls

    def play(self):
        turn = cycle(self.players)
        dice_roll = self.dice.roll(self.dice_rolls)
        while True:
            player = next(turn)
            player.move(next(dice_roll), self.spaces)
            if self.is_winner(player):
                return next(turn).score * self.dice.rolls

    def is_winner(self, player):
        return player.score >= self.win_score


def dirac_play(players, win_score=21, spaces=10, dice_faces=(1, 2, 3), dice_rolls=3):
    # each turn, 3 dice rolls in [1, 2, 3] gives 27 position increments, but some are identical
    # rolls is a dict: move -> frequency
    rolls = Counter(sum(p) for p in product(dice_faces, repeat=dice_rolls))
    positions = [p.position - 1 for p in players]  # position in [0-9] for modulo
    scores = [p.score for p in players]

    @cache  # warning do not modify parameters in function otherwise cache is corrupted...
    def play_all_universes(position1, position2, score1, score2, turn):
        wins = int(score1 >= win_score), int(score2 >= win_score)  # 0 or 1 for each
        if any(wins):
            return wins  # recursion stops on win

        wins1, wins2 = 0, 0
        for roll, universes in rolls.items():  # explore all universes
            if turn == 1:
                p1, p2 = (position1 + roll) % spaces, position2
                s1, s2 = score1 + (p1 + 1), score2
                next_turn = 2  # can't reuse 'turn' here, won't cache correctly
            else:
                p1, p2 = position1, (position2 + roll) % spaces
                s1, s2 = score1, score2 + (p2 + 1)
                next_turn = 1

            w1, w2 = play_all_universes(p1, p2, s1, s2, next_turn)  # recursive_call call
            wins1 += w1 * universes
            wins2 += w2 * universes

        return wins1, wins2

    return play_all_universes(*positions, *scores, turn=1)


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')
    with open(filename) as f:
        data = [(player_id, int(start_position))
                for (_, player_id, _, _, start_position) in map(str.split, f.readlines())]

    players = [Player(player_id, position) for player_id, position in data]
    game = Game(players, spaces=10, win_score=1000, dice=DeterministicDice(100), dice_rolls=3)
    game_score = game.play()

    print(f'Part 1: game score is {game_score}')
    if testing:
        assert game_score == expected1

    players = [Player(player_id, position) for player_id, position in data]
    wins = dirac_play(players, win_score=21, spaces=10, dice_faces=(1, 2, 3), dice_rolls=3)

    print(f'Part 2: max universes won is {max(wins)}')
    if testing:
        assert max(wins) == expected2


if __name__ == '__main__':
    main('test.txt', True, 739785, 444356092776315)
    main('input.txt')
