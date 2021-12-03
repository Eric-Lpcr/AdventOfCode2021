# Day 3: Binary Diagnostic

I choose to solve it with binary computation.

Input data is stored as a simple integer list.

Bit extraction is a made with a mask computed as 1 shifted to desired bit position.

I used the itertools.compress function to extract reports according
to a bit (bool) selector.
