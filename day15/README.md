# [Day 15: Chiton](https://adventofcode.com/2021/day/15)

Oh no, graph again!
And shortest path on a weighted graph... That immediately recalled me Dijkstra study 20 years ago during my late 
university, with a professor asking us to unwind the algorithm manually and write down (yes, with a pen and a paper) 
all the steps.
I think I learned about the algorithm (it stayed in my mind), but I also get traumatized ;-(

And tonight I really don't enjoy implementing such a thing.

So for one time, I'll do it like a serious lazy developer in the internet era: let's find a nice solution made by
someone else. I'm a bit frustrated, but otherwise I won't succeed.

Better than Dijkstra when you know the exact destination is A* algorithm:
[Introduction to the A* Algorithm](https://www.redblobgames.com/pathfinding/a-star/introduction.html).

*I wrote the text upper even before coding anything about the problem, except an attempt to get a list of list which
can be indexed as a matrix like this `mat[1, 2]`. Have a look at my `ListOfList`.*

Ok, got an excellent code in [implementation.py](implementation.py) from 
[Implementation of A*](https://www.redblobgames.com/pathfinding/a-star/implementation.html#python), 
just filled the right structure `GridWithWeights` with risk levels as weights, and call the `a_star_search` method.
That worked so well, with fancy graphics!

Ok, easy part 1, not so proud of me but after all, reuse is also part of the job.

Part 2: I was afraid it could be terrible!

But finally, I just needed to subclass the `GridWithWeights` with a 
constructor which takes the risk level grid pattern as a weight, and the repetition factors. The real size is computed 
(it is only used for bounding, and it doesn't generate memory usage). 
The weight is set only for the pattern, and I overloaded the cost accessor for any coordinate to come back in the
pattern with modulo, compute the increase according to the tile coordinates, and reduce it in the 1 to 9 range.
And I finally generalized part 1 to be like a part 2 with a single tile (expand factor is 1).

And here it goes, so efficient. Again a very nice library for graph algorithms, easy to use, easy to specialize.

Graphs make me go to bed so late...