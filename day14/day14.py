from collections import defaultdict
from functools import reduce
from itertools import pairwise


class BasicPolymer:
    def polymerize(self, reactions):
        return self

    def polymerize_times(self, pairs, times):
        for _ in range(times):
            self.polymerize(pairs)
        return self

    @property
    def note(self):
        return 0


class Polymer(BasicPolymer):
    def __init__(self, elements):
        self.elements = elements

    def polymerize(self, reactions):
        self.elements = str(reduce(lambda e1, e2: e1 + reactions.get(e1[-1] + e2, '') + e2, self.elements))
        return self

    @property
    def note(self):
        counts = [self.elements.count(element) for element in set(self.elements)]
        return max(counts) - min(counts)

    def __len__(self):
        return len(self.elements)

    def __repr__(self):
        return str(self.elements)


class BigPolymer(BasicPolymer):
    def __init__(self, elements):
        self.element_count = defaultdict(int, {element: elements.count(element) for element in set(elements)})
        pairs = list(''.join(pair) for pair in pairwise(elements))
        self.pair_counts = defaultdict(int, {pair: pairs.count(pair) for pair in set(pairs)})

    def polymerize(self, reactions):
        new_pairs = defaultdict(int)
        for pair, pair_count in self.pair_counts.items():
            new_element = reactions.get(pair)
            if new_element is not None:
                new_pairs[pair[0] + new_element] += pair_count
                new_pairs[new_element + pair[1]] += pair_count
                self.element_count[new_element] += pair_count
            else:
                new_pairs[pair] = pair_count
        self.pair_counts = new_pairs
        return self

    @property
    def note(self):
        return max(self.element_count.values()) - min(self.element_count.values())

    def __len__(self):
        return sum(self.element_count.values())

    def __repr__(self):
        return str(dict(self.element_count))


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')
    with open(filename) as f:
        polymer_str = f.readline().strip()
        f.readline()
        reactions = dict([line.strip().split(' -> ', 2) for line in f.readlines()])

    polymer = Polymer(polymer_str).polymerize_times(reactions, 10)
    print(f'Part 1: polymer note is {polymer.note} (its length is {len(polymer)})')
    if testing:
        assert polymer.note == expected1

    polymer = BigPolymer(polymer_str).polymerize_times(reactions, 40)
    print(f'Part 2: polymer note is {polymer.note} (its length is {len(polymer)})')
    if testing:
        assert polymer.note == expected2


if __name__ == '__main__':
    main('test.txt', True, 1588, 2188189693529)
    main('input.txt')
