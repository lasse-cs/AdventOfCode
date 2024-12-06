from guard_gallivant import parse, Cell, Direction, CellLocation
from pathlib import Path


def test_parse():
    file = Path(".") / "files" / "test_small_input.txt"
    guard = parse(file)
    expected_cells = [[Cell.FREE, Cell.BLOCKED], [Cell.FREE, Cell.FREE]]
    expected_direction = Direction(-1, 0)
    expected_location = CellLocation(1, 0)
    assert guard.board.cells == expected_cells
    assert guard.start_direction == expected_direction
    assert guard.start_location == expected_location


def test_patrol():
    file = Path(".") / "files" / "test_input.txt"
    guard = parse(file)
    visited_cells = guard.patrol()
    assert visited_cells == 41


def test_count_obstructables():
    file = Path(".") / "files" / "test_input.txt"
    guard = parse(file)
    count = guard.count_obstructables()
    assert count == 6
