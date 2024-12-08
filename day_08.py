#!/usr/bin/env python
from dataclasses import dataclass
import itertools as it
import math

@dataclass
class Grid:
    height: int
    width: int
    antennae: dict

    @classmethod
    def parse(cls, rawdata):
        data = rawdata.splitlines()
        height, width = len(data), len(data[0])
        antennae = {}

        for y, line in enumerate(data[::-1]):
            for x, char in enumerate(line):
                if char != ".":
                    antennae.setdefault(char, []).append(complex(x,y))

        return cls(height, width, antennae)

    def __contains__(self, coord):
        return 0 <= coord.real < self.width and 0 <= coord.imag < self.height

    def __iter__(self):
        return (complex(x,y) for x,y in it.product(range(self.width), range(self.height)))


def part_1(rawdata):
    grid = Grid.parse(rawdata)
    def antinodes():
        for locations in grid.antennae.values():
            for a,b in it.combinations(locations,2):
                # for each pair of antennae, we can find the two external 2:1
                # divisors using the Section formula https://en.wikipedia.org/wiki/Section_formula

                yield complex(2*a.real-b.real, 2*a.imag-b.imag)
                yield complex(2*b.real-a.real, 2*b.imag-a.imag)

    return str(len({a for a in antinodes() if a in grid}))

def part_2(rawdata):
    grid = Grid.parse(rawdata)

    antinodes = 0
    for c in grid:
        pairs = it.chain.from_iterable(it.combinations(l,2) for l in grid.antennae.values())

        for a,b in pairs:
            x1, y1 = b.real - a.real, b.imag - a.imag
            x2, y2 = c.real - a.real, c.imag - a.imag
            if math.isclose(abs(x1 * y2 - x2 * y1), 0):
                antinodes += 1
                break

    return str(antinodes)

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
    [(puzzle.examples[0].input_data, "34")])
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
