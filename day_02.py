#!/usr/bin/env python
import itertools as it

def parse(rawdata) -> list[list[int]]:
    return [[int(l) for l in line.split()] for line in rawdata.splitlines()]

def is_safe(report):
    differences = [a-b for a,b in it.pairwise(report)]
    increasing = all(-3 <= d < 0 for d in differences) 
    decreasing = all(0 < d <= 3 for d in differences)
    return increasing or decreasing

def part_1(rawdata):
    data = parse(rawdata)
    return str(sum(is_safe(report) for report in data))

def part_2(rawdata):
    data = parse(rawdata)
    return str(sum(is_safe(report) or any(is_safe(damped) for damped in it.combinations(report, len(report)-1)) for report in data))

from aocd import puzzle, submit
import pytest

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
def test_part_2(data, result):
    assert part_2(data) == result

if __name__ == "__main__":
    pytest.main([__file__])

    part_1_done = bool(puzzle.answered_a)
    submit(part_1(puzzle.input_data), part="a", reopen=False)

    if part_1_done:
        # Don't try part 2 yet if we only finished part 1 just now
        submit(part_2(puzzle.input_data), part="b", reopen=False)
