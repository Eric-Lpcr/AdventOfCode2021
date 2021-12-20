from itertools import pairwise, chain

# from itertools recipes (more_itertools)

def triple_wise(iterable):
    "Return overlapping triplets from an iterable"
    # triplewise('ABCDEFG') -> ABC BCD CDE DEF EFG
    for (a, _), (b, c) in pairwise(pairwise(iterable)):
        yield a, b, c


def flatten(list_of_lists):
    "Flatten one level of nesting"
    return chain.from_iterable(list_of_lists)


def decode(line):
    return line.replace('.', '0').replace('#', '1')


def add_borders(image, fill_value=None, thickness=1):
    w = len(image[0]) + 2 * thickness
    return [fill_value * w] * thickness + \
           [fill_value * thickness + line + fill_value * thickness for line in image] + \
           [fill_value * w] * thickness


def enhance(image, algorithm, times):
    enhanced_image = image
    borderlands = '0'
    for _ in range(times):
        extended_image = add_borders(enhanced_image, borderlands, 2)
        enhanced_image = []
        for three_lines in triple_wise(extended_image):  # three lines sliding window
            enhanced_line = ''
            for square in zip(*list(triple_wise(line) for line in three_lines)):  # three columns sliding window
                square_code = int(''.join(flatten(square)), 2)
                enhanced_line += algorithm[square_code]
            enhanced_image.append(enhanced_line)

        # infinite space around image will change according to 0 or 511 code
        borderlands = algorithm[int(borderlands * 9, 2)]

    return enhanced_image


def print_image(image):
    image = [line.replace('0', '.').replace('1', '#') for line in image]
    print('\n'.join(image), '\n')


def count(image):
    return sum(line.count('1') for line in image)


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')
    with open(filename) as f:
        algorithm = decode(f.readline().strip())
        f.readline()
        image = [decode(line.strip()) for line in f.readlines()]

    enhanced_image = enhance(image, algorithm, 2)
    pixel_count = count(enhanced_image)

    print(f'Part 1: lit pixel count is {pixel_count}')
    if testing:
        print_image(enhanced_image)
        print()
        assert pixel_count == expected1

    enhanced_image = enhance(image, algorithm, 50)
    pixel_count = count(enhanced_image)

    print(f'Part 2: lit pixel count is {pixel_count}')
    if testing:
        print_image(enhanced_image)
        print()
        assert pixel_count == expected2


if __name__ == '__main__':
    main('test.txt', True, 35, 3351)
    main('input.txt')
