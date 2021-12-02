import sys


class Submarine:
    def __init__(self, hpos=0, depth=0):
        self.hpos = hpos
        self.depth = depth

    def forward(self, units):
        self.hpos += units

    def down(self, units):
        self.depth += units

    def up(self, units):
        self.depth -= units

    def move(self, command, units):
        m = getattr(self, command)
        if m is not None:
            m(units)

    def navigate(self, commands):
        for command in commands:
            self.move(*command)


class Submarine2(Submarine):
    def __init__(self, hpos=0, depth=0, aim=0):
        Submarine.__init__(self, hpos, depth)
        self.aim = aim

    def forward(self, units):
        self.hpos += units
        self.depth += self.aim * units

    def down(self, units):
        self.aim += units

    def up(self, units):
        self.aim -= units


def main():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    with open(filename) as f:
        commands = [(command, int(units)) for command, units in [line.split() for line in f.readlines()]]

    submarine = Submarine()
    submarine.navigate(commands)
    print(f"Part 1: position is {submarine.hpos * submarine.depth}")

    submarine2 = Submarine2()
    submarine2.navigate(commands)
    print(f"Part 2: position is {submarine2.hpos * submarine2.depth}")


if __name__ == '__main__':
    main()
