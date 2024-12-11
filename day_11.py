#!/usr/bin/env python
from collections import Counter
from math import log10

def transform(stones):
    new_stones = Counter()
    for stone, count in stones.items():
        if stone == 0:
            new_stones[1] += count
        elif not (d := int(log10(stone) + 1)) % 2:
            a,b = divmod(stone,10**(d//2))
            new_stones[a] += count
            new_stones[b] += count
        else:
            new_stones[stone*2024] += count

    return new_stones

def part_1(rawdata):
    stones = Counter(int(s) for s in rawdata.split())
    naive_count = Counter()
    for _ in range(25):
        stones = transform(stones)

    return str(stones.total())

def part_2(rawdata):
    stones = Counter(int(s) for s in rawdata.split())
    naive_count = Counter()
    for _ in range(75):
        stones = transform(stones)

    return str(stones.total())
from aocd import puzzle, submit
import pytest
import sys


@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
    [("125 17", "55312")])
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
