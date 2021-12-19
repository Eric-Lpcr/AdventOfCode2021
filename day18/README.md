# [Day 18: Snailfish](https://adventofcode.com/2021/day/18)

Strange numbers, looking like binary trees.

I built a `SnailFishNumber` class with a basic arithmetic to support addition and comparison.

`max()` works with `__gt__()` method overriden to be plugged on magnitude computation.

`sum()` works with `__add__()` method overriden to support juxtaposition and reduction.
As `sum()` default initial value is int 0, first addition triggered is (0 + a snail fish number), something that `ìnt`
`__add__` doesn't really like. Python addition is nicely implemented to try a reverse call to (a snail fish number + 0)
via the class `__radd__`.

Reduction algorithm is made over a pre-order traversal which sorts elements in a left to right manner which allows:
- easy looking for leftmost exploding pair or literal overvalue, 
- finding previous/next numbers to increment when a pair explodes.

Made a lot of tests for this challenge, got them apart in [test.py](test.py).
`