#!/usr/bin/env python
import networkx as nx
import itertools as it

def part_1(rawdata):
    network = nx.Graph()
    network.add_edges_from(line.split("-") for line in rawdata.splitlines())
    
    def all_connected(n1, n2, n3):
        return network.has_edge(n1,n2) and network.has_edge(n1, n3) and network.has_edge(n2,n3)

    return sum(any(n.startswith("t") for n in nodes) and all_connected(*nodes) for nodes in it.combinations(network.nodes,3))

def part_2(rawdata):
    network = nx.Graph()
    network.add_edges_from(line.split("-") for line in rawdata.splitlines())
    return ",".join(sorted(max(nx.find_cliques(network), key=len)))

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
[(puzzle.examples[0].input_data, 7)])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
[(puzzle.examples[0].input_data, "co,de,ka,ta")])
def test_part_2(data, result):
    assert part_2(data) == result

if __name__ == "__main__":
    if (test_result := pytest.main([__file__])):
        sys.exit(test_result)

    part_1_done = bool(puzzle.answered_a)
    submit(part_1(puzzle.input_data), part="a", reopen=False)

    if part_1_done:
        # Don't try part 2 yet if we only finished part 1 just now
        submit(part_2(puzzle.input_data), part="b", reopen=False)
