#!/usr/bin/env python
def parse(rawdata):
    left, right = [],[]
    for line in rawdata.splitlines():
        l,r = line.split()
        left.append(int(l))
        right.append(int(r))
    return left, right

def part_1(rawdata):
    left, right = parse(rawdata)
    left.sort()
    right.sort()
    return str(sum(abs(l-r) for l,r in zip(left,right)))

def part_2(rawdata):
    left, right = parse(rawdata)
    return str(sum(n*right.count(n) for n in left))

from aocd import puzzle, submit
import pytest

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
def test_part_2(data, result):
    # aoce is incorrectly parsing this example
    if result == '9':
        result = '31'
    assert part_2(data) == result

pytest.main([__file__])

submit(part_1(puzzle.input_data), part="a", reopen=False)
submit(part_2(puzzle.input_data), part="b", reopen=False)
