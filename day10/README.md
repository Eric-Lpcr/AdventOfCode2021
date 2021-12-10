# [Day 10: Syntax Scoring](https://adventofcode.com/2021/day/10)

Working with an instruction stack for opening characters. 
When a closing char is encountered, it shall match the opening which is on top of the stack, otherwise it's an error.
If stack is not empty at the end of the line, then it's an incomplete line.

Autocompletion score is computed by unstacking (reverse iteration) the remaining openings and reducing their points 
with a lambda scoring function.

I used an enum to return the status for each line, besides its score.