#!/usr/bin/env python
from collections import deque

class Topograph:
    def __init__(self, rawdata):
        self.map = {}
        self.trailheads = set()

        data = rawdata.splitlines()[::-1]
        self.height, self.width = len(data), len(data[0])
        for y, line in enumerate(data):
            for x, char in enumerate(line):
                height = int(char)
                point = complex(x,y)
                self.map[point] = height
                if not height:
                    self.trailheads.add(point)

    def reachable_peaks(self, trailhead):
        directions = [1j,-1j,1,-1]
        peaks_reached = set()
        visited = set()
        to_visit = deque([trailhead])
        while to_visit:
            here = to_visit.popleft()
            if here in visited or here in peaks_reached:
                continue
            if self.map[here] == 9:
                peaks_reached.add(here)
                continue

            for d in directions:
                there = here+d
                if there not in self.map:
                    continue
                if self.map[there] - self.map[here] == 1:
                    to_visit.append(there)

        return peaks_reached

    def all_trails(self, trailhead):
        directions = [1j,-1j,1,-1]
        found_trails = set()
        to_visit = deque([(trailhead,)])

        while to_visit:
            trail_so_far = to_visit.popleft()
            here = trail_so_far[-1]
            if self.map[here] == 9:
                found_trails.add(trail_so_far)

            for d in directions:
                there = here+d
                if there not in self.map:
                    continue
                if self.map[there] - self.map[here] == 1:
                    to_visit.append(trail_so_far + (there,))
        return found_trails

def part_1(rawdata):
    topo = Topograph(rawdata)
    return str(sum(len(topo.reachable_peaks(p)) for p in topo.trailheads))

def part_2(rawdata):
    topo = Topograph(rawdata)
    return str(sum(len(topo.all_trails(p)) for p in topo.trailheads))

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
[("""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""", "36")])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
[("""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""", "81")])
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
