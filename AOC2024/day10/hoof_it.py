from argparse import ArgumentParser
from pathlib import Path
from typing import NamedTuple
from collections.abc import Iterable


class Direction(NamedTuple):
    row: int
    column: int


class CellLocation(NamedTuple):
    row: int
    column: int

    def move_in(self, direction: Direction) -> "CellLocation":
        return CellLocation(self.row + direction.row, self.column + direction.column)


class TopographicMap:
    def __init__(self, cells: list[list[int]]):
        self._cells = cells
        self._directions = [
            Direction(-1, 0),
            Direction(1, 0),
            Direction(0, -1),
            Direction(0, 1),
        ]

    def __getitem__(self, cl: CellLocation) -> int:
        return self._cells[cl.row][cl.column]

    def _is_location_on_map(self, cl: CellLocation):
        if cl.row < 0 or cl.row >= len(self._cells):
            return False
        return 0 <= cl.column < len(self._cells[cl.row])

    def _get_successors(self, cl: CellLocation) -> list[CellLocation]:
        successors = []
        for direction in self._directions:
            next_location = cl.move_in(direction)
            if not self._is_location_on_map(next_location):
                continue
            if self[next_location] - self[cl] == 1:
                successors.append(next_location)
        return successors

    def score_trailhead(self, trailhead: CellLocation) -> int:
        frontier: list[CellLocation] = [trailhead]
        ends: set[CellLocation] = set()
        visited: set[CellLocation] = set()

        while len(frontier) > 0:
            current: CellLocation = frontier.pop()
            if self[current] == 9:
                ends.add(current)
                continue

            for successor in self._get_successors(current):
                if successor in visited:
                    continue
                visited.add(successor)
                frontier.append(successor)
        return len(ends)

    def score_map(self) -> int:
        total: int = 0
        for row_index, row in enumerate(self._cells):
            for column_index, cell in enumerate(row):
                if cell != 0:
                    continue
                total += self.score_trailhead(CellLocation(row_index, column_index))
        return total

    @staticmethod
    def parse(lines: Iterable[str]) -> "TopographicMap":
        cells: list[list[int]] = []
        for line in lines:
            cells.append([int(digit) if digit != "." else -1 for digit in line.strip()])
        return TopographicMap(cells)


def parse(file: Path) -> "TopographicMap":
    with file.open("r") as f:
        return TopographicMap.parse(f)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("filename")

    args = parser.parse_args()
    file = Path(args.filename)

    map: TopographicMap = parse(file)
    score: int = map.score_map()
    print(f"The map has score {score}")
