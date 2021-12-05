# [Day 3: Binary Diagnostic](https://adventofcode.com/2021/day/3)

I choose to solve it with binary computation.

Input data is stored as a simple integer list.

Bit extraction is made with a mask computed as 1 shifted to desired bit position.

I used the `itertools.compress` function to extract reports according
to a bit (bool) selector.

No need for log2 computation in order to get the number of bits in a number,
there's a builtin function on int for that: `bit_length`
