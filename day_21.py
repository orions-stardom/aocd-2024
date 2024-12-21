#!/usr/bin/env python
import networkx as nx
import itertools as it
from functools import cache

numpad = nx.DiGraph()

for row in "0A", "123", "456", "789":
    numpad.add_edges_from(it.pairwise(row), direction=">") 
    numpad.add_edges_from(it.pairwise(row[::-1]), direction="<")

for column in "147", "0258", "A369":
    numpad.add_edges_from(it.pairwise(column), direction="^")
    numpad.add_edges_from(it.pairwise(column[::-1]), direction="v")

dpad = nx.DiGraph()
for row in "^A", "<v>":
    dpad.add_edges_from(it.pairwise(row), direction=">") 
    dpad.add_edges_from(it.pairwise(row[::-1]), direction="<")
for column in "v^", ">A":
    dpad.add_edges_from(it.pairwise(column), direction="^")
    dpad.add_edges_from(it.pairwise(column[::-1]), direction="v")

def path_as_directions(keypad, path):
    return (keypad.edges[edge]["direction"] for edge in it.pairwise(path))

@cache
def least_cost(s,d,robots):
    # number of keystrokes on one dpad to move a robot
    # from s to d on its own dpad
    if robots == 1:
        return nx.shortest_path_length(dpad, s, d) + 1

    # if there's more than one robot, then we need to think about 
    # all the paths
    possible_paths = [path_as_directions(dpad, path) for path in nx.all_shortest_paths(dpad, s, d)]
    costs = [sum(least_cost(a,b,robots-1) for a,b in it.pairwise(path)) for path in possible_paths]
    return min(costs)+1

@cache
def least_cost_numpad(s,d,robots):
    possible_paths = [path_as_directions(numpad, path) for path in nx.all_shortest_paths(numpad, s, d)]
    costs = [sum(least_cost(a,b,robots) for a,b in it.pairwise(path)) for path in possible_paths]
    return min(costs)

@cache
def best_indirect_path_length(from_key, to_key, layers_of_indirection):
    candidates = ["".join(numpad.edges[edge]["direction"] for edge in it.pairwise(path))+"A" for path in nx.all_shortest_paths(numpad, from_key, to_key) ]
    for _ in range(layers_of_indirection-1):
        next_indirect_candidates = []
        for candidate in candidates:
            parts = []
            for here,there in it.pairwise("A"+candidate):
                paths = list(nx.all_shortest_paths(dpad, here, there))
                indirect_codes  = ["".join(dpad.edges[edge]["direction"] for edge in it.pairwise(path))+"A" for path in paths ]
                parts.append(indirect_codes)

            new_candidates = parts[0]
            for part in parts[1:]:
                new_candidates = [a+b for a in new_candidates for b in part]

            next_indirect_candidates.extend(new_candidates)

        cutoff = min(len(c) for c in next_indirect_candidates)
        candidates = [c for c in next_indirect_candidates if len(c) == cutoff]
    return cutoff

def complexity(code, layers_of_indirection):
    # size = sum(best_indirect_path_length(a,b, layers_of_indirection) for a,b in it.pairwise("A"+code))
    size = sum(least_cost_numpad(a,b, layers_of_indirection) for a,b in it.pairwise("A"+code))
    return size * int(code[:-1])

def part_1(rawdata):
    return sum(complexity(code, 3) for code in rawdata.splitlines())

def part_2(rawdata):
    return sum(complexity(code, 26) for code in rawdata.splitlines())

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
[("""\
029A
980A
179A
456A
379A""", 126384)])
def test_part_1(data, result):
    assert part_1(data) == result

# @pytest.mark.parametrize("data, result",
#      [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
# def test_part_2(data, result):
#     assert part_2(data) == result

if __name__ == "__main__":
    if (test_result := pytest.main([__file__])):
        sys.exit(test_result)

    part_1_done = bool(puzzle.answered_a)
    submit(part_1(puzzle.input_data), part="a", reopen=False)

    if part_1_done:
        # Don't try part 2 yet if we only finished part 1 just now
        submit(part_2(puzzle.input_data), part="b", reopen=False)
