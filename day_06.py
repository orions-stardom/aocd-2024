#!/usr/bin/env python
import itertools as it
from copy import deepcopy

class Loop(BaseException):
    pass

class Grid:
    def __init__(self, rawdata):
        data = rawdata.splitlines()
        self.width, self.height = len(data[0]), len(data)
        self.obstacles:set[complex] = set()

        # flip the y axis so we count up from the bottom
        for y, row in enumerate(data[::-1]):
            for x, char in enumerate(row):
                if char == "^":
                    self.guard_start = complex(x,y)
                if char == "#":
                    self.obstacles.add(complex(x,y))

    def __contains__(self, coord:complex):
        """
        True if the given coord is a valid coordinate in the grid, regardless of whether it is passable

        """
        return 0 <= coord.real < self.width and 0 <= coord.imag < self.height

    def steps_till_offgrid(self) -> set[complex]:
        seen_positions = set()
        seen_states = set()
        here = self.guard_start
        direction = 1j
        while True:
            if (here, direction) in seen_states:
                raise Loop
            seen_positions.add(here)
            seen_states.add((here, direction))

            test = here + direction
            if test not in self:
                return seen_positions
            if test in self.obstacles:
                direction = direction * -1j 
                continue

            here = test

    @property
    def has_loop(self):
        try:
            self.steps_till_offgrid()
        except Loop:
            return True
        else:
            return False

    @property
    def passable_coordinates(self):
        # return (c for c in map(complex, ) if c not in self.obstacles)
        for x, y in it.product(range(self.width), range(self.height)):
            c = complex(x,y)
            if c not in self.obstacles:
                yield c

    def with_extra_obstacle_at(self, coord):
        other = deepcopy(self)
        other.obstacles.add(coord)
        return other

def part_1(rawdata):
    grid = Grid(rawdata)
    return str(len(grid.steps_till_offgrid()))

def part_2(rawdata):
    grid = Grid(rawdata)
    # candidates = set(grid.passable_coordinates)
    candidates = grid.steps_till_offgrid()
    candidates.discard(grid.guard_start)
    return str(sum(grid.with_extra_obstacle_at(cand).has_loop for cand in candidates))

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
     [(puzzle.examples[0].input_data, "6")])
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
