from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import NamedTuple, Optional
from enum import StrEnum
from collections import deque


class MemoryCell(StrEnum):
    SAFE = "."
    CORRUPTED = "#"


class Direction(NamedTuple):
    row: int
    column: int


DIRECTIONS: list[Direction] = [
    Direction(-1, 0),
    Direction(0, 1),
    Direction(1, 0),
    Direction(0, -1),
]


class MemoryLocation(NamedTuple):
    row: int
    column: int

    def move_in(self, direction: Direction) -> "MemoryLocation":
        return MemoryLocation(self.row + direction.row, self.column + direction.column)

    def get_neighbours(self) -> list["MemoryLocation"]:
        return [self.move_in(d) for d in DIRECTIONS]


class MemoryPath(NamedTuple):
    current: MemoryLocation
    previous: Optional["MemoryPath"]

    def get_step_count(self) -> int:
        return len(self.get_as_list()) - 1

    def get_as_list(self) -> list[MemoryLocation]:
        location_list: list[MemoryLocation] = []
        current: MemoryPath | None = self
        while current is not None:
            location_list.append(current.current)
            current = current.previous
        return location_list


@dataclass
class Memory:
    def __init__(self, rows: int, columns: int):
        self.rows: int = rows
        self.columns: int = columns
        self.start: MemoryLocation = MemoryLocation(0, 0)
        self.goal: MemoryLocation = MemoryLocation(self.rows - 1, self.columns - 1)
        self.cells: list[list[MemoryCell]] = [
            [MemoryCell.SAFE for _ in range(columns)] for _ in range(rows)
        ]

    def _is_location_in_memory(self, ml: MemoryLocation) -> bool:
        if ml.row < 0 or ml.row >= self.rows:
            return False
        return 0 <= ml.column < self.columns

    def corrupt_cell(self, ml: MemoryLocation):
        self.cells[ml.row][ml.column] = MemoryCell.CORRUPTED

    def get_cell(self, ml: MemoryLocation):
        return self.cells[ml.row][ml.column]

    def pathfind(self) -> MemoryPath | None:
        frontier: deque[MemoryPath] = deque()
        frontier.append(MemoryPath(self.start, None))
        visited: set[MemoryLocation] = {self.start}
        while len(frontier) > 0:
            current_path = frontier.popleft()
            current_location = current_path.current
            if current_location == self.goal:
                return current_path

            for neighbour in current_location.get_neighbours():
                if not self._is_location_in_memory(neighbour):
                    continue
                if neighbour in visited:
                    continue
                if self.get_cell(neighbour) is not MemoryCell.SAFE:
                    continue
                frontier.append(MemoryPath(neighbour, current_path))
                visited.add(neighbour)
        return None

    def get_steps_required(self) -> int:
        path: MemoryPath | None = self.pathfind()
        if path is None:
            return -1
        return path.get_step_count()


def parse(lines: list[str]) -> list[MemoryLocation]:
    locations: list[MemoryLocation] = []
    for line in lines:
        split_line: list[str] = line.strip().split(",")
        assert len(split_line) == 2
        ml: MemoryLocation = MemoryLocation(int(split_line[1]), int(split_line[0]))
        locations.append(ml)
    return locations


def get_first_blocker(
    memory: Memory, instructions: list[MemoryLocation]
) -> MemoryLocation | None:
    current: MemoryPath | None = memory.pathfind()
    assert current is not None
    current_as_list: list[MemoryLocation] = current.get_as_list()
    for instruction in instructions:
        memory.corrupt_cell(instruction)
        if all(memory.get_cell(ml) is MemoryCell.SAFE for ml in current_as_list):
            continue
        current = memory.pathfind()
        if not current:
            return instruction
        current_as_list = current.get_as_list()
    return None


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)
    with file.open("r") as f:
        lines: list[str] = f.readlines()
    instructions: list[MemoryLocation] = parse(lines)

    memory: Memory = Memory(71, 71)

    for i in range(1024):
        memory.corrupt_cell(instructions[i])
    steps: int = memory.get_steps_required()
    print(f"The minimum number of steps required is {steps} after 1 kilobyte")

    blocker: MemoryLocation | None = get_first_blocker(memory, instructions)
    if blocker is None:
        print("There is no blocker")
    else:
        print(f"The first blocker is at {blocker.column},{blocker.row}")
