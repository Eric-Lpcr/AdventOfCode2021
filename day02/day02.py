class Submarine:
    def __init__(self, h_pos=0, depth=0):
        self.h_pos = h_pos
        self.depth = depth

    def forward(self, units):
        self.h_pos += units

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
    def __init__(self, h_pos=0, depth=0, aim=0):
        Submarine.__init__(self, h_pos, depth)
        self.aim = aim

    def forward(self, units):
        self.h_pos += units
        self.depth += self.aim * units

    def down(self, units):
        self.aim += units

    def up(self, units):
        self.aim -= units


def main(filename):
    print(f'--------- {filename}')
    with open(filename) as f:
        commands = [(command, int(units)) for command, units in [line.split() for line in f.readlines()]]

    submarine = Submarine()
    submarine.navigate(commands)
    print(f"Part 1: position is {submarine.h_pos * submarine.depth}")

    submarine2 = Submarine2()
    submarine2.navigate(commands)
    print(f"Part 2: position is {submarine2.h_pos * submarine2.depth}")


if __name__ == '__main__':
    main('test.txt')
    main('input.txt')
