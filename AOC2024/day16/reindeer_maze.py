from argparse import ArgumentParser
from collections.abc import Iterable
from enum import StrEnum
from pathlib import Path
from typing import NamedTuple, Optional


class Cell(StrEnum):
    FREE = "."
    WALL = "#"
    END = "E"
    START = "S"


class Direction(NamedTuple):
    row: int
    column: int

    def turn(self) -> tuple["Direction", "Direction"]:
        idx: int = DIRECTIONS.index(self)
        anti_clockwise: int = (len(DIRECTIONS) - 1 + idx) % len(DIRECTIONS)
        clockwise: int = (len(DIRECTIONS) + 1 + idx) % len(DIRECTIONS)
        return (DIRECTIONS[anti_clockwise], DIRECTIONS[clockwise])


NORTH: Direction = Direction(-1, 0)
EAST: Direction = Direction(0, 1)
SOUTH: Direction = Direction(1, 0)
WEST: Direction = Direction(0, -1)


DIRECTIONS: list[Direction] = [NORTH, EAST, SOUTH, WEST]


class Location(NamedTuple):
    row: int
    column: int

    def move_in(self, direction: Direction) -> "Location":
        return Location(self.row + direction.row, self.column + direction.column)


class State(NamedTuple):
    location: Location
    direction: Direction


class ScoredState(NamedTuple):
    state: State
    score: int
    previous: Optional["ScoredState"]

    def get_successors(self) -> list["ScoredState"]:
        carry_on_score = self.score + 1
        carry_on_direction = self.state.direction
        carry_on_location = self.state.location.move_in(self.state.direction)
        states = [
            ScoredState(
                State(carry_on_location, carry_on_direction), carry_on_score, self
            )
        ]
        turns = self.state.direction.turn()
        turn_score = self.score + 1001
        for turn in turns:
            turn_location = self.state.location.move_in(turn)
            states.append(ScoredState(State(turn_location, turn), turn_score, self))
        return states


class Maze:
    def __init__(self, cells: list[list[Cell]], reindeer_location: Location):
        self.cells: list[list[Cell]] = cells
        self.start_state = State(reindeer_location, EAST)

    def solve(self) -> tuple[int, int]:
        frontier: list[ScoredState] = []
        frontier.append(ScoredState(self.start_state, 0, None))
        explored: dict[State, int] = {self.start_state: 0}
        end_states: list[ScoredState] = []
        min_score: int | None = None

        while frontier:
            current_scored_state = frontier.pop()
            current_state, current_score, _ = current_scored_state
            cell: Cell = self[current_state.location]
            if cell is Cell.WALL:
                continue
            if min_score and current_score > min_score:
                continue
            if cell is Cell.END:
                if not min_score or current_score < min_score:
                    min_score = current_score
                    end_states = []
                end_states.append(current_scored_state)
                continue

            successors: list[ScoredState] = current_scored_state.get_successors()
            for successor in successors:
                successor_state = successor.state
                successor_score = successor.score
                if (
                    successor_state not in explored
                    or explored[successor_state] >= successor_score
                ):
                    explored[successor_state] = successor_score
                    frontier.append(successor)

        if not min_score:
            raise ValueError("No Path")
        seats: int = self._count_seats(end_states)
        return (min_score, seats)

    def _count_seats(self, end_states: list[ScoredState]) -> int:
        seen: set[Location] = set()
        for end_state in end_states:
            current: ScoredState | None = end_state
            while current:
                seen.add(current.state.location)
                current = current.previous
        return len(seen)

    def __getitem__(self, location: Location) -> Cell:
        return self.cells[location.row][location.column]

    @staticmethod
    def parse(lines: Iterable[str]) -> "Maze":
        cells: list[list[Cell]] = []
        reindeer: Location | None = None
        for row_index, row in enumerate(lines):
            maze_row: list[Cell] = []
            for column_index, cell in enumerate(row.strip()):
                maze_cell: Cell = Cell(cell)
                maze_row.append(maze_cell)
                if maze_cell is Cell.START:
                    reindeer = Location(row_index, column_index)
            cells.append(maze_row)
        if reindeer is None:
            raise ValueError("No Reindeer Found")
        return Maze(cells, reindeer)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)
    with file.open("r") as f:
        maze: Maze = Maze.parse(f)
    min_score, seats = maze.solve()
    print(f"The minimum score for the maze is {min_score}")
    print(f"The number of available seats is {seats}")
