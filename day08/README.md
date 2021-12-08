# [Day 8: Seven Segment Search](https://adventofcode.com/2021/day/8)

Well, part 1 seems really so simple, part 2 may be terrible.

Definition data is the number of segments each digit needs. 
As this number of segments is also a criteria, I built a reverse dict.

Part 1 is just about counting outputs that are unambiguous, i.e. their number of segments corresponds to a single digit.
As a small trick I extract these segment counts and check outputs for their length beeing inside.

Part 2: "_After some careful analysis_" he says... No more help for matching patterns to digits!
Hum, ok. At least the unambiguous lengths seen before give 4 matches over 10: digits 1, 4, 7 and 8 are quickly identified.

It then remains two groups of three digits:
- a 5 segments group with digits 2, 3 and 5.
  - In this group, digit 3 is the only one having __all__ digit 1 segments lighted.
- a 6 segments group with digits 0, 6 and 9.
  - In this one, digit 6 is the only white __not__ having __all__ digit 1 segments lighted.

Still remains two groups of two digits:
- a 5 segments group with digits 2 and 5.
- a 6 segments group with digits 0 and 9.

Both (2, 5) and (0, 9) differ from the lower left segment. 
How to find its letter?

Let's superimpose 3 and 4, we got all segments lighted except the lower left one (like in digit 9 representation). 
The lower left segment is on in 6 or 8, let's remove from one or the other all segments from 3 and 4, and we'll got it. 
Just need to match it against remaining patterns and that's it, got all the key.

I started using lists comprehensions with an if statement like `[item in list if item in other_list]` to filter patterns,
and I finally did it with set operations: `-` (minus) or `issubset` are very expressive in this case.

I tried to clear the code by adding some constants for the digits: they don't mix anymore with lengths.