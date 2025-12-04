import argparse
from enum import StrEnum
from pathlib import Path


class Location(StrEnum):
    FREE = "."
    ROLL = "@"


class Grid:
    def __init__(self, grid: list[list[Location]]):
        self.grid = grid

    @staticmethod
    def parse(text: str) -> "Grid":
        grid: list[list[Location]] = []
        for row_text in text.split("\n"):
            if not row_text:
                continue
            grid.append(
                [
                    Location.ROLL if c == Location.ROLL else Location.FREE
                    for c in row_text.strip()
                ]
            )
        return Grid(grid)

    def get(self, row: int, column: int) -> Location | None:
        if row < 0 or row >= len(self.grid):
            return None
        r = self.grid[row]
        if column < 0 or column >= len(r):
            return None
        return r[column]

    def set(self, row: int, column: int, location: Location):
        self.grid[row][column] = location

    def count_roll_neighbours(self, row, column) -> int:
        count = 0
        for r in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                if r == 0 and c == 0:
                    continue
                neighbour = self.get(row + r, column + c)
                count += 1 if neighbour is Location.ROLL else 0
        return count

    def is_accessible(self, row: int, column: int) -> bool:
        return self.count_roll_neighbours(row, column) < 4

    def count_accessible_rolls(self) -> int:
        return len(self.get_accessible_rolls())

    def get_accessible_rolls(self) -> list[tuple[int, int]]:
        accessible = []
        for r_idx, r in enumerate(self.grid):
            for c_idx, c in enumerate(r):
                if c is not Location.ROLL:
                    continue
                if self.is_accessible(r_idx, c_idx):
                    accessible.append((r_idx, c_idx))
        return accessible

    def count_all_accessible_rolls(self) -> int:
        count = 0
        while accessible := self.get_accessible_rolls():
            count += len(accessible)
            for row, column in accessible:
                self.set(row, column, Location.FREE)
        return count


def main():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    grid = Grid.parse(args.filename.read_text())
    print(grid.count_accessible_rolls())
    print(grid.count_all_accessible_rolls())
