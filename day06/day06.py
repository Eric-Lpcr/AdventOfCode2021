
def compute_lantern_fish_population(initial, days):
    new_cycle_start = 6
    fish_count = list(initial)
    for _ in range(days):
        youngsters = times_up = fish_count.pop(0)
        fish_count[new_cycle_start] += times_up
        fish_count.append(youngsters)
    return sum(fish_count)


def main(filename):
    print(f'--------- {filename}')
    with open(filename) as f:
        fishes = [int(s) for s in f.readline().split(',')]

    fish_count = [fishes.count(days_left) for days_left in range(9)]  # need to manage 0 to 8 days left population
    for days in [18, 80]:
        print(f'Part 1: after {days} days, count of fishes is {compute_lantern_fish_population(fish_count, days)}')
    days = 256
    print(f'Part 2: after {days} days, count of fishes is {compute_lantern_fish_population(fish_count, days)}')


if __name__ == '__main__':
    main('test.txt')
    main('input.txt')
