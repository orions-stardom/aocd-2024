#!/usr/bin/env python
from dataclasses import dataclass
import itertools as it
import more_itertools as mit

@dataclass
class Fragment:
    file_id: int|None
    start: int
    size: int

    @property
    def checksum(self):
        if self.is_free:
            return 0

        return sum(self.file_id * block for block in range(self.start, self.start+self.size))

    @property
    def is_free(self):
        return self.file_id is None

    def __str__(self):
        return ("." if self.is_free else str(self.file_id)) * self.size

class Filesystem:
    def __init__(self, rawdata):
        self.fragments = []
        block = 0
        
        ids = mit.interleave(it.count(), it.cycle([None]))
        for size, file_id  in zip(map(int,rawdata), ids):
            self.fragments.append( Fragment(file_id, block, size) )
            block += size 

    def __str__(self):
        return "".join(str(f) for f in sorted(self.fragments, key=lambda f: f.start))

    @property
    def files(self):
        return (f for f in self.fragments if not f.is_free and f.size > 0)

    def free_space(self, *, before, min_size=1):
        return (f for f in self.fragments if f.is_free and f.size >= min_size and f.start < before)

    @property
    def checksum(self):
        return sum(f.checksum for f in self.fragments)

def part_1(rawdata):
    fs = Filesystem(rawdata)

    for file in mit.always_reversible(fs.files):
        while file.size:
            try:
                target = mit.first(fs.free_space(before=file.start))
            except ValueError:
                break

            if target.size < file.size:
                target.file_id = file.file_id
                file.size -= target.size
            else:
                file.start, target.start, target.size = target.start,\
                                                        target.start+file.size,\
                                                        target.size - file.size

    return str(fs.checksum)

def part_2(rawdata):
    fs = Filesystem(rawdata)

    for file in mit.always_reversible(fs.files):
        try:
            target = mit.first(fs.free_space(before=file.start, min_size=file.size))
        except ValueError:
            continue

        file.start, target.start, target.size = target.start,\
                                                target.start+file.size,\
                                                target.size - file.size


    return str(fs.checksum)

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
