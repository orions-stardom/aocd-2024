#!/usr/bin/env python

import numpy as np
import itertools as it

diagonals =[ 
    np.array([
        list("X..."),
        list(".M.."),
        list("..A."),
        list("...S"),
    ]),

    np.array([
        list("S..."),
        list(".A.."),
        list("..M."),
        list("...X"),
    ]),

    np.array([
        list("...X"),
        list("..M."),
        list(".A.."),
        list("S..."),
    ]),

    np.array([
        list("...S"),
        list("..A."),
        list(".M.."),
        list("X..."),
    ]),
]

def part_1(rawdata):
    data = np.array([list(line) for line in rawdata.splitlines()])
    count = 0

    for row in data:
        count += "".join(row).count("XMAS")
        count += "".join(row).count("SAMX")

    for col in data.T:
        count += "".join(col).count("XMAS")
        count += "".join(col).count("SAMX")

    for window in it.chain.from_iterable(np.lib.stride_tricks.sliding_window_view(data, (4,4))):
        count += sum(((window==diag)|(diag==".")).all() for diag in diagonals)

    return str(count)
    
crossmass = [
    np.array([
        list("M.M"),
        list(".A."),
        list("S.S"),
    ]),

    np.array([
        list("M.S"),
        list(".A."),
        list("M.S"),
    ]),
        
    np.array([
        list("S.M"),
        list(".A."),
        list("S.M"),
    ]),
    np.array([
        list("S.S"),
        list(".A."),
        list("M.M"),
    ]),
]

def part_2(rawdata):
    data = np.array([list(line) for line in rawdata.splitlines()])
    count = 0

    for window in it.chain.from_iterable(np.lib.stride_tricks.sliding_window_view(data, (3,3))):
        count += sum(((window==cross)|(cross==".")).all() for cross in crossmass)

    return str(count)
from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     #[(ex.input_data, ex.answer_a) for ex in puzzle.examples])
    [("""..X...
        .SAMX.
        .A..A.
        XMAS.S
        .X....""", "4"),
     ("""MMMSXXMASM
         MSAMXMSMSA
         AMXSXMAAMM
         MSAMASMSMX
         XMASAMXAMM
         XXAMMXXAMA
         SMSMSASXSS
         SAXAMASAAA
         MAMMMXMMMM
         MXMXAXMASX""", "18")])
def test_part_1(data, result):
    data = "\n".join(line.strip() for line in data.splitlines())
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
     [("""MMMSXXMASM
         MSAMXMSMSA
         AMXSXMAAMM
         MSAMASMSMX
         XMASAMXAMM
         XXAMMXXAMA
         SMSMSASXSS
         SAXAMASAAA
         MAMMMXMMMM
         MXMXAXMASX""", "9")])

def test_part_2(data, result):
    data = "\n".join(line.strip() for line in data.splitlines())
    assert part_2(data) == result

if __name__ == "__main__":
    if (test_result := pytest.main([__file__])):
        sys.exit(test_result)

    part_1_done = bool(puzzle.answered_a)
    submit(part_1(puzzle.input_data), part="a", reopen=False)

    if part_1_done:
        # Don't try part 2 yet if we only finished part 1 just now
        submit(part_2(puzzle.input_data), part="b", reopen=False)
