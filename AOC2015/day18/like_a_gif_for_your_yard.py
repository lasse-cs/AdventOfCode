import argparse
from pathlib import Path

TURNS = 100


class Grid:
    def __init__(self, grid: list[list[bool]]):
        self.grid = grid
        self.rows = len(grid)
        self.columns = len(grid[0]) if self.rows else 0

    def evolve(self):
        new_grid = []
        for r_idx, row in enumerate(self.grid):
            new_row = []
            for c_idx, value in enumerate(row):
                neighbour_count = self._count_on_neighbours(r_idx, c_idx)
                if value:
                    new_value = neighbour_count in (2, 3)
                else:
                    new_value = neighbour_count == 3
                new_row.append(new_value)
            new_grid.append(new_row)
        self.grid = new_grid

    def count_on(self) -> int:
        return sum(
            self.grid[r][c] for r in range(self.rows) for c in range(self.columns)
        )

    def _count_on_neighbours(self, row, column) -> int:
        count = 0
        for r in range(row - 1, row + 2):
            for c in range(column - 1, column + 2):
                if r == row and c == column:
                    continue
                if self._is_on_grid(r, c):
                    count += self.grid[r][c]
        return count

    def turn_on_corners(self):
        self.grid[0][0] = True
        self.grid[0][-1] = True
        self.grid[-1][0] = True
        self.grid[-1][-1] = True

    def _is_on_grid(self, row, column) -> bool:
        if row < 0 or row >= self.rows:
            return False
        return 0 <= column < self.columns

    @staticmethod
    def parse(text: str) -> "Grid":
        grid = []
        for line in text.splitlines():
            grid.append([c == "#" for c in line.strip()])
        return Grid(grid)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    text = args.filename.read_text()
    grid = Grid.parse(text)
    for _ in range(TURNS):
        grid.evolve()
    print(grid.count_on())

    grid = Grid.parse(text)
    for _ in range(TURNS):
        grid.turn_on_corners()
        grid.evolve()
    grid.turn_on_corners()
    print(grid.count_on())


if __name__ == "__main__":
    main()
