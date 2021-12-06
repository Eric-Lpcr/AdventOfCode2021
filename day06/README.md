# [Day 6: Lanternfish](https://adventofcode.com/2021/day/6)

Hum, exponential in the challenge story means brute force will not work for part 2!

Clue is that we don't need to keep the individuals, these are lantern fishes after all... We just need to compute the 
total population after some days of continuous procreation, and we need to keep state of days countdown before babies 
plop!

A simple 9 items array will do the job. Each iteration moves the counts in the previous cell (those which were in 2
goes to 1). Special case for zeroes: they increase the sixths population and give birth to a brand-new generation 
of eights.

No library, no object, 4 lines of computation and everything else is decorum.