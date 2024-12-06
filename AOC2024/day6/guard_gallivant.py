from argparse import ArgumentParser
from pathlib import Path
from typing import NamedTuple
from enum import StrEnum


class Direction(NamedTuple):
    row: int
    column: int


DIRECTIONS = [
    Direction(-1, 0),
    Direction(0, 1),
    Direction(1, 0),
    Direction(0, -1),
]

GUARD_DIRECTION = [
    "^",
    ">",
    "v",
    "<",
]


class Cell(StrEnum):
    BLOCKED = "#"
    FREE = "."


class CellLocation(NamedTuple):
    row: int
    column: int


class Board:
    def __init__(self, cells: list[list[Cell]]):
        self.cells = cells

    def is_location_on_board(self, cl: CellLocation) -> bool:
        if cl.row < 0 or cl.row >= len(self.cells):
            return False
        return cl.column >= 0 and cl.column < len(self.cells[cl.row])

    def __getitem__(self, cl: CellLocation) -> Cell:
        return self.cells[cl.row][cl.column]

    def __setitem__(self, cl: CellLocation, cell: Cell) -> None:
        self.cells[cl.row][cl.column] = cell


class Guard:
    def __init__(self, location: CellLocation, direction: Direction, board: Board):
        self.start_direction = direction
        self.start_location = location
        self.board = board

    def reset(self):
        self.location = self.start_location
        self.direction = self.start_direction

    def patrol(self) -> int:
        self.reset()
        visited: set[tuple[CellLocation, Direction]] = set()
        while self.board.is_location_on_board(self.location):
            if (self.location, self.direction) in visited:
                return -1
            elif self.board[self.location] == Cell.FREE:
                visited.add((self.location, self.direction))
            elif self.board[self.location] == Cell.BLOCKED:
                self.undo_move()
                self.turn()
            self.move()
        return len({v[0] for v in visited})

    def count_obstructables(self) -> int:
        total: int = 0
        for row_index, row in enumerate(self.board.cells):
            for column_index, cell in enumerate(row):
                if cell == Cell.BLOCKED:
                    continue
                location = CellLocation(row_index, column_index)
                if location == self.start_location:
                    continue
                self.board[location] = Cell.BLOCKED
                if self.patrol() == -1:
                    total += 1
                self.board[location] = Cell.FREE
        return total

    def turn(self):
        self.direction = DIRECTIONS[
            (DIRECTIONS.index(self.direction) + 1) % len(DIRECTIONS)
        ]

    def move(self):
        self.location = CellLocation(
            self.location.row + self.direction.row,
            self.location.column + self.direction.column,
        )

    def undo_move(self):
        self.location = CellLocation(
            self.location.row - self.direction.row,
            self.location.column - self.direction.column,
        )


def parse(file: Path) -> Guard:
    cells: list[list[Cell]] = []
    with open(file, "r") as f:
        for row_index, row in enumerate(f):
            row_list: list[Cell] = []
            for column_index, cell in enumerate(row.strip()):
                if cell in GUARD_DIRECTION:
                    guard_direction = DIRECTIONS[GUARD_DIRECTION.index(cell)]
                    guard_location = CellLocation(row_index, column_index)
                    row_list.append(Cell.FREE)
                else:
                    row_list.append(Cell(cell))
            cells.append(row_list)

    board: Board = Board(cells)
    return Guard(guard_location, guard_direction, board)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)

    guard = parse(file)
    visited = guard.patrol()
    print(f"The guard visited {visited} cells on patrol")

    obstruct = guard.count_obstructables()
    print(f"There are {obstruct} places to obstruct")
