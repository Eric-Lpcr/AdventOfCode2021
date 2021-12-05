# [Day 2: Dive!](https://adventofcode.com/2021/day/2)

Submarine state updating with commands.

Here I execute the method named after the command with a search in class vars by its name (`getattr`)

Part 2 is about changing the behavior of the submarine, and I chose to subclass the part 1 class and override the commands.