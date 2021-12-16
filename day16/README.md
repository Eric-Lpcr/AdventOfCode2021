# [Day 16: Packet Decoder](https://adventofcode.com/2021/day/16)

Bit unpacking. There's nothing in the standard library to do that.

I wrote my solution backwards, first the packet decoder with all the protocol, calling a `get_int` method on a 
`BitStream` that I wrote later. For this one, I chose to maintain a two level input: the first in hexadecimal in which
I take digits to fill the second level after a conversion to binary, allowing the `get_int` method to return an integer
read from an arbitrary number of bits.

In part 1, I was already storing a tree of typed packets, and that proved to be very useful for part 2, 
as I just needed to add the packet value computation for operators.

Nothing really hard in this problem, just needed to read carefully the story.
