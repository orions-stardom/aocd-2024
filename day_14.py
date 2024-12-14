#!/usr/bin/env python
from parse import parse
import itertools as it
import more_itertools as mit

def parse_robots(rawdata):
    for line in rawdata.splitlines():
        px,py, vx,vy = parse("p={:n},{:n} v={:n},{:n}", line)
        yield complex(px,py), complex(vx,vy)

def part_1(rawdata, width=101, height=103):
    q1, q2, q3, q4 = 0, 0, 0, 0
    for p,v in parse_robots(rawdata):
        final_x, final_y = (p.real+100*v.real)%width, (p.imag+100*v.imag)%height
        left, right, top, bottom = final_x < width//2, final_x > width//2, final_y < height//2, final_y > height//2
        if left and top:
            q1 += 1
        elif right and top:
            q2 += 1
        elif left and bottom:
            q3 += 1
        elif right and bottom:
            q4 += 1

    return str(q1*q2*q3*q4)
        
def part_2(rawdata):
    width=101
    height=103
    robots = list(parse_robots(rawdata))

    def update_robot(p,v):
        return complex(int((p.real+v.real)%width), int((p.imag+v.imag)%height)), v

    for second in it.count(start=1):
        robots = [update_robot(*r) for r in robots]
        if mit.all_unique(p for p,v in robots):
            return str(second)

from aocd import puzzle, submit
import pytest
import sys

# @pytest.mark.parametrize("data, result",
#      [(puzzle.examples[0].input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1():
    data = puzzle.examples[0].input_data
    result = "12"
    assert part_1(data, 11, 7) == result

if __name__ == "__main__":
    if (test_result := pytest.main([__file__])):
        sys.exit(test_result)

    part_1_done = bool(puzzle.answered_a)
    submit(part_1(puzzle.input_data), part="a", reopen=False)

    if part_1_done:
        # Don't try part 2 yet if we only finished part 1 just now
        submit(part_2(puzzle.input_data), part="b", reopen=False)
