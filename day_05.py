#!/usr/bin/env python

from collections import defaultdict
from parse import parse

class Page:
    def __init__(self, page_no):
        self.page_no = page_no
        self.is_before = []
        self.is_after = []

    def __eq__(self, other):
        return self.page_no == other.page_no

    def __lt__(self, other):
        return other.page_no in self.is_before 
    
    def __gt__(self, other):
        return other.page_no in self.is_after

def parse_rules_and_updates(rawdata):
    rules_string, updates_string = rawdata.split("\n\n")
    rules = {} 
    for line in rules_string.splitlines():
        p1, p2 = parse("{:n}|{:n}", line)
        rules.setdefault(p1, Page(p1)).is_before.append(p2)
        rules.setdefault(p2, Page(p2)).is_after.append(p1)
    updates = [[int(p) for p in line.split(",")] for line in updates_string.splitlines()]
    return rules, updates

def is_in_order(update, rules):
    forbidden = set()
    for page in update:
        if page in forbidden:
            return False 
        forbidden.update(rules[page].is_after)
    return True

def part_1(rawdata):
    rules, updates = parse_rules_and_updates(rawdata)
    return str(sum(u[len(u) // 2] for u in updates if is_in_order(u, rules)))

def part_2(rawdata):
    rules, updates = parse_rules_and_updates(rawdata)
    to_fix = [update for update in updates if not is_in_order(update, rules)]
    fixed = [sorted(update, key=rules.get) for update in to_fix]
    return str(sum(u[len(u) // 2] for u in fixed))

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
    [(puzzle.examples[0].input_data, "123")])
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
