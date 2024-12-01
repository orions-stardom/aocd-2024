#!/usr/bin/env python

def part_1(rawdata):
    pass

def part_2(rawdata):
    pass

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

pytest.main([__file__])

part_1_done = puzzle.answered_a
submit(part_1(puzzle.input_data), part="a", reopen=False)

if part_1_done:
    # Don't try part 2 yet if we only finished part 1 just now
    submit(part_2(puzzle.input_data), part="b", reopen=False)
