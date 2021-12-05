# Day 5: Hydrothermal Venture

I used a dict with namedtuple (x,y) points as a key and number of vent lines as a value.

Vent lines are created from edges by iterating over x and y coordinates simultaneously thanks to an inclusive_range implementation.
This function takes into account incrementing or decrementing.

Instead of nested x and y loops, I used a zip_longest iterator which gives directly points and works for diagonals.
I needed to set the fill_value with x or y for horizontal or vertical lines.

Finally, to compute the number of overlapping lines, I just count the dict values which are greater than 1.
Note that I sum up a generator (no need for a list).

I tried to find an alternative with map to extract the values over 1. I fingered out how to avoid the classical lambda function and fund functools.partial, which can be used with an operator function.
Tip: partial allows to fill partially a function parameters, but left ones first. x>1 shoud then be reverted to 1<x and lead to partial(lt, 1).
The code becomes hard to understand at first sight.