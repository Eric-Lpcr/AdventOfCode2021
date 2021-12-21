from day19 import *


c = Coordinate(1, 2, 5)
assert c == c

b = Coordinate(0, 0, 0)
moved_b = b.move(1, 2, 5)
assert moved_b == Coordinate(1, 2, 5)

s = Scanner('test', [b, moved_b])
for x in range(10):
    print(s.move(x, x, x).beacons)



c_rot = list(c.rotations24())
assert len(c_rot) == len(set(c_rot)) == 24

c_rot_sub = set(Coordinate(c.x, c.y, c.z) for c in c_rot if c.x > 0)

assert Coordinate(1, 2, 5) in c_rot_sub

intersect = set(c_rot).intersection(c_rot_sub)
assert intersect == c_rot_sub

