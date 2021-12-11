# [Day 11: Dumbo Octopus](https://adventofcode.com/2021/day/11)

Grid and neighborhood again.

I use `itertools.product` to have a single for loop to scan the grid, instead of nested i, j loops. 

Proximity triggered flashes are managed with recursive calls. 
The thing here is to carefully differentiate 
the octopus which were ready to flash in step (they were 10, and they may level up to more) 
from those that are triggered (they were 9, and they become 10 during a flash).

Part 2 was trivial as I was already counting the flashes during a step, I just need to check if it's the full grid size.

I don't use lists comprehensions during the step, the starting matrix evolves step by step. 
That's the reason why I need a `deepcopy` to reset the octopuses after part 1 (just in case the synchronized
flash would occur during the 100 part 1 steps).

Having almost all methods taking the same first parameter made me refactor the solution with a class. The code is
simpler, and this time I paid a special attention to the class interface by making all internals protected.
