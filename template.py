#!/usr/bin/env python

def part_1(rawdata):
    pass

def part_2(rawdata):
    pass

from aocd import puzzle
import pytest

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in aocd.puzzle.examples])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_b) for ex in aocd.puzzle.examples])
def test_part_2(data, result):
    assert part_2(data) == result

pytest.main([__file__])

puzzle.answer_a = part_1(puzzle.input_data)

if puzzle.answered_a:
    puzzle.answer_b = part_2(puzzle.input_data)

