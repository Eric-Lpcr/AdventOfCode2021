# [Day 9: Smoke Basin](https://adventofcode.com/2021/day/9)

Ok, classic neighbor check on a matrix for part 1.

The trick here consists in adding borders (nines) to the map, and there's no more special case for border cells having less
neighbors than center ones.

I chose to keep chars in the matrix as they compare in the same way as numbers.

Part 2 : filling zones. I must admit I was bored to implement the algorithm on my own.
Google and Wikipedia were my friends: [Flood fill](https://en.wikipedia.org/wiki/Flood_fill)

I just needed to convert the lines from strings to lists of chars in order to set cell value. 
This is done implicitly when computing the base colored map and reducing everything but limits (nines) to zeroes
before filling.~~~~

Flood fill algorith is basic but not recursive, no need for optimization here. 

I later generalized the neighborhood definition.