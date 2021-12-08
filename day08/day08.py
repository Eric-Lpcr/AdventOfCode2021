from collections import defaultdict

ZERO, ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE = list(range(10))
digit_segment_count = {ZERO: 6, ONE: 2, TWO: 5, THREE: 5, FOUR: 4, FIVE: 5, SIX: 6, SEVEN: 3, EIGHT: 7, NINE: 6}

segment_count_digits = defaultdict(list)  # number of segments => digits having this size
[segment_count_digits[sc].append(digit) for digit, sc in digit_segment_count.items()]


def count_unambiguous_outputs(entries):
    unambiguous_segment_count = set(sc for sc, digits in segment_count_digits.items() if len(digits) == 1)
    result = sum(sum(len(output) in unambiguous_segment_count for output in outputs) for _, outputs in entries)
    return result


def sorted_chars(s):
    """Returns string with chars sorted"""
    return ''.join(sorted(s))


def decode_patterns(patterns):
    pattern_digit = dict()  # function result: gives digit as a string from ordered pattern string
    digit_pattern = dict()  # gives pattern char set from digit

    def learn(the_pattern, the_digit):
        if digit is not None:
            pattern_digit[sorted_chars(the_pattern)] = str(the_digit)
            digit_pattern[the_digit] = set(the_pattern)
            patterns.remove(the_pattern)

    # Solve unambiguous digits according to their number of segments
    unambiguous_digits = {sc: digits[0] for (sc, digits) in segment_count_digits.items() if len(digits) == 1}
    for pattern in list(patterns):
        segment_count = len(pattern)
        digit = unambiguous_digits.get(segment_count, None)
        learn(pattern, digit)

    # From 5 segments patterns (digits 2, 3, 5), only digit 3 has all digit 1 segments on
    # From 6 segments patterns (digits 0, 6, 9), only digit 6 doesn't have all digit 1 segments on
    for pattern in list(patterns):
        digit = None
        include_one = digit_pattern[ONE].issubset(set(pattern))
        segment_count = len(pattern)
        if segment_count == 5 and include_one:
            digit = THREE
        elif segment_count == 6 and not include_one:
            digit = SIX
        learn(pattern, digit)

    # Lower left segment is in digit 6 but not in 3 nor in 4
    #   (all 3 and 4 digits segments makes a 9 which is all except lower left)
    ll_segment = (digit_pattern[SIX] - digit_pattern[THREE] - digit_pattern[FOUR]).pop()

    # From 5 segments remaining patterns (digits 2 and 5), only digit 2 has upper right segment on
    # From 6 segments remaining patterns (digits 0 and 9), only 0 has lower left segment on
    for pattern in list(patterns):
        digit = None
        if len(pattern) == 5:
            digit = TWO if ll_segment in pattern else FIVE
        elif len(pattern) == 6:
            digit = ZERO if ll_segment in pattern else NINE
        learn(pattern, digit)

    if len(patterns) != 0:
        raise Exception('Some patterns have not been decoded')

    return pattern_digit


def solve_output(entry):
    patterns, outputs = entry
    entry_key = decode_patterns(patterns)
    entry_value = int(''.join([entry_key[sorted_chars(output)] for output in outputs]))
    return entry_value


def sum_up_outputs(entries):
    return sum(solve_output(entry) for entry in entries)


def main(filename):
    print(f'--------- {filename}')
    entries = list()
    with open(filename) as f:
        for line in f.readlines():
            patterns, outputs = line.split('|')
            entries.append((patterns.split(), outputs.split()))

    print(f'Part 1: unambiguous digits appearances are {count_unambiguous_outputs(entries)}')
    print(f'Part 2: sum of outputs is {sum_up_outputs(entries)}')


if __name__ == '__main__':
    main('test.txt')
    main('input.txt')
