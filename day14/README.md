# [Day 14: Extended Polymerization](https://adventofcode.com/2021/day/14)

I thought about another `pairwise` iteration problem at first, and I finally chose to use `reduce`. 
The new polymer is built by taking one by one the elements and eventually insert a new one if last appended and next one
form a pair which reacts.
This algorithm maintains a string exact description of the polymer.

After 10 iterations, the test polymer grows from 4 to 3,073 elements. That seems quite exponential... And gulp it doesn't
work for 40 iterations. I was so proud of my oneline reduce!

In the same way as [Day 6: Lanternfish](https://adventofcode.com/2021/day/6) problem, the goal is not to elaborate the
exact description, but to count elements.

With a bit of generalization, I wrote a BigPolymer class which computes differently. Now I keep track of the occurrence 
count of each pair of element, and also of each element.
In a step, it becomes a question of examining each kind of pair and to split it if a reaction applies. In this case, 
all these pairs disappear (their kind count becomes 0) and it appears two pairs and an element, all in the same amount.
I store the new pairs in a container not to modify the pair counts which remain to be processed.

That works nice, the test polymer grows from 4 to 3,298,534,883,329 elements in 40 iterations: that's a 3 petabytes 
string!
