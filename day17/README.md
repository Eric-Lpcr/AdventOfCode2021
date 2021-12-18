# [Day 17: Trick Shot](https://adventofcode.com/2021/day/17)

Ballistics... logic and mathematics.

Part 1 asks for logic and is so simple once found.
The probe shall go up until its speed decreases to 0, it then goes down and accelerates to reach same speed but negative
at y=0 (parabolic). Next speed is 1 higher and should not go lower than the target area bottom.

Part2: I didn't want to use full brute force, and I computed at least ranges of possible speeds both vertical and 
horizontal.


