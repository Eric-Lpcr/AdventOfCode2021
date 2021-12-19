from collections import deque
from copy import copy
from itertools import permutations
from operator import attrgetter


class SnailFishNumber:
    def __init__(self, content=None):
        """Content may be an int, a list of pairs, a list of two SnailFishNumbers"""
        if type(content) == list:
            self.value = None
            if type(content[0]) == SnailFishNumber:
                self.left = content[0]
            else:
                self.left = SnailFishNumber(content[0])
            if type(content[1]) == SnailFishNumber:
                self.right = content[1]
            else:
                self.right = SnailFishNumber(content[1])
        else:
            self.value = content
            self.left = None
            self.right = None

    @property
    def magnitude(self):
        if self.is_literal:
            return self.value
        else:
            return 3 * self.left.magnitude + 2 * self.right.magnitude

    @property
    def is_literal(self):
        return self.left is None and self.right is None

    @property
    def is_literal_pair(self):
        if self.is_literal:
            return False
        return self.left.is_literal and self.right.is_literal

    @classmethod
    def sum(cls, snail_fish_numbers):
        return sum(snail_fish_numbers, SnailFishNumber())

    # Neutral element for addition
    ZERO = None  # To be replaced by SnailFishNumber() after class definition

    def __add__(self, other):
        if self == SnailFishNumber.ZERO:
            return copy(other)
        s = SnailFishNumber([copy(self), copy(other)])
        # print(f'After addition: {s}')
        return s._reduce()

    def _reduce(self):
        explosion_level = 4
        split_level = 9

        while True:
            # Find a pair to explode
            post_order = self._post_order_traversal()
            index, to_explode, level = next(((i, sfn, lvl) for i, (sfn, lvl) in enumerate(post_order)
                                             if sfn.is_literal_pair and lvl >= explosion_level), (None, None, None))
            if to_explode is not None:
                previous_number = next((sfn for sfn, lvl in reversed(post_order[:index-2]) if sfn.is_literal), None)
                # index-2 because the two elements before to_explode are its own literals
                next_number = next((sfn for sfn, lvl in post_order[index + 1:] if sfn.is_literal), None)
                to_explode._explode(previous_number, next_number)
                # print(f'After explode: {self}')
                continue

            # Find a literal to split
            post_order = self._post_order_traversal()
            to_split = next((sfn for sfn, _ in post_order if sfn.is_literal and sfn.value > split_level), None)
            if to_split is not None:
                to_split._split()
                # print(f'After split: {self}')
            else:
                break

        return self

    def _explode(self, previous_number, next_number):
        if not self.is_literal_pair:
            return
        if previous_number:
            previous_number.value += self.left.value
        if next_number:
            next_number.value += self.right.value
        self.left = self.right = None
        self.value = 0

    def _split(self):
        if self.value <= 9:
            return
        self.left = SnailFishNumber(self.value // 2)
        self.right = SnailFishNumber((self.value + 1) // 2)
        self.value = None

    def _post_order_traversal(self, level=0):
        stack = list()
        if self.left:
            stack.extend(self.left._post_order_traversal(level + 1))
        if self.right:
            stack.extend(self.right._post_order_traversal(level + 1))
        stack.append((self, level))
        return stack

    def __eq__(self, other):
        if other is None:
            return False
        return self.value == other.value and self.left == other.left and self.right == other.right

    def __copy__(self):
        if self.is_literal:
            return SnailFishNumber(self.value)
        else:
            return SnailFishNumber([copy(self.left), copy(self.right)])

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        else:
            return f'[{str(self.left)},{str(self.right)}]'

    def __repr__(self):
        return str(self)


SnailFishNumber.ZERO = SnailFishNumber()


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')
    with open(filename) as f:
        numbers = [SnailFishNumber(eval(line)) for line in f.readlines()]

    s = SnailFishNumber.sum(numbers)
    print(f'Part 1: sum magnitude is {s.magnitude} (sum is {s})')
    if testing:
        assert s.magnitude == expected1

    sums = [a + b for a, b in permutations(numbers, 2)]
    max_sum = next(iter(reversed(sorted(sums, key=attrgetter('magnitude')))))

    print(f'Part 2: max magnitude of a sum is {max_sum.magnitude}')
    if testing:
        assert max_sum.magnitude == expected2


if __name__ == '__main__':
    main('test.txt', True, 4140, 3993)
    main('input.txt')
