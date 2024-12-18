#!/usr/bin/env python
from collections import deque

def bfs(size, fallen):
    start, target = 0, complex(size, size) 

    q = deque([(start, 0)])
    visited = set()

    while q:
        here, steps = q.popleft()

        if here == target:
            return steps
        if here in visited:
            continue

        visited.add(here)

        for direction in 1,-1,1j,-1j:
            there = here+direction
            if not 0 <= there.real <= size or not 0 <= there.imag <= size:
                continue
            if there in fallen:
                continue

            q.append((there,steps+1))

def part_1(rawdata, size=70, nfallen=1024):
    fallen = {complex(int(x),int(y)) for x,y in (line.split(",") for line in rawdata.splitlines()[:nfallen])}
    return str(bfs(size, fallen))

def part_2(rawdata, size=70, already_tested=1024):
    to_fall = [complex(int(x),int(y)) for x,y in (line.split(",") for line in rawdata.splitlines())]
    for n in range(already_tested+1, len(to_fall)):
        fallen = set(to_fall[:n])
        if bfs(size, fallen) is None:
            breaker = to_fall[n-1]
            return f"{int(breaker.real)},{int(breaker.imag)}"

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
 #    [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
[(puzzle.examples[0].input_data, "22")])
def test_part_1(data, result):
    assert part_1(data, 6, 12) == result

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
[(puzzle.examples[0].input_data, "6,1")])
def test_part_2(data, result):
    assert part_2(data, 6, 12) == result

if __name__ == "__main__":
    if (test_result := pytest.main([__file__])):
        sys.exit(test_result)

    part_1_done = bool(puzzle.answered_a)
    submit(part_1(puzzle.input_data), part="a", reopen=False)

    if part_1_done:
        # Don't try part 2 yet if we only finished part 1 just now
        submit(part_2(puzzle.input_data), part="b", reopen=False)
