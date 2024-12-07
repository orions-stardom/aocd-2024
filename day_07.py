#!/usr/bin/env python
import operator
from dataclasses import dataclass

@dataclass
class Equation:
    ns: list[int]
    target: int

    @classmethod
    def parse(cls, line):
        parts = line.split(":")
        return cls(ns=[int(n) for n in parts[1].split()], target=int(parts[0]))

    def can_calculate(self, possible_ops):
        def _calculate(n1, n2, *ns):
            for op in possible_ops:
                n0 = op(n1, n2)
                if not ns:
                    yield n0
                else:
                    yield from _calculate(n0, *ns)
                
        return any(n == self.target for n in _calculate(*self.ns))

def part_1(rawdata):
    data = [Equation.parse(line) for line in rawdata.splitlines()]
    return str(sum(eq.target for eq in data if eq.can_calculate([operator.add, operator.mul]))) 

def part_2(rawdata):
    data = [Equation.parse(line) for line in rawdata.splitlines()]

    def digits(n):
        res = 0
        while n:
            res += 1
            n //= 10
        return res

    def cat(a,b):
        return a*(10**digits(b)) + b

    return str(sum(eq.target for eq in data if eq.can_calculate([operator.add, operator.mul, cat]))) 

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
    [(puzzle.examples[0].input_data, "11387")])
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
