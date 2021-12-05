# [Day 1: Sonar Sweep](https://adventofcode.com/2021/day/1)

All is about executing operations on a sliding window over a list.

Python 3.10 introduces `itertools.pairwise` to iterate pairs. 

In the documentation, it gives a pythonic implementation which I mimicked to code a first version.

In the recipes, there's a trick to get a `triplewise` iterator with two nested pairwise.

I studied a bit of generalization to n-wise iterators in [wise.py]

Thanks to @mdumke I renamed nb_increases to count_increases to get a verbal form. 'nb' stands for 'number'
and it is often ambiguous as it stands both for 'number of' (count) and for the type (a number)