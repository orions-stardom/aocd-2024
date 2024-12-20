#!/usr/bin/env python
import networkx as nx
from collections import Counter
import itertools as it

def parse(rawdata):
    grid = {}
    for y, line in enumerate(rawdata.splitlines()):
        for x, char in enumerate(line):
            grid[complex(x,y)] = char

    G = nx.Graph()
    for here, c in grid.items():
        if c == "#":
            continue
        if c == "S":
            G.graph["start"] = here 
        if c == "E":
            G.graph["end"] = here

        for d in 1j,-1j,1,-1:
            there = here+d
            if there in grid and grid[there] in ".E":
                G.add_edge(here, there)

    return G 

def manhatten(p1, p2):
    d = p1-p2
    return int(abs(d.real) + abs(d.imag))

def part_1(rawdata, critical_val=100):
    G = parse(rawdata)
    distance_from_start = dict(nx.single_source_shortest_path_length(G, G.graph["start"]))
    distance_to_end = dict(nx.single_target_shortest_path_length(G, G.graph["end"]))
    base_time = distance_to_end[G.graph["start"]]

    # cheat_times = {(cheat_start, cheat_end): distance_from_start[cheat_start] + distance_to_end[cheat_end] + manhatten(cheat_start,cheat_end) 
    #                for cheat_start, cheat_end in it.product(G.nodes, repeat=2) 
    #                if manhatten(cheat_start, cheat_end) == 2 }

    # savings = Counter(base_time-t for t in cheat_times.values() if t<base_time)
    # return sum(v for k,v in savings.items() if k >= critical_val)
    def time_saved(cheat_start, cheat_end):
        cheat_time = distance_from_start[cheat_start] + distance_to_end[cheat_end] + manhatten(cheat_start,cheat_end)
        return base_time - cheat_time
    return sum(time_saved(cheat_start,cheat_end) >= critical_val for cheat_start, cheat_end in it.product(G.nodes, repeat=2) if manhatten(cheat_start, cheat_end) == 2)

def part_2(rawdata, critical_val=100):
    G = parse(rawdata)
    distance_from_start = dict(nx.single_source_shortest_path_length(G, G.graph["start"]))
    distance_to_end = dict(nx.single_target_shortest_path_length(G, G.graph["end"]))
    base_time = distance_to_end[G.graph["start"]]
    def time_saved(cheat_start, cheat_end):
        cheat_time = distance_from_start[cheat_start] + distance_to_end[cheat_end] + manhatten(cheat_start,cheat_end)
        return base_time - cheat_time
    return sum(time_saved(cheat_start,cheat_end) >= critical_val for cheat_start, cheat_end in it.product(G.nodes, repeat=2) if manhatten(cheat_start, cheat_end) <= 20)

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
[(puzzle.examples[0].input_data, 5)])
def test_part_1(data, result):
    assert part_1(data, 20) == result

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
[(puzzle.examples[0].input_data, 12+22+4+3)])
def test_part_2(data, result):
    assert part_2(data, 70) == result

if __name__ == "__main__":
    if (test_result := pytest.main([__file__])):
        sys.exit(test_result)

    part_1_done = bool(puzzle.answered_a)
    submit(part_1(puzzle.input_data), part="a", reopen=False)

    if part_1_done:
        # Don't try part 2 yet if we only finished part 1 just now
        submit(part_2(puzzle.input_data), part="b", reopen=False)
