from pathlib import Path
import pytest
from pytest import FixtureRequest
from reindeer_maze import Direction, Location, Maze, Cell, State


@pytest.fixture
def maze(request: FixtureRequest):
    filename = request.param
    file = Path(__file__).resolve().parent / "files" / filename
    with file.open("r") as f:
        return Maze.parse(f)


@pytest.mark.parametrize("maze", ("test_very_small_input.txt",), indirect=True)
def test_parse(maze: Maze):
    expected_cells: list[list[Cell]] = [
        [Cell.WALL, Cell.WALL, Cell.WALL, Cell.WALL],
        [Cell.WALL, Cell.FREE, Cell.END, Cell.WALL],
        [Cell.WALL, Cell.START, Cell.FREE, Cell.WALL],
        [Cell.WALL, Cell.WALL, Cell.WALL, Cell.WALL],
    ]
    expected_state = State(Location(2, 1), Direction(0, 1))

    assert maze.cells == expected_cells
    assert maze.start_state == expected_state


@pytest.mark.parametrize(
    ["maze", "score"],
    [
        ("test_very_small_input.txt", 1002),
        ("test_first_input.txt", 7036),
        ("test_second_input.txt", 11048),
    ],
    indirect=["maze"],
)
def test_score_solve(maze: Maze, score: int):
    actual_score, _ = maze.solve()
    assert actual_score == score


@pytest.mark.parametrize(
    ["maze", "seats"],
    [
        ("test_very_small_input.txt", 3),
        ("test_first_input.txt", 45),
        ("test_second_input.txt", 64),
    ],
    indirect=["maze"],
)
def test_seat_solve(maze: Maze, seats: int):
    _, actual_seats = maze.solve()
    assert actual_seats == seats
