#!/usr/bin/env python
import itertools as it
import more_itertools as mit
from collections import Counter, defaultdict

def secrets(seed):
    secret = seed
    while True:
        yield secret
        secret = ((secret * 64)  ^ secret) % 16777216
        secret = ((secret //32)  ^ secret) % 16777216
        secret = ((secret * 2048)^ secret) % 16777216

def part_1(rawdata):
    buyers = [int(line) for line in rawdata.splitlines()]
    final = {n: mit.nth(secrets(n), 2000) for n in buyers}
    return sum(mit.nth(secrets(n), 2000) for n in buyers)

def part_2(rawdata):
    buyers = [int(line) for line in rawdata.splitlines()]
    # change_sequences = Counter()
    total_bananas = defaultdict(int) 
    for buyer in buyers:
        daily_secrets = it.islice(secrets(buyer), 2001)
        prices = [n%10 for n in daily_secrets]
        changes = [(b-a, b) for a,b in it.pairwise(prices)]

        seen_sequences = set()
        for sequence in mit.windowed(changes, 4):
            change_sequence = tuple(change[0] for change in sequence)
            result_price = sequence[-1][1]

            if change_sequence in seen_sequences:
                continue

            seen_sequences.add(change_sequence)
            total_bananas[change_sequence] += result_price

    return max(total_bananas.values())

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
[
("""\
1
10
100
2024""", 37327623)])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
[
("""\
1
2
3
2024""", 23)])
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
