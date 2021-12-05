# [Day 4: Giant Squid](https://adventofcode.com/2021/day/4)

Bingo board is a matrix for which I chose to store cells in a list and use a single index from line/column. This facilitates finding a number, retrieving unmarked cells to compute score.

Line and column checking is a matter of slicing with `[start:end:step]`.
Score computing is an `itertools.compress` sum with negated marks as a selector.

I was pretty satisfied to let unmodified most of the code when implementing part 2. I just added `Board.clear()` method, when I fell in the classic trap forgetting to clear the boards between the two games.

I also got stuck a bit with removing board during iteration on the list of boards in part 2. 
**I MUST REMEMBER** to always iterate over a copy when removing!

Finally, I added the `BoardSet` class to encapsulate the playing methods and a global set clearing.

And made another improved version after I viewed some other people solutions. I added `bingo` and score attributes on `Board`, allowing better implementation for `play_to_loose`
