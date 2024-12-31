#!/usr/bin/env python
import networkx as nx
import itertools as it

def complexity_calculator(robots):
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
        dpad_complete = nx.DiGraph()

    for d1,d2 in it.product(dpad,repeat=2):
        dpad_complete.add_edge(d1, d2, weight_1=nx.shortest_path_length(dpad, d1, d2) + 1)

    for n in range(2, robots+1):
        for d1,d2 in it.product(dpad,repeat=2):
            if d1==d2:
                dpad_complete[d1][d2][f"weight_{n}"] = 1
            else:
                dpad_complete[d1][d2][f"weight_{n}"] = min(nx.path_weight(dpad_complete,["A"]+p, weight=f"weight_{n-1}") for p in nx.all_shortest_paths(dpad, d1,d2))+1
    
    numpad_complete = nx.DiGraph()
    for n1, n2 in it.product(numpad, repeat=2):
        if n1 == n2:
            weight = 1
        else:
            # find the possible ways to get from here to there as dpad instructions
            possible_paths = [[numpad[a][b]["direction"] for a,b in it.pairwise(path)] for path in nx.all_shortest_paths(numpad, n1, n2)] 
            weight = min(nx.path_weight(dpad_complete, ["A"]+p, weight=f"weight_{robots}") for p in possible_paths)+1

        numpad_complete.add_edge(n1, n2, weight=weight)

    return lambda code: nx.path_weight(numpad_complete, f"A{code}", weight="weight") * int(code.removesuffix("A"))

def part_1(rawdata):
    complexity = complexity_calculator(3)
    return sum(complexity(code) for code in rawdata.splitlines())

def part_2(rawdata):
    complexity = complexity_calculator(26)
    return sum(complexity(code) for code in rawdata.splitlines())

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
