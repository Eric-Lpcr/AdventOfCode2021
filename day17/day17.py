import re
from math import sqrt


class TargetArea:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min, self.x_max, self.y_min, self.y_max = x_min, x_max, y_min, y_max

    def __contains__(self, item):
        return self.x_min <= item[0] <= self.x_max and self.y_min <= item[1] <= self.y_max

    def __repr__(self):
        return f'target area: x={self.x_min}..{self.x_max}, y={self.y_min}..{self.y_max}'


def max_distance(speed):
    """Assuming speed is decreasing by one at each step, distance travelled whe speed is 0"""
    return int(speed * (speed + 1) / 2)  # sum of integers from speed to 0 <=> from 1 to speed = sum of n first integers



def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')
    with open(filename) as f:
        line = f.readline()
        match = re.match(r'target area:\s*x=(\-?\d+)\.\.(\-?\d+),\s*y=(\-?\d+)\.\.(\-?\d+)', line)
        target_area = TargetArea(*[int(m) for m in match.groups()])
    print(target_area)

    # maximal y speed to reach target
    # going up till speed is 0, going down and accelerating to same speed but negative at y=0 (parabolic)
    # next speed is 1 more and should not go lower than y_min
    vy_max = int(abs(target_area.y_min) - 1)
    y_top = int(vy_max * (vy_max + 1) / 2)  # sum(range(vy_max, 0, -1)) == sum of numbers from 1 to n == n(n+1)/2

    print(f'Part 1: highest y is {y_top} with initial y velocity {vy_max}')
    if testing:
        assert y_top == expected1

    # knowing speed, max reachable distance is sum(range(speed, 0, -1)) == sum of numbers from 1 to speed == n(n+1)/2
    # here we know the distance, and we want the speed to travel it
    # solution of (speed * (speed + 1) / 2 = distance
    # speed^2 + speed - 2 * distance = 0 second degree equation
    vx_min = int((-1 + sqrt(8 * target_area.x_min + 1)) / 2) + 1
    if not target_area.x_min <= max_distance(vx_min) <= target_area.x_max:
        raise Exception("No solution")  # in case vx_min steps over area

    vx_max = target_area.x_max  # go to farther x target position in a single step
    vy_min = target_area.y_min  # go to lowest y target position in a single step

    initial_velocities = []
    for vx in range(vx_min, vx_max + 1):  # [v_min, v_max] inclusive
        for vy in range(vy_min, vy_max + 1):  # [vy_min, vy_max] inclusive
            x = y = 0
            vvx, vvy = vx, vy
            searching = True
            while searching:
                x += vvx
                y += vvy
                if (x, y) in target_area:
                    initial_velocities.append((vx, vy))
                    searching = False
                if x > target_area.x_max or y < target_area.y_min:  # passed the area
                    searching = False
                vvx = max(0, vvx - 1)
                vvy -= 1

    print(f'Part 2: number of possible initial velocities is {len(initial_velocities)}')
    if testing:
        print(initial_velocities)
        assert len(initial_velocities) == expected2


if __name__ == '__main__':
    main('test.txt', True, 45, 112)
    main('input.txt')
