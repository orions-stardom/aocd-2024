#!/usr/bin/env python
from dataclasses import dataclass
import itertools as it
import more_itertools as mit
from functools import total_ordering

@total_ordering
@dataclass
class File:
    file_id: int
    start_block: int
    size: int
    space_after: int

    @property
    def checksum(self):
        return sum(self.file_id * block for block in range(self.start_block, self.start_block+self.size))

    def shrink_by(self, amount):
        self.size -= amount
        self.space_after += amount

    def __lt__(self, other):
        return self.start_block < other.start_block

    def __eq__(self, other):
        return self.start_block == other.start_block

def parse(rawdata):
    files = [] 
    block = 0
    file_id = 0

    data = [int(x) for x in rawdata]
    if len(data) % 2:
        # the last entry must be a file with no space after
        data.append(0)

    for file_id, (filesize, freesize) in enumerate(it.batched(data,2)):
        files.append( File(file_id, block, filesize, freesize) )
        block += filesize + freesize
    return files

def part_1(rawdata):
    files = parse(rawdata)

    while mit.ilen(f for f in files if f.space_after) > 1:
        to_move = max(files) 
        after = min(f for f in files if f.space_after)

        new_start = after.start_block + after.size
        if after.space_after > to_move.size:
            to_move.start_block, to_move.space_after, after.space_after = new_start, \
                                                                          after.space_after - to_move.size, \
                                                                          0
        else:
            # split the file in two
            files.append(File(to_move.file_id, new_start, after.space_after, 0))
            to_move.shrink_by(after.space_after)
            after.space_after = 0

    return str(sum(f.checksum for f in files))

def part_2(rawdata):
    files = parse(rawdata)

    for to_move in reversed(files):
        try:
            after = min(f for f in files if f.start_block < to_move.start_block and f.space_after >= to_move.size)
        except ValueError:
            continue

        to_move.start_block = after.start_block + after.size
        to_move.space_after = after.space_after - to_move.size
        after.space_after = 0

    return str(sum(f.checksum for f in files))

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     # [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
    [(puzzle.examples[0].input_data, "2858")])
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
