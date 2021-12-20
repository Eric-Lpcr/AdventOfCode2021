# [Day 20: Trench Map](https://adventofcode.com/2021/day/20)


A bit similar to [Day 9](https://adventofcode.com/2021/day/9), with a convolution.

I chose to change from classic iteration over neighbors extracted with coordinates, and I got a solution with combined 
triple-wise iterations over lines and columns as we wanted the full square.

The tricky part is about managing infinite space (Nobody's Chuck Norris...)
I chose to add a two cells thick empty border before starting the convolution.

Part 1 can be solved without taking care, because empty square always stay empty. But when part 2 comes, with its
algorithm(0) which flips from off to lit and algorithm(511) from lit to off, bordering needs to change its fill value
accordingly...

It seems to be the first time that the second part implies something which is not really present in the first part!
