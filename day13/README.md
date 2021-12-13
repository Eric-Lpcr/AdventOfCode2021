# [Day 13: Transparent Origami](https://adventofcode.com/2021/day/13)

Folding is axial symmetry.

Here I use a `Set` as a sparse matrix of dots. Paper is not bounded, so I need to compute width and height prior
to print. I like the `itemgetter` operator to map tuples to a single coordinate. A pity that it doesn't support
namedtuple named fields... 

Who did implement a pattern recognition to read the final message?
