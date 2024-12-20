from argparse import ArgumentParser
from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import NamedTuple, TypeAlias
from enum import StrEnum


class Cell(StrEnum):
    WALL = "#"
    START = "S"
    END = "E"
    TRACK = "."


class Direction(NamedTuple):
    row: int
    column: int


SINGLE_STEPS: list[Direction] = [
    Direction(-1, 0),
    Direction(0, 1),
    Direction(1, 0),
    Direction(0, -1),
]

DOUBLE_STEPS: list[Direction] = [
    Direction(-2, 0),
    Direction(-1, 1),
    Direction(-1, -1),
    Direction(0, 2),
    Direction(0, -2),
    Direction(1, 1),
    Direction(1, -1),
    Direction(2, 0),
]


def create_twenty_steps() -> list[tuple[Direction, int]]:
    directions: list[tuple[Direction, int]] = []
    for column in range(-20, 21):
        row_max: int = 20 - abs(column)
        for row in range(-row_max, row_max + 1):
            directions.append((Direction(row, column), abs(row) + abs(column)))
    return directions


WITHIN_TWENTY_STEPS: list[tuple[Direction, int]] = create_twenty_steps()


class Location(NamedTuple):
    row: int
    column: int

    def move_in(self, direction: Direction) -> "Location":
        return Location(self.row + direction.row, self.column + direction.column)

    def neighbors(self) -> list["Location"]:
        return [self.move_in(d) for d in SINGLE_STEPS]

    def cheat_neighbors(self, extra: bool) -> list[tuple["Location", int]]:
        if extra:
            return [(self.move_in(d[0]), d[1]) for d in WITHIN_TWENTY_STEPS]
        else:
            return [(self.move_in(d), 2) for d in DOUBLE_STEPS]


RacePath: TypeAlias = dict[Location, int]


class RaceTrack:
    def __init__(self, cells: list[list[Cell]], start: Location, end: Location):
        self.cells: list[list[Cell]] = cells
        self.start: Location = start
        self.end: Location = end

    def _is_location_on_track(self, location: Location) -> bool:
        if location.row < 0 or location.row >= len(self.cells):
            return False
        if location.column < 0 or location.column >= len(self.cells[location.row]):
            return False
        return self.cells[location.row][location.column] is not Cell.WALL

    def get_path(self) -> RacePath:
        path: RacePath = {self.end: 0}
        current: Location = self.end
        current_distance = 0
        while current != self.start:
            neighbors: list[Location] = current.neighbors()
            for neighbor in neighbors:
                if not self._is_location_on_track(neighbor):
                    continue
                if neighbor in path:
                    continue
                current = neighbor
            current_distance += 1

            path[current] = current_distance
        return path

    def get_cheat_counts(
        self, path: RacePath, minimum_saving: int, extra: bool = False
    ) -> dict[int, int]:
        cheat_counts: defaultdict[int, int] = defaultdict(int)

        for location, distance in path.items():
            for cheat_end, cheat_length in location.cheat_neighbors(extra):
                if not self._is_location_on_track(cheat_end):
                    continue
                neighbor_distance = path[cheat_end]
                saving = distance - neighbor_distance - cheat_length
                if saving < minimum_saving:
                    continue
                cheat_counts[saving] += 1

        return dict(cheat_counts)

    @staticmethod
    def parse(lines: Iterable[str]) -> "RaceTrack":
        cells: list[list[Cell]] = []
        start: Location | None = None
        finish: Location | None = None
        for row_index, row in enumerate(lines):
            row_list: list[Cell] = []
            for column_index, cell in enumerate(row.strip()):
                current_cell: Cell = Cell(cell)
                row_list.append(current_cell)
                if current_cell is Cell.START:
                    start = Location(row_index, column_index)
                elif current_cell is Cell.END:
                    finish = Location(row_index, column_index)
            cells.append(row_list)

        if start is None or finish is None:
            raise ValueError("Invalid racetrack")

        return RaceTrack(cells, start, finish)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("minimum", default=100, type=int)

    args = parser.parse_args()
    file: Path = Path(args.filename)
    minimum: int = args.minimum

    with file.open("r") as f:
        race_track: RaceTrack = RaceTrack.parse(f)
    race_path: RacePath = race_track.get_path()
    cheat_counts: dict[int, int] = race_track.get_cheat_counts(race_path, minimum)
    saving_count = sum(count for count in cheat_counts.values())
    print(f"There are {saving_count} cheats that save at least {minimum}")

    extra_cheat_counts: dict[int, int] = race_track.get_cheat_counts(
        race_path, minimum, True
    )
    extra_saving_count = sum(count for count in extra_cheat_counts.values())
    print(f"There are {extra_saving_count} extra cheats that save at least {minimum}")
