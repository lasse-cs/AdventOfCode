from pathlib import Path
import pytest
from restroom_redoubt import BoardSize, Robot, Position, Velocity, Board


@pytest.fixture
def board_size():
    return BoardSize(11, 7)


def test_move(board_size: BoardSize):
    initial_position: Position = Position(4, 1)
    velocity: Velocity = Velocity(2, -3)
    expected_positon: Position = Position(6, 5)
    assert initial_position.move(velocity, board_size) == expected_positon


def test_parse_robot(board_size: BoardSize):
    line: str = "p=0,4 v=3,-3"
    expected_robot: Robot = Robot(Position(0, 4), Velocity(3, -3), board_size)
    actual_robot = Robot.parse(line, board_size)
    assert expected_robot == actual_robot


def test_safety_factor(board_size: BoardSize):
    file: Path = Path(__file__).resolve().parent / "files" / "test_input.txt"
    with file.open("r") as f:
        board: Board = Board.parse(f, board_size)
        safety_factor = board.safety_factor_after_updates(100)
        assert safety_factor == 12


def test_board_print(board_size: BoardSize):
    file: Path = Path(__file__).resolve().parent / "files" / "test_input.txt"
    with file.open("r") as f:
        board: Board = Board.parse(f, board_size)
        expected = "1.12.......\n...........\n...........\n......11.11\n1.1........\n.........1.\n.......1..."
        assert str(board) == expected

        for _ in range(100):
            board.update()
        expected = "......2..1.\n...........\n1..........\n.11........\n.....1.....\n...12......\n.1....1...."
        assert str(board) == expected
