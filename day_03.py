#!/usr/bin/env python
import re

def part_1(rawdata):
    return str(sum(int(a)*int(b) for a,b in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", rawdata)))

def part_2(rawdata):
    do = True
    total = 0
    for instruction in re.findall(r"(?:mul\((\d{1,3}),(\d{1,3})\))|(do(?:n't)?)", rawdata):
        match instruction:
            case "", "", "do":
                do = True
            case "", "", "don't":
                do = False
            case a, b, "" if do:
                total += int(a)*int(b)
    return str(total)

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
    [("xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))", "161")] )
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_b) for ex in puzzle.examples] 
     [("xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))", "48")]
    )
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
