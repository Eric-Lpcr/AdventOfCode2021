from copy import copy
from itertools import permutations


class Node:
    def __init__(self):
        self.value = None
        self.left = None
        self.right = None

    @property
    def is_literal(self):
        return self.left is None and self.right is None

    @property
    def is_literal_pair(self):
        if self.is_literal:
            return False
        return self.left.is_literal and self.right.is_literal

    def pre_order_traversal(self, level=0):
        stack = list()
        stack.append((self, level))
        if self.left:
            stack.extend(self.left.pre_order_traversal(level + 1))
        if self.right:
            stack.extend(self.right.pre_order_traversal(level + 1))
        return stack

    def in_order_traversal(self, level=0):
        stack = list()
        if self.left:
            stack.extend(self.left.in_order_traversal(level + 1))
        stack.append((self, level))
        if self.right:
            stack.extend(self.right.in_order_traversal(level + 1))
        return stack

    def post_order_traversal(self, level=0):
        stack = list()
        if self.left:
            stack.extend(self.left.post_order_traversal(level + 1))
        if self.right:
            stack.extend(self.right.post_order_traversal(level + 1))
        stack.append((self, level))
        return stack

    def __eq__(self, other):
        if other is None:
            return False
        return self.value == other.value and self.left == other.left and self.right == other.right

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        else:
            return f'[{str(self.left)},{str(self.right)}]'

    def __repr__(self):
        return str(self)


class SnailFishNumber(Node):
    def __init__(self, content=None):
        """Argument must be an int, a string, a SnailFishNumber, or a list/tuple of two any of these"""
        super().__init__()

        if type(content) is str:
            content = eval(content)

        type_error = False

        if type(content) is int or content is None:
            self.value = content
            self.left = None
            self.right = None
        elif isinstance(content, SnailFishNumber) or issubclass(type(content), SnailFishNumber):
            self.value = content.value
            self.left = copy(content.left)
            self.right = copy(content.right)
        elif type(content) is list or type(content) is tuple:
            if len(content) != 2:
                type_error = True
            self.value = None
            self.left = SnailFishNumber(content[0])
            self.right = SnailFishNumber(content[1])
        else:
            type_error = True

        if type_error:
            raise TypeError(
                'SnailFishNumber() argument must be an int, a string, '
                + 'a SnailFishNumber, or a list/tuple of two any of these')

    @property
    def magnitude(self):
        if self.is_literal:
            return self.value
        else:
            return 3 * self.left.magnitude + 2 * self.right.magnitude

    # Neutral element for addition
    NONE = None  # To be replaced by SnailFishNumber() after class definition

    def __add__(self, other):
        if self == SnailFishNumber.NONE:
            return other
        if other == SnailFishNumber.NONE:
            return self
        s = SnailFishNumber([self, other])
        # print(f'After addition: {s}')
        return s._reduce()

    def __radd__(self, other):
        if type(other) == int and other == 0:  # to manage sum() default initial value int(0)
            return copy(self)
        else:
            return other.__add__(self)

    def __gt__(self, other):
        return self.magnitude > other.magnitude

    max_depth = 4
    max_literal_value = 9

    def _reduce(self):
        while True:
            # Find a pair to explode
            post_order = self.post_order_traversal()
            index, shall_explode, level = next(((i, sfn, lvl) for i, (sfn, lvl) in enumerate(post_order)
                                                if sfn.is_literal_pair and lvl >= SnailFishNumber.max_depth),
                                               (None, None, None))
            if shall_explode is not None:
                previous_number = next((sfn for sfn, lvl in reversed(post_order[:index-2]) if sfn.is_literal), None)
                # index-2 because the two elements before to_explode are its own literals
                next_number = next((sfn for sfn, lvl in post_order[index+1:] if sfn.is_literal), None)
                shall_explode.explode_pair(previous_number, next_number)
                # print(f'After explode: {self}')
                continue

            # Find a literal to split
            shall_split = next(
                (sfn for sfn, _ in post_order if sfn.is_literal and sfn.value > SnailFishNumber.max_literal_value),
                None)
            if shall_split is not None:
                shall_split.split_value()
                # print(f'After split: {self}')
            else:
                break

        return self

    def explode_pair(self, previous_number, next_number):
        if not self.is_literal_pair:
            return
        if previous_number:
            previous_number.value += self.left.value
        if next_number:
            next_number.value += self.right.value
        self.left = self.right = None
        self.value = 0

    def split_value(self):
        if self.value <= SnailFishNumber.max_literal_value:
            return
        self.left = SnailFishNumber(self.value // 2)
        self.right = SnailFishNumber((self.value + 1) // 2)
        self.value = None

    def __copy__(self):
        if self.is_literal:
            return SnailFishNumber(self.value)
        else:
            return SnailFishNumber([copy(self.left), copy(self.right)])


SnailFishNumber.NONE = SnailFishNumber()


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')
    with open(filename) as f:
        numbers = [SnailFishNumber(line) for line in f.readlines()]

    s = sum(numbers)
    print(f'Part 1: sum magnitude is {s.magnitude} (sum is {s})')
    if testing:
        assert s.magnitude == expected1

    max_sum = max(a + b for a, b in permutations(numbers, 2))
    print(f'Part 2: max magnitude of a pair sum is {max_sum.magnitude}')
    if testing:
        assert max_sum.magnitude == expected2


if __name__ == '__main__':
    main('test.txt', True, 4140, 3993)
    main('input.txt')
