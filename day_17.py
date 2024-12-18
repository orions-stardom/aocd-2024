#!/usr/bin/env python

def parse(rawdata):
    a,b,c,_,programdata = rawdata.splitlines()
    A = int(a.removeprefix("Register A: "))
    B = int(b.removeprefix("Register B: "))
    C = int(c.removeprefix("Register C: "))
    program = [int(x) for x in programdata.removeprefix("Program: ").split(",")]
    return program, A, B, C

def run_program(program, A, B, C):
    output = []
    instruction = 0
    while instruction < len(program):
        opcode, operand = program[instruction],program[instruction+1]
        combo = [0, 1, 2, 3, A, B, C]

        match opcode:
            case 0: # adv
                A = int(A / 2**combo[operand])
            case 1: # bxl
                B ^= operand
            case 2: # bst
                B = combo[operand] % 8
            case 3 if A: # jnz
                instruction = operand
                continue
            case 4: # bxc
                B ^= C
            case 5: # out
                output.append(combo[operand] % 8)
            case 6: # bdv
                B = int(A / 2**combo[operand])
            case 7: # cdv
                C = int(A / 2**combo[operand])

        instruction += 2

    return ",".join(str(x) for x in output)

def part_1(rawdata):
    return run_program(*parse(rawdata)) 

def part_2(rawdata):
    program, _, _, _ = parse(rawdata)
    # The program is a single loop that succesively divides the input number by 8,
    # and outputting one octal digit per iteration that depends on the current
    # quotient and remainder, stopping when the register value gets to 0. So the 
    # last output digit must depend only on the LSD of the input (leaving behind a 0 quotient).
    # So we can solve for that, and iteratively use that to solve for the next-least significant, etc
    check = [(len(program)-1, 0)]
    for position, solution_so_far in check:
        for candidate in range(8):
            need = ",".join(str(c) for c in program[position:])
            got = run_program(program, solution_so_far*8 + candidate, 0, 0)
            if need == got:
                if position == 0:
                    return candidate

                check.append((position-1, candidate))
        

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_a) for ex in puzzle.examples])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result",
     [(ex.input_data, ex.answer_b) for ex in puzzle.examples])
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
