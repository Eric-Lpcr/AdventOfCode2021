from day18 import *


class S(SnailFishNumber):
    def _pre_order_traversal(self, level=0):
        stack = list()
        stack.append((self, level))
        if self.left:
            stack.extend(self.left._pre_order_traversal(level + 1))
        if self.right:
            stack.extend(self.right._pre_order_traversal(level + 1))
        return stack

    def _in_order_traversal(self, level=0):
        stack = list()
        if self.left:
            stack.extend(self.left._in_order_traversal(level + 1))
        stack.append((self, level))
        if self.right:
            stack.extend(self.right._in_order_traversal(level + 1))
        return stack


def test_reduce():
    assert S([[[[[9, 8], 1], 2], 3], 4])._reduce() == S([[[[0, 9], 2], 3], 4])
    assert S([7, [6, [5, [4, [3, 2]]]]])._reduce() == S([7, [6, [5, [7, 0]]]])
    assert S([[6, [5, [4, [3, 2]]]], 1])._reduce() == S([[6, [5, [7, 0]]], 3])
    assert S([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])._reduce() == S(
        [[3, [2, [8, 0]]], [9, [5, [7, 0]]]])


def test_addition():
    assert S([1, 2]) + S([[3, 4], 5]) == S([[1, 2], [[3, 4], 5]])
    assert S([[[[4, 3], 4], 4], [7, [[8, 4], 9]]]) + S([1, 1]) == S(
        [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]])

    numbers = [S([i, i]) for i in range(1, 7)]
    assert S.sum(numbers[:4]) == S([[[[1, 1], [2, 2]], [3, 3]], [4, 4]])
    assert S.sum(numbers[:5]) == S([[[[3, 0], [5, 3]], [4, 4]], [5, 5]])
    assert S.sum(numbers[:6]) == S([[[[5, 0], [7, 4]], [5, 5]], [6, 6]])

    s = S([[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]]) \
        + S([7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]])
    assert s == S([[[[4, 0], [5, 4]], [[7, 7], [6, 0]]], [[8, [7, 7]], [[7, 9], [5, 0]]]])
    s += S([[2, [[0, 8], [3, 4]]], [[[6, 7], 1], [7, [1, 6]]]])
    assert s == S([[[[6, 7], [6, 7]], [[7, 7], [0, 7]]], [[[8, 7], [7, 7]], [[8, 8], [8, 0]]]])
    s += S([[[[2, 4], 7], [6, [0, 5]]], [[[6, 8], [2, 8]], [[2, 1], [4, 5]]]])
    s += S([7, [5, [[3, 8], [1, 4]]]])
    s += S([[2, [2, 2]], [8, [8, 1]]])
    s += S([2, 9])
    s += S([1, [[[9, 3], 9], [[9, 0], [0, 7]]]])
    s += S([[[5, [7, 4]], 7], 1])
    s += S([[[[4, 2], 2], 6], [8, 7]])
    assert s == S([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]])


def test_magnitude():
    assert S([9, 1]).magnitude == 29
    assert S([1, 9]).magnitude == 21.
    assert S([[9, 1], [1, 9]]).magnitude == 129.
    assert S([[1, 2], [[3, 4], 5]]).magnitude == 143
    assert S([[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]).magnitude == 1384
    assert S([[[[1, 1], [2, 2]], [3, 3]], [4, 4]]).magnitude == 445
    assert S([[[[3, 0], [5, 3]], [4, 4]], [5, 5]]).magnitude == 791
    assert S([[[[5, 0], [7, 4]], [5, 5]], [6, 6]]).magnitude == 1137
    assert S([[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]).magnitude == 3488


if __name__ == '__main__':
    test_magnitude()
    test_reduce()
    test_addition()
