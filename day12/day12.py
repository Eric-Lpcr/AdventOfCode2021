from collections import defaultdict


class Graph:
    def __init__(self):
        self._graph_dict = defaultdict(list)

    def add_edge(self, from_vertex, to_vertex):
        self._graph_dict[from_vertex].append(to_vertex)
        self._graph_dict[to_vertex].append(from_vertex)

    def find_all_paths(self, from_vertex, to_vertex, accept_vertex_fn, path=[]):
        """ Find all paths in graph,
        accept_vertex_fn takes vertex and path and should return whether vertex can be appended to path"""
        if from_vertex not in self._graph_dict:
            return []
        path.append(from_vertex)
        if from_vertex == to_vertex:
            return [path]
        paths = []
        for vertex in self._graph_dict[from_vertex]:
            if accept_vertex_fn(vertex, path):
                extended_paths = self.find_all_paths(vertex, to_vertex, accept_vertex_fn, path)
                for p in extended_paths:
                    paths.append(p)
        return paths


def accept_vertex_part1(vertex, path):
    return vertex.isupper() or vertex not in path


def accept_vertex_part2(vertex, path):
    if vertex.isupper() or vertex not in path:
        return True
    else:
        if vertex == 'start':
            return False
        lowercase_vertices = list(filter(str.islower, path))
        return len(lowercase_vertices) == len(set(lowercase_vertices))  # True if no double yet in path


def main(filename, testing=False, expected1=None, expected2=None):
    print(f'--------- {filename}')
    graph = Graph()
    with open(filename) as f:
        for line in f.read().splitlines():
            graph.add_edge(*line.split('-'))

    paths = graph.find_all_paths('start', 'end', accept_vertex_part1)
    print(f'Part 1: number of paths is {len(paths)}')
    if testing:
        assert(len(paths) == expected1)

    paths = graph.find_all_paths('start', 'end', accept_vertex_part2)
    print(f'Part 2: number of paths is {len(paths)}')
    if testing:
        assert(len(paths) == expected2)


if __name__ == '__main__':
    main('test1.txt', True, 10, 36)
    main('test2.txt', True, 19, 103)
    main('test3.txt', True, 226, 3509)
    main('input.txt')
