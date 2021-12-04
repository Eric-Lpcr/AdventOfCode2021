# Day 4: Giant Squid

Bingo board is a matrix for which I chose to store cells in a list and use a single index from line/column. This facilitates finding a number, retrieving unmarked cells to compute score.

Line and column checking is a matter of slicing with \[start:end:step\].
Score computing is an itertools.compress sum with negated marks as a selector.

I was satisfied to let unmodified most of the code when implementing part 2. I just added Board.clear()
Classic trap was to forget clearing the boards between the two games.

I also got stuck a bit with removing element during iteration on the list of boards in play_to_loose.

I MUST REMEMBER to iterate over a copy when removing!

