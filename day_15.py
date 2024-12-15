#!/usr/bin/env python
import itertools as it

def parse(rawdata):
    grid_data, moves = rawdata.split("\n\n")
    moves = moves.replace("\n", "")

    grid = {}
    robot = None 
    for y, line in enumerate(grid_data.splitlines()):
        for x, ch in enumerate(line):
            c = complex(x,y)
            if ch == "@":
                robot = c

            grid[c] = ch

    return grid, robot, moves

def process_move(grid, robot, move):
    direction = {"^": -1j, "v": 1j, "<": -1, ">": 1}[move]

    moved = []
    for pos in it.count(start=robot, step=direction):
        if grid[pos] == "#":
            return robot
        if grid[pos] == ".":
            moved.append(pos)
            break

        if grid[pos] == "O":
            moved.append(pos)
 
    grid[robot] = "."
    grid[moved[0]] = "@"
    if len(moved) > 1:
        grid[moved[-1]] = "O"

    return moved[0]

def process_move_with_wider_boxes(grid, robot, move):
    direction = {"^": -1j, "v": 1j, "<": -1, ">": 1}[move]

    if direction.real:
        # The boxes are wider but no taller so horizontal movement works 
        # mostly the same, except we have to actually update every grid position
        # we passed through, not just the first and last
        moved = [robot]
        for pos in it.count(start=robot, step=direction):
            if grid[pos] == "#":
                return robot
            if grid[pos] == ".":
                moved.append(pos)
                break
            if grid[pos] in "[]":
                if direction.real:
                    moved.append(pos)

        grid.update({pos: grid[pos-direction] for pos in moved})
        grid[robot] = "."
        return robot+direction

    else:
        # vertical movement is also the same, but harder
        moved = [{robot}]
        while not all(grid[p] == "." for p in moved[-1]):
            next_steps = set()
            for pos in moved[-1]:
                if grid[pos] == ".":
                    continue
                next_pos = pos+direction
                if grid[next_pos] == "#":
                    return robot
                if grid[next_pos] == ".":
                    next_steps.add(next_pos)
                    continue

                if grid[next_pos] == "[":
                    next_steps.add(next_pos)
                    next_steps.add(next_pos+1)

                if grid[next_pos] == "]":
                    next_steps.add(next_pos)
                    next_steps.add(next_pos-1)

            moved.append(next_steps)

        flat_moved = set(it.chain.from_iterable(moved))
        grid.update({pos: grid[pos-direction] if pos-direction in flat_moved else "." for pos in flat_moved})
        grid[robot] = "."
        grid[robot+direction]="@"
        return robot+direction


def print_grid(grid):
    width, height = int(max(c.real for c in grid))+1, int(max(c.imag for c in grid)) + 1
    print("\n".join("".join(grid[complex(x,y)] for x in range(width)) for y in range(height)))
    print()

def part_1(rawdata):
    grid, robot, moves = parse(rawdata)
    for move in moves:
        robot = process_move(grid, robot, move)

    return str(sum(100*int(c.imag)+int(c.real) for c in grid if grid[c]=="O"))

def part_2(rawdata):
    embiggened_data = rawdata.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")
    grid, robot, moves = parse(embiggened_data)

    for move in moves:
        robot = process_move_with_wider_boxes(grid, robot, move)

    return str(sum(100*int(c.imag)+int(c.real) for c in grid if grid[c]=="["))

from aocd import puzzle, submit
import pytest
import sys

@pytest.mark.parametrize("data, result", [
("""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<""", "2028"),
("""\##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^""", "10092")
 ])
def test_part_1(data, result):
    assert part_1(data) == result

@pytest.mark.parametrize("data, result", [
("""\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^""", "9021")
# ("""\
# #######
# #...#.#
# #.....#
# #..OO@#
# #..O..#
# #.....#
# #######

# <vv<<^^<<^^""", "")
])
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
