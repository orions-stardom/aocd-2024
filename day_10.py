#!/usr/bin/env python
from collections import deque, Counter

def count_trails(rawdata):
    grid = {}
    to_visit = deque([])

    data = rawdata.splitlines()[::-1]
    height, width = len(data), len(data[0])
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            point = complex(x,y)
            grid[point] = height = int(char)
            if not height:
                to_visit.append((point,point))

    trails = Counter()
    while to_visit:
        head, here = to_visit.popleft()
        if grid[here] == 9:
            trails[(head, here)] += 1

        for d in [1j,-1j,1,-1]:
            there = here+d
            if there not in grid:
                continue
            if grid[there] - grid[here] == 1:
                to_visit.append((head,there))

    return trails

def part_1(rawdata):
    return str(len(count_trails(rawdata)))

def part_2(rawdata):
    return str(count_trails(rawdata).total())

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
[("""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""", "36")])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
[("""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""", "81")])
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
