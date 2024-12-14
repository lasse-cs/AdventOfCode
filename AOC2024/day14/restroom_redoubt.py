from argparse import ArgumentParser
from collections.abc import Iterable
from pathlib import Path
from typing import NamedTuple
from re import Pattern, Match, compile


class BoardSize(NamedTuple):
    width: int
    height: int


class Velocity(NamedTuple):
    x: int
    y: int


class Position(NamedTuple):
    x: int
    y: int

    def move(self, velocity: Velocity, board_size: BoardSize) -> "Position":
        return Position(
            (board_size.width + self.x + velocity.x) % board_size.width,
            (board_size.height + self.y + velocity.y) % board_size.height,
        )


class Robot:
    ROBOT_PATTERN: Pattern = compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")

    def __init__(self, position: Position, velocity: Velocity, board_size: BoardSize):
        self.position: Position = position
        self.velocity: Velocity = velocity
        self.board_size: BoardSize = board_size

    def move(self):
        self.position = self.position.move(self.velocity, self.board_size)

    def get_quadrant(self) -> int | None:
        half_height: int = self.board_size.height // 2
        half_width: int = self.board_size.width // 2
        if self.position.x < half_width and self.position.y < half_height:
            return 0
        if self.position.x < half_width and self.position.y > half_height:
            return 1
        if self.position.x > half_width and self.position.y > half_height:
            return 2
        if self.position.x > half_width and self.position.y < half_height:
            return 3
        return None

    @classmethod
    def parse(cls, line: str, board_size: BoardSize) -> "Robot":
        match: Match | None = cls.ROBOT_PATTERN.match(line)
        if match is None:
            raise Exception
        position: Position = Position(int(match.group(1)), int(match.group(2)))
        velocity: Velocity = Velocity(int(match.group(3)), int(match.group(4)))
        return Robot(position, velocity, board_size)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Robot):
            return False
        if self.board_size != other.board_size:
            return False
        if self.position != other.position:
            return False
        return self.velocity == other.velocity


class Board:
    def __init__(self, board_size: BoardSize, robots: list[Robot]):
        self.board_size: BoardSize = board_size
        self.robots: list[Robot] = robots

    def update(self):
        for robot in self.robots:
            robot.move()

    def safety_factor_after_updates(self, num_updates: int) -> int:
        for i in range(num_updates):
            self.update()
        return self._safety_factor()

    def get_quadrant_counts(self) -> list[int]:
        quadrant_counts: list[int] = [0, 0, 0, 0]
        for robot in self.robots:
            quadrant: int | None = robot.get_quadrant()
            if quadrant is None:
                continue
            quadrant_counts[quadrant] += 1
        return quadrant_counts

    def _safety_factor(self) -> int:
        quadrant_counts: list[int] = self.get_quadrant_counts()

        total = 1
        for count in quadrant_counts:
            total *= count
        return total

    def __str__(self) -> str:
        rows: list[list[str]] = [
            ["." for _ in range(self.board_size.width)]
            for _ in range(self.board_size.height)
        ]
        for robot in self.robots:
            cur_char = rows[robot.position.y][robot.position.x]
            if cur_char == ".":
                new_char = "1"
            else:
                new_char = str(int(cur_char) + 1)
            rows[robot.position.y][robot.position.x] = new_char
        return "\n".join(["".join(row) for row in rows])

    def __eq__(self, other) -> bool:
        if not isinstance(other, Board):
            return False
        if self.board_size != other.board_size:
            return False
        return self.robots == other.robots

    @staticmethod
    def parse(lines: Iterable[str], board_size: BoardSize) -> "Board":
        robots: list[Robot] = [Robot.parse(line, board_size) for line in lines]
        return Board(board_size, robots)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)

    board_size = BoardSize(101, 103)
    with file.open("r") as f:
        board = Board.parse(f, board_size)
        safety: int = board.safety_factor_after_updates(100)
        print(f"After 100 seconds, the safety factor is {safety}")

    with file.open("r") as f:
        board = Board.parse(f, board_size)
    for i in range(10_001):
        quadrant_count: list[int] = board.get_quadrant_counts()
        if max(quadrant_count) > len(board.robots) // 2:
            print(f"Found an accumulation on update {i}")
            print(board)
        board.update()
