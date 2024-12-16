#!/usr/bin/env python
import itertools as it
import networkx as nx

def parse(rawdata):
    grid = {}
    for y, line in enumerate(rawdata.splitlines()):
        for x, char in enumerate(line):
            if char == "#":
                continue
            grid[complex(x,y)] = char

    graph = nx.DiGraph()
    for here in grid:
        if grid[here] == "S":
            graph.add_edge("start", (here, 1), weight=0)

        for facing in 1,-1,1j,-1j:
            if grid[here] == "E":
                graph.add_weighted_edges_from(((here, facing), "end", 0) for facing in (1j,-1j,1,-1))

            graph.add_edge((here,facing), (here,facing*-1j), weight=1000)
            graph.add_edge((here,facing), (here,facing*1j), weight=1000)
            
            there = here+facing
            if there not in grid:
                continue

            graph.add_edge((here,facing), (there,facing), weight=1)
    
    return graph

def part_1(rawdata):
    graph = parse(rawdata)
    return nx.shortest_path_length(graph, "start", "end", weight="weight")

def part_2(rawdata):
    graph = parse(rawdata)
    nodes = set(it.chain.from_iterable(nx.all_shortest_paths(graph, "start", "end", weight="weight")))
    nodes.discard("start")
    nodes.discard("end")
    positions = {p for p,d in nodes}
    return len(positions)

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
[
("""\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############""", 7036),

("""\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################""", 11048)

])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
[
("""\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############""", 45),

("""\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################""", 64)

])
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
