#!/usr/bin/env python
from dataclasses import dataclass, field
from collections import deque, Counter
import itertools as it
import more_itertools as mit


@dataclass
class Region:
    letter: str
    points: set[complex] = field(default_factory=set)

    @property
    def perimeter(self):
        return sum(c+d not in self.points for c in self.points for d in (1j,-1j,1,-1))

    @property
    def area(self):
        return len(self.points)

    @property
    def sides(self):
        # To count the sides, count the corners
        nsides = 0
        for x,y in it.product(*self.bounding_box):
            c = complex(x,y)
            dx, dy = 1, 1j
            innies = (c in self) + (c+dx in self) + (c+dy in self) + (c+dx+dy in self)
            if innies == 1:
                # ..
                # .x
                nsides += 1
            if innies == 2:
                # This is two corners:
                #   x.
                #   .x
                # and so is this:
                #   .x
                #   x.
                # but this isn't any:
                #    .x
                #    .x
                if c in self and c+dx+dy in self:
                    nsides += 2
                if c+dx in self and c+dy in self:
                    nsides += 2
            if innies == 3:
                # x.
                # xx
                nsides += 1
            if innies == 4:
                # never a corner
                pass
                    
        return nsides

    def __contains__(self, point):
        return point in self.points

    def __iter__(self):
        return iter(self.points)

    @property
    def bounding_box(self):
        xs = range(min(int(c.real) for c in self)-1, max(int(c.real) for c in self)+2)
        ys = range(min(int(c.imag) for c in self)-1, max(int(c.imag) for c in self)+2)
        return xs, ys

    def __str__(self):
        xs, ys = self.bounding_box
        return "\n".join("".join(self.letter if complex(x,y) in self else "." for x in xs) for y in ys)


def find_regions(rawdata: str) -> list[Region]:
    grid = {}
    for y, line in enumerate(rawdata.splitlines()):
        for x, char in enumerate(line):
            grid[complex(x, y)] = char

    regions = []
    while grid:
        q = deque([mit.first(grid)])
        regions.append(Region(grid[q[0]]))
        while q:
            here = q.popleft()
            if here in regions[-1].points:
                continue
            regions[-1].points.add(here)
            for direction in 1j,-1j,1,-1:
                there = here+direction
                if there not in grid:
                    continue
                if there in regions[-1].points:
                    continue
                if grid[here] != grid[there]:
                    continue
                q.append(there)

            del grid[here]
    return regions


def part_1(rawdata):
    regions = find_regions(rawdata)
    return str(sum(r.perimeter*r.area for r in regions))


def part_2(rawdata):
    regions = find_regions(rawdata)
    # breakpoint()
    return str(sum(r.sides*r.area for r in regions))

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
[("""RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""", "1930")])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
[
# ("""RRRRIICCFF
# RRRRIICCCF
# VVRRRCCFFF
# VVRCCCJFFF
# VVVVCJJCFE
# VVIVCCJJEE
# VVIIICJJEE
# MIIIIIJJEE
# MIIISIJEEE
# MMMISSJEEE""", "1206"),

# ("""OOOOO
# OXOXO
# OXXXO""", "160"),

("""\
BBBBB
BAAAB
BABAB
BAABB
BABAB
BAAAB
BBBBB""", "452") ])
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
