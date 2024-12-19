#!/usr/bin/env python
import re
from functools import cache

def part_1(rawdata):
    available, _, *needed = rawdata.splitlines()
    available = available.split(", ")
    test = re.compile("(" + "|".join(f"({a})" for a in available) + ")+")
    return str(sum(test.fullmatch(need) is not None for need in needed))

def part_2(rawdata):
    available, _, *needed = rawdata.splitlines()
    available = available.split(", ")
    total = 0

    @cache
    def count_ways(design):
        if design == "":
            return 1

        return sum(count_ways(design.removeprefix(a)) for a in available if design.startswith(a))

    total = sum(count_ways(d) for d in needed)
    return str(total)


from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
[(puzzle.examples[0].input_data, "16")])
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
