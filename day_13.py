#!/usr/bin/env python
from parse import parse
from dataclasses import dataclass

import sympy

@dataclass
class ClawMachine:
    ax: int
    ay: int
    bx: int
    by: int

    prize_x: int
    prize_y: int

    @classmethod
    def parse(cls, rawdata: str):
        aline, bline, prizeline = rawdata.splitlines()
        ax, ay = parse("Button A: X+{:d}, Y+{:d}", aline)
        bx, by = parse("Button B: X+{:d}, Y+{:d}", bline)
        prize_x, prize_y = parse("Prize: X={:d}, Y={:d}", prizeline)

        return cls(ax, ay, bx, by, prize_x, prize_y)

    def solve(self):
        a,b = sympy.symbols("A B", integer=True)

        sols = sympy.solve([self.ax*a + self.bx*b - self.prize_x,
                            self.ay*a + self.by*b - self.prize_y],
                           [a, b]
                           )
        if not sols:
            # No solutions
            return 0

        return 3*sols[a]+sols[b]


def part_1(rawdata):
    return str(sum(ClawMachine.parse(m).solve() for m in rawdata.split("\n\n")))

def part_2(rawdata):
    machines = [ClawMachine.parse(m) for m in rawdata.split("\n\n")]
    for m in machines:
        m.prize_x += 10000000000000
        m.prize_y += 10000000000000

    return str(sum(m.solve() for m in machines))

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
[(puzzle.examples[0].input_data, "480")])
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
