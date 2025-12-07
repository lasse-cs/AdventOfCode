import argparse
from pathlib import Path


FREE = "."
BEAM = "|"
START = "S"
SPLITTER = "^"


class Manifold:
    def __init__(self, grid_string: str):
        self.grid: list[list[str]] = []
        for row in grid_string.strip().split("\n"):
            r: list[str] = []
            for c in row.strip():
                if c == START:
                    self.start = len(r)
                r.append(c)
            self.grid.append(r)

    def count_splits(self) -> int:
        count = 0
        q = [self.start]
        current_row, num_rows = 0, len(self.grid)
        visited: set[tuple[int, int]] = set()
        while q and current_row < num_rows - 1:
            next_row = current_row + 1
            q_length = len(q)
            for _ in range(q_length):
                beam = q.pop(0)
                if (current_row, beam) in visited:
                    continue
                if self.grid[next_row][beam] == FREE:
                    q.append(beam)
                elif self.grid[next_row][beam] == SPLITTER:
                    count += 1
                    q.append(beam - 1)
                    q.append(beam + 1)
                visited.add((current_row, beam))
            current_row = next_row
        return count

    def count_timelines(self) -> int:
        return self._count_timelines(0, self.start, {})

    def _count_timelines(
        self, row: int, column: int, seen: dict[tuple[int, int], int]
    ) -> int:
        if row + 1 == len(self.grid):
            return 1
        if (row, column) in seen:
            return seen[(row, column)]

        if self.grid[row + 1][column] == SPLITTER:
            seen[(row, column)] = self._count_timelines(row + 1, column - 1, seen)
            seen[(row, column)] += self._count_timelines(row + 1, column + 1, seen)
        else:
            seen[(row, column)] = self._count_timelines(row + 1, column, seen)
        return seen[(row, column)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    args = parser.parse_args()

    manifold = Manifold(args.filename.read_text())
    print(manifold.count_splits())
    print(manifold.count_timelines())


if __name__ == "__main__":
    main()
