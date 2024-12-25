#!/usr/bin/env python
import itertools as it

def part_1(rawdata):
    keys = []
    locks = []
    for diagram in rawdata.split("\n\n"):
        bidding = ["".join(col).count("#")-1 for col in zip(*diagram.splitlines())]
        if diagram.startswith("#"):
            locks.append(bidding)
        else:
            keys.append(bidding)

    return str(sum(not any(lp+kp > 5 for lp, kp in zip(lock,key)) for lock, key in it.product(locks, keys)))

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
def test_part_2(data, result):
    assert part_2(data) == result

if __name__ == "__main__":
    if (test_result := pytest.main([__file__])):
        sys.exit(test_result)

    submit(part_1(puzzle.input_data), part="a", reopen=False)

